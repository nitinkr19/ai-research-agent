import { useState } from "react";

function App() {
  const [topic, setTopic] = useState("");
  const [plan, setPlan] = useState(null);
  const [report, setReport] = useState("");

  const runResearch = async () => {
    const response = await fetch(`/research?topic=${encodeURIComponent(topic)}`, {
      method: "POST"
    });

    const data = await response.json();
    setPlan(data.plan);
    setReport(data.report);
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
      <button onClick={runResearch}>Run Research</button>

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

