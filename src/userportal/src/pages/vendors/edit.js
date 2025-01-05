import React, { useEffect, useState } from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
import api from '../../api/Api';

const VendorEdit = () => {
    const { id } = useParams(); // Extract Vendor ID from URL
    const [name, setName] = useState('');
    const [address, setAddress] = useState('');
    const [contactName, setContactName] = useState('');
    const [contactEmail, setContactEmail] = useState('');
    const [contactPhone, setContactPhone] = useState('');
    const [contactType, setContactType] = useState('');
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

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
        setContactType(data.type);
      }
    
      const handleSubmit = async (e) => {
        e.preventDefault();
        try {
          var data = await api.vendors.update(id, name, address, contactName, contactEmail, contactPhone, contactType);
          updateDisplay(data);
          setSuccess('Vendor updated successfully!');
          setError(null);
        } catch (err) {
          console.error(err);
          setError('Failed to update Vendor');
          setSuccess(null);
        }
      };

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
          <i className="fas fa-save"></i> Save
        </Button>
        <Button type="button" variant="secondary" className="ms-2" onClick={() => window.location.href = '/vendors' }>
          <i className="fas fa-times"></i> Cancel
        </Button>
      </Form>
    </div>
  );
};

export default VendorEdit;