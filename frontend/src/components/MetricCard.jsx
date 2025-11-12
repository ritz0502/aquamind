import React from 'react';

const MetricCard = ({ title, subtitle, footer, children, onViewMore }) => {
  const styles = {
    card: {
      backgroundColor: '#08213a',
      padding: '20px',
      borderRadius: '14px',
      boxShadow: '0 4px 20px rgba(0, 0, 0, 0.3)',
      transition: 'all 0.3s',
      cursor: 'pointer',
      animation: 'fadeIn 0.5s ease-in',
      border: '1px solid rgba(0, 180, 216, 0.1)',
      height: '100%',
      display: 'flex',
      flexDirection: 'column'
    },
    cardTitle: {
      fontFamily: 'Merriweather, serif',
      fontSize: '18px',
      marginBottom: '6px',
      color: '#00b4d8',
      fontWeight: 'bold'
    },
    cardSubtitle: {
      fontSize: '12px',
      color: '#90e0ef',
      marginBottom: '15px'
    },
    content: {
      marginBottom: '15px',
      flex: 1
    },
    cardFooter: {
      marginTop: 'auto',
      fontSize: '11px',
      color: '#0077b6',
      display: 'flex',
      flexWrap: 'wrap',
      justifyContent: 'space-between',
      alignItems: 'center',
      paddingTop: '12px',
      borderTop: '1px solid rgba(0, 180, 216, 0.1)',
      gap: '8px'
    },
    viewMore: {
      color: '#00b4d8',
      fontSize: '12px',
      fontWeight: '600',
      cursor: 'pointer',
      transition: 'color 0.2s',
      whiteSpace: 'nowrap'
    }
  };

  return (
    <div className="metric-card" style={styles.card}>
      <style>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        .metric-card:hover {
          box-shadow: 0 0 25px rgba(0, 180, 216, 0.4) !important;
          transform: translateY(-5px);
        }
        
        .view-more:hover {
          color: #90e0ef !important;
          text-decoration: underline;
        }
      `}</style>
      
      <div style={styles.cardTitle}>{title}</div>
      <div style={styles.cardSubtitle}>{subtitle}</div>
      
      <div style={styles.content}>
        {children}
      </div>
      
      <div style={styles.cardFooter}>
        <span>{footer}</span>
        <span 
          className="view-more" 
          style={styles.viewMore}
          onClick={(e) => {
            e.stopPropagation();
            onViewMore && onViewMore();
          }}
        >
          View More →
        </span>
      </div>
    </div>
  );
};

export default MetricCard;