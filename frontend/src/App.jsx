import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import AquaMind from './pages/AquaMind';
import Dashboard from './pages/Dashboard';
import Pollution from './pages/Pollution';
import Coral from './pages/Pollution';
import Forecast from './pages/RiskPrediction';
import Activity from './pages/Pollution';
import Anomalies from './pages/Pollution';
import MEHI from './pages/Pollution';
import Hub from './pages/Pollution';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<AquaMind />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/pollution" element={<Pollution />} />
        <Route path="/coral" element={<Coral />} />
        <Route path="/forecast" element={<Forecast />} />
        <Route path="/activity" element={<Activity />} />
        <Route path="/anomalies" element={<Anomalies />} />
        <Route path="/mehi" element={<MEHI />} />
        <Route path="/hub" element={<Hub />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;