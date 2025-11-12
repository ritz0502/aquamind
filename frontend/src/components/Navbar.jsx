import { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Navbar.css';
import logo from '../assets/logo.png';

function Navbar() {
  const [isHovered, setIsHovered] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const navbarRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 50);
    const handleMouseEnter = () => setIsHovered(true);
    const handleMouseLeave = () => setIsHovered(false);

    window.addEventListener('scroll', handleScroll);
    if (navbarRef.current) {
      navbarRef.current.addEventListener('mouseenter', handleMouseEnter);
      navbarRef.current.addEventListener('mouseleave', handleMouseLeave);
    }

    return () => {
      window.removeEventListener('scroll', handleScroll);
      if (navbarRef.current) {
        navbarRef.current.removeEventListener('mouseenter', handleMouseEnter);
        navbarRef.current.removeEventListener('mouseleave', handleMouseLeave);
      }
    };
  }, []);

  const handleBrandClick = () => {
    navigate('/'); // Navigate to home
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <nav
      ref={navbarRef}
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

        <div className="navbar-center">
          <Link className="nav-link" to="/">Home</Link>
          <Link className="nav-link" to="/dashboard">Dashboard</Link>
          <Link className="nav-link" to="/about">About</Link>
          <Link className="nav-link" to="/contact">Contact</Link>
        </div>

        <div className="navbar-right"></div>
      </div>
    </nav>
  );
}

export default Navbar;
