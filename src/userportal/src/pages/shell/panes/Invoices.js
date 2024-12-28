// src/Transactions.js
import React from 'react';
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
        Header: 'Invoice Number',
        accessor: 'invoice_number',
      },
      {
        Header: 'Amount',
        accessor: 'amount',
      },
      {
        Header: 'Invoice Date',
        accessor: 'invoice_date',
      },
      {
        Header: 'Payment Status',
        accessor: 'payment_status',
      },
    ],
    []
  );

  const fetchVendors = async (skip, limit, sortBy, search) => {
    const response = await api.invoices.list(skip, limit, sortBy, search);
    return response;
  };

  return (
    <div>
      <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h1 className="h2">Invoices</h1>
      </div>
      <PagedTable columns={columns} fetchData={fetchVendors} />
    </div>
  );
};

export default SOWs;