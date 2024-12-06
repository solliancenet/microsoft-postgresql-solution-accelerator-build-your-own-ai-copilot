// src/App.js
import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Login from './pages/Login';
import Shell from './pages/shell/Shell';
import './App.css'; // Import the CSS file

function App() {
  // default to be logged in, if login is required, set it to false
  const [isLoggedIn, setIsLoggedIn] = useState(true);
  const [isDarkTheme, setIsDarkTheme] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  const toggleTheme = () => {
    setIsDarkTheme(!isDarkTheme);
  };

  useEffect(() => {
    document.body.className = isDarkTheme ? 'bg-dark text-white' : 'bg-light text-dark';
  }, [isDarkTheme]);

  return (
    <span>
      <header className={`navbar 'navbar-dark sticky-top bg-dark flex-md-nowrap p-0 shadow`}>
        <a className="navbar-brand col-md-3 col-lg-2 me-0 px-3 d-flex align-items-center" href="#">
          <img src="logo192.png" alt="Contoso Finance" className="logo" />
          <span className="ms-2 text-light">Contoso Finance</span>
        </a>
        <button className="navbar-toggler position-absolute d-md-none collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#sidebarMenu" aria-controls="sidebarMenu" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="navbar-nav flex-row">
          <div className="nav-item text-nowrap d-flex align-items-center">
            <div className="form-check form-switch me-3">
              <input className="form-check-input" type="checkbox" id="themeSwitch" checked={isDarkTheme} onChange={toggleTheme} />
              <label className="form-check-label" htmlFor="themeSwitch">
                <i className={`fas ${isDarkTheme ? 'fa-moon' : 'fa-sun'} me-2 text-light`}></i>
              </label>
            </div>
            {isLoggedIn && <a className="nav-link px-3 text-light" href="#" onClick={handleLogout}>Sign out</a>}
          </div>
        </div>
      </header>
      <div className={`container-fluid ${isDarkTheme ? 'bg-dark text-white' : 'bg-light text-dark'}`}>
        {isLoggedIn ? <Shell isDarkTheme={isDarkTheme} /> : <Login onLogin={handleLogin} />}
      </div>
    </span>
  );
}

export default App;
