import { useState } from "react";

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
      setReport(prev => prev + event.data);
    };
  
    eventSource.onerror = (err) => {
      console.log("SSE error:", err);
      eventSource.close();
      setLoading(false);
    };
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h2>AI Research Agent</h2>

      <textarea
        style={{ width: "100%", height: "100px" }}
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        placeholder="Enter research topic..."
      />

      <br /><br />
      <button onClick={runResearch} disabled={loading}>
        {loading ? "Running..." : "Run Research"}
      </button>

      {loading && <p>⏳ Generating research...</p>}

      {plan && (
        <>
          <h3>Plan</h3>
          <pre>{JSON.stringify(plan, null, 2)}</pre>
        </>
      )}

      {report && (
        <>
          <h3>Report</h3>
          <pre>{report}</pre>
        </>
      )}
    </div>
  );
}

export default App;
