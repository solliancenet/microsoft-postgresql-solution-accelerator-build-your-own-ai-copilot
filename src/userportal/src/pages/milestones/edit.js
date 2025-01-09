import React, { useState, useEffect } from 'react';
import { Form, Button } from 'react-bootstrap';
import { NumericFormat } from 'react-number-format';
import { useParams } from 'react-router-dom';
import api from '../../api/Api';
import ConfirmModal from '../../components/ConfirmModal';
import PagedTable from '../../components/PagedTable';

const MilestoneEdit = () => {
    const { id } = useParams(); // Extract ID from URL
    const [sowId, setSowId] = useState('');
    const [name, setName] = useState('');
    const [status, setStatus] = useState('');
    const [dueDate, setDueDate] = useState('');
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const [showDeleteDeliverableModal, setShowDeleteDeliverableModal] = useState(false);
    const [deliverableToDelete, setDeliverableToDelete] = useState(null);
    const [reloadDeliverables, setReloadDeliverables] = useState(false);

    const [statuses, setStatuses] = useState([]);


    useEffect(() => {
        // Fetch data when component mounts
        const fetchData = async () => {
            try {
                const data = await api.milestones.get(id);
                updateDisplay(data);
            } catch (err) {
                console.error(err);
                setError('Failed to load Milestone data');
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
        setSowId(data.sow_id);
        setName(data.name);
        setStatus(data.status);
        setDueDate(data.due_date);
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            var data = await api.milestones.update(id, name, status, dueDate);
            updateDisplay(data);
            setSuccess('Milestone updated successfully!');
            setError(null);
        } catch (err) {
            console.error(err);
            setError('Failed to update Milestone');
            setSuccess(null);
        }
    };

    const handleDeleteDeliverable = async () => {
        try {
            await api.deliverables.delete(deliverableToDelete);
            setSuccess('Deliverable deleted successfully!');
            setError(null);
            setShowDeleteDeliverableModal(false);
            setReloadDeliverables(true);
        } catch (err) {
            setSuccess(null);
            setError(err.message);
        }
    }

    const deliverableColumns = React.useMemo(
        () => [
            {
            Header: 'Name',
            accessor: 'name',
            },
            {
            Header: 'Description',
            accessor: 'description',
            },
            {
            Header: 'Amount',
            accessor: 'amount',
            },
            {
            Header: 'Status',
            accessor: 'status',
            },
            {
            Header: 'Actions',
            accessor: 'actions',
            Cell: ({ row }) => {
                return (
                <div>
                    <a href={`/deliverables/${row.original.id}`} className="btn btn-link" aria-label="Edit">
                        <i className="fas fa-edit"></i>
                    </a>
                    <Button
                    variant="danger"
                    size="sm"
                    onClick={() => {
                        setDeliverableToDelete(row.original.id);
                        setShowDeleteDeliverableModal(true);
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

    const fetchDeliverables = async () => {
        try {
            const data = await api.deliverables.list(id, 0, -1); // No pagination limit
            return data;
        } catch (err) {
            console.error(err);
            setError('Error fetching milestones');
            setSuccess(null);
        }
    }

    return (
    <div>
        <h1>Edit Milestone</h1>
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
                <Form.Label>Due Date</Form.Label>
                <Form.Control
                    type="date"
                    value={dueDate}
                    onChange={(e) => setDueDate(e.target.value)}
                    required
                />
            </Form.Group>
            <Button type="submit" variant="primary">
                <i className="fas fa-save"></i> Save
            </Button>
            <a href={`/sows/${sowId}`} className="btn btn-secondary ms-2" aria-label="Edit">
                <i className="fas fa-arrow-left"></i> Back to SOW
            </a>
        </Form>

        <hr />

        <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
            <h2 className="h2">Deliverables</h2>
            <Button variant="primary" onClick={() => window.location.href = `/deliverables/create/${id}`}>
                New Deliverable <i className="fas fa-plus" />
            </Button>
        </div>

        <PagedTable columns={deliverableColumns}
            fetchData={fetchDeliverables}
            reload={reloadDeliverables}
            showPagination={false}
        />

        <ConfirmModal
        show={showDeleteDeliverableModal}
        handleClose={() => setShowDeleteDeliverableModal(false)}
        handleConfirm={handleDeleteDeliverable}
        title="Delete Deliverable"
        message="Are you sure you want to delete this deliverable?"
        />
    </div>
    );
};

export default MilestoneEdit;