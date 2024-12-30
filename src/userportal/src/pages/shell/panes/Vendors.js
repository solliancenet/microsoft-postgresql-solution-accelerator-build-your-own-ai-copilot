// src/Transactions.js
import React from 'react';
import api from '../../../api/Api';
import PagedTable from '../../../components/PagedTable';

const Vendors = () => {
  const columns = React.useMemo(
    () => [
      {
        Header: 'ID',
        accessor: 'id',
      },
      {
        Header: 'Vendor Name',
        accessor: 'name',
      },
      {
        Header: 'Address',
        accessor: 'address',
      },
      {
        Header: 'Contact Person',
        accessor: 'contact_name',
      },
      {
        Header: 'Contact Email',
        accessor: 'contact_email',
      },
      {
        Header: 'Contact Phone',
        accessor: 'contact_phone',
      },
      {
        Header: 'Type',
        accessor: 'contact_type',
      },
    ],
    []
  );

  const fetchVendors = async (skip, limit, sortBy, search) => {
    const response = await api.vendors.list(skip, limit, sortBy, search);
    return response;
  };

  return (
    <div>
      <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h1 className="h2">Vendors</h1>
      </div>
      <PagedTable columns={columns} fetchData={fetchVendors} />
    </div>
  );
};

export default Vendors;