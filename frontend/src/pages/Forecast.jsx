import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Footer from "../components/Footer";

import { useOceanInput } from "../context/OceanInputContext";   // ← IMPORTANT

const VITE_API_URL = "http://localhost:5000";

function Forecast() {
  const navigate = useNavigate();
  const { inputs } = useOceanInput();   // ← GET GLOBAL COORDINATES

  const [formData, setFormData] = useState({
    lat: inputs.lat || "",
    lon: inputs.lon || "",
    forecast_days: 7,
    quick_mode: true,
  });

  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [plotUrl, setPlotUrl] = useState(null);
  const [reportText, setReportText] = useState(null);

  const resultsRef = useRef(null);

  // Update form whenever dashboard changes values
  useEffect(() => {
    if (inputs.lat && inputs.lon) {
      setFormData((prev) => ({
        ...prev,
        lat: inputs.lat,
        lon: inputs.lon,
      }));
    }
  }, [inputs.lat, inputs.lon]);

  // Auto-run forecast when page loads WITH coordinates
  useEffect(() => {
    if (inputs.lat && inputs.lon && !results && !loading) {
      handleRunForecast();
    }
  }, [inputs.lat, inputs.lon]);

  // Progress animation
  useEffect(() => {
    if (loading) {
      setProgress(0);
      const t = setInterval(() => {
        setProgress((p) => (p >= 90 ? 90 : p + 10));
      }, 500);
      return () => clearInterval(t);
    }
  }, [loading]);

  // ========= RUN FORECAST VIA SAME ROUTE AS RISK ========= //
  const handleRunForecast = async () => {
    setLoading(true);
    setError(null);
    setResults(null);
    setPlotUrl(null);
    setReportText(null);

    try {
      const response = await fetch(`${VITE_API_URL}/risk/run_pipeline`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          lat: parseFloat(formData.lat),
          lon: parseFloat(formData.lon),
          forecast_days: parseInt(formData.forecast_days),
          quick_mode: formData.quick_mode,
        }),
      });

      const data = await response.json();

      if (response.ok && data.status === "success") {
        setProgress(100);
        setResults(data);

        // FETCH PLOT
        const plotRes = await fetch(
          `${VITE_API_URL}/risk/get_plot?lat=${formData.lat}&lon=${formData.lon}`
        );
        if (plotRes.ok) {
          const blob = await plotRes.blob();
          setPlotUrl(URL.createObjectURL(blob));
        }

        // FETCH REPORT
        const reportRes = await fetch(
          `${VITE_API_URL}/risk/get_report?lat=${formData.lat}&lon=${formData.lon}`
        );
        if (reportRes.ok) {
          setReportText(await reportRes.text());
        }
      } else {
        setError(data.message || "Pipeline failed");
      }
    } catch (err) {
      setError(`Connection error: ${err.message}`);
    }

    setLoading(false);
  };

  // ========= INLINE CSS ========= //
  const s = {
    page: {
      minHeight: "100vh",
      background: "linear-gradient(180deg,#04121f,#061a2c)",
      color: "#fff",
      display: "flex",
      flexDirection: "column",
    },
    main: { display: "flex", flex: 1 },
    content: { flex: 1, padding: "2rem", paddingTop: "110px" },

    title: {
      fontSize: "2.6rem",
      background: "linear-gradient(90deg,#00b4d8,#0096b8)",
      WebkitBackgroundClip: "text",
      WebkitTextFillColor: "transparent",
      fontFamily: "Merriweather, serif",
    },

    subtitle: { color: "#90e0ef", fontFamily: "Poppins", marginBottom: "2rem" },

    card: {
      background: "rgba(6,26,44,0.6)",
      padding: "1.5rem",
      borderRadius: "12px",
      border: "1px solid rgba(0,180,216,0.3)",
      marginBottom: "2rem",
    },

    cardTitle: {
      fontSize: "1.3rem",
      fontFamily: "Merriweather",
      color: "#00b4d8",
      marginBottom: "1rem",
    },

    plot: { width: "100%", borderRadius: "12px", marginTop: "1rem" },

    report: {
      whiteSpace: "pre-wrap",
      background: "#04121f",
      padding: "1rem",
      borderRadius: "10px",
      border: "1px solid #0096b8",
    },

    btnRow: { display: "flex", gap: "1rem", marginTop: "1rem" },

    btn: {
      padding: "0.75rem 2rem",
      borderRadius: "50px",
      background: "linear-gradient(135deg,#00b4d8,#0096b8)",
      border: "none",
      color: "#fff",
      cursor: "pointer",
      fontWeight: 600,
    },

    disabled: { opacity: 0.4, cursor: "not-allowed" },
  };

  return (
    <div style={s.page}>
      <Navbar />

      <div style={s.main}>
        <Sidebar />
        <div style={s.content}>
          <h1 style={s.title}>🌊 Ocean Forecast</h1>
          <p style={s.subtitle}>Auto-analysis using selected coordinates</p>

          {/* RESULTS OR LOADER */}
          {loading && (
            <div style={s.card}>
              <h2 style={s.cardTitle}>Running model... {progress}%</h2>
            </div>
          )}

          {error && (
            <div style={s.card}>
              <p style={{ color: "#ff6b6b" }}>⚠ {error}</p>
            </div>
          )}

          {results && (
            <div ref={resultsRef}>
              {/* Plot */}
              {plotUrl && (
                <div style={s.card}>
                  <h2 style={s.cardTitle}>📊 Forecast Plot</h2>
                  <img src={plotUrl} style={s.plot} />
                </div>
              )}

              {/* Report */}
              {reportText && (
                <div style={s.card}>
                  <h2 style={s.cardTitle}>📝 Forecast Report</h2>
                  <pre style={s.report}>{reportText}</pre>
                </div>
              )}
            </div>
          )}

          {/* Bottom Buttons */}
          <div style={s.btnRow}>
            <button style={s.btn} onClick={() => navigate("/coral")}>
              ← Previous
            </button>

            <button
              style={{ ...s.btn, ...(results ? {} : s.disabled) }}
              disabled={!results}
              onClick={() => navigate("/activity")}
            >
              Next →
            </button>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
}

export default Forecast;
