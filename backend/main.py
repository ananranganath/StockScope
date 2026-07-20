from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel

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
    return {
        "ticker": stock.ticker.upper(),
        "message": f"Analyzing {stock.ticker.upper()}..."
    }