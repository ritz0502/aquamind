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

// ⭐ Add these imports
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

function About() {
  return (
    <>
      {/* ⭐ Navbar added */}
      <Navbar />

      <div className="about-page">
        {/* Section 1 - Header */}
        <section 
          className="about-header" 
          style={{ backgroundImage: `url(${aboutbg})` }}
        >
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
                  <li className="challenge-item"><span className="bullet-icon">⚠</span>Coral bleaching and reef degradation</li>
                  <li className="challenge-item"><span className="bullet-icon">⚠</span>Marine pollution and plastic accumulation</li>
                  <li className="challenge-item"><span className="bullet-icon">⚠</span>Rising ocean temperatures</li>
                  <li className="challenge-item"><span className="bullet-icon">⚠</span>Biodiversity loss and species extinction</li>
                  <li className="challenge-item"><span className="bullet-icon">⚠</span>Coastal waste accumulation</li>
                  <li className="challenge-item"><span className="bullet-icon">⚠</span>Harmful algal blooms</li>
                </ul>
              </div>

              <div className="solution-column">
                <h2 className="section-heading">AquaMind's AI-Powered Solution</h2>
                <p className="solution-description">
                  We combine satellite imagery, machine learning models,
                  and real-time analytics to deliver comprehensive ocean monitoring.
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
              A passionate group of technologists, engineers, and ocean lovers.
            </p>

            <div className="team-grid">
              <div className="team-card">
                <div className="team-image" style={{ backgroundImage: `url(${reetika})` }} />
                <h3 className="team-name">Reetika Gupta</h3>
                <p className="team-role">Full-Stack Developer</p>
              </div>

              <div className="team-card">
                <div className="team-image" style={{ backgroundImage: `url(${arushi})` }} />
                <h3 className="team-name">Arushi Jain</h3>
                <p className="team-role">Full-Stack Developer</p>
              </div>

              <div className="team-card">
                <div className="team-image" style={{ backgroundImage: `url(${kriya})` }} />
                <h3 className="team-name">Kriya Mehta</h3>
                <p className="team-role">AI/ML Engineer</p>
              </div>

              <div className="team-card">
                <div className="team-image" style={{ backgroundImage: `url(${prachi})` }} />
                <h3 className="team-name">Prachi Barhate</h3>
                <p className="team-role">Full-Stack Developer</p>
              </div>

              <div className="team-card">
                <div className="team-image" style={{ backgroundImage: `url(${kshitij})` }} />
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
              Built with cutting-edge technologies for ocean intelligence.
            </p>

            <div className="tech-icons">
              {/* your icons code same */}
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

      {/* ⭐ Footer added */}
      <Footer />
    </>
  );
}

export default About;
