import React from 'react';

const Pollution = () => {
  const styles = {
    container: {
      padding: '100px 50px',
      backgroundColor: '#04121f',
      minHeight: '100vh',
      color: '#e3f6fc'
    },
    title: {
      fontFamily: 'Merriweather, serif',
      fontSize: '36px',
      color: '#00b4d8',
      marginBottom: '20px'
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