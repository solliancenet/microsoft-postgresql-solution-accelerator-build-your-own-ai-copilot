import React, { useState, useEffect } from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';
import { NumericFormat } from 'react-number-format';
import { useParams } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import api from '../../api/Api';
import ConfirmModal from '../../components/ConfirmModal';
import PagedTable from '../../components/PagedTable';
import ReactMarkdown from 'react-markdown';

const useQuery = () => {
  return new URLSearchParams(useLocation().search);
};

const SOWEdit = () => {
  const query = useQuery();
  const { id } = useParams(); // Extract SOW ID from URL
  const [sowNumber, setSowNumber] = useState('');
  const [sowVendorId, setSowVendorId] = useState('');
  const [sowDocument, setSowDocument] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [budget, setBudget] = useState('');
  const [metadata, setMetadata] = useState('');
  const [summary, setSummary] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [showValidation, setShowValidation] = useState(false);

  const [vendors, setVendors] = useState([]);
  const [validations, setValidations] = useState([]);

  const [showDeleteMilestoneModal, setShowDeleteMilestoneModal] = useState(false);
  const [milestoneToDelete, setMilestoneToDelete] = useState(null);
  const [reloadMilestones, setReloadMilestones] = useState(false);

  useEffect(() => {
    const message = query.get('success');
    if (message) {
      setSuccess(message);
    }
    const validation = query.get('showValidation');
    if (validation) {
      setShowValidation(true);
    }
  }, [useLocation().search]);

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

      const fetchValidations = async () => {
        try {
          const data = await api.validationResults.sow(id);
          setValidations(data.data);
        } catch (err) {
          console.error(err);
          setError('Error fetching Validations');
          setSuccess(null);
        }
      };
      fetchValidations();
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
    setSowVendorId(data.vendor_id);
    setSowDocument(data.document);
    setStartDate(data.start_date);
    setEndDate(data.end_date);
    setBudget(data.budget);
    setMetadata(data.metadata ? JSON.stringify(data.metadata, null, 2) : '');
    setSummary(data.summary);
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      var data = {
        number: sowNumber,
        vendor_id: sowVendorId,
        start_date: startDate,
        end_date: endDate,
        budget: parseFloat(budget)
      };
      var updatedItem = await api.sows.update(id, data);

      updateDisplay(updatedItem);
      setSuccess('SOW updated successfully!');
      setError(null);
    } catch (err) {
      console.error(err);
      setError('Failed to update SOW');
      setSuccess(null);
    }
  };

  const handleDeleteMilestone = async () => {
    try {
      await api.milestones.delete(milestoneToDelete);
      setSuccess('Milestone deleted successfully!');
      setError(null);
      setShowDeleteMilestoneModal(false);
      setReloadMilestones(true);
    } catch (err) {
      setSuccess(null);
      setError(err.message);
    }
  };

  const milestoneColumns = React.useMemo(
    () => [
      {
        Header: 'Name',
        accessor: 'name',
      },
      {
        Header: 'Due Date',
        accessor: 'due_date',
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
              <a href={`/milestones/${row.original.id}`} className="btn btn-link" aria-label="Edit">
                <i className="fas fa-edit"></i>
              </a>
              <Button
                variant="danger"
                size="sm"
                onClick={() => {
                  setMilestoneToDelete(row.original.id);
                  setShowDeleteMilestoneModal(true);
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

  const fetchMilestones = async () => {
    try {
      const data = await api.milestones.list(id, 0, -1); // No pagination limit
      setReloadMilestones(false);
      return data;
    } catch (err) {
      console.error(err);
      setError('Error fetching milestones');
      setSuccess(null);
    }
  };
  
  const runManualValidation = async () => {
      try {
        await api.sows.validate(id);
        window.location.href = `/sows/${id}?showValidation=true`;
      }
      catch (err) {
        console.error(err);
        setError('Manual validation failed!');
      }
    };

  return (
    <div>
      <h1>Edit SOW</h1>
      <hr/>
      {error && <div className="alert alert-danger">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}
      <Form onSubmit={handleSubmit}>
        <Row>
          <Col>
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
          </Col>
          <Col>
            <Form.Group className="mb-3">
              <Form.Label>SOW</Form.Label>
              <Form.Control
                type="text"
                value={sowNumber}
                onChange={(e) => setSowNumber(e.target.value)}
                required
              />
            </Form.Group>
          </Col>  
        </Row>
        <Row>
          <Col>
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
          <Col>
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
          <Col>
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
            <code>{sowDocument}</code>
            <a href={api.documents.getUrl(sowDocument)} target="_blank" rel="noreferrer">
              <i className="fas fa-download ms-3"></i>
            </a>
          </div>
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>Summary</Form.Label>
          <Form.Control
            as="textarea"
            value={summary}
            onChange={(e) => setSummary(e.target.value)}
            style={{ height: '8em' }}
            required
            disabled
          />
        </Form.Group>
        {/* <Form.Group className="mb-3">
          <Form.Label>Metadata</Form.Label>
          <Form.Control
            as="textarea"
            value={metadata}
            onChange={(e) => setMetadata(e.target.value)}
            style={{ height: '8em' }}
            readOnly
          />
        </Form.Group> */}
        <Button type="submit" variant="primary">
          <i className="fas fa-save"></i> Save
        </Button>
        <Button type="button" variant="secondary" className="ms-2" onClick={() => window.location.href = '/sows' }>
          <i className="fas fa-times"></i> Cancel
        </Button>
        <a href={`/vendors/${sowVendorId}`} className="btn btn-link ms-2">
          Go to Vendor
        </a>
      </Form>

      <hr />

      <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h2 className="h2">Milestones</h2>
        <Button variant="primary" onClick={() => window.location.href = `/milestones/create/${id}`}>
          New Milestone <i className="fas fa-plus" />
        </Button>
      </div>

      <PagedTable columns={milestoneColumns}
        fetchData={fetchMilestones}
        reload={reloadMilestones}
        showPagination={false}
        />

      <ConfirmModal
        show={showDeleteMilestoneModal}
        handleClose={() => setShowDeleteMilestoneModal(false)}
        handleConfirm={handleDeleteMilestone}
        title="Delete Milestone"
        message="Are you sure you want to delete this milestone?"
      />

    <hr />

    <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
      <h2 className="h2">Validations</h2>
      <Button variant="primary" onClick={() => runManualValidation()}>
        Run Manual Validation<i className="fas fa-gear" />
      </Button>
    </div>

    <table className="table">
      <thead>
        <tr role="row">
          <th colspan="1" role="columnheader">Passed?</th>
          <th colspan="1" role="columnheader">Timestamp</th>
          <th colspan="1" role="columnheader">Result</th>
        </tr>
      </thead>
      <tbody>
        {validations.length === 0 && (
          <tr>
            <td colspan="3">No validations found</td>
            </tr>
              )}
        {validations.map((validation) => (
          <tr key={validation.id}>
            <td>{validation.validation_passed ? <span><i className="fas fa-check-circle text-success"></i> Passed</span> : <span><i className="fas fa-times-circle text-danger"></i> Failed</span>}</td>
            <td>{validation.datestamp}</td>
            <td>
              <div style={{ height: '12em', overflowY: 'scroll', border: '0.1em #ccc solid' }}>
                <ReactMarkdown>{validation.result}</ReactMarkdown>
              </div>
            </td>
          </tr>
        ))}
      </tbody>
    </table>

      {showValidation && validations && validations.length > 0 && (
        <>
        <div className="blur-overlay"></div>
        <div className="modal show d-block" tabIndex="-1" role="dialog">
          <div className="modal-dialog" role="document">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Validation Result: {validations[0].validation_passed ? <span><i className="fas fa-check-circle text-success"></i> Passed</span> : <span><i className="fas fa-times-circle text-danger"></i> Failed</span>}</h5>
              </div>
              <div className="modal-body">
                <div style={{ height: '20em', overflowY: 'scroll', border: '0.1em #ccc solid' }}>
                  <ReactMarkdown>{validations[0].result}</ReactMarkdown>
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setShowValidation(false)}>Close</button>
              </div>
            </div>
          </div>
        </div>
        </>
      )}

    </div>
  );
};

export default SOWEdit;