export default function AnalystQueue({ queue }) {
  return (
    <div>
      <h2>Analyst Queue</h2>

      {queue.map((item, idx) => (
        <div
          key={idx}
          style={{
            border: "1px solid #ccc",
            padding: "12px",
            marginBottom: "12px",
            borderRadius: "8px"
          }}
        >
          <h3>{item.transaction_id}</h3>
          <p>Risk Level: {item.risk_level}</p>
          <p>Action: {item.recommended_action}</p>
          <p>Risk Score: {item.risk_score}</p>
        </div>
      ))}
    </div>
  );
}