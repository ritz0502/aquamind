import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import Footer from '../components/Footer';
import MapPicker from '../components/MapPicker';
import { useOceanInput } from '../context/OceanInputContext';
import { useModelResults } from '../context/ModelResultsContext';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
  const navigate = useNavigate();
  const { inputs, updateInput, updateMultipleInputs } = useOceanInput();
  const { results } = useModelResults();
  const [imageFile, setImageFile] = useState(null);

  const handleLocationSelect = (lat, lon) => {
    updateMultipleInputs({
      lat: lat.toFixed(4),
      lon: lon.toFixed(4)
    });
  };

  // const handleImageUpload = (e) => {
  //   const file = e.target.files[0];
  //   if (file) {
  //     setImageFile(file);
  //     const reader = new FileReader();
  //     reader.onloadend = () => {
  //       updateInput('imageUrl', reader.result);
  //     };
  //     reader.readAsDataURL(file);
  //   }
  // };

  const handleAnalyze = () => {
    if (!inputs.lat || !inputs.lon || !inputs.depth || !inputs.salinity || !inputs.temperature || !inputs.pH) {
      alert('Please fill all required fields');
      return;
    }
    navigate('/pollution');
  };

  const hasResults = Object.values(results).some(r => r !== null);

  const styles = {
    pageContainer: {
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
    mainLayout: {
      display: 'flex',
      flex: 1
    },
    contentArea: {
      flex: 1,
      padding: '2rem',
      paddingBottom: '100px',
      paddingTop: '50px'
    },
    header: {
      fontFamily: 'Merriweather, serif',
      fontSize: '2.5rem',
      marginBottom: '1rem',
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
    inputSection: {
      background: 'rgba(6, 26, 44, 0.6)',
      padding: '2rem',
      borderRadius: '16px',
      border: '1px solid rgba(0, 180, 216, 0.3)',
      marginBottom: '2rem',
      boxShadow: '0 4px 20px rgba(0, 0, 0, 0.3)'
    },
    inputGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
      gap: '1.5rem',
      marginTop: '1.5rem'
    },
    inputGroup: {
      display: 'flex',
      flexDirection: 'column'
    },
    label: {
      fontFamily: 'Poppins, sans-serif',
      fontSize: '0.9rem',
      marginBottom: '0.5rem',
      color: '#90e0ef'
    },
    input: {
      padding: '0.75rem',
      borderRadius: '8px',
      border: '1px solid rgba(0, 180, 216, 0.4)',
      background: 'rgba(4, 18, 31, 0.8)',
      color: '#fff',
      fontFamily: 'Poppins, sans-serif',
      fontSize: '0.95rem',
      outline: 'none',
      transition: 'all 0.3s ease'
    },
    fileInput: {
      padding: '0.5rem',
      borderRadius: '8px',
      border: '1px solid rgba(0, 180, 216, 0.4)',
      background: 'rgba(4, 18, 31, 0.8)',
      color: '#90e0ef',
      fontFamily: 'Poppins, sans-serif',
      fontSize: '0.9rem',
      cursor: 'pointer'
    },
    analyzeButton: {
      marginTop: '2rem',
      padding: '1rem 3rem',
      fontSize: '1.1rem',
      fontFamily: 'Poppins, sans-serif',
      fontWeight: '600',
      background: 'linear-gradient(135deg, #00b4d8, #0096b8)',
      border: 'none',
      borderRadius: '50px',
      color: '#fff',
      cursor: 'pointer',
      boxShadow: '0 0 20px rgba(0, 180, 216, 0.4)',
      transition: 'all 0.3s ease',
      textTransform: 'uppercase',
      letterSpacing: '1px'
    },
    summarySection: {
      marginTop: '3rem'
    },
    summaryHeader: {
      fontFamily: 'Merriweather, serif',
      fontSize: '2rem',
      marginBottom: '2rem',
      color: '#00b4d8'
    },
    cardsGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))',
      gap: '2rem'
    },
    card: {
      background: 'rgba(6, 26, 44, 0.7)',
      padding: '1.5rem',
      borderRadius: '12px',
      border: '1px solid rgba(0, 180, 216, 0.3)',
      boxShadow: '0 4px 15px rgba(0, 0, 0, 0.3)',
      transition: 'all 0.3s ease',
      cursor: 'pointer'
    },
    cardTitle: {
      fontFamily: 'Merriweather, serif',
      fontSize: '1.3rem',
      color: '#00b4d8',
      marginBottom: '1rem'
    },
    cardMetric: {
      fontFamily: 'Poppins, sans-serif',
      fontSize: '2rem',
      fontWeight: 'bold',
      color: '#90e0ef',
      marginBottom: '0.5rem'
    },
    cardInsight: {
      fontFamily: 'Poppins, sans-serif',
      fontSize: '0.9rem',
      color: '#caf0f8',
      marginBottom: '1rem'
    },
    chartContainer: {
      marginTop: '1rem',
      height: '150px'
    }
  };

  const modelCards = [
    { key: 'pollution', title: 'Ocean Pollution', icon: '🏭' },
    { key: 'coral', title: 'Coral Health', icon: '🪸' },
    { key: 'forecast', title: 'Ocean Forecast', icon: '🌊' },
    { key: 'activity', title: 'Human Activity', icon: '🚢' },
    { key: 'anomalies', title: 'Anomaly Detection', icon: '⚠️' },
    { key: 'mehi', title: 'Marine Ecosystem Health', icon: '🐠' }
  ];

  return (
    <div style={styles.pageContainer}>
      <Navbar />
      <div style={styles.mainLayout}>
        <Sidebar />
        <div style={styles.contentArea}>
          <h1 style={styles.header}>Ocean Analysis Dashboard</h1>
          <p style={styles.subheader}>Select a location and enter ocean parameters to begin analysis</p>

          <div style={styles.inputSection}>
            <h3 style={{ fontFamily: 'Merriweather, serif', fontSize: '1.5rem', marginBottom: '1rem' }}>
              Select Location on Map
            </h3>
            <MapPicker onLocationSelect={handleLocationSelect} />

            <h3 style={{ fontFamily: 'Merriweather, serif', fontSize: '1.5rem', marginBottom: '1rem' }}>
              Ocean Parameters
            </h3>
            <div style={styles.inputGrid}>
              <div style={styles.inputGroup}>
                <label style={styles.label}>Latitude *</label>
                <input
                  type="text"
                  style={styles.input}
                  value={inputs.lat}
                  onChange={(e) => updateInput('lat', e.target.value)}
                  placeholder="Click map or enter latitude"
                />
              </div>
              <div style={styles.inputGroup}>
                <label style={styles.label}>Temperature (°C) *</label>
                <input
                  type="number"
                  style={styles.input}
                  value={inputs.temperature}
                  onChange={(e) => updateInput('temperature', e.target.value)}
                  placeholder="e.g., 25"
                />
              </div>
              <div style={styles.inputGroup}>
                <label style={styles.label}>pH Level *</label>
                <input
                  type="number"
                  step="0.1"
                  style={styles.input}
                  value={inputs.pH}
                  onChange={(e) => updateInput('pH', e.target.value)}
                  placeholder="e.g., 8.1"
                />
              </div>
              <div style={styles.inputGroup}>
                <label style={styles.label}>Water Depth (m) *</label>
                <input
                  type="number"
                  style={styles.input}
                  value={inputs.depth}
                  onChange={(e) => updateInput('depth', e.target.value)}
                  placeholder="e.g., 50"
                />
              </div>
              <div style={styles.inputGroup}>
                <label style={styles.label}>Salinity (PSU) *</label>
                <input
                  type="number"
                  style={styles.input}
                  value={inputs.salinity}
                  onChange={(e) => updateInput('salinity', e.target.value)}
                  placeholder="e.g., 35"
                />
              </div>
              <div style={styles.inputGroup}>
                <label style={styles.label}>Temperature (°C) *</label>
                <input
                  type="number"
                  style={styles.input}
                  value={inputs.temperature}
                  onChange={(e) => updateInput('temperature', e.target.value)}
                  placeholder="e.g., 25"
                />
              </div>
              <div style={styles.inputGroup}>
                <label style={styles.label}>pH Level *</label>
                <input
                  type="number"
                  step="0.1"
                  style={styles.input}
                  value={inputs.pH}
                  onChange={(e) => updateInput('pH', e.target.value)}
                  placeholder="e.g., 8.1"
                />
              </div>
              
            </div>

            <button
              style={styles.analyzeButton}
              onClick={handleAnalyze}
              onMouseEnter={(e) => {
                e.target.style.transform = 'translateY(-2px)';
                e.target.style.boxShadow = '0 0 30px rgba(0, 180, 216, 0.6)';
              }}
              onMouseLeave={(e) => {
                e.target.style.transform = 'translateY(0)';
                e.target.style.boxShadow = '0 0 20px rgba(0, 180, 216, 0.4)';
              }}
            >
              Analyze My Ocean
            </button>
          </div>

          {hasResults && (
            <div style={styles.summarySection}>
              <h2 style={styles.summaryHeader}>Analysis Summary</h2>
              <div style={styles.cardsGrid}>
                {modelCards.map(({ key, title, icon }) => {
                  const result = results[key];
                  if (!result) return null;

                  return (
                    <div
                      key={key}
                      style={styles.card}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.transform = 'translateY(-5px)';
                        e.currentTarget.style.boxShadow = '0 8px 25px rgba(0, 180, 216, 0.4)';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'translateY(0)';
                        e.currentTarget.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.3)';
                      }}
                    >
                      <h3 style={styles.cardTitle}>{icon} {title}</h3>
                      <div style={styles.cardMetric}>
                        {result.results?.score || result.results?.health_score || result.results?.risk_level || 'N/A'}
                      </div>
                      <p style={styles.cardInsight}>{result.results?.insight}</p>
                      {result.results?.chartData && (
                        <div style={styles.chartContainer}>
                          <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={result.results.chartData}>
                              <CartesianGrid strokeDasharray="3 3" stroke="rgba(0, 180, 216, 0.2)" />
                              <XAxis dataKey="day" stroke="#90e0ef" />
                              <YAxis stroke="#90e0ef" />
                              <Tooltip
                                contentStyle={{
                                  background: '#04121f',
                                  border: '1px solid #00b4d8',
                                  borderRadius: '8px'
                                }}
                              />
                              <Line type="monotone" dataKey="value" stroke="#00b4d8" strokeWidth={2} />
                            </LineChart>
                          </ResponsiveContainer>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default Dashboard;