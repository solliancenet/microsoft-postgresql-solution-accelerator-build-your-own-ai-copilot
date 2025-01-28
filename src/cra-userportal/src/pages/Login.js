// src/Login.js
import React, { useState } from 'react';
import './Login.css'; // Import the CSS file for additional styling if needed

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState('finance user');
  const [password, setPassword] = useState('********');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Add your authentication logic here
    // if (username === 'admin' && password === 'password') {
      onLogin();
    // } else {
    //   alert('Invalid credentials');
    // }
  };

  return (
    <main className="form-signin">
      <form onSubmit={handleSubmit}>
        <h1 className="h3 mb-3 fw-normal">Please sign in</h1>

        <div className="form-floating">
          <input
            type="text"
            className="form-control"
            id="floatingInput"
            placeholder="name@example.com"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <label htmlFor="floatingInput">Email address</label>
        </div>
        <div className="form-floating">
          <input
            type="password"
            className="form-control"
            id="floatingPassword"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <label htmlFor="floatingPassword">Password</label>
        </div>

        <div className="checkbox mb-3">
          <label>
            <input type="checkbox" value="remember-me" /> Remember me
          </label>
        </div>
        <button className="w-100 btn btn-lg btn-primary" type="submit">Sign in</button>
        <p className="mt-5 mb-3 text-muted">&copy; 2024</p>
      </form>
    </main>
  );
};

export default Login;