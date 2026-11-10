import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { getHistory, type PricePoint } from "./api";

const PERIODS = [
    { value: "1mo", label: "1M" },
    { value: "6mo", label: "6M" },
    { value: "1y", label: "1Y" },
    { value: "5y", label: "5Y" },
];

function PriceChart({ ticker }: { ticker: string }) {
    const [period, setPeriod] = useState("1y");
    const [points, setPoints] = useState<PricePoint[]>([]);
    const [error, setError] = useState("");

    useEffect(() => {
        let cancelled = false;
        setError("");

        getHistory(ticker, period)
            .then((data) => {
                if (!cancelled) setPoints(data);
            })
            .catch((err) => {
                if (!cancelled) setError(err.message);
            });

        return () => {
            cancelled = true;
        };
    }, [ticker, period]);

    return (
        <div className="chart">
            <div className="periods">
                {PERIODS.map((p) => (
                    <button
                        key={p.value}
                        className={p.value === period ? "active" : ""}
                        onClick={() => setPeriod(p.value)}
                    >
                        {p.label}
                    </button>
                ))}
            </div>
            
            {error ? (
                <p className="error">{error}</p>
            ) : (
                <div style={{width: "100%", height: 300 }}>
                    <ResponsiveContainer>
                        <LineChart data={points}>
                            <XAxis dataKey="date" minTickGap={40} />
                            <YAxis domain={["auto", "auto"]} />
                            <Tooltip />
                            <Line type="monotone" dataKey="close" stroke="#2e4fa8" dot={false} />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            )}
        </div>
    );
}

export default PriceChart;