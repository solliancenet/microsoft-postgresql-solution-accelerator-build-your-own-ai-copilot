// src/Transactions.js
import React, { useEffect, useState } from 'react';
import api from '../../../api/Api';

const Vendors = () => {
  const [vendors, setVendors] = useState([]);
  const [total, setTotal] = useState(0);
  const [skip, setSkip] = useState(0);
  const [limit, setLimit] = useState(10);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchVendors = async (skip, limit) => {
    setLoading(true);
    try {
      const response = await api.vendors.list(skip, limit);
      setVendors(response.data);
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
    fetchVendors(skip, limit);
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
        <h1 className="h2">Vendors</h1>
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
                <th>Vendor Name</th>
                <th>Address</th>
                <th>Contact Person</th>
                <th>Contact Email</th>
                <th>Contact Phone</th>
                <th>Type</th>
              </tr>
            </thead>
            <tbody>
              {vendors.map((vendor) => (
                <tr key={vendor.id}>
                  <td>{vendor.id}</td>
                  <td>{vendor.name}</td>
                  <td>{vendor.address}</td>
                  <td>{vendor.contact_name}</td>
                  <td>{vendor.contact_email}</td>
                  <td>{vendor.contact_phone}</td>
                  <td>{vendor.contact_type}</td>
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

export default Vendors;