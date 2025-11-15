import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Footer from "../components/Footer";

import { useModelResults } from "../context/ModelResultsContext";

const API_BASE_URL = "http://localhost:5000";

function Pollution() {
  const navigate = useNavigate();
  const { updateResult } = useModelResults();

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  const runModel = async () => {
    if (!selectedFile) {
      setError("Please upload an image");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(`${API_BASE_URL}/pollution/infer`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok && data.status === "success") {
        setResult(data.prediction);
        updateResult("pollution", data);
      } else {
        setError(data.message || "Analysis failed.");
      }
    } catch (err) {
      setError("Connection error: " + err.message);
    }

    setLoading(false);
  };

  // Styles
  const s = {
    page: {
      display: 'flex',
      flexDirection: 'column',
      minHeight: '100vh',
      backgroundColor: '#04121f',
      paddingTop: '80px',
      paddingBottom: '60px',
      fontFamily: 'Poppins, sans-serif',
      color: '#e3f6fc',
      position: 'relative'
    },
    main: { display: "flex", flex: 1 },
    content: { flex: 1,
      padding: '2rem',
      paddingBottom: '100px',
      paddingTop:'50px'
     },
    title: {
      fontSize: "2.6rem",
      background: "linear-gradient(90deg,#00b4d8,#0096b8)",
      WebkitBackgroundClip: "text",
      WebkitTextFillColor: "transparent",
      fontFamily: "Merriweather, serif",
    },
    subtitle: { color: "#90e0ef", marginBottom: "2rem" },
    card: {
      background: "rgba(6,26,44,0.6)",
      padding: "1.5rem",
      borderRadius: "12px",
      border: "1px solid rgba(0,180,216,0.3)",
      marginBottom: "2rem",
    },
    cardTitle: { color: "#00b4d8", fontSize: "1.3rem", marginBottom: "1rem" },
    img: { width: "100%", borderRadius: "12px", marginTop: "1rem" },
    btn: {
      padding: "0.8rem 2rem",
      background: "linear-gradient(135deg,#00b4d8,#0096b8)",
      borderRadius: "50px",
      border: "none",
      cursor: "pointer",
      color: "#fff",
      fontWeight: 600,
      marginRight: "1rem",
    },
    error: { color: "#ff6b6b", marginTop: "1rem" },
  };

  return (
    <div style={s.page}>
      <Navbar />

      <div style={s.main}>
        <Sidebar />

        <div style={s.content}>
          <h1 style={s.title}>🏭 Marine Pollution Detection</h1>
          <p style={s.subtitle}>Upload an ocean image to analyze</p>

          {/* Upload Input */}
          <div style={s.card}>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setSelectedFile(e.target.files[0])}
              style={{ marginBottom: "1rem" }}
            />

            <button
              style={s.btn}
              onClick={runModel}
              disabled={!selectedFile}
            >
              Run Pollution Detection
            </button>
          </div>

          {loading && (
            <div style={s.card}>
              <h2 style={s.cardTitle}>Running Model… Please wait</h2>
            </div>
          )}

          {error && (
            <div style={s.card}>
              <p style={s.error}>⚠ {error}</p>
            </div>
          )}

          {result && (
            <div style={s.card}>
              <h2 style={s.cardTitle}>Prediction Result</h2>

              <p><b>Type:</b> {result.type}</p>
              <p><b>Explanation:</b> {result.explanation}</p>

              {result.annotated && (
                <>
                  <h3 style={s.cardTitle}>Annotated Output</h3>
                  <img
                    src={`${API_BASE_URL}/static/pollution/final_overlay.jpg?v=${Date.now()}`}
                    alt="Annotated Output"
                    style={s.img}
                  />
                </>
              )}

              <button style={s.btn} onClick={() => navigate("/coral")}>
                Next →
              </button>
            </div>
          )}
        </div>
      </div>

      <Footer />
    </div>
  );
}

export default Pollution;
