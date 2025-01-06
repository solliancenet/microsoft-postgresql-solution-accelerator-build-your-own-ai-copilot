import React, { useState } from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';
import { NumericFormat } from 'react-number-format';
import api from '../../api/Api';

const InvoiceCreate = () => {
  const [invoiceNumber, setInvoiceNumber] = useState('');
  const [amount, setAmount] = useState('');
  const [invoiceDate, setInvoiceDate] = useState('');
  const [paymentStatus, setPaymentStatus] = useState('');
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      var data = await api.invoice.create(file, invoiceNumber, amount, invoiceDate, paymentStatus);
      setSuccess('MSA created successfully!');
      window.location.href = `/invoices/${data.id}`;
      setError(null);
    } catch (err) {
      console.error(err);
      setError('Failed to create Invoice');
      setSuccess(null);
    }
  };

  return (
    <div>
      <h1>Create Invoice</h1>
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
          <Form.Label>Invoice Number</Form.Label>
          <Form.Control
            type="text"
            value={invoiceNumber}
            onChange={(e) => setInvoiceNumber(e.target.value)}
            required
          />
        </Form.Group>
        <Row className="mb-3">
          <Col md={6}>
            <Form.Group className="mb-3">
              <Form.Label>Amount</Form.Label>
              <Form.Control
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                required
                />
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group className="mb-3">
              <Form.Label>Payment Status</Form.Label>
              <Form.Control
                type="text"
                value={paymentStatus}
                onChange={(e) => setPaymentStatus(e.target.value)}
                required
              />
            </Form.Group>
          </Col>
        </Row>
        <Button type="submit" variant="primary">
          <i className="fas fa-plus"></i> Create
        </Button>
        <Button type="button" variant="secondary" className="ms-2" onClick={() => window.location.href = '/invoices' }>
          <i className="fas fa-times"></i> Cancel
        </Button>
      </Form>
    </div>
  );
};

export default InvoiceCreate;