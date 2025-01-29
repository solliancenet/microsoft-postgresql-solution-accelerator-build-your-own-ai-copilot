import React, { useState, useEffect } from 'react';
import { Form, Button } from 'react-bootstrap';
import { NumericFormat } from 'react-number-format';
import { useParams } from 'react-router-dom';
import api from '../../api/Api';

const DeliverableCreate = () => {
  const { milestoneId } = useParams(); // Extract from URL
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [status, setStatus] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const [statuses, setStatuses] = useState([]);

  useEffect(() => {
    // Fetch data when component mounts
    const fetchStatuses = async () => {
      try {
        const data = await api.statuses.list();
        setStatuses(data);
      } catch (err) {
        setError('Failed to load statuses');
      }
    }
    fetchStatuses();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      
      var data = {
        name: name,
        description: description,
        amount: amount,
        status: status,
        due_date: dueDate
      };
      var newItem = await api.deliverables.create(milestoneId, data);

      setSuccess('Deliverable created successfully!');
      window.location.href = `/deliverables/${newItem.id}`;
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
              <Form.Label>Description</Form.Label>
              <Form.Control
                  as="textarea"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  required
              />
          </Form.Group>
          <Form.Group className="mb-3">
              <Form.Label>Status</Form.Label>
              <Form.Control
                as="select"
                value={status}
                onChange={(e) => setStatus(e.target.value)}
                required
                >
                  <option value="">Select Status</option>
                  {statuses.map((status) => (
                    <option key={status.name} value={status.name}>
                      {status.name}
                    </option>
                  ))}
                </Form.Control>
          </Form.Group>
          <Form.Group className="mb-3">
              <Form.Label>Amount</Form.Label>
              <NumericFormat
                  className="form-control"
                  value={amount}
                  thousandSeparator={true}
                  prefix={'$'}
                  onValueChange={(values) => {
                      const { value } = values;
                      setAmount(value);
                  }}
                  required
              />
          </Form.Group>
          <Form.Group className="mb-3">
              <Form.Label>Due Date</Form.Label>
              <Form.Control
                  type="date"
                  value={dueDate}
                  onChange={(e) => setDueDate(e.target.value)}
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