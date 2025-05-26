import React, { useState } from "react";
import axios from "axios";

function App() {
  const [code, setCode] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult("Analyzing...");

    try {
      const res = await axios.post("http://localhost:5000/analyze", {
        code: code,
      });

      setResult(res.data.analysis || "No result received.");
    } catch (err) {
      console.error(err);
      setResult("❌ Error: " + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>🔍 Universal Code Analyzer</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          className="code-box"
          rows="10"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Paste code in any language here..."
        ></textarea>
        <button className="analyze-btn" type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Code"}
        </button>
      </form>

      <div className="result-box">
        <h2>📊 Analysis Results:</h2>
        <pre>{result}</pre>
      </div>
    </div>
  );
}

export default App;

