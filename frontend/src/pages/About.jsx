import React from 'react';
import './About.css';
import aboutbg from '../assets/aboutbg.jpg';
import reetika from '../assets/reetika.jpg';
import arushi from '../assets/arushi.jpg';
import prachi from '../assets/prachi.jpg';
import kriya from '../assets/kriya.jpg';
import { Link } from "react-router-dom";
import aboutend from '../assets/aboutend.jpg';
import kshitij from '../assets/kshitij.jpg';


function About() {
  return (
    <div className="about-page">
      {/* Section 1 - Header */}
      <section className="about-header" style={{ backgroundImage: `url(${aboutbg})` }}>
        <div className="container">
          <h1 className="main-heading">About Us</h1>
          <div className="info-cards">
            <div className="info-card">
              <div className="card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 2L2 7l10 5 10-5-10-5z" />
                  <path d="M2 17l10 5 10-5M2 12l10 5 10-5" />
                </svg>
              </div>
              <h3 className="card-heading">Our Mission</h3>
              <p className="card-text">
                To harness cutting-edge AI technology and data analytics to monitor,
                protect, and restore ocean health, empowering scientists and
                conservationists with actionable insights for a sustainable marine future.
              </p>
            </div>
            <div className="info-card">
              <div className="card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10" />
                  <path d="M12 6v6l4 2" />
                </svg>
              </div>
              <h3 className="card-heading">Our Vision</h3>
              <p className="card-text">
                A world where technology and nature work in harmony, where real-time
                data transforms ocean conservation efforts, and where every coastal
                community has the tools to protect their marine ecosystems for generations.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Section 2 - Challenges + AI Solution */}
      <section className="challenges-solution">
        <div className="container">
          <div className="two-column-layout">
            <div className="challenges-column">
              <h2 className="section-heading">The Challenges Our Oceans Face</h2>
              <ul className="challenges-list">
                <li className="challenge-item">
                  <span className="bullet-icon">⚠</span>
                  <span>Coral bleaching and reef degradation</span>
                </li>
                <li className="challenge-item">
                  <span className="bullet-icon">⚠</span>
                  <span>Marine pollution and plastic accumulation</span>
                </li>
                <li className="challenge-item">
                  <span className="bullet-icon">⚠</span>
                  <span>Rising ocean temperatures</span>
                </li>
                <li className="challenge-item">
                  <span className="bullet-icon">⚠</span>
                  <span>Biodiversity loss and species extinction</span>
                </li>
                <li className="challenge-item">
                  <span className="bullet-icon">⚠</span>
                  <span>Coastal waste accumulation</span>
                </li>
                <li className="challenge-item">
                  <span className="bullet-icon">⚠</span>
                  <span>Harmful algal blooms</span>
                </li>
              </ul>
            </div>
            <div className="solution-column">
              <h2 className="section-heading">AquaMind's AI-Powered Solution</h2>
              <p className="solution-description">
                We combine satellite imagery, machine learning models,
                and real-time analytics to deliver comprehensive ocean monitoring.
                Our platform provides early warnings, predictive insights, and
                actionable data to help protect marine ecosystems.
              </p>
              <div className="solution-cards">
                <div className="solution-card">
                  <div className="solution-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <circle cx="12" cy="12" r="10" />
                      <path d="M12 8v8m-4-4h8" />
                    </svg>
                  </div>
                  <h4 className="solution-title">Pollution Detection</h4>
                  <p className="solution-text">
                    AI-powered image analysis identifies plastic debris, oil spills,
                    and contaminants in real-time.
                  </p>
                </div>
                <div className="solution-card">
                  <div className="solution-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z" />
                      <path d="M12 6v6l4 2" />
                    </svg>
                  </div>
                  <h4 className="solution-title">Coral Health Monitoring</h4>
                  <p className="solution-text">
                    Track coral bleaching events and reef vitality using
                    multispectral imaging and ML models.
                  </p>
                </div>
                <div className="solution-card">
                  <div className="solution-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M3 3v18h18" />
                      <path d="M18 17l-5-5-4 4-4-4" />
                    </svg>
                  </div>
                  <h4 className="solution-title">Ocean Forecasting</h4>
                  <p className="solution-text">
                    Predict temperature changes, current patterns, and extreme
                    weather impacts on marine life.
                  </p>
                </div>
                <div className="solution-card">
                  <div className="solution-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <rect x="3" y="3" width="18" height="18" rx="2" />
                      <path d="M9 9h6v6H9z" />
                    </svg>
                  </div>
                  <h4 className="solution-title">Marine Activity Insights</h4>
                  <p className="solution-text">
                    Monitor fishing activity, vessel traffic, and protected area
                    compliance using satellite data.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Section 3 - Team */}
      <section className="team-section">
        <div className="container">
          <h2 className="section-heading">Meet Our Dedicated Team</h2>
          <p className="team-subtitle">
            A passionate group of technologists, engineers, and ocean lovers working to safeguard our planet's waters.
          </p>
          <div className="team-grid">
            <div className="team-card">
              <div className="team-image"
                style={reetika ? { backgroundImage: `url(${reetika})` } : {}}>
                {!reetika && <div className="image-placeholder">R</div>}
              </div>
              <h3 className="team-name">Reetika Gupta</h3>
              <p className="team-role">Full-Stack Developer</p>
            </div>
            <div className="team-card">
              <div className="team-image"
                style={arushi ? { backgroundImage: `url(${arushi})` } : {}}>
                {!arushi && <div className="image-placeholder">A</div>}
              </div>
              <h3 className="team-name">Arushi Jain</h3>
              <p className="team-role">Full-Stack Developer</p>
            </div>
            <div className="team-card">
              <div className="team-image"
                style={kriya ? { backgroundImage: `url(${kriya})` } : {}}>
                {!kriya && <div className="image-placeholder">K</div>}
              </div>
              <h3 className="team-name">Kriya Mehta</h3>
              <p className="team-role">AI/ML Engineer</p>
            </div>
            <div className="team-card">
              <div className="team-image"
                style={prachi ? { backgroundImage: `url(${prachi})` } : {}}>
                {!prachi && <div className="image-placeholder">P</div>}
              </div>
              <h3 className="team-name">Prachi Barhate</h3>
              <p className="team-role">Full-Stack Developer</p>
            </div>
            <div className="team-card">
              <div className="team-image"
                style={kshitij ? { backgroundImage: `url(${kshitij})` } : {}}>
                {!kshitij && <div className="image-placeholder">K</div>}
              </div>
              <h3 className="team-name">Kshitij Aggarwal</h3>
              <p className="team-role">AI/ML Engineer</p>
            </div>
          </div>
        </div>
      </section>

      {/* Section 4 - Tech Stack */}
      <section className="tech-stack">
        <div className="container">
          <h2 className="section-heading">Our Powerful Tech Stack</h2>
          <p className="tech-subtitle">
            Built with cutting-edge technologies for real-time ocean intelligence and scalable data processing.
          </p>
          <div className="tech-icons">
            <div className="tech-item">
              <div className="tech-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="3" />
                  <path d="M12 1v6m0 6v6M5.64 5.64l4.24 4.24m4.24 4.24l4.24 4.24M1 12h6m6 0h6M5.64 18.36l4.24-4.24m4.24-4.24l4.24-4.24" />
                </svg>
              </div>
              <p className="tech-label">Machine Learning</p>
            </div>
            <div className="tech-item">
              <div className="tech-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z" />
                  <polyline points="7.5 4.21 12 6.81 16.5 4.21" />
                  <polyline points="7.5 19.79 7.5 14.6 3 12" />
                  <polyline points="21 12 16.5 14.6 16.5 19.79" />
                  <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
                  <line x1="12" y1="22.08" x2="12" y2="12" />
                </svg>
              </div>
              <p className="tech-label">Deep Learning</p>
            </div>
            <div className="tech-item">
              <div className="tech-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10" />
                  <path d="M2 12h20M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z" />
                </svg>
              </div>
              <p className="tech-label">Geospatial Data</p>
            </div>
            <div className="tech-item">
              <div className="tech-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M3 3v18h18" />
                  <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3" />
                </svg>
              </div>
              <p className="tech-label">Ocean Modeling</p>
            </div>
            <div className="tech-item">
              <div className="tech-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="2" y="3" width="20" height="14" rx="2" />
                  <line x1="8" y1="21" x2="16" y2="21" />
                  <line x1="12" y1="17" x2="12" y2="21" />
                </svg>
              </div>
              <p className="tech-label">LLM + Analytics</p>
            </div>
          </div>
        </div>
      </section>

      {/* Section 5 - CTA */}
      <section className="cta-section" style={{ backgroundImage: `url(${aboutend})` }}>
        <div className="container">
          <h2 className="cta-heading">
            Join us in protecting marine life with data and intelligence
          </h2>
          <Link to="/dashboard" className="cta-button">
            Explore Dashboard
          </Link>

        </div>
      </section>
    </div>
  );
}

export default About;