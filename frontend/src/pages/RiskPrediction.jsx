import { useState, useEffect, useRef } from 'react';
import './RiskPrediction.css';
import TextCursor from '../components/TextCursor';
import { MapContainer, TileLayer, useMapEvents, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

const API_BASE_URL = 'http://localhost:5000';

// Custom marker icon
const customIcon = new L.Icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.3/dist/images/marker-shadow.png',
});

function LocationSelector({ onLocationSelect }) {
  useMapEvents({
    click(e) {
      onLocationSelect(e.latlng);
    },
  });
  return null;
}

function RiskPrediction() {
  const [formData, setFormData] = useState({
    lat: '',
    lon: '',
    forecast_days: 30,
    quick_mode: true,
  });

  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [plotUrl, setPlotUrl] = useState(null);
  const [reportText, setReportText] = useState(null);
  const [selectedLocation, setSelectedLocation] = useState(null);

  const resultsRef = useRef(null);

  // Progress animation
  useEffect(() => {
    if (loading) {
      setProgress(0);
      const interval = setInterval(() => {
        setProgress((p) => (p >= 90 ? 90 : p + 10));
      }, 500);
      return () => clearInterval(interval);
    }
  }, [loading]);

  // Scroll to results
  useEffect(() => {
    if (results && resultsRef.current) {
      resultsRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }, [results]);

  // Handle inputs
  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleMapClick = (latlng) => {
    setFormData((prev) => ({
      ...prev,
      lat: latlng.lat.toFixed(4),
      lon: latlng.lng.toFixed(4),
    }));
    setSelectedLocation(latlng);
  };

  // Handle submit (main logic)
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResults(null);
    setPlotUrl(null);
    setReportText(null);

    const lat = parseFloat(formData.lat);
    const lon = parseFloat(formData.lon);

    if (!lat || !lon || isNaN(lat) || isNaN(lon)) {
      setError("Invalid coordinates");
      return;
    }

    setLoading(true);

    try {
      // Run pipeline
      const response = await fetch(`${API_BASE_URL}/risk/run_pipeline`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          lat,
          lon,
          forecast_days: parseInt(formData.forecast_days),
          quick_mode: formData.quick_mode,
        }),
      });

      const data = await response.json();

      if (response.ok && data.status === "success") {
        setProgress(100);
        setResults(data);

        // === Fetch Plot ===
        const plotRes = await fetch(`${API_BASE_URL}/risk/get_plot?lat=${lat}&lon=${lon}`);
        if (plotRes.ok) {
          const blob = await plotRes.blob();
          setPlotUrl(URL.createObjectURL(blob));
        }

        // === Fetch Report (NEW) ===
        const reportRes = await fetch(`${API_BASE_URL}/risk/get_report?lat=${lat}&lon=${lon}`);
        if (reportRes.ok) {
          const text = await reportRes.text();
          setReportText(text);
        }
      } else {
        setError(data.message || "Pipeline failed");
      }

    } catch (err) {
      setError(`Connection error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const presetLocations = [
    { name: 'Great Barrier Reef', lat: -18.2871, lon: 147.6992 },
    { name: 'Maldives', lat: 3.2028, lon: 73.2207 },
    { name: 'Caribbean Sea', lat: 14.5994, lon: -61.0242 },
    { name: 'Gulf of Mexico', lat: 25.0, lon: -90.0 },
  ];

  const loadPreset = (preset) => {
    setFormData({
      ...formData,
      lat: preset.lat.toString(),
      lon: preset.lon.toString(),
    });
    setSelectedLocation({ lat: preset.lat, lng: preset.lon });
  };

  return (
    <div className="risk-prediction-page">
      <TextCursor text="🐟" delay={0.01} spacing={100} followMouseDirection randomFloat exitDuration={0.5} removalInterval={30} maxPoints={5} />

      {/* Header */}
      <section className="risk-hero-section with-bg">
        <div className="risk-hero-overlay"></div>
        <div className="risk-hero-content">
          <h1 className="risk-hero-title">Marine Risk Prediction</h1>
          <p className="risk-hero-subtitle">AI-powered forecasting to assess marine environmental risks</p>
        </div>
      </section>

      {/* Main */}
      <section className="risk-main-section">
        <div className="risk-container">

          {/* Map */}
          <div className="risk-card map-card">
            <h2 className="card-title">🗺️ Select Location on Map</h2>
            <MapContainer center={[20, 0]} zoom={2} style={{ height: '400px', width: '100%', borderRadius: '12px' }}>
              <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
              <LocationSelector onLocationSelect={handleMapClick} />
              {selectedLocation && (
                <Marker position={selectedLocation} icon={customIcon}>
                  <Popup>
                    Selected Location <br />
                    Lat: {selectedLocation.lat.toFixed(4)} <br />
                    Lon: {selectedLocation.lng.toFixed(4)}
                  </Popup>
                </Marker>
              )}
            </MapContainer>
          </div>

          {/* Input */}
          <div className="risk-card input-card">
            <h2 className="card-title">📍 Location & Settings</h2>

            <form onSubmit={handleSubmit} className="risk-form">
              <div className="form-grid">
                <div className="form-group">
                  <label>Latitude</label>
                  <input type="number" name="lat" step="0.0001" value={formData.lat} onChange={handleInputChange} disabled={loading} />
                </div>
                <div className="form-group">
                  <label>Longitude</label>
                  <input type="number" name="lon" step="0.0001" value={formData.lon} onChange={handleInputChange} disabled={loading} />
                </div>
              </div>

              <div className="form-group">
                <label>Forecast Period: {formData.forecast_days} days</label>
                <input type="range" name="forecast_days" min="7" max="90" value={formData.forecast_days} onChange={handleInputChange} disabled={loading} />
              </div>

              <div className="form-group checkbox-group">
                <label>
                  <input type="checkbox" name="quick_mode" checked={formData.quick_mode} onChange={handleInputChange} disabled={loading} />
                  Quick Mode
                </label>
              </div>

              <button type="submit" className="submit-button" disabled={loading}>
                {loading ? "Running..." : "▶ Run Prediction"}
              </button>
            </form>

            {/* Presets */}
            <div className="preset-locations">
              <p className="preset-label">Quick presets:</p>
              <div className="preset-buttons">
                {presetLocations.map((preset, i) => (
                  <button key={i} onClick={() => loadPreset(preset)} disabled={loading}>
                    {preset.name}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Error */}
          {error && (
            <div className="risk-card error-card">
              <p className="error-message">⚠ {error}</p>
            </div>
          )}

          {/* Results */}
          {results && (
            <div ref={resultsRef} className="results-section">

              {/* Plot */}
              {plotUrl && (
                <div className="risk-card plot-card">
                  <h2 className="card-title">📊 Marine Risk Plot</h2>
                  <img src={plotUrl} className="risk-plot-image" />
                </div>
              )}

              {/* Report */}
              {reportText && (
                <div className="risk-card report-card">
                  <h2 className="card-title">📝 Marine Risk Report</h2>
                  <pre className="report-text">{reportText}</pre>
                </div>
              )}

            </div>
          )}

        </div>
      </section>
    </div>
  );
}

export default RiskPrediction;
