import React, { useState, useEffect } from 'react';
import { Form, Button } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
import { NumericFormat } from 'react-number-format';
import api from '../../api/Api';

const InvoiceLineItemEdit = () => {
    const { id } = useParams(); // Extract from URL
    const [invoiceId, setInvoiceId] = useState('');
    const [description, setDescription] = useState('');
    const [amount, setAmount] = useState('');
    const [status, setStatus] = useState('');
    const [dueDate, setDueDate] = useState('');
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    
    const [statuses, setStatuses] = useState([]);
    const [invoices, setInvoices] = useState([]);
    
    useEffect(() => {
        // Fetch data when component mounts
        const fetchData = async () => {
        try {
            const data = await api.invoiceLineItems.get(id);
            updateDisplay(data);
        } catch (err) {
            setError('Failed to load Invoice Line Item data');
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

        const fetchInvoices = async () => {
            try {
                const data = await api.invoices.list(-1, 0, -1); // Fetch all invoices
                setInvoices(data.data);
            } catch (err) {
                setError('Failed to load invoices');
            }
        };
        fetchInvoices();
    }, [id]);
    
    const updateDisplay = (data) => {
        setInvoiceId(data.invoice_id);
        setDescription(data.description);
        setAmount(data.amount);
        setStatus(data.status);
        setDueDate(data.due_date);
    };
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
        var data = {
            invoice_id: invoiceId,
            description: description,
            amount: amount,
            status: status,
            due_date: dueDate
        };
        await api.invoiceLineItems.update(id, data);
    
        setSuccess('Invoice Line Item updated successfully!');
        setError(null);
        } catch (err) {
        console.error(err);
        setError('Failed to update Invoice Line Item');
        setSuccess(null);
        }
    };
    
    return (
        <div>
        <h1>Edit Invoice Line Item</h1>
        <hr/>
        {error && <div className="alert alert-danger">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}
        <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
                <Form.Label>Invoice</Form.Label>
                <Form.Control
                as="select"
                value={invoiceId}
                onChange={(e) => setInvoiceId(e.target.value)}
                >
                <option value="">Select Invoice</option>
                {invoices.map((invoice) => (
                    <option key={invoice.id} value={invoice.id}>
                    {invoice.number}
                    </option>
                ))}
                </Form.Control>
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Description</Form.Label>
                <Form.Control
                type="text"
                placeholder="Enter description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Amount</Form.Label>
                <NumericFormat
                className="form-control"
                value={amount}
                onValueChange={(values) => {
                    const { formattedValue, value } = values;
                    setAmount(value);
                }}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Status</Form.Label>
                <Form.Control
                as="select"
                value={status}
                onChange={(e) => setStatus(e.target.value)}
                >
                <option value="">Select Status</option>
                {statuses.map((status) => (
                    <option key={status.id} value={status.id}>
                    {status.name}
                    </option>
                ))}
                </Form.Control>
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Due Date</Form.Label>
                <Form.Control
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                />
            </Form.Group>

            <Button type="submit" variant="primary">
                <i className="fas fa-save"></i> Save
            </Button>
            <a href={`/invoices/${invoiceId}`} className="btn btn-secondary ms-2" aria-label="Cancel">
                <i className="fas fa-arrow-left"></i> Back to Invoice
            </a>
        </Form>
        </div>
    );
};

export default InvoiceLineItemEdit;
