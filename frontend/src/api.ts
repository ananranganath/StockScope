const API_URL = import.meta.env.VITE_API_URL;

export type STOCK = {
    ticker: string;
    name: string | null;
    price: number;
    currency: string | null;
    sector: string | null;
    industry: string | null;
    market_cap: number | null;
    pe_ratio: number | null;
};

export async function getStock(ticker: string): Promise<STOCK> {
    let response: Response;
    try {
        response = await fetch(`${API_URL}/api/stocks/${encodeURIComponent(ticker)}`);
    } catch {
        throw new Error("Can't reach the backend. Is uvicorn running?");
    }

    const body = await response.json();
    if (!response.ok) {
        throw new Error(body.detail || "Something went wrong.");
    }
    return body;
}