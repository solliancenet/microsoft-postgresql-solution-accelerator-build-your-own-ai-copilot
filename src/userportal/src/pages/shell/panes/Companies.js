// src/Transactions.js
import React, { useEffect, useState } from 'react';
import api from '../../../api/Api';

const Companies = () => {
  const [companies, setCompanies] = useState([]);
  const [total, setTotal] = useState(0);
  const [skip, setSkip] = useState(0);
  const [limit, setLimit] = useState(10);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchCompanies = async (skip, limit) => {
    setLoading(true);
    try {
      const response = await api.companies.list(skip, limit);
      setCompanies(response.data);
      setTotal(response.total);
      setSkip(response.skip);
      setLimit(response.limit);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCompanies(skip, limit);
  }, [skip, limit]);

  const handlePrevious = () => {
    if (skip > 0) {
      setSkip(skip - limit);
    }
  };

  const handleNext = () => {
    if (skip + limit < total) {
      setSkip(skip + limit);
    }
  };

  return (
    <div>
      <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h1 className="h2">Companies</h1>
      </div>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>Error: {error}</p>
      ) : (
        <div>
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Company Name</th>
                <th>Address</th>
                <th>Contact Person</th>
                <th>Contact Email</th>
              </tr>
            </thead>
            <tbody>
              {companies.map((company) => (
                <tr key={company.id}>
                  <td>{company.id}</td>
                  <td>{company.company_name}</td>
                  <td>{company.address}</td>
                  <td>{company.contact_person}</td>
                  <td>{company.contact_email}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="d-flex justify-content-between">
            <button className="btn btn-primary" onClick={handlePrevious} disabled={skip === 0}>
              Previous
            </button>
            <button className="btn btn-primary" onClick={handleNext} disabled={skip + limit >= total}>
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Companies;