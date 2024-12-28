import React, { useEffect, useState } from 'react';
import Table from './Table';

const PagedTable = ({ columns, fetchData }) => {
  const [data, setData] = useState([]);
  const [total, setTotal] = useState(0);
  const [skip, setSkip] = useState(0);
  const [limit, setLimit] = useState(10);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = async (skip, limit) => {
    setLoading(true);
    try {
      const response = await fetchData(skip, limit);
      setData(response.data);
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
    loadData(skip, limit);
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
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>Error: {error}</p>
      ) : (
        <div>
          <Table columns={columns} data={data} />
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

export default PagedTable;