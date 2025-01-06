import React, { useState, useEffect } from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';
import { NumericFormat } from 'react-number-format';
import { useParams } from 'react-router-dom';
import api from '../../api/Api';

const MSAEdit = () => {
  const { id } = useParams(); // Extract MSA ID from URL
  const [msaTitle, setMsaTitle] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [msaDocument, setMsaDocument] = useState('');
  const [additionalInfo, setAdditionalInfo] = useState('');
  const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
  
    useEffect(() => {
      // Fetch data when component mounts
      const fetchData = async () => {
        try {
          const data = await api.msas.get(id);
          updateDisplay(data);
        } catch (err) {
          setError('Failed to load MSA data');
        }
      };
      fetchData();
    }, [id]);
  
    const updateDisplay = (data) => {
      setMsaTitle(data.msa_title);
      setStartDate(data.start_date);
      setEndDate(data.end_date);
      setMsaDocument(data.msa_document);
      setAdditionalInfo(data.additional_info ? JSON.stringify(data.additional_info) : '');
    }
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      try {
        var data = await api.msas.update(id, msaTitle, startDate, endDate);
        updateDisplay(data);
        setSuccess('MSA updated successfully!');
        setError(null);
      } catch (err) {
        console.error(err);
        setError('Failed to update MSA');
        setSuccess(null);
      }
    };

  return (
    <div>
      <h1>Edit MSA</h1>
      <hr/>
      {error && <div className="alert alert-danger">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Title</Form.Label>
          <Form.Control
            type="text"
            value={msaTitle}
            onChange={(e) => setMsaTitle(e.target.value)}
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
          <Form.Label>Document</Form.Label>
          <div className="d-flex">
            <code>{msaDocument}</code>
            <a href={api.documents.getUrl(msaDocument)} target="_blank" rel="noreferrer">
              <i className="fas fa-download ms-3"></i>
            </a>
          </div>
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Details</Form.Label>
          <Form.Control
            as="textarea"
            value={additionalInfo}
            onChange={(e) => setAdditionalInfo(e.target.value)}
            style={{ height: '8em' }}
            readOnly
          />
        </Form.Group>
        <Button type="submit" variant="primary">
          <i className="fas fa-save"></i> Save
        </Button>
        <Button type="button" variant="secondary" className="ms-2" onClick={() => window.location.href = '/msas' }>
          <i className="fas fa-times"></i> Cancel
        </Button>
      </Form>
    </div>
  );
};

export default MSAEdit;