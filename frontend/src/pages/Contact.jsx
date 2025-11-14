import React, { useState } from 'react';
import './Contact.css';
<<<<<<< HEAD
import contactbg from "../assets/contactbg.jpg";
import contactend from "../assets/contactend.jpg";

=======
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

import contactbg from "../assets/contactbg.jpg";
import contactend from "../assets/contactend.jpg";

import { Link } from "react-router-dom";

>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8

function Contact() {
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    subject: 'General',
    message: ''
  });

<<<<<<< HEAD
  const handleInputChange = (e) => {
    const { name, value } = e;
=======
  const handleInputChange = ({ name, value }) => {
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
<<<<<<< HEAD
    // Add your form submission logic here
    alert('Thank you for reaching out! We will get back to you soon.');
=======
    alert('Thank you for reaching out! We will get back to you soon.');

>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
    setFormData({
      fullName: '',
      email: '',
      subject: 'General',
      message: ''
    });
  };

  return (
<<<<<<< HEAD
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
                <label htmlFor="fullName" className="form-label">Full Name</label>
                <input
                  type="text"
                  id="fullName"
                  name="fullName"
                  className="form-input"
                  value={formData.fullName}
                  onChange={(e) => handleInputChange(e.target)}
                  required
                  placeholder="Enter your full name"
                />
              </div>

              <div className="form-group">
                <label htmlFor="email" className="form-label">Email Address</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  className="form-input"
                  value={formData.email}
                  onChange={(e) => handleInputChange(e.target)}
                  required
                  placeholder="your.email@example.com"
                />
              </div>

              <div className="form-group">
                <label htmlFor="subject" className="form-label">Subject</label>
                <select
                  id="subject"
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
                <label htmlFor="message" className="form-label">Message</label>
                <textarea
                  id="message"
                  name="message"
                  className="form-textarea"
                  value={formData.message}
                  onChange={(e) => handleInputChange(e.target)}
                  required
                  placeholder="Tell us how we can help..."
                  rows="6"
                ></textarea>
              </div>

              <button type="submit" className="form-button">
                Send Message
              </button>
            </form>
          </div>
        </div>
      </section>

      {/* Section 4 - Social Media */}
      <section className="social-section">
        <div className="container">
          <h2 className="social-title">Connect With Us</h2>
          <div className="social-icons">
            <a href="#linkedin" className="social-link" aria-label="LinkedIn">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
              </svg>
            </a>
            <a href="#github" className="social-link" aria-label="GitHub">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
              </svg>
            </a>
            <a href="#instagram" className="social-link" aria-label="Instagram">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0C8.74 0 8.333.015 7.053.072 5.775.132 4.905.333 4.14.63c-.789.306-1.459.717-2.126 1.384S.935 3.35.63 4.14C.333 4.905.131 5.775.072 7.053.012 8.333 0 8.74 0 12s.015 3.667.072 4.947c.06 1.277.261 2.148.558 2.913.306.788.717 1.459 1.384 2.126.667.666 1.336 1.079 2.126 1.384.766.296 1.636.499 2.913.558C8.333 23.988 8.74 24 12 24s3.667-.015 4.947-.072c1.277-.06 2.148-.262 2.913-.558.788-.306 1.459-.718 2.126-1.384.666-.667 1.079-1.335 1.384-2.126.296-.765.499-1.636.558-2.913.06-1.28.072-1.687.072-4.947s-.015-3.667-.072-4.947c-.06-1.277-.262-2.149-.558-2.913-.306-.789-.718-1.459-1.384-2.126C21.319 1.347 20.651.935 19.86.63c-.765-.297-1.636-.499-2.913-.558C15.667.012 15.26 0 12 0zm0 2.16c3.203 0 3.585.016 4.85.071 1.17.055 1.805.249 2.227.415.562.217.96.477 1.382.896.419.42.679.819.896 1.381.164.422.36 1.057.413 2.227.057 1.266.07 1.646.07 4.85s-.015 3.585-.074 4.85c-.061 1.17-.256 1.805-.421 2.227-.224.562-.479.96-.899 1.382-.419.419-.824.679-1.38.896-.42.164-1.065.36-2.235.413-1.274.057-1.649.07-4.859.07-3.211 0-3.586-.015-4.859-.074-1.171-.061-1.816-.256-2.236-.421-.569-.224-.96-.479-1.379-.899-.421-.419-.69-.824-.9-1.38-.165-.42-.359-1.065-.42-2.235-.045-1.26-.061-1.649-.061-4.844 0-3.196.016-3.586.061-4.861.061-1.17.255-1.814.42-2.234.21-.57.479-.96.9-1.381.419-.419.81-.689 1.379-.898.42-.166 1.051-.361 2.221-.421 1.275-.045 1.65-.06 4.859-.06l.045.03zm0 3.678c-3.405 0-6.162 2.76-6.162 6.162 0 3.405 2.76 6.162 6.162 6.162 3.405 0 6.162-2.76 6.162-6.162 0-3.405-2.76-6.162-6.162-6.162zM12 16c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4zm7.846-10.405c0 .795-.646 1.44-1.44 1.44-.795 0-1.44-.646-1.44-1.44 0-.794.646-1.439 1.44-1.439.793-.001 1.44.645 1.44 1.439z" />
              </svg>
            </a>
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
          <button className="cta-button">Explore Dashboard</button>
        </div>
      </section>
    </div>
  );
}

export default Contact;
=======
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
>>>>>>> 806c8e1921104feee35ce99ac3e5bd22697574c8
