// src/App.js
import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Login from './pages/Login';
import Shell from './pages/shell/Shell';
import './App.css'; // Import the CSS file

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  return (
    <span>
      <header className="navbar navbar-dark sticky-top bg-dark flex-md-nowrap p-0 shadow">
        <a className="navbar-brand col-md-3 col-lg-2 me-0 px-3" href="#">
          <img src="logo192.png" alt="" width="18" height="18" />
          Contoso Finance
        </a>
        <button className="navbar-toggler position-absolute d-md-none collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#sidebarMenu" aria-controls="sidebarMenu" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="navbar-nav">
          <div className="nav-item text-nowrap">
            {isLoggedIn && <a className="nav-link px-3" href="#" onClick={handleLogout}>Sign out</a>}
          </div>
        </div>
      </header>

      <div className="container-fluid">
        {isLoggedIn ? <Shell /> : <Login onLogin={handleLogin} />}
      </div>
    </span>
  );
}

export default App;
