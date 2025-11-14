import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import Footer from '../components/Footer';
import { useOceanInput } from '../context/OceanInputContext';
import { useModelResults } from '../context/ModelResultsContext';
<<<<<<< HEAD
import { runModel } from '../api/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
=======
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8

const Anomalies = () => {
  const navigate = useNavigate();
  const { inputs } = useOceanInput();
  const { updateResult } = useModelResults();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleRunModel = async () => {
    setLoading(true);
<<<<<<< HEAD
    try {
      const response = await runModel('anomalies', inputs);
      setResult(response);
      updateResult('anomalies', response);
    } catch (error) {
      alert('Error running anomaly detection model. Please try again.');
=======

    try {
      const response = await axios.post(
        "http://localhost:5000/api/anomalies/run",
        inputs,
        { headers: { "Content-Type": "application/json" } }
      );

      console.log("API RESPONSE:", response.data);

      setResult(response.data);
      updateResult("anomalies", response.data);

    } catch (error) {
      console.error("Anomaly model error:", error);
      alert("Error running anomaly detection model. Please try again.");
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
    } finally {
      setLoading(false);
    }
  };

  const styles = {
    pageContainer: {
      display: 'flex',
      flexDirection: 'column',
      minHeight: '100vh',
      background: 'linear-gradient(180deg, #04121f 0%, #061a2c 100%)',
      color: '#fff'
    },
    mainLayout: {
      display: 'flex',
      flex: 1
    },
    contentArea: {
      flex: 1,
      padding: '2rem',
<<<<<<< HEAD
      paddingBottom: '100px',
      paddingTop: '100px'

=======
      paddingBottom: '220px',   // ⭐ Increased
      paddingTop: '100px'
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
    },
    header: {
      fontFamily: 'Merriweather, serif',
      fontSize: '2.5rem',
      marginBottom: '0.5rem',
      background: 'linear-gradient(90deg, #00b4d8, #0096b8)',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
      backgroundClip: 'text'
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
      boxShadow: '0 4px 15px rgba(0, 0, 0, 0.3)'
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
    inputItem: {
      fontFamily: 'Poppins, sans-serif',
      fontSize: '0.9rem'
    },
    inputLabel: {
      color: '#90e0ef',
      marginRight: '0.5rem'
    },
    inputValue: {
      color: '#fff',
      fontWeight: '500'
    },
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
      boxShadow: '0 0 15px rgba(0, 180, 216, 0.3)',
      transition: 'all 0.3s ease'
    },
    secondaryButton: {
      background: 'rgba(0, 180, 216, 0.2)',
      border: '1px solid rgba(0, 180, 216, 0.5)'
    },
    disabledButton: {
      opacity: 0.5,
      cursor: 'not-allowed'
    },
    alertBadge: {
      display: 'inline-block',
      padding: '0.5rem 1rem',
      borderRadius: '20px',
      fontSize: '1rem',
      fontWeight: 'bold',
      marginBottom: '1rem',
      fontFamily: 'Poppins, sans-serif'
    },
    riskLow: {
      background: 'rgba(0, 255, 0, 0.2)',
      color: '#00ff00',
      border: '1px solid rgba(0, 255, 0, 0.4)'
    },
    riskMedium: {
      background: 'rgba(255, 165, 0, 0.2)',
      color: '#ffa500',
      border: '1px solid rgba(255, 165, 0, 0.4)'
    },
    riskHigh: {
      background: 'rgba(255, 0, 0, 0.2)',
      color: '#ff0000',
      border: '1px solid rgba(255, 0, 0, 0.4)'
    },
    resultInsight: {
      fontSize: '1.1rem',
      color: '#caf0f8',
      marginBottom: '2rem',
      fontFamily: 'Poppins, sans-serif'
    },
    anomalyList: {
      marginTop: '1rem',
      marginBottom: '2rem'
    },
    anomalyItem: {
      background: 'rgba(0, 180, 216, 0.1)',
      padding: '1rem',
      borderRadius: '8px',
      marginBottom: '0.5rem',
      border: '1px solid rgba(0, 180, 216, 0.2)',
      fontFamily: 'Poppins, sans-serif',
      fontSize: '0.95rem'
    },
    chartContainer: {
      height: '300px',
<<<<<<< HEAD
      marginTop: '2rem'
    }
=======
      minHeight: '300px',
      width: '100%',
      minWidth: 0,
      marginTop: '2rem',
      marginBottom: '120px'   // ⭐ ADDED
    }

>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
  };

  const getRiskStyle = (risk) => {
    if (!risk) return styles.riskLow;
    const riskLower = risk.toLowerCase();
    if (riskLower.includes('high')) return styles.riskHigh;
<<<<<<< HEAD
    if (riskLower.includes('medium') || riskLower.includes('moderate')) return styles.riskMedium;
=======
    if (riskLower.includes('medium') || riskLower.includes('moderate'))
      return styles.riskMedium;
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
    return styles.riskLow;
  };

  return (
    <div style={styles.pageContainer}>
      <Navbar />
      <div style={styles.mainLayout}>
        <Sidebar />
        <div style={styles.contentArea}>
          <h1 style={styles.header}>⚠️ Anomaly Detection</h1>
          <p style={styles.subheader}>Identifying unusual patterns and environmental irregularities</p>

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
              <div style={styles.inputItem}>
                <span style={styles.inputLabel}>Depth:</span>
                <span style={styles.inputValue}>{inputs.depth ? `${inputs.depth}m` : 'N/A'}</span>
              </div>
              <div style={styles.inputItem}>
                <span style={styles.inputLabel}>Temperature:</span>
                <span style={styles.inputValue}>{inputs.temperature ? `${inputs.temperature}°C` : 'N/A'}</span>
              </div>
              <div style={styles.inputItem}>
                <span style={styles.inputLabel}>Salinity:</span>
                <span style={styles.inputValue}>{inputs.salinity ? `${inputs.salinity} PSU` : 'N/A'}</span>
              </div>
              <div style={styles.inputItem}>
                <span style={styles.inputLabel}>pH:</span>
                <span style={styles.inputValue}>{inputs.pH || 'N/A'}</span>
              </div>
            </div>
          </div>

<<<<<<< HEAD
          {result && (
            <div style={styles.section}>
              <h3 style={styles.sectionTitle}>Anomaly Detection Results</h3>
              <div style={{ ...styles.alertBadge, ...getRiskStyle(result.results?.risk_level) }}>
                {result.results?.risk_level || 'Unknown Risk'}
              </div>
              <p style={styles.resultInsight}>{result.results?.insight}</p>
              
=======
          {/* ⭐ FULL RESULTS SECTION FIXED */}
          {result && (
            <div style={styles.section}>
              <h3 style={styles.sectionTitle}>Anomaly Detection Results</h3>

              <div style={{ ...styles.alertBadge, ...getRiskStyle(result.results?.risk_level) }}>
                {result.results?.risk_level || 'Unknown Risk'}
              </div>

              <p style={styles.resultInsight}>{result.results?.insight}</p>

>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
              {result.results?.anomalies && result.results.anomalies.length > 0 && (
                <div style={styles.anomalyList}>
                  <h4 style={{ ...styles.sectionTitle, fontSize: '1.1rem' }}>Detected Anomalies:</h4>
                  {result.results.anomalies.map((anomaly, index) => (
                    <div key={index} style={styles.anomalyItem}>
                      {anomaly}
                    </div>
                  ))}
                </div>
              )}

<<<<<<< HEAD
              {result.results?.chartData && (
                <div style={styles.chartContainer}>
                  <ResponsiveContainer width="100%" height="100%">
=======
              {/* ⭐ FIXED CHART */}
              {result.results?.chartData && (
                <div style={styles.chartContainer}>
                  <ResponsiveContainer width="100%" aspect={3}>
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
                    <LineChart data={result.results.chartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(0, 180, 216, 0.2)" />
                      <XAxis dataKey="time" stroke="#90e0ef" />
                      <YAxis stroke="#90e0ef" />
                      <Tooltip
                        contentStyle={{
                          background: '#04121f',
                          border: '1px solid #00b4d8',
                          borderRadius: '8px'
                        }}
                      />
                      <ReferenceLine y={75} stroke="#ff0000" strokeDasharray="3 3" label="Threshold" />
                      <Line type="monotone" dataKey="reading" stroke="#00b4d8" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              )}
            </div>
          )}

<<<<<<< HEAD
=======
          <div style={{ height: "40px" }}></div>   {/* spacer */}

>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
          <div style={styles.buttonGroup}>
            <button
              style={{ ...styles.button, ...styles.secondaryButton }}
              onClick={() => navigate('/activity')}
<<<<<<< HEAD
              onMouseEnter={(e) => {
                e.target.style.transform = 'translateY(-2px)';
                e.target.style.boxShadow = '0 0 20px rgba(0, 180, 216, 0.4)';
              }}
              onMouseLeave={(e) => {
                e.target.style.transform = 'translateY(0)';
                e.target.style.boxShadow = '0 0 15px rgba(0, 180, 216, 0.3)';
              }}
            >
              ← Previous
            </button>
=======
            >
              ← Previous
            </button>

>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
            <button
              style={styles.button}
              onClick={handleRunModel}
              disabled={loading}
<<<<<<< HEAD
              onMouseEnter={(e) => {
                if (!loading) {
                  e.target.style.transform = 'translateY(-2px)';
                  e.target.style.boxShadow = '0 0 25px rgba(0, 180, 216, 0.5)';
                }
              }}
              onMouseLeave={(e) => {
                e.target.style.transform = 'translateY(0)';
                e.target.style.boxShadow = '0 0 15px rgba(0, 180, 216, 0.3)';
              }}
            >
              {loading ? 'Running...' : 'Run Model'}
            </button>
            <button
              style={{
                ...styles.button,
                ...(result ? {} : styles.disabledButton)
              }}
              onClick={() => navigate('/mehi')}
              disabled={!result}
              onMouseEnter={(e) => {
                if (result) {
                  e.target.style.transform = 'translateY(-2px)';
                  e.target.style.boxShadow = '0 0 25px rgba(0, 180, 216, 0.5)';
                }
              }}
              onMouseLeave={(e) => {
                e.target.style.transform = 'translateY(0)';
                e.target.style.boxShadow = '0 0 15px rgba(0, 180, 216, 0.3)';
              }}
=======
            >
              {loading ? 'Running...' : 'Run Model'}
            </button>

            <button
              style={{ ...styles.button, ...(result ? {} : styles.disabledButton) }}
              onClick={() => navigate('/mehi')}
              disabled={!result}
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
            >
              Next →
            </button>
          </div>
<<<<<<< HEAD
=======

>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
        </div>
      </div>
      <Footer />
    </div>
  );
};

<<<<<<< HEAD
export default Anomalies;
=======
export default Anomalies;
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
