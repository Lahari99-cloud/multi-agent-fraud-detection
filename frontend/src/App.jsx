import { useEffect, useState } from "react";
import { api } from "./api";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell
} from "recharts";

export default function App() {
  const [queue, setQueue] = useState([]);
  const [metrics, setMetrics] = useState("");

  useEffect(() => {
  fetchQueue();
  fetchMetrics();

  const socket = new WebSocket(
    "ws://127.0.0.1:8000/ws/fraud-stream"
  );

  socket.onmessage = (event) => {
    const liveEvent = JSON.parse(event.data);

    setQueue((prev) => [liveEvent, ...prev.slice(0, 9)]);
  };

  return () => socket.close();
}, []);

  async function fetchQueue() {
    const res = await api.get("/analyst/queue");
    setQueue(res.data);
  }

  async function fetchMetrics() {
    const res = await api.get("/metrics");
    setMetrics(res.data);
  }

 const riskCounts = {
  LOW: 0,
  MEDIUM: 0,
  HIGH: 0,
  CRITICAL: 0
};

queue.forEach((q) => {
  if (riskCounts[q.risk_level] !== undefined) {
    riskCounts[q.risk_level]++;
  }
});

const riskData = Object.entries(riskCounts).map(
  ([name, value]) => ({
    name,
    value
  })
);

  const trendData = [
    { time: "09:00", fraud: 2 },
    { time: "10:00", fraud: 4 },
    { time: "11:00", fraud: 3 },
    { time: "12:00", fraud: 7 },
    { time: "13:00", fraud: 5 },
    { time: "14:00", fraud: 9 }
  ];

  const flaggedCount = queue.length;
  const criticalCount = queue.filter((q) => q.risk_level === "CRITICAL").length;
  const highCount = queue.filter((q) => q.risk_level === "HIGH").length;

  return (
    <div style={styles.page}>
      <nav style={styles.navbar}>
        <div>
          <h1 style={styles.logo}>FraudOps AI</h1>
          <p style={styles.subtitle}>Enterprise Multi-Agent Fraud Decisioning</p>
        </div>
        <div style={styles.statusBadge}>LIVE MONITORING</div>
      </nav>

      <section style={styles.kpiGrid}>
        <KpiCard title="Analyst Queue" value={flaggedCount} label="Cases awaiting review" />
        <KpiCard title="High Risk" value={highCount} label="Analyst review required" />
        <KpiCard title="Critical Risk" value={criticalCount} label="Soft-decline candidates" />
        <KpiCard title="API Status" value="OK" label="FastAPI service healthy" />
      </section>

      <section style={styles.grid}>
        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Risk Distribution</h2>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={riskData}>
              <XAxis dataKey="name" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip />
              <Bar dataKey="value" fill="#38bdf8" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Fraud Trend</h2>
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={trendData}>
              <XAxis dataKey="time" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip />
              <Line type="monotone" dataKey="fraud" stroke="#f97316" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section style={styles.grid}>
        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Analyst Review Queue</h2>

          {queue.length === 0 ? (
            <p style={styles.empty}>No analyst review cases currently queued.</p>
          ) : (
            queue.map((item, idx) => (
              <div key={idx} style={styles.caseCard}>
                <div style={styles.caseHeader}>
                  <strong>{item.transaction_id}</strong>
                  <span style={getSeverityStyle(item.risk_level)}>
                    {item.risk_level}
                  </span>
                </div>
                <p>Action: {item.recommended_action}</p>
                <p>Risk Score: {item.risk_score}</p>
                <p style={styles.explanation}>{item.explanation}</p>
              </div>
            ))
          )}
        </div>

        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Prometheus Metrics</h2>
          <pre style={styles.metrics}>{metrics}</pre>
        </div>
      </section>
    </div>
  );
}

function KpiCard({ title, value, label }) {
  return (
    <div style={styles.kpiCard}>
      <p style={styles.kpiTitle}>{title}</p>
      <h2 style={styles.kpiValue}>{value}</h2>
      <p style={styles.kpiLabel}>{label}</p>
    </div>
  );
}

function getSeverityStyle(level) {
  const base = {
    padding: "4px 10px",
    borderRadius: "999px",
    fontSize: "12px",
    fontWeight: 700
  };

  if (level === "CRITICAL") {
    return { ...base, background: "#7f1d1d", color: "#fecaca" };
  }

  if (level === "HIGH") {
    return { ...base, background: "#9a3412", color: "#fed7aa" };
  }

  if (level === "MEDIUM") {
    return { ...base, background: "#713f12", color: "#fef3c7" };
  }

  return { ...base, background: "#064e3b", color: "#bbf7d0" };
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "linear-gradient(135deg, #020617, #0f172a)",
    color: "#e5e7eb",
    padding: "28px",
    fontFamily: "Inter, Arial, sans-serif"
  },
  navbar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "28px"
  },
  logo: {
    margin: 0,
    fontSize: "32px",
    color: "#f8fafc"
  },
  subtitle: {
    margin: "6px 0 0",
    color: "#94a3b8"
  },
  statusBadge: {
    background: "#052e16",
    color: "#86efac",
    padding: "10px 16px",
    borderRadius: "999px",
    fontWeight: 700,
    border: "1px solid #166534"
  },
  kpiGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
    gap: "18px",
    marginBottom: "22px"
  },
  kpiCard: {
    background: "rgba(15, 23, 42, 0.9)",
    border: "1px solid #1e293b",
    borderRadius: "18px",
    padding: "20px",
    boxShadow: "0 20px 40px rgba(0,0,0,0.25)"
  },
  kpiTitle: {
    color: "#94a3b8",
    margin: 0
  },
  kpiValue: {
    fontSize: "34px",
    margin: "10px 0",
    color: "#f8fafc"
  },
  kpiLabel: {
    margin: 0,
    color: "#64748b"
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "22px",
    marginBottom: "22px"
  },
  card: {
    background: "rgba(15, 23, 42, 0.92)",
    border: "1px solid #1e293b",
    borderRadius: "22px",
    padding: "22px",
    boxShadow: "0 20px 40px rgba(0,0,0,0.3)"
  },
  cardTitle: {
    marginTop: 0,
    color: "#f8fafc"
  },
  caseCard: {
    background: "#020617",
    border: "1px solid #334155",
    borderRadius: "14px",
    padding: "16px",
    marginBottom: "14px"
  },
  caseHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center"
  },
  explanation: {
    color: "#94a3b8",
    lineHeight: 1.5
  },
  metrics: {
    background: "#020617",
    color: "#22c55e",
    padding: "16px",
    borderRadius: "14px",
    maxHeight: "360px",
    overflow: "auto",
    fontSize: "12px"
  },
  empty: {
    color: "#94a3b8"
  }
};