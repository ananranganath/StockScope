import yfinance as yf
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from valuation import run_dcf

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/stocks/{ticker}")
def get_stock(ticker: str):
    symbol = ticker.strip().upper()

    try:
        info = yf.Ticker(symbol).info
    except Exception:
        raise HTTPException(status_code=503, detail="Couldn't reach Yahoo Finance. Try again in a minute.")

    price = info.get("currentPrice") or info.get("regularMarketPrice") 
    if price is None:
        raise HTTPException(status_code=404, detail=f"No data found for '{symbol}'.")

    return {
        "ticker": symbol,
        "name": info.get("longName"),
        "price": price,
        "currency": info.get("currency"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
    }

@app.get("/api/stocks/{ticker}/history")
def get_history(ticker: str, period: str = "1y"):
    symbol = ticker.strip().upper()

    allowed = ["1mo", "6mo", "1y", "5y"]
    if period not in allowed:
        raise HTTPException(status_code=400, detail="Period must be one of: 1mo, 6mo, 1y, 5y.")

    #5 years of daily prices is a lot of points, so use weekly prices for it
    interval = "1wk" if period == "5y" else "1d"

    try:
        df = yf.Ticker(symbol).history(period=period, interval=interval)
    except Exception:
        raise HTTPException(status_code=503, detail="Couldn't reach Yahoo Finance. Try again in a minute.")
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No price history found for '{symbol}'.")

    points = []
    for timestamp, close in df["Close"].dropna().items():
        points.append({
            "date": timestamp.strftime("%Y-%m-%d"),
            "close": round(float(close), 2),
        })
    return {"ticker": symbol, "period": period, "points": points}

@app.get("/api/stocks/{ticker}/valuation")
def get_valuation(
    ticker: str,
    growth: float = 0.08,
    terminal_growth: float = 0.025,
    discount: float = 0.09,
):

    symbol = ticker.strip().upper()

    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        cashflow = stock.cashflow
    except Exception:
        raise HTTPException(status_code=503, detail="Couldn't reach Yahoo Finance. Try again in a minute.")
    price = info.get("currentPrice") or info.get("regularMarketPrice")
    if price is None:
        raise HTTPException(status_code=404, detail=f"No data found for '{symbol}'.")

    # A DCF values one company's cash flows, so it doesn't work for ETFs or funds.
    if info.get("quoteType") != "EQUITY":
        raise HTTPException(status_code=422, detail=f"A DCF values a single company, so it doesn't apply to {symbol}.")
    if cashflow is None or cashflow.empty or "Free Cash Flow" not in cashflow.index:
        raise HTTPException(status_code=422, detail=f"No free cash flow data is available for {symbol}.")
    fcf_history = cashflow.loc["Free Cash Flow"].dropna()
    if fcf_history.empty:
        raise HTTPException(status_code=422, detail=f"No free cash flow data is available for {symbol}.")
    latest_fcf = float(fcf_history.iloc[0])   # Yahoo lists the newest year first.

    shares = info.get("sharesOutstanding")
    if not shares:
        raise HTTPException(status_code=422, detail=f"Shares outstanding aren't available for {symbol}.")
    cash = info.get("totalCash") or 0
    debt = info.get("totalDebt") or 0

    try:
        value= run_dcf(latest_fcf, shares, cash, debt, growth, terminal_growth, discount)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error))

    upside = value/price -1
    if upside > 0.15:
        verdict = "undervalued"
    elif upside < -0.15:
        verdict = "overvalued"
    else:
        verdict = "fairly valued"

    return {
        "ticker": symbol,
        "price": price,
        "currency": info.get("currency"),
        "intrinsic_value": round(value, 2),
        "upside": round(upside, 4),
        "verdict": verdict,
        "assumptions": {
            "growth": growth,
            "terminal_growth": terminal_growth,
            "discount": discount,
        },
        "inputs": {
            "free_cash_flow": latest_fcf,
            "shares": shares,
            "cash": cash,
            "debt": debt,
        },
    }