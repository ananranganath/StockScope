import { useState, type FormEvent } from "react";
import { getStock, type STOCK } from "./api";

function App() {
    const [ticker, setTicker] = useState("");
    const [stock, setStock] = useState<STOCK | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    async function handleSubmit(event: FormEvent) {
        event.preventDefault();
        if (!ticker.trim()) return;

        setLoading(true);
        setError("");
        setStock(null);

        try {
          setStock(await getStock(ticker.trim()));
        } catch (err) {
            setError((err as Error).message);
        } finally {
            setLoading(false);
        }
    }

    return (
      <main>
        <h1>StockScope</h1>

        <form onSubmit={handleSubmit}>
          <input
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            placeholder="Enter a ticker, e.g., AAPL"
          />
          <button type="submit" disabled={loading}>
            {loading ? "Loading..." : "Analyze"}
          </button>
        </form>

        {error && <p className="error" >{error}</p>}
        
        {stock && (
          <section>
            <h2>
              {stock.name} ({stock.ticker})
            </h2>
            <p className="price">
              {stock.currency} {stock.price.toFixed(2)}
            </p>
            <p>Sector: {stock.sector ?? "-"}</p>
            <p>Industry: {stock.industry ?? "-"}</p>
            <p>Market cap: {stock.market_cap?.toLocaleString() ?? "-"}</p>
            <p>P/E ratio: {stock.pe_ratio?.toFixed(2) ?? "-"}</p>
          </section>
        )}
      </main>
    );
  }

export default App;
          