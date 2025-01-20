import React, { useState, useEffect } from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
import { NumericFormat } from 'react-number-format';
import api from '../../api/Api';

const MSACreate = () => {
  const { vendorId } = useParams();
  const [msaVendorId, setMsaVendorId] = useState(vendorId);
  const [msaTitle, setMsaTitle] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      var data = {
        vendor_id: msaVendorId,
        title: msaTitle,
        start_date: startDate,
        end_date: endDate
      };
      var newItem = await api.msas.create(file, data);

      setSuccess('MSA created successfully!');
      window.location.href = `/msas/${newItem.id}`;
      setError(null);
    } catch (err) {
      console.error(err);
      setError('Failed to create MSA');
      setSuccess(null);
    }
  };

  return (
    <div>
      <h1>Create MSA</h1>
      <hr/>
      {error && <div className="alert alert-danger">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Document</Form.Label>
          <Form.Control
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            required
          />
        </Form.Group>
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
            value={msaTitle}
            onChange={(e) => setMsaTitle(e.target.value)}
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
        <Button type="submit" variant="primary">
          <i className="fas fa-plus"></i> Create
        </Button>
        <Button type="button" variant="secondary" className="ms-2" onClick={() => window.location.href = '/msas' }>
          <i className="fas fa-times"></i> Cancel
        </Button>
      </Form>
    </div>
  );
};

export default MSACreate;