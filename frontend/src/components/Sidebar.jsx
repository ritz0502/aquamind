import React, { useEffect, useRef, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";

const Sidebar = ({ sidebarOpen, setSidebarOpen, isMobile }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const sidebarRef = useRef(null);
  const [isStuck, setIsStuck] = useState(false);

  const navItems = [
    { icon: "💧", label: "Pollution Detection", path: "/pollution" },
    { icon: "🪸", label: "Coral Health", path: "/coral" },
    { icon: "📈", label: "Risk Forecast", path: "/forecast" },
    { icon: "🚢", label: "Human Activity", path: "/activity" },
    { icon: "⚠️", label: "Anomalies", path: "/anomalies" },
    { icon: "🧠", label: "MEHI Index", path: "/mehi" },
  ];

  const handleNavigation = (path) => {
    navigate(path);
    if (isMobile) setSidebarOpen(false);
  };

  useEffect(() => {
    const footer = document.querySelector("footer");
    if (!footer || !sidebarRef.current) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsStuck(true);
        } else {
          setIsStuck(false);
        }
      },
      {
        root: null,
        threshold: 0,
      }
    );

    observer.observe(footer);

    return () => observer.disconnect();
  }, []);

  const styles = {
      sidebar: {
        width: '260px',
        backgroundColor: '#061a2c',
        padding: '30px 20px',
        paddingBottom: '20px',
        paddingTop: '0px',
        borderRight: '1px solid rgba(0, 180, 216, 0.2)',
        
        position: 'sticky',
        top: '60px',
        height: 'calc(100vh - 80px)',    // navbar height
        
        overflowY: 'auto',
        overflowX: 'hidden',

        zIndex: 10
      },
    navContainer: {
      flexGrow: 1,
      overflowY: "auto",
      padding: "30px 20px",
    },
    sidebarItem: {
      padding: "14px 18px",
      marginBottom: "10px",
      borderRadius: "10px",
      cursor: "pointer",
      transition: "all 0.3s",
      display: "flex",
      alignItems: "center",
      gap: "12px",
      backgroundColor: "rgba(0, 180, 216, 0.05)",
      fontSize: "14px",
      color: "#e3f6fc",
    },
    sidebarItemActive: {
      backgroundColor: "rgba(0, 180, 216, 0.2)",
      borderLeft: "4px solid #00b4d8",
      fontWeight: "600",
    },
    icon: { fontSize: "20px" },
    footer: {
      borderTop: "1px solid rgba(0,180,216,0.2)",
      textAlign: "center",
      padding: "12px 0",
      color: "#88aacc",
      fontSize: "13px",
      backgroundColor: "#061a2c",
    },
  };

  return (
    <aside ref={sidebarRef} style={styles.sidebar}>
      <style>{`
        .sidebar-item:hover {
          background-color: rgba(0, 180, 216, 0.15) !important;
          transform: translateX(5px);
        }
        ::-webkit-scrollbar {
          width: 8px;
        }
        ::-webkit-scrollbar-track {
          background: #04121f;
        }
        ::-webkit-scrollbar-thumb {
          background: #00b4d8;
          border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
          background: #0096b8;
        }
      `}</style>

      {/* Scrollable navigation */}
      <div style={styles.navContainer}>


        {navItems.map((item, idx) => {
          const isActive = location.pathname === item.path;
          return (
            <div
              key={idx}
              className="sidebar-item"
              style={{
                ...styles.sidebarItem,
                ...(isActive ? styles.sidebarItemActive : {}),
              }}
              onClick={() => handleNavigation(item.path)}
            >
              <span style={styles.icon}>{item.icon}</span>
              <span>{item.label}</span>
            </div>
          );
        })}
      </div>

    </aside>
  );
};

export default Sidebar;
