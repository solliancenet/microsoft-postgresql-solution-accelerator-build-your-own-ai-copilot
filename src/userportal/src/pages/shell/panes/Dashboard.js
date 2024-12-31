// src/DashboardView.js
import React from 'react';
import api from '../../../api/Api'; // Adjust the path as necessary
import AIChat from '../../../components/AIChat'; // Adjust the path as necessary

const DashboardView = () => {
  // const handleCheckAPIConnection = async () => {
  //   try {
  //     const status = await api.getStatus();
  //     if (status.status === true) {
  //       alert('API is up and running');
  //     } else {
  //       alert(`API Status: ${JSON.stringify(status)}`);
  //     }
  //   } catch (error) {
  //     alert('Error fetching API status');
  //   }
  // };

  return (
    <div className="table-responsive">
      <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h1 className="h2">Dashboard</h1>
      </div>
      
      <AIChat />

      {/* <h2 className="mt-5">App Status Test</h2>
      <div>
        <button type="button" className="btn btn-primary" onClick={handleCheckAPIConnection}>
          Check API Connection
        </button>
      </div> */}
    </div>
  );
};

export default DashboardView;