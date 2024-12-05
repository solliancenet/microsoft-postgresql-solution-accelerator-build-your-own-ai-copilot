// src/Shell.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes, NavLink } from 'react-router-dom';

import { APIUrl } from './../../api/APIConfig';

import UserProfile from './../../components/UserProfile';

import Dashboard from './panes/Dashboard';
import Transactions from './panes/Transactions';
import Documents from './panes/Documents';

const Shell = ({ isDarkTheme }) => {
  const userName = "John Doe"; // Replace with actual user name
  const userAvatar = "user-avatar.svg"; // Replace with actual avatar URL

  return (
    <Router>
      <div className="container-fluid">
        <div className="row">
        <nav id="sidebarMenu" className={`col-md-3 col-lg-2 d-md-block sidebar collapse d-flex flex-column ${isDarkTheme ? 'bg-dark text-white' : 'bg-light text-dark'}`}>
        <div className="position-sticky pt-3">
              <ul className="nav flex-column">
                <li className="nav-item">
                  <NavLink className="nav-link" to="/" end>
                    <i className="fas fa-home"></i> Dashboard
                  </NavLink>
                </li>
                <li className="nav-item">
                  <NavLink className="nav-link" to="/transactions">
                    <i className="fas fa-chart-bar"></i> Transactions
                  </NavLink>
                </li>
                <li className="nav-item">
                  <NavLink className="nav-link" to="/documents">
                    <i className="fas fa-file-alt"></i> Documents
                  </NavLink>
                </li>
              </ul>
              <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mb-1">
                Reports
                <button type="button" className="btn btn-sm btn-outline-secondary" title="New Report">
                  <i className="fas fa-plus"></i>
                </button>
              </h6>
              <ul className="nav flex-column">
                <li className="nav-item">
                  <a className="nav-link" href="#">
                    <i className="fas fa-chart-line"></i> Current month
                  </a>
                  <a className="nav-link" href="#">
                    <i className="fas fa-chart-line"></i> Last quarter
                  </a>
                </li>
              </ul>
            </div>

            <div className="sidebar-sticky-bottom pt-3">
              <UserProfile name={userName} avatar={userAvatar} />
              <br/><small>{APIUrl}</small>
            </div>
          </nav>

          <main className="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <Routes>
              <Route exact path="/" element={<Dashboard />} />
              <Route path="/transactions" element={<Transactions />} />
              <Route path="/documents" element={<Documents />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
};

export default Shell;