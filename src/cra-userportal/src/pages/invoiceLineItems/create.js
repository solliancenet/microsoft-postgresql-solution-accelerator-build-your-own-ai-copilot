import React, { useState, useEffect } from 'react';
import { Form, Button } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
import { NumericFormat } from 'react-number-format';
import api from '../../api/Api';

const InvoiceLineItemCreate = () => {
  const { invoiceId } = useParams(); // Extract from URL
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
        invoice_id: invoiceId,
        description: description,
        amount: amount,
        status: status,
        due_date: dueDate
      };
      var newItem = await api.invoiceLineItems.create(data);

      setSuccess('Invoice Line Item created successfully!');
      window.location.href = `/invoice-line-items/${newItem.id}`;
      setError(null);
    } catch (err) {
      console.error(err);
      setError('Failed to create Invoice Line Item');
      setSuccess(null);
    }
  };

  return (
    <div>
      <h1>Create Invoice Line Item</h1>
      <hr/>
      {error && <div className="alert alert-danger">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}
      <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-3">
            <Form.Label>Description</Form.Label>
            <Form.Control
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
            />
        </Form.Group>
        <Form.Group className="mb-3">
            <Form.Label>Amount</Form.Label>
            <NumericFormat
              className="form-control"
              value={amount}
              onValueChange={(values) => {
                const { formattedValue, value } = values;
                setAmount(value);
              }}
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
        <a href={`/invoices/${invoiceId}`} className="btn btn-secondary ms-2" aria-label="Cancel">
          <i className="fas fa-arrow-left"></i> Back to Invoice
        </a>
      </Form>
    </div>
  );
};

export default InvoiceLineItemCreate;