import React from 'react';
import api from '../../../api/Api';
import PagedTable from '../../../components/PagedTable';

const Companies = () => {
  const columns = React.useMemo(
    () => [
      {
        Header: 'ID',
        accessor: 'id',
      },
      {
        Header: 'Company Name',
        accessor: 'company_name',
      },
      {
        Header: 'Address',
        accessor: 'address',
      },
      {
        Header: 'Contact Person',
        accessor: 'contact_person',
      },
      {
        Header: 'Contact Email',
        accessor: 'contact_email',
      },
    ],
    []
  );

  const fetchCompanies = async (skip, limit, sortBy, search) => {
    const response = await api.companies.list(skip, limit, sortBy, search);
    return response;
  };

  return (
    <div>
      <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h1 className="h2">Companies</h1>
      </div>
      <PagedTable columns={columns} fetchData={fetchCompanies} />
    </div>
  );
};

export default Companies;