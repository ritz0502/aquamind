import './Footer.css';
import logo from '../assets/logo.png';

function Footer() {
  return (
    <footer className="am-footer">
      <div className="am-footer-container">

        <div className="am-footer-section am-footer-brand">
          <div className="am-footer-brand-content">
            <img src={logo} alt="AquaMind Logo" className="am-footer-logo" />
            <h3 className="am-footer-brand-name">AquaMind</h3>
          </div>
          <p className="am-footer-brand-tagline">Reviving Oceans with Intelligence</p>
        </div>

        <div className="am-footer-section am-footer-links">
          <h4 className="am-footer-title">Quick Links</h4>
          <ul className="am-footer-links-list">
            <li><a href="/">Home</a></li>
            <li><a href="/dashboard">Dashboard</a></li>
            <li><a href="/about">About</a></li>
            <li><a href="/contact">Contact</a></li>
          </ul>
        </div>

        <div className="am-footer-section am-footer-contact">
          <h4 className="am-footer-title">Contact Info</h4>
          <div className="am-footer-contact-info">
            <p>Email: <a href="mailto:contact@aquamind.ai">contact@aquamind.ai</a></p>
            <p>Location: Mumbai, India</p>
          </div>
        </div>

        <div className="am-footer-section am-footer-social">
          <h4 className="am-footer-title">Connect With Us</h4>
          <div className="am-footer-social-links">
            <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer">
              <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
                <rect x="2" y="9" width="4" height="12"></rect>
                <circle cx="4" cy="4" r="2"></circle>
              </svg>
            </a>

            <a href="https://instagram.com" target="_blank" rel="noopener noreferrer">
              <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
              </svg>
            </a>

            <a href="https://github.com" target="_blank" rel="noopener noreferrer">
              <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path>
              </svg>
            </a>
          </div>
        </div>

      </div>

      <div className="am-footer-bottom">
        <p className="am-footer-copy">© 2025 AquaMind. All rights reserved.</p>
      </div>
    </footer>
  );
}

export default Footer;
