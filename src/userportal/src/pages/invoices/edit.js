import React, { useState, useEffect } from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';
import { NumericFormat } from 'react-number-format';
import { useParams } from 'react-router-dom';
import api from '../../api/Api';

const InvoiceEdit = () => {
  const { id } = useParams(); // Extract MSA ID from URL
  const [invoiceNumber, setInvoiceNumber] = useState('');
  const [amount, setAmount] = useState('');
  const [invoiceDate, setInvoiceDate] = useState('');
  const [paymentStatus, setPaymentStatus] = useState('');
  const [document, setDocument] = useState('');
  const [metadata, setMetadata] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const [statuses, setStatuses] = useState([]);
  
  useEffect(() => {
    // Fetch data when component mounts
    const fetchData = async () => {
      try {
        const data = await api.invoices.get(id);
        updateDisplay(data);
      } catch (err) {
        setError('Failed to load Invoice data');
      }
    };
    fetchData();

    const fetchStatuses = async () => {
      try {
        const data = await api.statuses.list();
        setStatuses(data);
      } catch (err) {
        setError('Failed to load statuses');
      }
    }
    fetchStatuses();
  }, [id]);

  const updateDisplay = (data) => {
    setInvoiceNumber(data.number);
    setAmount(data.amount);
    setInvoiceDate(data.invoice_date);
    setPaymentStatus(data.payment_status);
    setMetadata(data.metadata ? JSON.stringify(data.metadata, null, 2) : '');
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      var data = await api.invoices.update(id, invoiceNumber, amount, invoiceDate, paymentStatus);
      updateDisplay(data);
      setSuccess('Invoice updated successfully!');
      setError(null);
    } catch (err) {
      console.error(err);
      setError('Failed to update Invoice');
      setSuccess(null);
    }
  };

  return (
    <div>
      <h1>Edit Invoice</h1>
      <hr/>
      {error && <div className="alert alert-danger">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Invoice Number</Form.Label>
          <Form.Control
            type="text"
            value={invoiceNumber}
            onChange={(e) => setInvoiceNumber(e.target.value)}
            required
          />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Amount</Form.Label>
          <NumericFormat
            className="form-control"
            value={amount}
            onValueChange={(values) => setAmount(values.floatValue)}
            thousandSeparator={true}
            prefix={'$'}
            required
          />
        </Form.Group>
        <Row className="mb-3">
          <Col md={6}>
            <Form.Group className="mb-3">
              <Form.Label>Invoice Date</Form.Label>
              <Form.Control
                type="date"
                value={invoiceDate}
                onChange={(e) => setInvoiceDate(e.target.value)}
                required
              />
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group className="mb-3">
              <Form.Label>Payment Status</Form.Label>
              <Form.Control
                as="select"
                value={paymentStatus}
                onChange={(e) => setPaymentStatus(e.target.value)}
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
          </Col>
        </Row>
        <Form.Group className="mb-3">
          <Form.Label>Document</Form.Label>
          <div className="d-flex">
            <code>{document}</code>
            <a href={api.documents.getUrl(document)} target="_blank" rel="noreferrer">
              <i className="fas fa-download ms-3"></i>
            </a>
          </div>
        </Form.Group>
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
        <Button type="button" variant="secondary" className="ms-2" onClick={() => window.location.href = '/invoices' }>
          <i className="fas fa-times"></i> Cancel
        </Button>
      </Form>
    </div>
  );
};

export default InvoiceEdit;