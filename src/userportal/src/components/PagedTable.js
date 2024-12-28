import React, { useEffect, useState } from 'react';
import Table from './Table';

const PagedTable = ({ columns, fetchData }) => {
  const [data, setData] = useState([]);
  const [total, setTotal] = useState(0);
  const [skip, setSkip] = useState(0);
  const [limit, setLimit] = useState(10);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sortBy, setSortBy] = useState([]);

  const loadData = async (skip, limit, sortBy) => {
    setLoading(true);
    try {
      const sortbyParam = sortBy.length > 0 ? `${sortBy[0].id}:${sortBy[0].desc ? 'desc' : 'asc'}` : '';
      const response = await fetchData(skip, limit, sortbyParam);
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
    loadData(skip, limit, sortBy);
  }, [skip, limit, sortBy]);

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

  const handleSortChange = (newSortBy) => {
    setSortBy(newSortBy || '');
  };

  return (
    <div>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>Error: {error}</p>
      ) : (
        <div>
          <Table columns={columns} data={data} onSortChange={handleSortChange} />
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