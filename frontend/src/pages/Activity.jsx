import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import Footer from '../components/Footer';
import { useOceanInput } from '../context/OceanInputContext';
import { useModelResults } from '../context/ModelResultsContext';

// ✅ Correct environment variable
const BACKEND_BASE =
  import.meta.env.VITE_API_BASE || "http://localhost:5000";

const Activity = () => {
  const navigate = useNavigate();
  const { inputs } = useOceanInput();
  const { updateResult } = useModelResults();

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  // ----------------------------------
  // RUN MODEL (Flask API Integration)
  // ----------------------------------
  const handleRunModel = async () => {
    if (!inputs.lat || !inputs.lon) {
      alert("Latitude and longitude are required.");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_BASE}/activity/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          lat: parseFloat(inputs.lat),
          lon: parseFloat(inputs.lon),
        }),
      });

      if (!response.ok) throw new Error("Model execution failed");
      const data = await response.json();

      setResult(data);
      updateResult("activity", data); // store in global context
    } catch (error) {
      console.error(error);
      alert("Error connecting to backend or running the model.");
    } finally {
      setLoading(false);
    }
  };

  // ----------------------------------
  // STYLES
  // ----------------------------------
  const styles = {
    pageContainer: {
      display: 'flex',
      flexDirection: 'column',
      minHeight: '100vh',
      background: 'linear-gradient(180deg, #04121f 0%, #061a2c 100%)',
      color: '#fff'
    },
    mainLayout: { display: 'flex', flex: 1 },
    contentArea: {
      flex: 1,
      padding: '2rem',
      paddingBottom: '100px',
      paddingTop: '100px'
    },
    header: {
      fontFamily: 'Merriweather, serif',
      fontSize: '2.5rem',
      marginBottom: '0.5rem',
      background: 'linear-gradient(90deg, #00b4d8, #0096b8)',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent'
    },
    subheader: {
      fontFamily: 'Poppins, sans-serif',
      fontSize: '1rem',
      color: '#90e0ef',
      marginBottom: '2rem'
    },
    section: {
      background: 'rgba(6, 26, 44, 0.6)',
      padding: '1.5rem',
      borderRadius: '12px',
      border: '1px solid rgba(0, 180, 216, 0.3)',
      marginBottom: '2rem',
      boxShadow: '0 4px 15px rgba(0,0,0,0.3)'
    },
    sectionTitle: {
      fontFamily: 'Merriweather, serif',
      fontSize: '1.3rem',
      color: '#00b4d8',
      marginBottom: '1rem'
    },
    inputGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
      gap: '1rem'
    },
    inputItem: { fontFamily: 'Poppins, sans-serif', fontSize: '0.9rem' },
    inputLabel: { color: '#90e0ef', marginRight: '0.5rem' },
    inputValue: { color: '#fff', fontWeight: '500' },

    // BUTTONS
    buttonGroup: {
      display: 'flex',
      gap: '1rem',
      marginTop: '2rem',
      flexWrap: 'wrap'
    },
    button: {
      padding: '0.75rem 2rem',
      fontSize: '1rem',
      fontFamily: 'Poppins, sans-serif',
      fontWeight: '600',
      background: 'linear-gradient(135deg, #00b4d8, #0096b8)',
      border: 'none',
      borderRadius: '50px',
      color: '#fff',
      cursor: 'pointer',
      boxShadow: '0 0 15px rgba(0,180,216,0.3)',
      transition: 'all 0.3s ease'
    },
    disabledButton: { opacity: 0.5, cursor: 'not-allowed' },

    // METRICS GRID
    metricsGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(3, 1fr)',
      gap: '1.5rem',
      marginBottom: '2rem'
    },
    metricCard: {
      background: 'rgba(0, 180, 216, 0.1)',
      padding: '1rem 1.5rem',
      borderRadius: '10px',
      border: '1px solid rgba(0,180,216,0.3)',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    },
    metricValue: {
      fontSize: '1.6rem',
      fontWeight: '700',
      color: '#00b4d8',
      fontFamily: 'Poppins'
    },
    metricLabel: {
      fontSize: '0.9rem',
      color: '#90e0ef',
      marginTop: '0.5rem'
    },
    resultInsight: {
      fontSize: '1.1rem',
      color: '#caf0f8',
      marginBottom: '1rem'
    }
  };

  return (
    <div style={styles.pageContainer}>
      <Navbar />

      <div style={styles.mainLayout}>
        <Sidebar />

        <div style={styles.contentArea}>
          <h1 style={styles.header}>🚢 Human Activity Analysis</h1>
          <p style={styles.subheader}>Monitoring human-linked coastal activity & risk intensity.</p>

          {/* Input Parameters */}
          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>Current Input Parameters</h3>
            <div style={styles.inputGrid}>
              <div style={styles.inputItem}>
                <span style={styles.inputLabel}>Latitude:</span>
                <span style={styles.inputValue}>{inputs.lat || 'N/A'}</span>
              </div>
              <div style={styles.inputItem}>
                <span style={styles.inputLabel}>Longitude:</span>
                <span style={styles.inputValue}>{inputs.lon || 'N/A'}</span>
              </div>
            </div>
          </div>

          {/* Model Results */}
          {result && (
            <div style={styles.section}>
              <h3 style={styles.sectionTitle}>Activity Risk Model Results</h3>

              <div style={styles.metricsGrid}>
                <div style={styles.metricCard}>
                  <div style={styles.metricValue}>
                    {result.score?.toFixed(1)}
                  </div>
                  <div style={styles.metricLabel}>Risk Score</div>
                </div>

                <div style={styles.metricCard}>
                  <div style={styles.metricValue}>{result.badge}</div>
                  <div style={styles.metricLabel}>Badge</div>
                </div>

                <div style={styles.metricCard}>
                  <div style={styles.metricValue}>{result.features?.ports}</div>
                  <div style={styles.metricLabel}>Nearby Ports</div>
                </div>

                <div style={styles.metricCard}>
                  <div style={styles.metricValue}>{result.features?.industries}</div>
                  <div style={styles.metricLabel}>Industries</div>
                </div>

                <div style={styles.metricCard}>
                  <div style={styles.metricValue}>{result.features?.hotels}</div>
                  <div style={styles.metricLabel}>Hotels</div>
                </div>

                <div style={styles.metricCard}>
                  <div style={styles.metricValue}>{result.features?.ships}</div>
                  <div style={styles.metricLabel}>Ships Density</div>
                </div>
              </div>

              {/* Recommendation */}
              <p
                style={styles.resultInsight}
                dangerouslySetInnerHTML={{
                  __html: result.recommendation
                    .replace(/\|/g, "")
                    .replace(/-\s*/g, "• ")
                    .replace(/\.\s+/g, ".<br><br>")
                }}
              ></p>

              {/* Heatmap */}
              {/* Heatmap */}
<iframe
  key={Date.now()}
  src={`${BACKEND_BASE}/heatmaps/activity_map.html?t=${Date.now()}`}
  style={{
    width: "100%",
    height: "500px",
    border: "none",
    borderRadius: "12px",
    marginTop: "20px",
    background: "#fff"
  }}
  title="activity-map"
/>


            </div>
          )}

          {/* Run Button */}
          <div style={styles.buttonGroup}>
            <button
              style={{
                ...styles.button,
                ...(loading ? styles.disabledButton : {}),
              }}
              onClick={handleRunModel}
              disabled={loading}
            >
              {loading ? "Running..." : "Run Model"}
            </button>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default Activity;
