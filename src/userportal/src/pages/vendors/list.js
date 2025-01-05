import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../../api/Api';
import { Button } from 'react-bootstrap';
import ConfirmModal from '../../components/ConfirmModal'; 
import PagedTable from '../../components/PagedTable';

const VendorList = () => {
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [sowToDelete, setSowToDelete] = useState(null);
  const [reload, setReload] = useState(false);
  
  const handleDelete = async () => {
    if (!sowToDelete) return;

    try {
      await api.vendors.delete(sowToDelete);
      setSuccess('Vendor deleted successfully!');
      setError(null);
      setShowDeleteModal(false);
      setReload(true); // Refresh the data
    } catch (err) {
      setSuccess(null);
      setError(err.message);
    }
  }

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
      {
        Header: 'Actions',
        accessor: 'actions',
        Cell: ({ row }) => (
          <div>
            <a href={`/vendors/${row.original.id}`} className="btn btn-link" aria-label="Edit">
              <i className="fas fa-edit"></i>
            </a>
            <Button variant="danger" onClick={() => { setSowToDelete(row.original.id); setShowDeleteModal(true); }} aria-label="Delete">
              <i className="fas fa-trash-alt"></i>
            </Button>
          </div>
        ),
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
        <Link to="/vendoes/create" className="btn btn-primary">New <i className="fas fa-plus" /></Link>
      </div>
      
      <PagedTable columns={columns} fetchData={fetchVendors} reload={reload} />

      <ConfirmModal
        show={showDeleteModal}
        handleClose={() => setShowDeleteModal(false)}
        handleConfirm={handleDelete}
        message="Are you sure you want to delete this SOW?"
      />
    </div>
  );
};

export default VendorList;