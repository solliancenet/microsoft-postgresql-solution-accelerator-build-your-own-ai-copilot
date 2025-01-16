import React, { useState, useEffect } from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';
import { NumericFormat } from 'react-number-format';
import { useParams } from 'react-router-dom';
import api from '../../api/Api';

const MSAEdit = () => {
  const { id } = useParams(); // Extract MSA ID from URL
  const [msaVendorId, setMsaVendorId] = useState('');
  const [title, setTitle] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [metadata, setMetadata] = useState(null);
  const [success, setSuccess] = useState(null);
  const [error, setError] = useState(null);

  const [vendors, setVendors] = useState([]);
  
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
    setMetadata(data.metadata ? JSON.stringify(data.metadata, null, 2) : '');
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      var data = await api.msas.update(id, title, startDate, endDate);
      updateDisplay(data);
      setSuccess('MSA updated successfully!');
      setError(null);
    } catch (err) {
      console.error(err);
      setError('Failed to update MSA');
      setSuccess(null);
    }
  };

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
            disabled
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
                required
              />
            </Form.Group>
          </Col>
        </Row>
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
    </div>
  );
};

export default MSAEdit;