<<<<<<< HEAD
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import Footer from '../components/Footer';
import { useOceanInput } from '../context/OceanInputContext';
import { useModelResults } from '../context/ModelResultsContext';
import { runModel } from '../api/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Coral = () => {
  const navigate = useNavigate();
  const { inputs } = useOceanInput();
  const { updateResult } = useModelResults();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleRunModel = async () => {
    setLoading(true);
    try {
      const response = await runModel('coral', inputs);
      setResult(response);
      updateResult('coral', response);
    } catch (error) {
      alert('Error running coral health model. Please try again.');
=======
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Footer from "../components/Footer";
import axios from "axios";

const Coral = () => {
  const navigate = useNavigate();
  const [imageFile, setImageFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    setImageFile(file);
    setPreviewUrl(URL.createObjectURL(file));
  };

  const handleRunModel = async () => {
    if (!imageFile) {
      alert("Please upload a coral image first.");
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("image", imageFile);

      const response = await axios.post(
        "http://localhost:5000/coral/predict",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      console.log("CORAL API RESPONSE:", response.data);
      setResult(response.data);
    } catch (error) {
      console.error("Coral model error:", error);
      alert("Error running coral health model. Please try again.");
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
    } finally {
      setLoading(false);
    }
  };

  const styles = {
    pageContainer: {
<<<<<<< HEAD
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
      paddingBottom: '100px',
      paddingTop: '100px'

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
    imagePreview: {
      marginTop: '1rem',
      maxWidth: '300px',
      borderRadius: '8px',
      border: '2px solid rgba(0, 180, 216, 0.3)'
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
    resultMetric: {
      fontSize: '3rem',
      fontWeight: 'bold',
      color: '#00b4d8',
      marginBottom: '1rem',
      fontFamily: 'Poppins, sans-serif'
    },
    resultInsight: {
      fontSize: '1.1rem',
      color: '#caf0f8',
      marginBottom: '2rem',
      fontFamily: 'Poppins, sans-serif'
    },
    chartContainer: {
      height: '300px',
      marginTop: '2rem'
    }
=======
      display: "flex",
      flexDirection: "column",
      minHeight: "100vh",
      background: "linear-gradient(180deg, #04121f 0%, #061a2c 100%)",
      color: "#fff",
    },
    mainLayout: {
      display: "flex",
      flex: 1,
    },
    contentArea: {
      flex: 1,
      padding: "2rem",
      paddingBottom: "120px",
      paddingTop: "100px",
    },
    header: {
      fontFamily: "Merriweather, serif",
      fontSize: "2.5rem",
      marginBottom: "0.5rem",
      background: "linear-gradient(90deg, #00b4d8, #0096b8)",
      WebkitBackgroundClip: "text",
      WebkitTextFillColor: "transparent",
      backgroundClip: "text",
    },
    subheader: {
      fontFamily: "Poppins, sans-serif",
      fontSize: "1rem",
      color: "#90e0ef",
      marginBottom: "2rem",
    },
    section: {
      background: "rgba(6, 26, 44, 0.6)",
      padding: "1.5rem",
      borderRadius: "12px",
      border: "1px solid rgba(0, 180, 216, 0.3)",
      marginBottom: "2rem",
      boxShadow: "0 4px 15px rgba(0, 0, 0, 0.3)",
    },
    sectionTitle: {
      fontFamily: "Merriweather, serif",
      fontSize: "1.3rem",
      color: "#00b4d8",
      marginBottom: "1rem",
    },
    imagePreview: {
      marginTop: "1rem",
      maxWidth: "300px",
      borderRadius: "8px",
      border: "2px solid rgba(0, 180, 216, 0.3)",
    },
    buttonGroup: {
      display: "flex",
      gap: "1rem",
      marginTop: "2rem",
      flexWrap: "wrap",
    },
    button: {
      padding: "0.75rem 2rem",
      fontSize: "1rem",
      fontFamily: "Poppins, sans-serif",
      fontWeight: "600",
      background: "linear-gradient(135deg, #00b4d8, #0096b8)",
      border: "none",
      borderRadius: "50px",
      color: "#fff",
      cursor: "pointer",
      boxShadow: "0 0 15px rgba(0, 180, 216, 0.3)",
      transition: "all 0.3s ease",
    },
    secondaryButton: {
      background: "rgba(0, 180, 216, 0.2)",
      border: "1px solid rgba(0, 180, 216, 0.5)",
    },
    resultBox: {
      marginTop: "1rem",
      padding: "1.2rem",
      background: "rgba(0, 50, 70, 0.4)",
      borderRadius: "8px",
      border: "1px solid rgba(0, 180, 216, 0.2)",
    },
    probabilityItem: {
      fontFamily: "Poppins, sans-serif",
      fontSize: "0.95rem",
      padding: "8px 0",
      borderBottom: "1px solid rgba(0, 180, 216, 0.1)",
    },
    resultMetric: {
      fontSize: "2.4rem",
      fontWeight: "bold",
      color: "#00b4d8",
      marginBottom: "1rem",
      fontFamily: "Poppins, sans-serif",
    },
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
  };

  return (
    <div style={styles.pageContainer}>
      <Navbar />
      <div style={styles.mainLayout}>
        <Sidebar />
<<<<<<< HEAD
        <div style={styles.contentArea}>
          <h1 style={styles.header}>🪸 Coral Health Analysis</h1>
          <p style={styles.subheader}>Assessing coral reef vitality and bleaching risk</p>

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
                <span style={styles.inputLabel}>pH:</span>
                <span style={styles.inputValue}>{inputs.pH || 'N/A'}</span>
              </div>
            </div>
            {inputs.imageUrl && (
              <div>
                <h4 style={{ ...styles.sectionTitle, fontSize: '1.1rem', marginTop: '1.5rem' }}>Coral Image</h4>
                <img src={inputs.imageUrl} alt="Coral" style={styles.imagePreview} />
              </div>
=======

        <div style={styles.contentArea}>
          <h1 style={styles.header}>🪸 Coral Health Analysis</h1>
          <p style={styles.subheader}>
            Upload a coral image to detect bleaching condition.
          </p>

          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>Upload Coral Image</h3>

            <input
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
              style={{ marginTop: "10px" }}
            />

            {previewUrl && (
              <img
                src={previewUrl}
                alt="Coral Preview"
                style={styles.imagePreview}
              />
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
            )}
          </div>

          {result && (
            <div style={styles.section}>
              <h3 style={styles.sectionTitle}>Analysis Results</h3>
<<<<<<< HEAD
              <div style={styles.resultMetric}>Health Score: {result.results?.health_score}</div>
              <p style={styles.resultInsight}>{result.results?.insight}</p>
              {result.results?.chartData && (
                <div style={styles.chartContainer}>
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={result.results.chartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(0, 180, 216, 0.2)" />
                      <XAxis dataKey="month" stroke="#90e0ef" />
                      <YAxis stroke="#90e0ef" />
                      <Tooltip
                        contentStyle={{
                          background: '#04121f',
                          border: '1px solid #00b4d8',
                          borderRadius: '8px'
                        }}
                      />
                      <Line type="monotone" dataKey="health" stroke="#00b4d8" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              )}
=======

              <div style={styles.resultMetric}>
                Status: {result.label.toUpperCase()}
              </div>

              <div style={styles.resultBox}>
                {Object.entries(result.probabilities).map(([cls, prob]) => (
                  <div key={cls} style={styles.probabilityItem}>
                    {cls.toUpperCase()}: {(prob * 100).toFixed(2)}%
                  </div>
                ))}
              </div>
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
            </div>
          )}

          <div style={styles.buttonGroup}>
            <button
              style={{ ...styles.button, ...styles.secondaryButton }}
<<<<<<< HEAD
              onClick={() => navigate('/pollution')}
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
              onClick={() => navigate("/pollution")}
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
              onClick={() => navigate('/forecast')}
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
              {loading ? "Running..." : "Run Model"}
            </button>

            <button
              style={{
                ...styles.button,
                ...(result ? {} : styles.disabledButton),
              }}
              onClick={() => navigate("/forecast")}
              disabled={!result}
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
            >
              Next →
            </button>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

<<<<<<< HEAD
export default Coral;
=======
export default Coral;
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
