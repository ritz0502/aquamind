import { useState, useEffect, useRef } from 'react';
import './Navbar.css';
import logo from '../assets/logo.png';

function Navbar() {
  const [isHovered, setIsHovered] = useState(false);
  // 1. New state to track scrolling
  const [isScrolled, setIsScrolled] = useState(false);
  const navbarRef = useRef(null);

  useEffect(() => {
    // Scroll handling logic
    const handleScroll = () => {
      // Set to true if the vertical scroll position is more than 50px
      setIsScrolled(window.scrollY > 50); 
    };

    // Hover handling logic (existing)
    const handleMouseEnter = () => setIsHovered(true);
    const handleMouseLeave = () => setIsHovered(false);

    // Attach listeners
    window.addEventListener('scroll', handleScroll);
    if (navbarRef.current) {
      navbarRef.current.addEventListener('mouseenter', handleMouseEnter);
      navbarRef.current.addEventListener('mouseleave', handleMouseLeave);
    }

    // Cleanup
    return () => {
      window.removeEventListener('scroll', handleScroll); // Remove scroll listener
      if (navbarRef.current) {
        navbarRef.current.removeEventListener('mouseenter', handleMouseEnter);
        navbarRef.current.removeEventListener('mouseleave', handleMouseLeave);
      }
    };
  }, []);

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) element.scrollIntoView({ behavior: 'smooth' });
  };

  const handleBrandClick = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <nav
      ref={navbarRef}
      // 2. Add the 'scrolled' class when isScrolled is true
      className={`navbar ${isHovered ? 'hovered' : ''} ${isScrolled ? 'scrolled' : ''}`}
    >
      <div className="navbar-container">
        <div className="navbar-left">
          <div className="navbar-logo" onClick={handleBrandClick}>
            <img src={logo} alt="AquaMind Logo" />
          </div>
          <div className="navbar-brand" onClick={handleBrandClick}>
            AquaMind
          </div>
        </div>

        {/* This is the element we will hide in CSS */}
        <div className="navbar-center">
          <a className="nav-link" onClick={() => scrollToSection('home')}>Home</a>
          <a className="nav-link" href="#dashboard">Dashboard</a>
          <a className="nav-link" href="#about">About</a>
          <a className="nav-link" href="#contact">Contact</a>
        </div>

        <div className="navbar-right"></div>
      </div>
    </nav>
  );
}

export default Navbar;