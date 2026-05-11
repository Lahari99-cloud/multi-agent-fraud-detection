export default function FraudMetrics({ metrics }) {
  return (
    <div>
      <h2>Fraud Metrics</h2>

      <pre
        style={{
          background: "#111",
          color: "#0f0",
          padding: "16px",
          borderRadius: "8px",
          overflowX: "auto"
        }}
      >
        {metrics}
      </pre>
    </div>
  );
}