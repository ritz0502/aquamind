import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import Footer from '../components/Footer';
import { useOceanInput } from '../context/OceanInputContext';
import { useModelResults } from '../context/ModelResultsContext';
import { runModel } from '../api/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Activity = () => {
  const navigate = useNavigate();
  const { inputs } = useOceanInput();
  const { updateResult } = useModelResults();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleRunModel = async () => {
    setLoading(true);
    try {
      const response = await runModel('activity', inputs);
      setResult(response);
      updateResult('activity', response);
    } catch (error) {
      alert('Error running activity model. Please try again.');
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
    disabledButton: {
      opacity: 0.5,
      cursor: 'not-allowed'
    },
    metricsGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
      gap: '1.5rem',
      marginBottom: '2rem'
    },
    metricCard: {
      background: 'rgba(0, 180, 216, 0.1)',
      padding: '1rem',
      borderRadius: '8px',
      border: '1px solid rgba(0, 180, 216, 0.3)',
      textAlign: 'center'
    },
    metricValue: {
      fontSize: '2.5rem',
      fontWeight: 'bold',
      color: '#00b4d8',
      fontFamily: 'Poppins, sans-serif'
    },
    metricLabel: {
      fontSize: '0.9rem',
      color: '#90e0ef',
      marginTop: '0.5rem',
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
  };

  return (
    <div style={styles.pageContainer}>
      <Navbar />
      <div style={styles.mainLayout}>
        <Sidebar />
        <div style={styles.contentArea}>
          <h1 style={styles.header}>🚢 Human Activity Analysis</h1>
          <p style={styles.subheader}>Monitoring shipping traffic, tourism, and marine activity</p>

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

          {result && (
            <div style={styles.section}>
              <h3 style={styles.sectionTitle}>Activity Analysis Results</h3>
              <div style={styles.metricsGrid}>
                <div style={styles.metricCard}>
                  <div style={styles.metricValue}>{result.results?.ships_detected || 0}</div>
                  <div style={styles.metricLabel}>Ships Detected</div>
                </div>
                <div style={styles.metricCard}>
                  <div style={styles.metricValue}>{result.results?.ports_nearby || 0}</div>
                  <div style={styles.metricLabel}>Nearby Ports</div>
                </div>
                <div style={styles.metricCard}>
                  <div style={styles.metricValue}>{result.results?.tourism_density || 0}</div>
                  <div style={styles.metricLabel}>Tourism Density</div>
                </div>
              </div>
              <p style={styles.resultInsight}>{result.results?.insight}</p>
              {result.results?.chartData && (
                <div style={styles.chartContainer}>
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={result.results.chartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(0, 180, 216, 0.2)" />
                      <XAxis dataKey="category" stroke="#90e0ef" />
                      <YAxis stroke="#90e0ef" />
                      <Tooltip
                        contentStyle={{
                          background: '#04121f',
                          border: '1px solid #00b4d8',
                          borderRadius: '8px'
                        }}
                      />
                      <Bar dataKey="count" fill="#00b4d8" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              )}
            </div>
          )}

          <div style={styles.buttonGroup}>
            <button
              style={{ ...styles.button, ...styles.secondaryButton }}
              onClick={() => navigate('/forecast')}
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
                ...(result ? {} : styles.disabledButton)
              }}
              onClick={() => navigate('/anomalies')}
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

export default Activity;  