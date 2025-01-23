import React from 'react';
import CopilotChat from '../../components/CopilotChat';

const Dashboard = () => {
  return (
    <div className="table-responsive">
      <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h1 className="h2">Dashboard</h1>
      </div>
      
      <CopilotChat />

    </div>
  );
};

export default Dashboard;