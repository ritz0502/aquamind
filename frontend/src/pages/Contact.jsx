import React, { useState } from 'react';
import './Contact.css';
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

import contactbg from "../assets/contactbg.jpg";
import contactend from "../assets/contactend.jpg";

import { Link } from "react-router-dom";


function Contact() {
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    subject: 'General',
    message: ''
  });

  const handleInputChange = ({ name, value }) => {
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
    alert('Thank you for reaching out! We will get back to you soon.');

    setFormData({
      fullName: '',
      email: '',
      subject: 'General',
      message: ''
    });
  };

  return (
    <>
      <Navbar />

      <div className="contact-page">

        {/* Section 1 - Header */}
        <section
          className="contact-header"
          style={{ backgroundImage: `url(${contactbg})` }}
        >
          <div className="container">
            <h1 className="header-title">Get in Touch</h1>
            <p className="header-subtitle">
              We're here to answer questions, collaborate, and support ocean conservation.
            </p>
          </div>
        </section>

        {/* Section 2 - Contact Methods */}
        <section className="contact-methods">
          <div className="container">
            <div className="methods-grid">

              <div className="method-card">
                <div className="method-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                    <polyline points="22,6 12,13 2,6" />
                  </svg>
                </div>
                <h3 className="method-heading">Email</h3>
                <p className="method-text">contact@aquamind.ai</p>
              </div>

              <div className="method-card">
                <div className="method-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
                    <circle cx="12" cy="10" r="3" />
                  </svg>
                </div>
                <h3 className="method-heading">Location</h3>
                <p className="method-text">Mumbai, India</p>
              </div>

              <div className="method-card">
                <div className="method-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M3 11l18-5v12L3 14v-3z" />
                    <path d="M11.6 16.8a3 3 0 1 1-5.8-1.6" />
                  </svg>
                </div>
                <h3 className="method-heading">Reach Us</h3>
                <p className="method-text">Available for collaborations and research partnerships</p>
              </div>

            </div>
          </div>
        </section>

        {/* Section 3 - Contact Form */}
        <section className="contact-form-section">
          <div className="container">
            <div className="form-wrapper">
              <h2 className="form-title">Send Us a Message</h2>
              <p className="form-description">
                Fill out the form below and we'll respond as soon as possible.
              </p>

              <form className="contact-form" onSubmit={handleSubmit}>

                <div className="form-group">
                  <label className="form-label">Full Name</label>
                  <input
                    type="text"
                    name="fullName"
                    className="form-input"
                    value={formData.fullName}
                    onChange={(e) => handleInputChange(e.target)}
                    required
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Email</label>
                  <input
                    type="email"
                    name="email"
                    className="form-input"
                    value={formData.email}
                    onChange={(e) => handleInputChange(e.target)}
                    required
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Subject</label>
                  <select
                    name="subject"
                    className="form-select"
                    value={formData.subject}
                    onChange={(e) => handleInputChange(e.target)}
                    required
                  >
                    <option value="General">General Inquiry</option>
                    <option value="Dashboard Access">Dashboard Access</option>
                    <option value="Bug Report">Bug Report</option>
                    <option value="Partnership">Partnership Opportunity</option>
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Message</label>
                  <textarea
                    name="message"
                    className="form-textarea"
                    value={formData.message}
                    onChange={(e) => handleInputChange(e.target)}
                    required
                    rows="6"
                  />
                </div>

                <button type="submit" className="form-button">Send Message</button>
              </form>
            </div>
          </div>
        </section>

        {/* Section 4 - Social Media */}
        <section className="social-section">
          <div className="container">
            <h2 className="social-title">Connect With Us</h2>

            <div className="social-icons">
              {/* your SVG icons here (same as before) */}
            </div>
          </div>
        </section>

        {/* Section 5 - Final CTA */}
        <section
          className="final-cta"
          style={{ backgroundImage: `url(${contactend})` }}
        >
          <div className="container">
            <h2 className="cta-text">
              Together, we can restore the oceans — one insight at a time.
            </h2>
            <Link to="/dashboard">
              <button className="cta-button">Explore Dashboard</button>
            </Link>
          </div>
        </section>

      </div>

      <Footer />
    </>
  );
}

export default Contact;
