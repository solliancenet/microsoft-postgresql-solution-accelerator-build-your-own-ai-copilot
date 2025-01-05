import React, { useEffect, useState } from 'react';
import Table from './Table';

const PagedTable = ({ columns, fetchData, searchEnabled = false, reload }) => {
  const [data, setData] = useState([]);
  const [total, setTotal] = useState(0);
  const [skip, setSkip] = useState(0);
  const [limit, setLimit] = useState(10);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sortBy, setSortBy] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');

  const loadData = async (skip, limit, sortBy, searchQuery) => {
    setLoading(true);
    try {
      const sortbyParam = (sortBy && sortBy.length > 0) ? `${sortBy[0].id} ${sortBy[0].desc ? 'desc' : 'asc'}` : '';
      const response = await fetchData(skip, limit, sortbyParam, searchQuery);
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
    loadData(skip, limit, sortBy, searchQuery);
  }, [skip, limit, sortBy, searchQuery, reload]);

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
    if (JSON.stringify(sortBy) !== JSON.stringify(newSortBy)) {
      setSortBy(newSortBy);
    }
  };

  const updateSearch = (value) => {
    setSkip(0);
    setSearchQuery(value);
  }

  const clearSearch = () => {
    updateSearch('');
  }

  const pageIndex = Math.floor(skip / limit) + 1;
  const pageCount = Math.ceil(total / limit);

  return (
    <div>
      {searchEnabled && (
        <div className="d-flex justify-content-between mb-3">
          <div></div>
          <div className="d-flex">
            <input
              type="text"
              className="form-control"
              placeholder="Search..."
              value={searchQuery}
              onChange={(e) => updateSearch(e.target.value)}
            />
            <button className="btn btn-primary ml-2" onClick={clearSearch}>Clear</button>
          </div>
        </div>
      )}
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>Error: {error}</p>
      ) : (
        <div>
          <Table
            columns={columns}
            data={data}
            loading={loading}
            onSortChange={handleSortChange}
          />
          <div className="d-flex justify-content-between">
            <button className="btn btn-primary" onClick={handlePrevious} disabled={skip === 0}>
              Previous
            </button>
            <div className="pagination-info">
              Page {pageIndex} of {pageCount}
            </div>
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