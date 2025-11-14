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
    } finally {
      setLoading(false);
    }
  };

  const styles = {
    pageContainer: {
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
  };

  return (
    <div style={styles.pageContainer}>
      <Navbar />
      <div style={styles.mainLayout}>
        <Sidebar />

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
            )}
          </div>

          {result && (
            <div style={styles.section}>
              <h3 style={styles.sectionTitle}>Analysis Results</h3>

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
            </div>
          )}

          <div style={styles.buttonGroup}>
            <button
              style={{ ...styles.button, ...styles.secondaryButton }}
              onClick={() => navigate("/pollution")}
            >
              ← Previous
            </button>

            <button
              style={styles.button}
              onClick={handleRunModel}
              disabled={loading}
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

export default Coral;
