import React, { useState } from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';
import { NumericFormat } from 'react-number-format';
import api from '../../api/Api';

const VendorCreate = () => {
    const [name, setName] = useState('');
    const [address, setAddress] = useState('');
    const [contactName, setContactName] = useState('');
    const [contactEmail, setContactEmail] = useState('');
    const [contactPhone, setContactPhone] = useState('');
    const [contactType, setContactType] = useState('');
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try
        {
          var data = {
            name: name,
            address: address,
            contact_name: contactName,
            contact_email: contactEmail,
            contact_phone: contactPhone,
            contact_type: contactType
          };
          var newItem = await api.vendors.create(data);

          setSuccess('Vendor created successfully!');
          window.location.href = `/vendors/${newItem.id}`;
          setError(null);
        } catch (err) {
          console.error(err);
          setError('Failed to create Vendor' + err);
          setSuccess(null);
        }
    };

  return (
    <div>
      <h1>Create Vendor</h1>
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
          />
        </Form.Group>
        <Form.Group className="mb-3">
            <Form.Label>Address</Form.Label>
            <Form.Control
            type="text"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            required
            />
        </Form.Group>
        <Form.Group className="mb-3">
            <Form.Label>Contact Name</Form.Label>
            <Form.Control
            type="text"
            value={contactName}
            onChange={(e) => setContactName(e.target.value)}
            required
            />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Contact Email</Form.Label>
          <Form.Control
            type="email"
            value={contactEmail}
            onChange={(e) => setContactEmail(e.target.value)}
            required
            />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Contact Phone</Form.Label>
          <Form.Control
            type="tel"
            value={contactPhone}
            onChange={(e) => setContactPhone(e.target.value)}
            required
            />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Contact Type</Form.Label>
          <Form.Control
            type="text"
            value={contactType}
            onChange={(e) => setContactType(e.target.value)}
            required
            />
        </Form.Group>
        <Button type="submit" variant="primary">
          <i className="fas fa-plus"></i> Create
        </Button>
        <Button type="button" variant="secondary" className="ms-2" onClick={() => window.location.href = '/vendors' }>
          <i className="fas fa-times"></i> Cancel
        </Button>
      </Form>
    </div>
  );
};

export default VendorCreate;