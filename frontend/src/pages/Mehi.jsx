import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import Footer from '../components/Footer';
import { useOceanInput } from '../context/OceanInputContext';
import { useModelResults } from '../context/ModelResultsContext';
import { runModel } from '../api/api';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer } from 'recharts';

const Mehi = () => {
  const navigate = useNavigate();
  const { inputs } = useOceanInput();
  const { updateResult } = useModelResults();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleRunModel = async () => {
    setLoading(true);
    try {
      const response = await runModel('mehi', inputs);
      setResult(response);
      updateResult('mehi', response);
    } catch (error) {
      alert('Error running MEHI model. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleViewSummary = () => {
    navigate('/dashboard');
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
    summaryButton: {
      background: 'linear-gradient(135deg, #00ff87, #00d9ff)',
      boxShadow: '0 0 20px rgba(0, 255, 135, 0.4)'
    },
    disabledButton: {
      opacity: 0.5,
      cursor: 'not-allowed'
    },
    resultMetric: {
      fontSize: '4rem',
      fontWeight: 'bold',
      color: '#00b4d8',
      marginBottom: '1rem',
      fontFamily: 'Poppins, sans-serif',
      textAlign: 'center'
    },
    resultInsight: {
      fontSize: '1.1rem',
      color: '#caf0f8',
      marginBottom: '2rem',
      fontFamily: 'Poppins, sans-serif',
      textAlign: 'center'
    },
    chartContainer: {
      height: '400px',
      marginTop: '2rem',
      display: 'flex',
      justifyContent: 'center'
    },
    healthGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
      gap: '1.5rem',
      marginTop: '2rem'
    },
    healthCard: {
      background: 'rgba(0, 180, 216, 0.1)',
      padding: '1.5rem',
      borderRadius: '12px',
      border: '1px solid rgba(0, 180, 216, 0.3)',
      textAlign: 'center'
    },
    healthValue: {
      fontSize: '2rem',
      fontWeight: 'bold',
      color: '#90e0ef',
      fontFamily: 'Poppins, sans-serif'
    },
    healthLabel: {
      fontSize: '0.9rem',
      color: '#00b4d8',
      marginTop: '0.5rem',
      fontFamily: 'Poppins, sans-serif',
      fontWeight: '600'
    }
  };

  return (
    <div style={styles.pageContainer}>
      <Navbar />
      <div style={styles.mainLayout}>
        <Sidebar />
        <div style={styles.contentArea}>
          <h1 style={styles.header}>🐠 Marine Ecosystem Health Index (MEHI)</h1>
          <p style={styles.subheader}>Comprehensive assessment of marine ecosystem vitality</p>

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

          {result && (
            <div style={styles.section}>
              <h3 style={styles.sectionTitle}>MEHI Assessment Results</h3>
              <div style={styles.resultMetric}>{result.results?.mehi_score || 'N/A'}</div>
              <p style={styles.resultInsight}>{result.results?.insight}</p>
              
              {result.results?.indicators && (
                <div style={styles.healthGrid}>
                  {Object.entries(result.results.indicators).map(([key, value]) => (
                    <div key={key} style={styles.healthCard}>
                      <div style={styles.healthValue}>{value}</div>
                      <div style={styles.healthLabel}>
                        {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {result.results?.radarData && (
                <div style={styles.chartContainer}>
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart data={result.results.radarData}>
                      <PolarGrid stroke="rgba(0, 180, 216, 0.3)" />
                      <PolarAngleAxis dataKey="indicator" stroke="#90e0ef" />
                      <PolarRadiusAxis stroke="#90e0ef" />
                      <Radar
                        name="Health Metrics"
                        dataKey="value"
                        stroke="#00b4d8"
                        fill="#00b4d8"
                        fillOpacity={0.4}
                        strokeWidth={2}
                      />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
              )}
            </div>
          )}

          <div style={styles.buttonGroup}>
            <button
              style={{ ...styles.button, ...styles.secondaryButton }}
              onClick={() => navigate('/anomalies')}
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
            <button
              style={styles.button}
              onClick={handleRunModel}
              disabled={loading}
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
                ...styles.summaryButton,
                ...(result ? {} : styles.disabledButton)
              }}
              onClick={handleViewSummary}
              disabled={!result}
              onMouseEnter={(e) => {
                if (result) {
                  e.target.style.transform = 'translateY(-2px)';
                  e.target.style.boxShadow = '0 0 30px rgba(0, 255, 135, 0.6)';
                }
              }}
              onMouseLeave={(e) => {
                e.target.style.transform = 'translateY(0)';
                e.target.style.boxShadow = '0 0 20px rgba(0, 255, 135, 0.4)';
              }}
            >
              View Summary Dashboard ✨
            </button>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default Mehi;