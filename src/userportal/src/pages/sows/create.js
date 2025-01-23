import React, { useState, useEffect } from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';
import { NumericFormat } from 'react-number-format';
import { useParams } from 'react-router-dom';
import api from '../../api/Api';
import config from '../../config';

const getDefaultNumber = () => {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `SOW-${year}-${month}${day}`;
};

const SOWCreate = () => {
  const { vendorId } = useParams();
  const [sowNumber, setSowNumber] = useState(getDefaultNumber());
  const [sowVendorId, setSowVendorId] = useState(vendorId);
  const [startDate, setStartDate] = useState('2024-01-01');
  const [endDate, setEndDate] = useState('2024-12-31');
  const [budget, setBudget] = useState('0');
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
        setError('Error fetching Vendors');
        setSuccess(null);
      }
    };

    fetchVendors();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      var data = {
        number: sowNumber,
        vendor_id: sowVendorId,
        start_date: startDate,
        end_date: endDate,
        budget: parseFloat(budget)
      };
      var newItem = await api.sows.create(file, data);
      
      setSuccess('SOW created successfully!');
      window.location.href = `/sows/${newItem.id}`;
      setError(null);
    } catch (err) {
      console.error(err);
      setError('Failed to create SOW');
      setSuccess(null);
    }
  };

  return (
    <div>
      <h1>Create SOW</h1>
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
        <Form.Group>
          <Form.Label>Vendor</Form.Label>
          <Form.Control
            as="select"
            value={sowVendorId}
            onChange={(e) => setSowVendorId(e.target.value)}
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

        {config.displayFieldOnCreate && (
          <>
          <Form.Group className="mb-3">
            <Form.Label>SOW Number</Form.Label>
            <Form.Control
              type="text"
              value={sowNumber}
              onChange={(e) => setSowNumber(e.target.value)}
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
            <Form.Label>Budget</Form.Label>
            <NumericFormat
              className="form-control"
              value={budget}
              thousandSeparator={true}
              prefix={'$'}
              onValueChange={(values) => {
                const { value } = values;
                setBudget(value);
              }}
              required
            />
          </Form.Group>
        </>
        )}
        <br/>
        <Button type="submit" variant="primary">
          <i className="fas fa-plus"></i> Create
        </Button>
        <Button type="button" variant="secondary" className="ms-2" onClick={() => window.location.href = '/sows' }>
          <i className="fas fa-times"></i> Cancel
        </Button>
      </Form>
    </div>
  );
};

export default SOWCreate;