import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Footer from "../components/Footer";

import { useOceanInput } from "../context/OceanInputContext";
import { useModelResults } from "../context/ModelResultsContext";

const API_BASE_URL = "http://localhost:5000";

function Pollution() {
  const navigate = useNavigate();
  const { inputs } = useOceanInput();       
  const { updateResult } = useModelResults();

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Convert base64 → Blob
  const base64ToBlob = (base64) => {
    const arr = base64.split(",");
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n--) u8arr[n] = bstr.charCodeAt(n);
    return new Blob([u8arr], { type: mime });
  };

  // Auto-run model when page loads
  useEffect(() => {
    if (!inputs.imageUrl) {
      setError("No image found. Please upload an image on the Dashboard.");
      return;
    }
    runModel();
  }, []);

  const runModel = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const blob = base64ToBlob(inputs.imageUrl);
      const file = new File([blob], "ocean.jpg", { type: blob.type });

      const formData = new FormData();
      formData.append("file", file);

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
      paddingTop:'100px'
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
    disabled: { opacity: 0.4, cursor: "not-allowed" },
    error: { color: "#ff6b6b", marginTop: "1rem" },
  };

  return (
    <div style={s.page}>
      <Navbar />

      <div style={s.main}>
        <Sidebar />

        <div style={s.content}>
          <h1 style={s.title}>🏭 Marine Pollution Detection</h1>
          <p style={s.subtitle}>Analyzing your uploaded ocean image…</p>

          {/* LOADING */}
          {loading && (
            <div style={s.card}>
              <h2 style={s.cardTitle}>Running Model… Please wait</h2>
            </div>
          )}

          {/* ERROR */}
          {error && (
            <div style={s.card}>
              <p style={s.error}>⚠ {error}</p>
              <button style={s.btn} onClick={() => navigate("/dashboard")}>
                ← Go Back
              </button>
            </div>
          )}

          {/* RESULT */}
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
