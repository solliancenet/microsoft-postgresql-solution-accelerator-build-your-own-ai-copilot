import React, { useState, useEffect } from 'react';
import { Form, Button } from 'react-bootstrap';
import { NumericFormat } from 'react-number-format';
import { useParams } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import api from '../../api/Api';
import PagedTable from '../../components/PagedTable';
import ConfirmModel from '../../components/ConfirmModal';

const useQuery = () => {
  return new URLSearchParams(useLocation().search);
};

const InvoiceEdit = () => {
  const query = useQuery();
  const { id } = useParams(); // Extract Vendor ID from URL
  const [vendorId, setVendorId] = useState(0);
  const [sowId, setSowId] = useState('');
  const [invoiceNumber, setInvoiceNumber] = useState('');
  const [amount, setAmount] = useState('');
  const [invoiceDate, setInvoiceDate] = useState('');
  const [paymentStatus, setPaymentStatus] = useState('');
  const [document, setDocument] = useState('');
  const [metadata, setMetadata] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [showValidation, setShowValidation] = useState(false);

  const [showDeleteInvoiceLineItemModal, setShowDeleteInvoiceLineItemModal] = useState(false);
  const [reloadInvoiceLineItems, setReloadInvoiceLineItems] = useState(false);
  const [invoiceLineItemToDelete, setInvoiceLineItemToDelete] = useState(null);

  const [statuses, setStatuses] = useState([]);
  const [vendors, setVendors] = useState([]);
  const [sows, setSows] = useState([]);

  useEffect(() => {
    const message = query.get('success');
    if (message) {
      setSuccess(message);
    }
    const validation = query.get('showValidation');
    if (validation) {
      setShowValidation(true);
    }
  }, [query]);

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
  }, [id]);

  useEffect(() => {
    // Fetch SOWs when vendor changes
    const fetchSows = async () => {
      try {
        const data = await api.sows.list(vendorId, 0, -1); // No pagination limit
        setSows(data.data);
      } catch (err) {
        setError('Failed to load SOWs');
      }
    };
    fetchSows();
  }, [vendorId]);

  const updateDisplay = (data) => {
    setVendorId(data.vendor_id);
    setSowId(data.sow_id);
    setInvoiceNumber(data.number);
    setAmount(data.amount);
    setInvoiceDate(data.invoice_date);
    setPaymentStatus(data.payment_status);
    setDocument(data.document);
    setMetadata(data.metadata ? JSON.stringify(data.metadata, null, 2) : '');
  };

  const fetchInvoiceLineItems = async () => {
    try {
      const result = await api.invoiceLineItems.list(id, 0, -1); // No pagination limit
      setReloadInvoiceLineItems(false);
      return result;
    } catch (err) {
      console.error(err);
      setError('Failed to load Invoice Line Items');
      setSuccess(null);
    }
  };

  const invoiceLineItemsColumns = React.useMemo(
    () => [
      {
        Header: "Description",
        accessor: "description",
      },
      {
        Header: "Amount",
        accessor: "amount",
      },
      {
        Header: "Status",
        accessor: "status",
      },
      { 
        Header: "Due Date",
        accessor: "due_date",
      },
      {
        Header: "Actions",
        accessor: "actions",
        Cell: ({ row }) => {
          return (
            <div>
              <a href={`/invoice-line-items/${row.original.id}`} className="btn btn-link" aria-label="Edit">
                <i className="fas fa-edit"></i>
              </a>
              <Button
                variant="danger"
                size="sm"
                onClick={() => {
                  setInvoiceLineItemToDelete(row.original.id);
                  setShowDeleteInvoiceLineItemModal(true);
                }}
              >
                Delete
              </Button>
            </div>
          );
        },
      },
    ],
    []
  );

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      var data = {
        vendor_id: vendorId,
        sow_id: sowId,
        number: invoiceNumber,
        amount: amount,
        invoice_date: invoiceDate,
        payment_status: paymentStatus
      };
      var updatedItem = await api.invoices.update(id, data);
      
      updateDisplay(updatedItem);
      setSuccess('Invoice updated successfully!');
      setError(null);
    } catch (err) {
      console.error(err);
      setError('Failed to update Invoice');
      setSuccess(null);
    }
  };

  const handleDeleteInvoiceLineItem = async () => {
    try {
      await api.invoiceLineItems.delete(invoiceLineItemToDelete);
      setReloadInvoiceLineItems(true);
      setShowDeleteInvoiceLineItemModal(false);
    } catch (err) {
      console.error(err);
      setError('Failed to delete Invoice Line Item');
    }
  }

  return (
    <div>
      <h1>Edit Invoice</h1>
      <hr/>
      {error && <div className="alert alert-danger">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}
      <Form onSubmit={handleSubmit}>
        <Form.Group>
          <Form.Label>Vendor</Form.Label>
          <Form.Control
            as="select"
            value={vendorId}
            onChange={(e) => setVendorId(e.target.value)}
            required
            disabled={vendors.length === 0}
          >
            {vendors.length === 0 ? (
              <option value="">Loading Vendors...</option>
            ) : (
              <option value="">Select Vendor</option>
            )}
            {vendors.map((vendor) => (
              <option key={vendor.id} value={vendor.id}>
                {vendor.name}
              </option>
            ))}
          </Form.Control>
        </Form.Group>
        <Form.Group>
          <Form.Label>SOW</Form.Label>
          <Form.Control
            as="select"
            value={sowId}
            onChange={(e) => setSowId(e.target.value)}
            required
            disabled={sows.length === 0}
          >
            {sows.length === 0 ? (
              <option value="">Loading SOWs...</option>
            ) : (
              <option value="">Select SOW</option>
            )}
            {sows.map((sow) => (
              <option key={sow.id} value={sow.id}>
                {sow.number}
              </option>
            ))}
          </Form.Control>
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
        <Form.Group className="mb-3">
          <Form.Label>Invoice Date</Form.Label>
          <Form.Control
            type="date"
            value={invoiceDate}
            onChange={(e) => setInvoiceDate(e.target.value)}
            required
          />
        </Form.Group>
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
        <a href={`/vendors/${vendorId}`} className="btn btn-link ms-2">
          Go to Vendor
        </a>
      </Form>

      <hr />
      <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h2 className="h2">Line Items</h2>
        <Button variant="primary" onClick={() => window.location.href = `/invoice-line-items/create/${id}`}>
          New Line Item<i className="fas fa-plus" />
        </Button>
      </div>

      <PagedTable columns={invoiceLineItemsColumns}
        fetchData={fetchInvoiceLineItems}
        reload={reloadInvoiceLineItems}
        showPagination={false}
        />

      <ConfirmModel
        show={showDeleteInvoiceLineItemModal}
        handleClose={() => setShowDeleteInvoiceLineItemModal(false)}
        handleConfirm={handleDeleteInvoiceLineItem}
        title="Delete Invoice Line Item"
        message="Are you sure you want to delete this Invoice Line Item?"
        />

    </div>
  );
};

export default InvoiceEdit;