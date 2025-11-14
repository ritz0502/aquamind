import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Footer from "../components/Footer";
import "./Mehi.css";

const Mehi = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState(null);

  const handleFetchSummary = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/summary");
      const data = await response.json();
      setSummary(data);
    } catch (error) {
      alert("Error fetching summary data");
    }
    setLoading(false);
  };

  const handleDownload = () => {
    if (!summary) return;

    const blob = new Blob([JSON.stringify(summary, null, 2)], {
      type: "application/json",
    });

    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "MEHI_Summary.json";
    link.click();
  };

  return (
    <div className="mehi-page">
      <Navbar />

      <div className="mehi-main">
        <Sidebar />

        <div className="mehi-content">
          <h1 className="mehi-title">🐠 Marine Ecosystem Health Index (MEHI)</h1>
          <p className="mehi-subtitle">
            Combined analysis of marine health using all model outputs.
          </p>

          <button
            className="mehi-btn mehi-btn-primary"
            onClick={handleFetchSummary}
            disabled={loading}
          >
            {loading ? "Fetching..." : "Fetch Latest Summary"}
          </button>

          {/* ===== SUMMARY BLOCK ===== */}
          {summary && (
            <div className="summary-grid">

              {/* ===== MEHI SCORE ===== */}
              <div className="mehi-score-box">
                <div className="mehi-score">{summary.mehi ?? "N/A"}</div>
                <div className="mehi-score-label">Overall Marine Health Score</div>
              </div>

              {/* ===== RISK CARD ===== */}
              <div className="summary-card">
                <h3 className="card-title">Risk</h3>

                <div className="card-item">
                  <span className="card-label">Risk Level:</span>
                  <span className="card-value">{summary.risk?.risk_level}</span>
                </div>

                <div className="card-item">
                  <span className="card-label">Coordinates:</span>
                  <span className="card-value">
                    {summary.risk?.coordinates?.lat}, {summary.risk?.coordinates?.lon}
                  </span>
                </div>
              </div>

              {/* ===== POLLUTION CARD ===== */}
              <div className="summary-card">
                <h3 className="card-title">Pollution</h3>

                <div className="card-item">
                  <span className="card-label">Type:</span>
                  <span className="card-value">{summary.pollution?.type}</span>
                </div>

                <div className="card-item">
                  <span className="card-label">Explanation:</span>
                  <span className="card-value">{summary.pollution?.explanation}</span>
                </div>
              </div>

              {/* ===== CORAL CARD ===== */}
              <div className="summary-card">
                <h3 className="card-title">Coral</h3>

                <div className="card-item">
                  <span className="card-label">Health Score:</span>
                  <span className="card-value">
                    {summary.coral?.health_score ?? "N/A"}
                  </span>
                </div>
              </div>

              {/* ===== BUTTONS ===== */}
              <div className="button-row">
                <button
                  className="mehi-btn mehi-btn-download"
                  onClick={handleDownload}
                >
                  ⬇ Download Summary
                </button>

                <button
                  className="mehi-btn mehi-btn-green"
                  onClick={() => navigate("/dashboard")}
                >
                  Go to Dashboard →
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default Mehi;
