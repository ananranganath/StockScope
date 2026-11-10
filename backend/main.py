import yfinance as yf
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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