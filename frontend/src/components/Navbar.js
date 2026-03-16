import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FaMapMarkedAlt, FaHome } from 'react-icons/fa';
import './Navbar.css';

function Navbar() {
  const location = useLocation();

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <img src="/logo.png" alt="VietHerb Logo" className="brand-logo" />
          {/* <span>VIETHERB</span> */}
        </Link>
        <div className="navbar-links">
          <Link
            to="/"
            className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
          >
            <FaHome />
            <span>Danh mục</span>
          </Link>
          <Link
            to="/chatbot"
            className={`nav-link ${location.pathname === '/chatbot' ? 'active' : ''}`}
          >
            <FaMapMarkedAlt />
            <span>Bản đồ tìm kiếm</span>
          </Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
