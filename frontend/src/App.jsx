import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

import { OceanInputProvider } from './context/OceanInputContext';
import { ModelResultsProvider } from './context/ModelResultsContext';

import AquaMind from "./pages/AquaMind";
import Dashboard from "./pages/Dashboard";
import Pollution from "./pages/Pollution";
import Coral from "./pages/Coral";
import Forecast from "./pages/Forecast";
import Activity from "./pages/Activity";
import Anomalies from "./pages/Anomalies";
import Mehi from "./pages/Mehi";
<<<<<<< HEAD
=======
import About from "./pages/About";
import Contact from "./pages/Contact";
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8

function App() {
  return (
    <OceanInputProvider>
      <ModelResultsProvider>

        <Router>
          <Routes>

            {/* ✅ Landing Page (ONLY page where App.jsx adds Navbar + Footer) */}
            <Route
              path="/"
              element={
                <>
                  <Navbar />
                  <AquaMind />
                  <Footer />
                </>
              }
            />

            {/* ❗ All other pages ALREADY include navbar/sidebar/footer themselves */}
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/pollution" element={<Pollution />} />
            <Route path="/coral" element={<Coral />} />
            <Route path="/forecast" element={<Forecast />} />
            <Route path="/activity" element={<Activity />} />
            <Route path="/anomalies" element={<Anomalies />} />
            <Route path="/mehi" element={<Mehi />} />
<<<<<<< HEAD

=======
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} />
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
          </Routes>
        </Router>

      </ModelResultsProvider>
    </OceanInputProvider>
  );
}

export default App;
