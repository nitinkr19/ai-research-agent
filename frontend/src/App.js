import { useState } from "react";

function App() {
  const [topic, setTopic] = useState("");
  const [plan, setPlan] = useState(null);
  const [report, setReport] = useState("");
  const [loading, setLoading] = useState(false);

  const runResearch = async () => {
    setLoading(true);
    setReport("");
    setPlan(null);
  
    const response = await fetch(`/research-stream?topic=${encodeURIComponent(topic)}`, {
      method: "POST"
    });
  
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
  
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
  
      const chunk = decoder.decode(value);
      setReport(prev => prev + chunk);
    }
  
    setLoading(false);
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
