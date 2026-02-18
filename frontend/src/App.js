import { useState } from "react";
import { renderFormattedReport } from "./reportFormatting";

function App() {
  const [topic, setTopic] = useState("");
  const [plan] = useState(null);
  const [report, setReport] = useState("");
  const [loading, setLoading] = useState(false);

  const API_BASE = process.env.REACT_APP_API_URL;

  const runResearch = () => {
    setLoading(true);
    setReport("");

    const eventSource = new EventSource(
      `${API_BASE}/research-stream?topic=${encodeURIComponent(topic)}`
    );

    eventSource.onmessage = (event) => {
      setReport((prev) => prev + event.data);
    };

    eventSource.onerror = (err) => {
      console.log("SSE error:", err);
      eventSource.close();
      setLoading(false);
    };
  };

  const spinnerStyle = {
    width: "16px",
    height: "16px",
    border: "2px solid #ccc",
    borderTop: "2px solid #007bff",
    borderRadius: "50%",
    animation: "spin 0.8s linear infinite",
  };

  return (
    <div
      style={{
        padding: "40px",
        fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif",
        maxWidth: "1200px",
        margin: "0 auto",
      }}
    >
      <h2 style={{ marginBottom: "30px", color: "#333" }}>AI Research Agent</h2>
      <style>
      {`
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
      `}
      </style>

      <textarea
        style={{
          width: "100%",
          height: "100px",
          padding: "12px",
          fontSize: "16px",
          border: "1px solid #ddd",
          borderRadius: "6px",
          fontFamily: "inherit",
          resize: "vertical",
          boxSizing: "border-box",
        }}
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        placeholder="Enter research topic..."
      />

      <br />
      <br />
      <button
        onClick={runResearch}
        disabled={loading}
        style={{
          position: "relative",
          zIndex: 1,
          padding: "12px 24px",
          fontSize: "16px",
          cursor: loading ? "not-allowed" : "pointer",
          marginBottom: "20px",
          backgroundColor: loading ? "#ccc" : "#007bff",
          color: "white",
          border: "none",
          borderRadius: "6px",
          fontWeight: "500",
          transition: "background-color 0.2s",
        }}
      >
        {loading ? "Running..." : "Run Research"}
      </button>

      {loading && (
        <div style={{ 
          marginTop: "10px", 
          display: "flex", 
          alignItems: "center", 
          gap: "8px",
          color: "#666"
        }}>
          <div style={spinnerStyle}></div>
          <span>Generating research...</span>
        </div>
      )}

      {plan && (
        <div style={{ marginTop: "30px" }}>
          <h3 style={{ color: "#333", marginBottom: "15px" }}>Plan</h3>
          <div
            style={{
              backgroundColor: "#f8f9fa",
              padding: "20px",
              borderRadius: "6px",
              border: "1px solid #e9ecef",
              overflowX: "auto",
              whiteSpace: "pre-wrap",
              wordBreak: "break-word",
            }}
          >
            <pre
              style={{
                margin: 0,
                whiteSpace: "pre-wrap",
                wordBreak: "break-word",
                fontFamily: "inherit",
              }}
            >
              {JSON.stringify(plan, null, 2)}
            </pre>
          </div>
        </div>
      )}

      {report && (
        <div style={{ marginTop: "30px" }}>
          <h3 style={{ color: "#333", marginBottom: "15px" }}>Report</h3>
          <div
            style={{
              backgroundColor: "#ffffff",
              padding: "30px",
              borderRadius: "8px",
              border: "1px solid #e9ecef",
              boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
              maxHeight: "70vh",
              overflowY: "auto",
              overflowX: "hidden",
              lineHeight: "1.6",
              fontSize: "15px",
              color: "#333",
            }}
          >
            <div
              style={{
                wordWrap: "break-word",
                wordBreak: "break-word",
                overflowWrap: "break-word",
                maxWidth: "100%",
              }}
            >
              {renderFormattedReport(report)}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
