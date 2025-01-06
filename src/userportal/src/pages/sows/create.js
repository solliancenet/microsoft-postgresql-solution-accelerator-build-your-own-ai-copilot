import React, { useState } from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';
import { NumericFormat } from 'react-number-format';
import api from '../../api/Api';

const SOWCreate = () => {
  const [sowTitle, setSowTitle] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [budget, setBudget] = useState('');
  const [details, setDetails] = useState('');
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      var data = await api.sows.create(file, sowTitle, startDate, endDate, parseFloat(budget), details);
      setSuccess('SOW created successfully!');
      window.location.href = `/sows/${data.id}`;
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
        <Form.Group className="mb-3">
          <Form.Label>SOW Title</Form.Label>
          <Form.Control
            type="text"
            value={sowTitle}
            onChange={(e) => setSowTitle(e.target.value)}
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