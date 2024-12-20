// src/DashboardView.js
import React from 'react';

import api from '../../../api/Api'; // Adjust the path as necessary

import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const DashboardView = () => {
  const data = {
    labels: ['Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
    datasets: [
      {
        label: 'Transactions',
        data: [15339,
          21345,
          18483,
          24003,
          23489,
          24092,
          12034],
        lineTension: 0,
        fill: true,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Transactions per day'
      },
      legend: {
        position: 'bottom',
        display: false
      }
    }
  };

  const handleCheckAPIConnection = async () => {
    try {
      const status = await api.getStatus();
      if (status.status === true) {
        alert('API is up and running');
      } else {
        alert(`API Status: ${JSON.stringify(status)}`);
      }
    } catch (error) {
      alert('Error fetching API status');
    }
  };

  return (
    <div className="table-responsive">
      <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h1 className="h2">Dashboard</h1>
        <div className="btn-toolbar mb-2 mb-md-0">
          <div className="btn-group me-2">
            <button type="button" className="btn btn-sm btn-outline-secondary">
              <i className="fas fa-share"></i> Share
            </button>
            <button type="button" className="btn btn-sm btn-outline-secondary">
              <i className="fas fa-file-export"></i> Export
            </button>
          </div>
          <button type="button" className="btn btn-sm btn-outline-secondary dropdown-toggle">
            <i className="fas fa-calendar-alt"></i> This week
          </button>
        </div>
      </div>

      <Line data={data} options={options} />

      <h2>App Status Test</h2>
      <div>
        <button type="button" className="btn btn-primary" onClick={handleCheckAPIConnection}>
          Check API Connection
        </button>
      </div>

      <h2>Section title</h2>
      <div className="table-responsive">
        <table className="table table-striped table-sm">
          <thead>
            <tr>
              <th>Id</th>
              <th>Header</th>
              <th>Header</th>
              <th>Header</th>
              <th>Header</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1,001</td>
              <td>random</td>
              <td>data</td>
              <td>placeholder</td>
              <td>text</td>
            </tr>
            <tr>
              <td>1,002</td>
              <td>placeholder</td>
              <td>irrelevant</td>
              <td>visual</td>
              <td>layout</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DashboardView;