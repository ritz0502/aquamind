import LiquidChrome from './LiquidChrome';
import './AquaMind.css';
import { useEffect, useRef } from 'react';

import feature1 from '../assets/feature1.jpg';
import feature2 from '../assets/feature2.jpg';
import feature3 from '../assets/feature3.jpg';
import feature4 from '../assets/feature4.jpg';


function AquaMind() {
  const scrollToFeatures = () => {
    document.getElementById('features').scrollIntoView({ behavior: 'smooth' });
  };

  //new
  const featuresRef = useRef(null);

  useEffect(() => {
    const handleScroll = () => {
      const scrollY = window.scrollY;
      if (featuresRef.current) {
        // Move background slower than scroll for parallax effect
        featuresRef.current.style.backgroundPositionY = `${scrollY * 0.3}px`;
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const features = [
    {
      // icon: '🧪',
      number: '1',
      name: 'Pollution Detection',
      subtitle: 'Tracking the unseen threats',
      description:
        "AquaMind's AI scans real-time satellite and sonar data to detect chemical spills, microplastic zones, and waste accumulation. It identifies pollution sources early, empowering swift action to protect marine life and coastal communities.",
      image: feature1,
    },
    {
      // icon: '🪸',
      number: '2',
      name: 'Coral Health Monitoring',
      subtitle: 'Guardians of the reef',
      description:
        'Using deep learning models and spectral imaging, AquaMind continuously monitors coral color, temperature shifts, and bleaching patterns. Our algorithms help researchers predict coral stress and plan timely restoration efforts to revive dying reefs.',
      image: feature2,
    },
    {
      // icon: '🌦️',
      number: '3',
      name: 'Ocean Forecasting',
      subtitle: 'Predicting the tides of change',
      description:
        "AquaMind's predictive analytics interpret climate, salinity, and current flow data to forecast marine trends. From storm surges to migration shifts, our insights help shape sustainable navigation, fishing, and conservation strategies.",
      image: feature3,
    },
    {
      // icon: '🐋',
      number: '4',
      name: 'Marine Activity Insights',
      subtitle: 'Decoding life beneath',
      description:
        'By analyzing sonar and movement data, AquaMind maps marine species activity and behavioral shifts. This helps track endangered species, assess ecosystem balance, and deepen our understanding of ocean biodiversity.',
      image: feature4,
    },
  ];

  return (
    <div className="aquamind-landing">
      <section className="hero-section">
        <div className="hero-background">
          <LiquidChrome
            baseColor={[0.1, 0.5, 0.7]}
            speed={0.4}
            amplitude={0.3}
            interactive={true}
          />
        </div>
        <div className="hero-overlay"></div>
        <div className="hero-content">
          <h1 className="hero-title">Reviving Oceans with Intelligence</h1>
          <p className="hero-subtitle">
            AquaMind uses AI-driven insights to detect pollution, forecast marine trends, and protect coral ecosystems — empowering us to heal our oceans one byte at a time.
          </p>
          <button className="cta-button" onClick={scrollToFeatures}>
            Explore the Deep
          </button>
        </div>
      </section>

      <section id="features" ref={featuresRef} className="features-section">
        <div className="features-overlay"></div>
        <div className="features-content">
          <div className="features-header">
            <h2 className="features-title">The Four Pillars of AquaMind</h2>
          </div>

          {features.map((feature, index) => (
            <div
              key={index}
              className={`feature-item ${index % 2 !== 0 ? 'reverse' : ''}`}
            >
              <div className="feature-text">
                <div className="feature-icon">{feature.icon}</div>
                <h3 className="feature-number">{feature.number}. {feature.name}</h3>
                <p className="feature-subtitle">{feature.subtitle}</p>
                <p className="feature-description">{feature.description}</p>
              </div>
              <div className="feature-image-container">
                <div
                  className="blob"
                  style={{ backgroundImage: `url(${feature.image})` }}
                ></div>
              </div>
            </div>
          ))}

          <div className="final-cta">
            <button className="cta-button-secondary">Try Dashboard</button>
          </div>
        </div>
      </section>
    </div>
  );
}

export default AquaMind;
