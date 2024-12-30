import React, { useState, useEffect } from 'react';
import { Form, Button, Modal } from 'react-bootstrap';
import { NumericFormat } from 'react-number-format';
import { useParams } from 'react-router-dom';
import api from '../../../../api/Api';

const EditSOW = () => {
  const { id } = useParams(); // Extract SOW ID from URL
  const [sowTitle, setSowTitle] = useState('');
  const [sowDocument, setSowDocument] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [budget, setBudget] = useState('');
  const [details, setDetails] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  useEffect(() => {
    // Fetch SOW data when component mounts
    const fetchSOW = async () => {
      try {
        const data = await api.sows.get(id);
        updateDisplay(data);
      } catch (err) {
        setError('Failed to load SOW data');
      }
    };
    fetchSOW();
  }, [id]);

  const updateDisplay = (data) => {
    setSowTitle(data.sow_title);
    setSowDocument(data.sow_document);
    setStartDate(data.start_date);
    setEndDate(data.end_date);
    setBudget(data.budget);
    setDetails(data.details ? JSON.stringify(data.details) : '');
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log(budget);
      var data = await api.sows.update(id, sowTitle, startDate, endDate, parseFloat(budget));
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
          <Form.Label>SOW Title</Form.Label>
          <Form.Control
            type="text"
            value={sowTitle}
            onChange={(e) => setSowTitle(e.target.value)}
            required
          />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Start Date</Form.Label>
          <Form.Control
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            required
          />
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>End Date</Form.Label>
          <Form.Control
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            required
          />
        </Form.Group>
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
        <Form.Group className="mb-3">
          <Form.Label>Document</Form.Label>
          <div className="d-flex">
            <Form.Control
              type="text"
              value={sowDocument}
              readOnly
              className="form-control-plaintext"
            />
            <a href={api.documents.getUrl(sowDocument)} target="_blank" rel="noreferrer">
              <i className="fas fa-download"></i>
            </a>
          </div>
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Details</Form.Label>
          <Form.Control
            as="textarea"
            value={details}
            onChange={(e) => setDetails(e.target.value)}
            readOnly
          />
        </Form.Group>
        <Button type="submit" variant="primary">
          <i className="fas fa-save"></i> Save
        </Button>
        <Button type="button" variant="secondary" className="ms-2" onClick={() => window.history.back()}>
          <i className="fas fa-times"></i> Cancel
        </Button>
      </Form>
    </div>
  );
};

export default EditSOW;