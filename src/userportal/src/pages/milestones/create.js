import React, { useState, useEffect } from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
import api from '../../api/Api';

const MilestoneCreate = () => {
  const { sowId } = useParams(); // Extract from URL
  const [name, setName] = useState('');
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
        sow_id: sowId,
        name: name,
        status: status,
        due_date: dueDate
      };
      var newItem = await api.milestones.create(data);

      setSuccess('Milestone created successfully!');
      window.location.href = `/milestones/${newItem.id}`;
      setError(null);
    } catch (err) {
      console.error(err);
      setError('Failed to create Milestone');
      setSuccess(null);
    }
  };

  return (
    <div>
      <h1>Create Milestone</h1>
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
        <a href={`/sows/${sowId}`} className="btn btn-secondary ms-2" aria-label="Cancel">
          <i className="fas fa-arrow-left"></i> Back to Sow
        </a>
      </Form>
    </div>
  );
};

export default MilestoneCreate;