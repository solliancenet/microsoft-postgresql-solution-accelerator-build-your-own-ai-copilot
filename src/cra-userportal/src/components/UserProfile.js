// src/UserProfile.js
import React from 'react';
import './UserProfile.css'; // Import the CSS file for styling

const UserProfile = ({ name, avatar }) => {
  return (
    <div className="user-profile">
      <img src={avatar} alt="User Avatar" className="user-avatar" />
      <span className="user-name">{name}</span>
    </div>
  );
};

export default UserProfile;