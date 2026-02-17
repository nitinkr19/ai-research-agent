import { useState } from "react";
import {
  formatJsonAsBullets,
  renderFormattedText,
  renderMarkdown,
} from "./reportFormatting";

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
    <div style={{ 
      padding: "40px", 
      fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif",
      maxWidth: "1200px",
      margin: "0 auto"
    }}>
      <h2 style={{ marginBottom: "30px", color: "#333" }}>AI Research Agent</h2>

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
          boxSizing: "border-box"
        }}
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        placeholder="Enter research topic..."
      />

      <br /><br />
      <button 
        onClick={runResearch} 
        disabled={loading}
        style={{
          position: 'relative',
          zIndex: 1,
          padding: '12px 24px',
          fontSize: '16px',
          cursor: loading ? 'not-allowed' : 'pointer',
          marginBottom: '20px',
          backgroundColor: loading ? '#ccc' : '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          fontWeight: '500',
          transition: 'background-color 0.2s'
        }}
      >
        {loading ? "Running..." : "Run Research"}
      </button>

      {loading && <p style={{ marginTop: '10px', position: 'relative', zIndex: 0, color: '#666' }}>⏳ Generating research...</p>}

      {plan && (
        <div style={{ marginTop: '30px' }}>
          <h3 style={{ color: '#333', marginBottom: '15px' }}>Plan</h3>
          <div style={{
            backgroundColor: '#f8f9fa',
            padding: '20px',
            borderRadius: '6px',
            border: '1px solid #e9ecef',
            overflowX: 'hidden',
            wordBreak: 'break-word',
            lineHeight: '1.8'
          }}>
            <div style={{ marginLeft: '10px' }}>
              {renderMarkdown(formatJsonAsBullets(plan))}
            </div>
          </div>
        </div>
      )}

      {report && (
        <div style={{ marginTop: '30px' }}>
          <h3 style={{ color: '#333', marginBottom: '15px' }}>Report</h3>
          <div style={{
            backgroundColor: '#ffffff',
            padding: '30px',
            borderRadius: '8px',
            border: '1px solid #e9ecef',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
            maxHeight: '70vh',
            overflowY: 'auto',
            overflowX: 'hidden',
            lineHeight: '1.8',
            fontSize: '15px',
            color: '#333'
          }}>
            <div style={{
              wordWrap: 'break-word',
              wordBreak: 'break-word',
              overflowWrap: 'break-word',
              maxWidth: '100%'
            }}>
              {renderFormattedText(report)}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
