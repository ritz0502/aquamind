import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import MetricCard from '../components/MetricCard';
import { CoralHealthChart, RiskForecastChart, MEHIChart } from '../components/Charts';

const Dashboard = () => {
  const navigate = useNavigate();
  const [latitude, setLatitude] = useState('');
  const [longitude, setLongitude] = useState('');
  const [image, setImage] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
      if (window.innerWidth >= 768) {
        setSidebarOpen(false);
      }
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const handleAnalyze = () => {
    console.log('Analyzing Ocean Zone:', {
      latitude,
      longitude,
      image: image ? image.name : 'No image selected'
    });
  };

  const alerts = [
    { icon: '🔴', text: 'Oil spill detected near Sector Gamma', time: '5m ago' },
    { icon: '🟠', text: 'Unusual vessel activity', time: '30m ago' },
    { icon: '🔵', text: 'Mild coral bleaching detected', time: '1h ago' }
  ];

  const styles = {
    container: {
      display: 'flex',
      minHeight: '100vh',
      backgroundColor: '#04121f',
      paddingTop: '80px',
      paddingBottom: '60px',
      fontFamily: 'Poppins, sans-serif',
      color: '#e3f6fc',
      position: 'relative'
    },
    overlay: {
      display: sidebarOpen && isMobile ? 'block' : 'none',
      position: 'fixed',
      top: '80px',
      left: 0,
      right: 0,
      bottom: '60px',
      backgroundColor: 'rgba(0, 0, 0, 0.6)',
      zIndex: 98
    },
    main: {
      flex: 1,
      padding: isMobile ? '20px' : '30px',
      marginLeft: isMobile ? 0 : '260px',
      width: isMobile ? '100%' : 'calc(100% - 260px)',
      maxWidth: '100%'
    },
    menuButton: {
      position: 'fixed',
      top: '90px',
      left: '15px',
      zIndex: 100,
      backgroundColor: '#00b4d8',
      border: 'none',
      borderRadius: '8px',
      padding: '10px 12px',
      cursor: 'pointer',
      color: '#fff',
      boxShadow: '0 2px 10px rgba(0, 180, 216, 0.3)',
      display: isMobile ? 'flex' : 'none',
      alignItems: 'center',
      justifyContent: 'center'
    },
    header: {
      backgroundColor: '#08213a',
      padding: isMobile ? '20px' : '25px',
      borderRadius: '14px',
      marginBottom: isMobile ? '20px' : '30px',
      display: 'flex',
      flexDirection: isMobile ? 'column' : 'row',
      gap: isMobile ? '15px' : '0',
      justifyContent: 'space-between',
      alignItems: isMobile ? 'stretch' : 'center',
      boxShadow: '0 4px 20px rgba(0, 0, 0, 0.3)'
    },
    mehiProgress: {
      flex: 1,
      maxWidth: isMobile ? '100%' : '300px'
    },
    mehiLabel: {
      fontSize: isMobile ? '13px' : '14px',
      marginBottom: '8px',
      color: '#90e0ef',
      fontWeight: '600'
    },
    progressBar: {
      width: '100%',
      height: isMobile ? '10px' : '12px',
      backgroundColor: '#061a2c',
      borderRadius: '20px',
      overflow: 'hidden'
    },
    progressFill: {
      height: '100%',
      background: 'linear-gradient(90deg, #00b4d8, #0077b6)',
      width: '78%',
      borderRadius: '20px',
      transition: 'width 0.5s ease'
    },
    progressText: {
      fontSize: isMobile ? '11px' : '12px',
      marginTop: '5px',
      color: '#90e0ef'
    },
    headerInfo: {
      display: 'flex',
      flexWrap: 'wrap',
      gap: isMobile ? '12px' : '30px',
      fontSize: isMobile ? '12px' : '14px',
      alignItems: 'center'
    },
    inputPanel: {
      backgroundColor: '#08213a',
      padding: isMobile ? '20px' : '25px',
      borderRadius: '14px',
      marginBottom: isMobile ? '20px' : '30px',
      boxShadow: '0 4px 20px rgba(0, 0, 0, 0.3)'
    },
    inputTitle: {
      marginBottom: isMobile ? '15px' : '20px',
      color: '#00b4d8',
      fontFamily: 'Merriweather, serif',
      fontSize: isMobile ? '18px' : '20px'
    },
    inputGrid: {
      display: 'grid',
      gridTemplateColumns: isMobile ? '1fr' : 'repeat(auto-fit, minmax(200px, 1fr))',
      gap: isMobile ? '15px' : '20px',
      marginBottom: isMobile ? '15px' : '20px'
    },
    input: {
      padding: '12px 16px',
      backgroundColor: '#061a2c',
      border: '1px solid rgba(0, 180, 216, 0.3)',
      borderRadius: '8px',
      color: '#e3f6fc',
      fontSize: '14px',
      outline: 'none',
      transition: 'border-color 0.3s',
      width: '100%'
    },
    button: {
      padding: isMobile ? '12px 24px' : '14px 32px',
      background: 'linear-gradient(90deg, #00b4d8, #0077b6)',
      border: 'none',
      borderRadius: '8px',
      color: '#fff',
      fontSize: isMobile ? '15px' : '16px',
      fontWeight: '600',
      cursor: 'pointer',
      transition: 'transform 0.2s',
      boxShadow: '0 4px 15px rgba(0, 180, 216, 0.3)',
      width: isMobile ? '100%' : 'auto'
    },
    grid: {
      display: 'grid',
      gridTemplateColumns: isMobile 
        ? '1fr' 
        : 'repeat(auto-fill, minmax(350px, 1fr))',
      gap: isMobile ? '20px' : '25px'
    },
    alertItem: {
      padding: '12px',
      backgroundColor: '#061a2c',
      borderRadius: '8px',
      marginBottom: '10px',
      display: 'flex',
      flexDirection: isMobile ? 'column' : 'row',
      gap: isMobile ? '8px' : '0',
      justifyContent: 'space-between',
      alignItems: isMobile ? 'flex-start' : 'center'
    },
    alertText: {
      display: 'flex',
      gap: '10px',
      alignItems: 'center',
      flex: 1
    },
    alertTime: {
      fontSize: '11px',
      color: '#90e0ef'
    }
  };

  return (
    <div style={styles.container}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Poppins:wght@300;400;600&display=swap');
        
        * {
          box-sizing: border-box;
        }
        
        .input:focus {
          border-color: #00b4d8;
        }
        
        .button:hover {
          transform: scale(1.05);
        }
        
        .button:active {
          transform: scale(0.98);
        }

        .menu-button:hover {
          background-color: #0096b8;
        }
      `}</style>

      {/* Mobile Menu Button */}
      <button 
        className="menu-button"
        style={styles.menuButton}
        onClick={() => setSidebarOpen(!sidebarOpen)}
      >
        {sidebarOpen ? '✕' : '☰'}
      </button>

      {/* Overlay */}
      <div 
        style={styles.overlay}
        onClick={() => setSidebarOpen(false)}
      />

      <Sidebar 
        sidebarOpen={sidebarOpen} 
        setSidebarOpen={setSidebarOpen}
        isMobile={isMobile}
      />

      <div style={styles.main}>
        {/* Header Bar */}
        <div style={styles.header}>
          <div style={styles.mehiProgress}>
            <div style={styles.mehiLabel}>MEHI Summary</div>
            <div style={styles.progressBar}>
              <div style={styles.progressFill}></div>
            </div>
            <div style={styles.progressText}>78% Healthy</div>
          </div>
          <div style={styles.headerInfo}>
            <div>📅 {new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</div>
            <div>📍 34.0522, -118.2437</div>
            <div style={{ fontSize: '20px', cursor: 'pointer' }}>🔔</div>
          </div>
        </div>

        {/* Input Panel */}
        <div style={styles.inputPanel}>
          <h3 style={styles.inputTitle}>Analyze Ocean Zone</h3>
          <div style={styles.inputGrid}>
            <input
              className="input"
              type="text"
              placeholder="Latitude (e.g., 34.0522)"
              value={latitude}
              onChange={(e) => setLatitude(e.target.value)}
              style={styles.input}
            />
            <input
              className="input"
              type="text"
              placeholder="Longitude (e.g., -118.2437)"
              value={longitude}
              onChange={(e) => setLongitude(e.target.value)}
              style={styles.input}
            />
            <input
              className="input"
              type="file"
              accept="image/*"
              onChange={(e) => setImage(e.target.files[0])}
              style={styles.input}
            />
          </div>
          <button className="button" style={styles.button} onClick={handleAnalyze}>
            Analyze Ocean Zone
          </button>
        </div>

        {/* Dashboard Grid */}
        <div style={styles.grid}>
          {/* Pollution Detection Card */}
          <MetricCard
            title="Pollution Detection"
            subtitle="AI-Powered Water Quality Analysis"
            footer="Powered by CNN + LLM"
            onViewMore={() => navigate('/pollution')}
          >
            <div style={{
              height: '180px',
              backgroundColor: '#061a2c',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              backgroundImage: 'linear-gradient(135deg, #061a2c 0%, #0a2f4a 100%)'
            }}>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '48px', marginBottom: '10px' }}>💧</div>
                <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#00b4d8' }}>72%</div>
                <div style={{ fontSize: '16px', color: '#90e0ef', marginTop: '5px' }}>Clean Water</div>
              </div>
            </div>
          </MetricCard>

          {/* Coral Health Card */}
          <MetricCard
            title="Coral Health"
            subtitle="Real-time Reef Monitoring"
            footer="Powered by EfficientNet + LLM"
            onViewMore={() => navigate('/coral')}
          >
            <CoralHealthChart />
          </MetricCard>

          {/* Risk Forecast Card */}
          <MetricCard
            title="Risk Forecast"
            subtitle="24-Hour Prediction Model"
            footer="Powered by Prophet"
            onViewMore={() => navigate('/forecast')}
          >
            <RiskForecastChart />
          </MetricCard>

          {/* Human Activity Card */}
          <MetricCard
            title="Human Activity"
            subtitle="Vessel Tracking & Impact Analysis"
            footer="Powered by AISstream + Regression"
            onViewMore={() => navigate('/activity')}
          >
            <div style={{
              height: '180px',
              backgroundColor: '#061a2c',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '48px', marginBottom: '10px' }}>🗺️</div>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#ffd60a' }}>156</div>
                <div style={{ fontSize: '14px', color: '#90e0ef', marginTop: '5px' }}>Active Vessels</div>
                <div style={{ fontSize: '14px', color: '#ff6b35', marginTop: '8px' }}>12 High Impact Zones</div>
              </div>
            </div>
          </MetricCard>

          {/* Alerts & Anomalies Card */}
          <MetricCard
            title="Alerts & Anomalies"
            subtitle="Real-time Threat Detection"
            footer="Powered by Anomaly Detection"
            onViewMore={() => navigate('/anomalies')}
          >
            <div style={{ maxHeight: '180px', overflowY: 'auto' }}>
              {alerts.map((alert, idx) => (
                <div key={idx} style={styles.alertItem}>
                  <div style={styles.alertText}>
                    <span style={{ fontSize: '18px' }}>{alert.icon}</span>
                    <span style={{ fontSize: '13px' }}>{alert.text}</span>
                  </div>
                  <span style={styles.alertTime}>{alert.time}</span>
                </div>
              ))}
            </div>
          </MetricCard>

          {/* MEHI Index Card */}
          <MetricCard
            title="MEHI Index"
            subtitle="Marine Ecosystem Health Score"
            footer="Powered by Aggregation + LLM"
            onViewMore={() => navigate('/mehi')}
          >
            <MEHIChart />
          </MetricCard>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;