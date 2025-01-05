import React from 'react';
import api from '../../../api/Api';
import PagedTable from '../../../components/PagedTable';

const Msas = () => {
  const columns = React.useMemo(
    () => [
      {
        Header: 'ID',
        accessor: 'id',
      },
      {
        Header: 'Title',
        accessor: 'title',
      },
      {
        Header: 'Start Date',
        accessor: 'start_date',
      },
      {
        Header: 'End Date',
        accessor: 'end_date',
      },
    ],
    []
  );

  const fetchData = async (skip, limit, sortBy, search) => {
    const response = await api.msas.list(skip, limit, sortBy, search);
    return response;
  };

  return (
    <div>
      <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h1 className="h2">MSAs</h1>
      </div>
      <PagedTable columns={columns} fetchData={fetchData} />
    </div>
  );
};

export default Msas;