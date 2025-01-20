import React, { useState, useEffect } from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
import api from '../../api/Api';
import ConfirmModal from '../../components/ConfirmModal';
import PagedTable from '../../components/PagedTable';

const MSAEdit = () => {
  const { id } = useParams(); // Extract MSA ID from URL
  const [msaVendorId, setMsaVendorId] = useState('');
  const [title, setTitle] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [document, setDocument] = useState(null);
  const [metadata, setMetadata] = useState(null);
  const [success, setSuccess] = useState(null);
  const [error, setError] = useState(null);

  const [vendors, setVendors] = useState([]);
  
  const [showDeleteSowModal, setShowDeleteSowModal] = useState(false);
  const [sowToDelete, setSowToDelete] = useState(null);
  const [reloadSows, setReloadSows] = useState(false);

  useEffect(() => {
    const fetchVendors = async () => {
      try {
        const data = await api.vendors.list(0, -1); // No pagination limit
        setVendors(data.data);
      } catch (err) {
        console.error(err);
        setError('Error fetching vendors');
        setSuccess(null);
      }
    };

    fetchVendors();
  }, []);

  useEffect(() => {
    // Fetch data when component mounts
    const fetchData = async () => {
      try {
        const data = await api.msas.get(id);
        updateDisplay(data);
      } catch (err) {
        setError('Failed to load MSA data');
      }
    };
    fetchData();
  }, [id]);

  const updateDisplay = (data) => {
    setMsaVendorId(data.vendor_id);
    setTitle(data.title);
    setStartDate(data.start_date);
    setEndDate(data.end_date);
    setDocument(data.document);
    setMetadata(data.metadata ? JSON.stringify(data.metadata, null, 2) : '');
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      var data = {
        vendor_id: msaVendorId,
        title: title,
        start_date: startDate,
        end_date: endDate
      };
      var updatedItem = await api.msas.update(id, data);

      updateDisplay(updatedItem);
      setSuccess('MSA updated successfully!');
      setError(null);
    } catch (err) {
      console.error(err);
      setError('Failed to update MSA');
      setSuccess(null);
    }
  };

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
      <h1>Edit MSA</h1>
      <hr/>
      {error && <div className="alert alert-danger">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Vendor</Form.Label>
          <Form.Control
            as="select"
            value={msaVendorId}
            onChange={(e) => setMsaVendorId(e.target.value)}
            required
          >
            <option value="">Select Vendor</option>
            {vendors.map((vendor) => (
              <option key={vendor.id} value={vendor.id}>
                {vendor.name}
              </option>
            ))}
          </Form.Control>
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Title</Form.Label>
          <Form.Control
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </Form.Group>
        <Row className="mb-3">
          <Col md={6}>
            <Form.Group className="mb-3">
              <Form.Label>Start Date</Form.Label>
              <Form.Control
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                required
              />
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group className="mb-3">
              <Form.Label>End Date</Form.Label>
              <Form.Control
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </Form.Group>
          </Col>
        </Row>
        <Form.Group className="mb-3">
          <Form.Label>Document</Form.Label>
          <div className="d-flex">
            <code>{document}</code>
            <a href={api.documents.getUrl(document)} target="_blank" rel="noreferrer">
              <i className="fas fa-download ms-3"></i>
            </a>
          </div>
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Metadata</Form.Label>
          <Form.Control
            as="textarea"
            value={metadata}
            onChange={(e) => setMetadata(e.target.value)}
            style={{ height: '8em' }}
            readOnly
          />
        </Form.Group>
        <Button type="submit" variant="primary">
          <i className="fas fa-save"></i> Save
        </Button>
        <Button type="button" variant="secondary" className="ms-2" onClick={() => window.location.href = '/msas' }>
          <i className="fas fa-times"></i> Cancel
        </Button>
        <a href={`/vendors/${msaVendorId}`} className="btn btn-link ms-2">
          Go to Vendor
        </a>
      </Form>

      <hr />

      <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h2 className="h2">SOWs</h2>
        <Button variant="primary" onClick={() => window.location.href = `/sows/create/${id}`}>
          New Sow <i className="fas fa-plus" />
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

export default MSAEdit;