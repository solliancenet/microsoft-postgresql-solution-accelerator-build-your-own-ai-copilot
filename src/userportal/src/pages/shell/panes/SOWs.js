// src/Transactions.js
import React from 'react';
import { Link } from 'react-router-dom';
import api from '../../../api/Api';
import PagedTable from '../../../components/PagedTable';

const SOWs = () => {
  const columns = React.useMemo(
    () => [
      {
        Header: 'ID',
        accessor: 'id',
      },
      {
        Header: 'Title',
        accessor: 'sow_title',
      },
      {
        Header: 'Start Date',
        accessor: 'start_date',
      },
      {
        Header: 'End Date',
        accessor: 'end_date',
      },
      {
        Header: 'Budget',
        accessor: 'budget',
      },
      {
        Header: 'Actions',
        accessor: 'actions',
        Cell: ({ row }) => (
          <div>
            <a href={`${api.documents.getUrl(row.original.sow_document)}`} target="_blank" rel="noopener noreferrer" className="btn btn-link" aria-label="Download">
              <i className="fas fa-download"></i>
            </a>
          </div>
        ),
      },
    ],
    []
  );

  const fetchVendors = async (skip, limit, sortBy, search) => {
    const response = await api.sows.list(skip, limit, sortBy, search);
    return response;
  };

  return (
    <div>
      <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h1 className="h2">SOWs</h1>
        <Link to="/sows/create" className="btn btn-primary">New <i className="fas fa-plus" /></Link>
      </div>
      <PagedTable columns={columns} fetchData={fetchVendors} />
    </div>
  );
};

export default SOWs;