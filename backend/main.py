from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import yfinance as yf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StockRequest(BaseModel):
    ticker: str


@app.get("/")
def home():
    return {"message": "Backend is working!"}


@app.post("/analyze")
def analyze_stock(stock: StockRequest):
    ticker = yf.Ticker(stock.ticker)

    info = ticker.info

    return {
        "ticker": stock.ticker.upper(),
        "company": info.get("longName"),
        "price": info.get("currentPrice"),
        "currency": info.get("currency")
    }