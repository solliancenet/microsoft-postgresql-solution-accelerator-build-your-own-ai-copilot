import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../../api/Api';
import { Button } from 'react-bootstrap';
import ConfirmModal from '../../components/ConfirmModal'; 
import PagedTable from '../../components/PagedTable';

const MilestoneList = () => {
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [milestoneToDelete, setMilestoneToDelete] = useState(null);
    const [reload, setReload] = useState(false);
    
    const handleDelete = async () => {
        if (!milestoneToDelete) return;
    
        try {
        await api.milestones.delete(milestoneToDelete);
        setSuccess('Milestone deleted successfully!');
        setError(null);
        setShowDeleteModal(false);
        setReload(true); // Refresh the data
        } catch (err) {
        setSuccess(null);
        setError(err.message);
        }
    }
    
    const columns = React.useMemo(
        () => [
        {
            Header: 'Milestone Name',
            accessor: 'milestone_name',
        },
        {
            Header: 'SOW ID',
            accessor: 'sow_id',
        },
        {
            Header: 'Milestone Status',
            accessor: 'milestone_status',
        },
        {
            Header: 'Due Date',
            accessor: 'due_date',
        },
        {
            Header: 'Actions',
            accessor: 'id',
            Cell: ({ value }) => {
            return (
                <div>
                <Link to={`/milestones/edit/${value}`}>
                    <Button variant="primary" size="sm" className="mr-2">
                    Edit
                    </Button>
                </Link>
                <Button
                    variant="danger"
                    size="sm"
                    onClick={() => {
                    setMilestoneToDelete(value);
                    setShowDeleteModal(true);
                    }}
                >
                    Delete
                </Button>
                </div>
            );
            }
        },
        ],
        []
    );

    const fetchData = async (skip, limit, sortBy, search) => {
        const response = await api.milestones.list(skip, limit, sortBy, search);
        return response;
    };

    return (
        <div>
          <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
            <h1 className="h2">Milestones</h1>
            <Link to="/milestones/create" className="btn btn-primary">New <i className="fas fa-plus" /></Link>
          </div>
          {error && <div className="alert alert-danger">{error}</div>}
          {success && <div className="alert alert-success">{success}</div>}
    
          <PagedTable columns={columns} fetchData={fetchData} reload={reload} />
    
          <ConfirmModal
            show={showDeleteModal}
            handleClose={() => setShowDeleteModal(false)}
            handleConfirm={handleDelete}
            message="Are you sure you want to delete this Milestone?"
          />
        </div>
      );
    };
    
    export default MilestoneList;