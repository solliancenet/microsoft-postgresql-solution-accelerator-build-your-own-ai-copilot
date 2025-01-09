import React, { useState, useEffect } from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';
import { NumericFormat } from 'react-number-format';
import { useParams } from 'react-router-dom';
import api from '../../api/Api';

const DeliverableEdit = () => {
    const { id } = useParams(); // Extract ID from URL
    const [milestoneId, setMilestoneId] = useState('');
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [amount, setAmount] = useState('');
    const [status, setStatus] = useState('');
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const [statuses, setStatuses] = useState([]);

    useEffect(() => {
        // Fetch data when component mounts
        const fetchData = async () => {
            try {
                const data = await api.deliverables.get(id);
                updateDisplay(data);
            } catch (err) {
                console.error(err);
                setError('Failed to load Deliverable data');
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
        setMilestoneId(data.milestone_id);
        setName(data.name);
        setDescription(data.description);
        setAmount(data.amount);
        setStatus(data.status);
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            var data = await api.deliverables.update(id, name, description, amount, status);
            updateDisplay(data);
            setSuccess('Deliverable updated successfully!');
            setError(null);
        } catch (err) {
            console.error(err);
            setError('Failed to update Deliverable');
            setSuccess(null);
        }
    };

    return (
    <div>
        <h1>Edit Deliverable</h1>
        <hr/>
        {error && <div className="alert alert-danger">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}
        <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
                <Form.Label>Name</Form.Label>
                <Form.Control
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Status</Form.Label>
                <Form.Control
                as="select"
                value={status}
                onChange={(e) => setStatus(e.target.value)}
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
                <Form.Label>Amount</Form.Label>
                <NumericFormat
                    className="form-control"
                    value={amount}
                    thousandSeparator={true}
                    prefix={'$'}
                    onValueChange={(values) => {
                        const { value } = values;
                        setAmount(value);
                    }}
                    required
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Description</Form.Label>
                <Form.Control
                    as="textarea"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    required
                />
            </Form.Group>
            <Button type="submit" variant="primary">
                <i className="fas fa-save"></i> Save
            </Button>
            <a href={`/milestones/${milestoneId}`} className="btn btn-secondary ms-2" aria-label="Cancel">
                <i className="fas fa-arrow-left"></i> Back to Milestone
            </a>
        </Form>
    </div>
    );
};

export default DeliverableEdit;