import React, { useState, useEffect } from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';
import { NumericFormat } from 'react-number-format';
import { useParams } from 'react-router-dom';
import api from '../../api/Api';

const DeliverableCreate = () => {
  const { milestoneId } = useParams(); // Extract from URL
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [status, setStatus] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      var data = await api.deliverables.create(milestoneId, name, description, amount, status);
      setSuccess('Deliverable created successfully!');
      window.location.href = `/deliverables/${data.id}`;
      setError(null);
    } catch (err) {
      console.error(err);
      setError('Failed to create Deliverable');
      setSuccess(null);
    }
  };

  return (
    <div>
      <h1>Create Deliverable</h1>
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
              <Form.Label>Status</Form.Label>
              <Form.Control
              type="text"
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              required
              />
          </Form.Group>
          <Form.Group className="mb-3">
              <Form.Label>Amount</Form.Label>
              <NumericFormat
                  className="form-control"
                  value={amount}
                  onValueChange={(values) => {
                      const { value } = values;
                      setAmount(value);
                  }}
                  required
              />
          </Form.Group>
          <Form.Group className="mb-3">
              <Form.Label>Description</Form.Label>
              <Form.Control
                  as="textarea"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  required
              />
          </Form.Group>
      
          <Button type="submit" variant="primary">
            <i className="fas fa-plus"></i> Create
          </Button>
          <a href={`/milestones/${milestoneId}`} className="btn btn-secondary ms-2" aria-label="Cancel">
            <i className="fas fa-arrow-left"></i> Back to Milestone
          </a>
      </Form>
    </div>
  );
};

export default DeliverableCreate;