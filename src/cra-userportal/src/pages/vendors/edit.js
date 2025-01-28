import React, { useEffect, useState } from 'react';
import { Form, Button, } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
import api from '../../api/Api';
import ConfirmModal from '../../components/ConfirmModal';
import PagedTable from '../../components/PagedTable';

const VendorEdit = () => {
    const { id } = useParams(); // Extract Vendor ID from URL
    const [name, setName] = useState('');
    const [address, setAddress] = useState('');
    const [contactName, setContactName] = useState('');
    const [contactEmail, setContactEmail] = useState('');
    const [contactPhone, setContactPhone] = useState('');
    const [contactType, setContactType] = useState('');
    const [website, setWebsite] = useState('');
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    
    const [showDeleteSowModal, setShowDeleteSowModal] = useState(false);
    const [sowToDelete, setSowToDelete] = useState(null);
    const [reloadSows, setReloadSows] = useState(false);
    
    useEffect(() => {
        // Fetch SOW data when component mounts
        const fetchSOW = async () => {
          try {
            const data = await api.vendors.get(id);
            updateDisplay(data);
          } catch (err) {
            setError('Failed to load Vendor data');
          }
        };
        fetchSOW();
      }, [id]);
    
      const updateDisplay = (data) => {
        setName(data.name);
        setAddress(data.address);
        setContactName(data.contact_name);
        setContactEmail(data.contact_email);
        setContactPhone(data.contact_phone);
        setWebsite(data.website);
        setContactType(data.type);
      }
    
      const handleSubmit = async (e) => {
        e.preventDefault();
        // try {
        //   var data = {
        //     name: name,
        //     address: address,
        //     contact_name: contactName,
        //     contact_email: contactEmail,
        //     contact_phone: contactPhone,
        //     type: contactType
        //   };
        //   var updatedItem = await api.vendors.update(id, data);

        //   updateDisplay(updatedItem);
        //   setSuccess('Vendor updated successfully!');
        //   setError(null);
        // } catch (err) {
        //   console.error(err);
        //   setError('Failed to update Vendor');
        //   setSuccess(null);
        // }
      };


  const sowColumns = React.useMemo(
    () => [
      {
        Header: 'Number',
        accessor: 'number',
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
        Cell: ({ row }) => {
          return (
            <div>
              <a href={`/sows/${row.original.id}`} className="btn btn-link" aria-label="Edit">
                <i className="fas fa-edit"></i>
              </a>
              <Button
                variant="danger"
                size="sm"
                onClick={() => {
                  setSowToDelete(row.original.id);
                  setShowDeleteSowModal(true);
                }}
              >
                Delete
              </Button>
            </div>
          );
        },
      },
    ],
    []
  );

  const handleDeleteSow = async () => {
      try {
        await api.sows.delete(sowToDelete);
        setSuccess('SOW deleted successfully!');
        setError(null);
        setShowDeleteSowModal(false);
        setReloadSows(true);
      } catch (err) {
        setSuccess(null);
        setError(err.message);
      }
    }
      
  const fetchSows = async () => {
    try {
      const data = await api.sows.list(id, 0, -1); // No pagination limit
      return data;
    } catch (err) {
      console.error(err);
      setError('Error fetching SOWs');
      setSuccess(null);
    }
  }

  return (
    <div>
      <h1>Edit Vendor</h1>
      <hr/>
      {error && <div className="alert alert-danger">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Name</Form.Label>
          <Form.Control
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            disabled
          />
        </Form.Group>
        <Form.Group className="mb-3">
            <Form.Label>Address</Form.Label>
            <Form.Control
            type="text"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            required
            disabled
            />
        </Form.Group>
        <Form.Group className="mb-3">
            <Form.Label>Contact Name</Form.Label>
            <Form.Control
            type="text"
            value={contactName}
            onChange={(e) => setContactName(e.target.value)}
            required
            disabled
            />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Contact Email</Form.Label>
          <Form.Control
            type="email"
            value={contactEmail}
            onChange={(e) => setContactEmail(e.target.value)}
            required
            disabled
            />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Contact Phone</Form.Label>
          <Form.Control
            type="tel"
            value={contactPhone}
            onChange={(e) => setContactPhone(e.target.value)}
            required
            disabled
            />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Contact Type</Form.Label>
          <Form.Control
            type="text"
            value={contactType}
            onChange={(e) => setContactType(e.target.value)}
            required
            disabled
            />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Website</Form.Label>
          <Form.Control
            type="text"
            value={website}
            onChange={(e) => setWebsite(e.target.value)}
            required
            disabled
            />
        </Form.Group>
        
        {/* <Button type="submit" variant="primary">
          <i className="fas fa-save"></i> Save
        </Button>
        <Button type="button" variant="secondary" className="ms-2" onClick={() => window.location.href = '/vendors' }>
          <i className="fas fa-times"></i> Cancel
        </Button> */}
      </Form>

      <hr />

      <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h2 className="h2">SOWs</h2>
        <Button variant="primary" onClick={() => window.location.href = `/sows/create/${id}`}>
          New SOW <i className="fas fa-plus" />
        </Button>
      </div>

      <PagedTable columns={sowColumns}
        fetchData={fetchSows}
        reload={reloadSows}
        showPagination={false}
        />

      <ConfirmModal
        show={showDeleteSowModal}
        handleClose={() => setShowDeleteSowModal(false)}
        handleConfirm={handleDeleteSow}
        title="Delete SOW"
        message="Are you sure you want to delete this SOW?"
      />
    </div>
  );
};

export default VendorEdit;