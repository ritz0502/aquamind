import React from 'react';

// Function to calculate summary statistics for the chart data
function summarizeGraph(data) {
  if (!data || data.length === 0) return "No data available to summarize.";

  const values = data.map(d => d.reading);
  const max = Math.max(...values);
  const min = Math.min(...values);
  const avg = (values.reduce((a, b) => a + b, 0) / values.length).toFixed(1);

  return `
    The chart shows anomaly readings across 12 recorded hours.
    The highest reading is ${max}, while the lowest is ${min}.
    The average reading is ${avg}, indicating ${
      avg > 75
        ? "high environmental fluctuations."
        : avg > 55
        ? "moderate variability."
        : "stable ocean conditions."
    }
  `;
}

// GraphExplanation component
const GraphExplanation = ({ chartData, insight, riskLevel }) => {
  const summary = summarizeGraph(chartData);

  return (
    <div
      style={{
        background: "rgba(0, 180, 216, 0.1)",
        padding: "1rem",
        borderRadius: "10px",
        marginTop: "20px",
        border: "1px solid rgba(0, 180, 216, 0.3)"
      }}
    >
      <h4 style={{ color: "#00b4d8", marginBottom: "0.5rem" }}>Graph Interpretation</h4>
      
      {/* Show insight */}
      <p style={{ color: "#caf0f8", fontFamily: "Poppins", lineHeight: "1.5" }}>
        {insight}
      </p>

      {/* Show the graph summary */}
      <div style={{ color: "#caf0f8", fontFamily: "Poppins", marginTop: "1rem" }}>
        <h5 style={{ color: "#00b4d8" }}>Summary:</h5>
        <p>{summary}</p>
      </div>

      {/* Show Risk Level */}
      <div style={{ color: "#caf0f8", fontFamily: "Poppins", marginTop: "1rem" }}>
        <h5 style={{ color: "#00b4d8" }}>Risk Level:</h5>
        <p>{riskLevel}</p>
      </div>
    </div>
  );
};

export default GraphExplanation;
