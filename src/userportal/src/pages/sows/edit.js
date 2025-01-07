import React, { useState, useEffect } from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';
import { NumericFormat } from 'react-number-format';
import { useParams } from 'react-router-dom';
import api from '../../api/Api';

const SOWEdit = () => {
  const { id } = useParams(); // Extract SOW ID from URL
  const [sowNumber, setSowNumber] = useState('');
  const [msaId, setMsaId] = useState('');
  const [sowDocument, setSowDocument] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [budget, setBudget] = useState('');
  const [metadata, setMetadata] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const [msas, setMsas] = useState([]);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await api.msas.list(0, -1); // No pagination limit
        setMsas(data.data);
      } catch (err) {
        console.error(err);
        setError('Error fetching MSAs');
        setSuccess(null);
      }
    };

    fetchData();
  }, [id]);

  useEffect(() => {
    // Fetch data when component mounts
    const fetchData = async () => {
      try {
        const data = await api.sows.get(id);
        updateDisplay(data);
      } catch (err) {
        console.error(err);
        setError('Failed to load SOW data');
      }
    };
    fetchData();
  }, [id]);

  const updateDisplay = (data) => {
    setSowNumber(data.number);
    setMsaId(data.msa_id);
    setSowDocument(data.document);
    setStartDate(data.start_date);
    setEndDate(data.end_date);
    setBudget(data.budget);
    setMetadata(data.metadata ? JSON.stringify(data.metadata) : '');
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      var data = await api.sows.update(id, sowNumber, msaId, startDate, endDate, parseFloat(budget));
      updateDisplay(data);
      setSuccess('SOW updated successfully!');
      setError(null);
    } catch (err) {
      console.error(err);
      setError('Failed to update SOW');
      setSuccess(null);
    }
  };

  return (
    <div>
      <h1>Edit SOW</h1>
      <hr/>
      {error && <div className="alert alert-danger">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}
      <Form onSubmit={handleSubmit}>
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
        <Row className="mb-3">
          <Col md={6}>
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
          </Col>
          <Col md={6}>
            <Form.Group className="mb-3">
              <Form.Label>Document</Form.Label>
              <div className="d-flex">
                <code>{sowDocument}</code>
                <a href={api.documents.getUrl(sowDocument)} target="_blank" rel="noreferrer">
                  <i className="fas fa-download ms-3"></i>
                </a>
              </div>
            </Form.Group>
          </Col>
        </Row>
        <Form.Group className="mb-3">
          <Form.Label>Details</Form.Label>
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
        <Button type="button" variant="secondary" className="ms-2" onClick={() => window.location.href = '/sows' }>
          <i className="fas fa-times"></i> Cancel
        </Button>
      </Form>
    </div>
  );
};

export default SOWEdit;