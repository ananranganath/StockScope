import { useState } from "react";
function App() {
    const [ticker, setTicker] = useState("");

    const [message, setMessage] = useState("");

   const handleAnalyze = async () => {
  const response = await fetch("http://127.0.0.1:8000/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      ticker: ticker,
    }),
  });

  const data = await response.json();

  setMessage(data.message);
};

  return (
    <main>
      <h1>Stock Scope</h1>

      <p>
        Analyze stocks using intrinsic valuation models and AI-powered
        investment insights.
      </p>

      <hr />

      <h2>Stock Analysis</h2>

      <input
        type="text"
  placeholder="Enter stock ticker (e.g. AAPL)"
  value={ticker}
  onChange={(event) => setTicker(event.target.value)}
      />

      <br />
      <br />

     <button onClick={handleAnalyze}>Analyze</button>
      {ticker && (
  <div>
    <h3>Selected Stock</h3>
    <p>{ticker.toUpperCase()}</p>
  </div>
)}
{ticker && (
  <div>
    <h3>Recommendation</h3>
    <p>Waiting for analysis...</p>
  </div>
)}
{ticker && (
  <div>
    <h3>Investor Summary</h3>

    <p>
      The AI-generated investment summary will appear here after the
      valuation is complete.
    </p>
  </div>
)}

{message && (
  <div>
    <h3>Backend Response</h3>
    <p>{message}</p>
  </div>
)}

    </main>
  );
}

export default App;