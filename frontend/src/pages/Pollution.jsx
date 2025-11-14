import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import Footer from '../components/Footer';
import { useOceanInput } from '../context/OceanInputContext';
import { useModelResults } from '../context/ModelResultsContext';
import { runModel } from '../api/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Pollution = () => {
  const navigate = useNavigate();
  const { inputs } = useOceanInput();
  const { updateResult } = useModelResults();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleRunModel = async () => {
    setLoading(true);
    try {
      const response = await runModel('pollution', inputs);
      setResult(response);
      updateResult('pollution', response);
    } catch (error) {
      alert('Error running pollution model. Please try again.');
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
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>🌊 Pollution Detection</h2>
      <p>Coming Soon...</p>
    </div>
  );
};

export default Pollution;