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
  const [selectedLocation, setSelectedLocation] = useState(null);
  
  const resultsRef = useRef(null);

  // Simulate progress
  useEffect(() => {
    if (loading) {
      setProgress(0);
      const interval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 90) {
            clearInterval(interval);
            return 90;
          }
          return prev + 10;
        });
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResults(null);
    setPlotUrl(null);

    if (!formData.lat || !formData.lon) {
      setError('Please select coordinates from the map or enter them manually.');
      return;
    }

    const lat = parseFloat(formData.lat);
    const lon = parseFloat(formData.lon);

    if (isNaN(lat) || isNaN(lon)) {
      setError('Please enter valid numeric coordinates');
      return;
    }

    if (lat < -90 || lat > 90) {
      setError('Latitude must be between -90 and 90');
      return;
    }

    if (lon < -180 || lon > 180) {
      setError('Longitude must be between -180 and 180');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/run_pipeline`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          lat: lat,
          lon: lon,
          forecast_days: parseInt(formData.forecast_days),
          quick_mode: formData.quick_mode,
        }),
      });

      const data = await response.json();

      if (response.ok && data.status === 'success') {
        setProgress(100);
        setResults(data);
        const plotResponse = await fetch(`${API_BASE_URL}/get_plot?lat=${lat}&lon=${lon}`);
        if (plotResponse.ok) {
          const blob = await plotResponse.blob();
          setPlotUrl(URL.createObjectURL(blob));
        }
      } else {
        setError(data.message || 'Pipeline execution failed');
      }
    } catch (err) {
      setError(`Connection error: ${err.message}. Make sure Flask backend is running.`);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (riskLevel) => {
    const level = riskLevel?.toLowerCase() || '';
    if (level.includes('low')) return '#10b981';
    if (level.includes('medium') || level.includes('moderate')) return '#f59e0b';
    if (level.includes('high')) return '#ef4444';
    return '#6b7280';
  };

  const getRiskIcon = (riskLevel) => {
    const level = riskLevel?.toLowerCase() || '';
    if (level.includes('low')) return '✓';
    if (level.includes('medium') || level.includes('moderate')) return '⚠';
    if (level.includes('high')) return '⚠';
    return '?';
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
      <TextCursor
        text="🐟"
        delay={0.01}
        spacing={100}
        followMouseDirection={true}
        randomFloat={true}
        exitDuration={0.5}
        removalInterval={30}
        maxPoints={5}
      />

      {/* Header Section */}
      <section className="risk-hero-section with-bg">
        <div className="risk-hero-overlay"></div>
        <div className="risk-hero-content">
          <h1 className="risk-hero-title">Marine Risk Prediction</h1>
          <p className="risk-hero-subtitle">
            AI-powered forecasting to assess marine environmental risks and protect ocean ecosystems
          </p>
        </div>
      </section>

      {/* Main Section */}
      <section className="risk-main-section">
        <div className="risk-container">

          {/* Map Section */}
          <div className="risk-card map-card">
            <h2 className="card-title">🗺️ Select Location on Map</h2>
            <MapContainer
              center={[20, 0]}
              zoom={2}
              style={{ height: '400px', width: '100%', borderRadius: '12px' }}
            >
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution="© OpenStreetMap contributors"
              />
              <LocationSelector onLocationSelect={handleMapClick} />
              {selectedLocation && (
                <Marker position={selectedLocation} icon={customIcon}>
                  <Popup>
                    Selected Location<br />
                    Lat: {selectedLocation.lat.toFixed(4)}<br />
                    Lon: {selectedLocation.lng.toFixed(4)}
                  </Popup>
                </Marker>
              )}
            </MapContainer>
          </div>

          {/* Existing Input Form */}
          <div className="risk-card input-card">
            <h2 className="card-title">📍 Location & Settings</h2>
            <form onSubmit={handleSubmit} className="risk-form">
              {/* Latitude & Longitude Inputs */}
              <div className="form-grid">
                <div className="form-group">
                  <label htmlFor="lat">Latitude</label>
                  <input
                    type="number"
                    id="lat"
                    name="lat"
                    step="0.0001"
                    placeholder="e.g., -18.2871"
                    value={formData.lat}
                    onChange={handleInputChange}
                    disabled={loading}
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="lon">Longitude</label>
                  <input
                    type="number"
                    id="lon"
                    name="lon"
                    step="0.0001"
                    placeholder="e.g., 147.6992"
                    value={formData.lon}
                    onChange={handleInputChange}
                    disabled={loading}
                  />
                </div>
              </div>

              {/* Rest remains same */}
              <div className="form-group">
                <label htmlFor="forecast_days">
                  Forecast Period: {formData.forecast_days} days
                </label>
                <input
                  type="range"
                  id="forecast_days"
                  name="forecast_days"
                  min="7"
                  max="90"
                  step="1"
                  value={formData.forecast_days}
                  onChange={handleInputChange}
                  disabled={loading}
                  className="range-slider"
                />
                <div className="range-labels">
                  <span>7 days</span>
                  <span>90 days</span>
                </div>
              </div>

              <div className="form-group checkbox-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    name="quick_mode"
                    checked={formData.quick_mode}
                    onChange={handleInputChange}
                    disabled={loading}
                  />
                  <span>Quick Mode (faster processing)</span>
                </label>
              </div>

              <button type="submit" className="submit-button" disabled={loading}>
                {loading ? 'Running Analysis...' : '▶ Run Prediction'}
              </button>
            </form>

            {/* Presets */}
            <div className="preset-locations">
              <p className="preset-label">Quick presets:</p>
              <div className="preset-buttons">
                {presetLocations.map((preset, index) => (
                  <button
                    key={index}
                    onClick={() => loadPreset(preset)}
                    className="preset-button"
                    disabled={loading}
                  >
                    {preset.name}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Results/Error/Loading unchanged */}
          {error && (
            <div className="risk-card error-card">
              <div className="error-content">
                <span className="error-icon">⚠</span>
                <p className="error-message">{error}</p>
              </div>
            </div>
          )}

          {loading && (
            <div className="risk-card loading-card">
              <h2 className="card-title">⏱ Processing Pipeline</h2>
              {/* ... existing loading code unchanged ... */}
            </div>
          )}

          {results && (
            <div ref={resultsRef} className="results-section">
              {/* existing results section unchanged */}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

export default RiskPrediction;
