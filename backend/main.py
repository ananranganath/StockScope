import yfinance as yf
from fastapi import FastAPI
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
@app.get ("/api/stocks/{ticker}")
def get_stock (ticker: str):
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