import React, { useState, useEffect } from 'react';
import { Form, Button, Spinner, Alert } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
import api from '../../api/Api';

const InvoiceCreate = () => {
  const { vendorId } = useParams();
  const [invoiceId, setInvoiceId]  = useState(0);
  const [invoiceVendorId, setInvoiceVendorId] = useState(vendorId);
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const [errorDetail, setErrorDetail] = useState(null);
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
        setErrorDetail(null);
        setSuccess(null);
      }
    };

    fetchVendors();
  }, []);

  const handleAnalyzeDocument = async (e) => {
    e.preventDefault();

    setShowUpload(false);
  
    var newInvoiceId = 0;
    try {
      setError(null);
      setErrorDetail(null);
      
      setLoading('Analyzing document with AI...');

      const result = await api.invoices.analyze(file, { vendor_id: invoiceVendorId });

      if (result.hasError) {
        setError(result.message);
        setErrorDetail(result.error);
        setShowUpload(true);
        setSuccess(null);
        setLoading(null);
        return false;
      }

      setInvoiceId(result.invoice.id);
      newInvoiceId = result.invoice.id

    } catch (err) {
      console.error(err);
      setShowUpload(true);
      setError('Error analyzing document');
      setErrorDetail(null);
      setSuccess(null);
      setLoading(null);
      return false;
    }

    try {
      setLoading('Validating document with AI...');     
      await api.invoices.validate(newInvoiceId);

    } catch (err) {
      console.error(err);
      // still continue on, since the Invoice is already created in the database
    }

    setError(null);
    const successMessage = "Invoice created successfully with fields populated by AI!";
    window.location.href = `/invoices/${newInvoiceId}?success=${successMessage}&showValidation=true`;
  };

  return (
    <div>
      <h1>Create Invoice</h1>
      <hr/>
      {error && <div className="alert alert-danger">
        <p>{error}</p>
          {errorDetail && (
            <p style={{ maxHeight: '10em', overflowY: 'scroll', backgroundColor: '#fff', padding: '0.3em', borderRadius: '0.3em' }} dangerouslySetInnerHTML={{ __html: (errorDetail || '').replace(/\n/g, '<br/>') }}></p>
          )}
        </div>}
      {success && <div className="alert alert-success">{success}</div>}

      {showUpload && (
        <>
      <Form onSubmit={handleAnalyzeDocument}>
        <Form.Group>
          <Form.Label>Vendor</Form.Label>
          <Form.Control
            as="select"
            value={vendorId}
            onChange={(e) => setInvoiceVendorId(e.target.value)}
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
        <Button type="button" variant="secondary" className="ms-2" onClick={() => window.location.href = '/invoices' }>
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

export default InvoiceCreate;