import React, { useState, useEffect } from 'react';
import { Form, Button, Spinner, Alert } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
import api from '../../api/Api';

const SOWCreate = () => {
  const { vendorId } = useParams();
  const [sowId, setSowId]  = useState(0);
  const [sowVendorId, setSowVendorId] = useState(vendorId);
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showUpload, setShowUpload] = useState(true);

  const [vendors, setVendors] = useState([]);


  useEffect(() => {
    const fetchVendors = async () => {
      try {
        const data = await api.vendors.list(0, -1); // No pagination limit
        setVendors(data.data);
      } catch (err) {
        console.error(err);
        setError('Error fetching Vendors');
        setSuccess(null);
      }
    };

    fetchVendors();
  }, []);

  const handleAnalyzeDocument = async (e) => {
    e.preventDefault();
    
    setShowUpload(false);

    try {
      setLoading('Analyzing document with AI...');

      const result = await api.sows.analyze(file, { vendor_id: sowVendorId });
      setSowId(result.id);

    } catch (err) {
      console.error(err);
      setShowUpload(true);
      setError('Error analyzing document');
      setSuccess(null);
      setLoading(null);
      return false;
    }

    try {
      setLoading('Validating document with AI...');
      await api.sows.validate(sowId);
      
    } catch (err) {
      console.error(err);
      // still continue on, since the SOW is already created in the database
    }

    setError(null);
    const successMessage = "SOW created successfully with fields populated by AI!"
    window.location.href = `/sows/${sowId}?success=${successMessage}&showValidation=true`;
  };

  return (
    <div>
      <h1>Create SOW</h1>
      <hr/>
      {error && <div className="alert alert-danger">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      {showUpload && (
          <>
        <Form onSubmit={handleAnalyzeDocument}>
          <Form.Group>
            <Form.Label>Vendor</Form.Label>
            <Form.Control
              as="select"
              value={sowVendorId}
              onChange={(e) => setSowVendorId(e.target.value)}
              required
            >
              <option value="">Select Vendor</option>
              {vendors.map((vendor) => (
                <option key={vendor.id} value={vendor.id}>
                  {vendor.name}
                </option>
              ))}
            </Form.Control>
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Document</Form.Label>
            <Form.Control
              type="file"
              onChange={(e) => setFile(e.target.files[0])}
              required
            />
          </Form.Group>
          <Button type="submit" variant="primary">
            <i className="fas fa-search"></i> Analyze Document
          </Button>
          <Button type="button" variant="secondary" className="ms-2" onClick={() => window.location.href = '/sows' }>
            <i className="fas fa-times"></i> Cancel
          </Button>
        </Form>
      </>
      )}

      {loading && (
      <Alert variant="info" className="mt-3 p-5 text-center">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">{loading}</span>
        </Spinner>
        <div>{loading}</div>
      </Alert>
      )}
    </div>
  );
};

export default SOWCreate;