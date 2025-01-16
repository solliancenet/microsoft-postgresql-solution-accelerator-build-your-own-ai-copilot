import React, { useState, useEffect } from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';
import { NumericFormat } from 'react-number-format';
import api from '../../api/Api';

const SOWCreate = () => {
  const [sowNumber, setSowNumber] = useState('');
  const [msaId, setMsaId] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [budget, setBudget] = useState('');
  const [metadata, setMetadata] = useState('');
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const [msas, setMsas] = useState([]);

  useEffect(() => {
    const fetchMsas = async () => {
      try {
        const data = await api.msas.list(-1, 0, -1); // No pagination limit
        setMsas(data.data);
      } catch (err) {
        console.error(err);
        setError('Error fetching MSAs');
        setSuccess(null);
      }
    };

    fetchMsas();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      var data = await api.sows.create(file, sowNumber, msaId, startDate, endDate, parseFloat(budget), metadata);
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
          <Form.Label>SOW Number</Form.Label>
          <Form.Control
            type="text"
            value={sowNumber}
            onChange={(e) => setSowNumber(e.target.value)}
            required
          />
        </Form.Group>
        <Form.Group>
          <Form.Label>MSA</Form.Label>
          <Form.Control
            as="select"
            value={msaId}
            onChange={(e) => setMsaId(e.target.value)}
            required
          >
            <option value="">Select MSA</option>
            {msas.map((msa) => (
              <option key={msa.id} value={msa.id}>
                {msa.title}
              </option>
            ))}
          </Form.Control>
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