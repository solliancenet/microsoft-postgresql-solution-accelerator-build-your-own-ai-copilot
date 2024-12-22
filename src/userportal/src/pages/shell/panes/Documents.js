// src/Documents.js
import React, { useEffect, useState } from 'react';
import api from '../../../api/Api'; // Adjust the path as necessary

import { Table, Button, Modal, Form } from 'react-bootstrap';
import { useTable, useSortBy } from 'react-table';


const Documents = () => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [file, setFile] = useState(null);

  const fetchDocuments = async () => {
    try {
      const data = await api.documents.list();
      setDocuments(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchDocuments();
  }, []);


  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    try {
      await api.documents.upload(file);
      setShowModal(false);
      await fetchDocuments(); // Refresh the document list
    } catch (err) {
      setError(err.message);
    }
  };

  const columns = React.useMemo(
    () => [
      {
        Header: 'Filename',
        accessor: 'filename',
      },
      {
        Header: 'Content Type',
        accessor: 'content_type',
      },
      {
        Header: 'Created',
        accessor: 'created',
        Cell: ({ value }) => new Date(value).toLocaleString(),
      },
      {
        Header: '',
        accessor: 'blob_name',
        Cell: ({ value }) => (
          <a href={`${api.documents.getUrl(value)}`} target="_blank" rel="noopener noreferrer">Download</a>
        ),
      }
    ],
    []
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable({ columns, data: documents }, useSortBy);

  if (loading) {
    return <p>Loading documents...</p>;
  }

  if (error) {
    return <p>Error loading documents: {error}</p>;
  }

  return (
    <div>
      <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
        <h1 className="h2">Documents</h1>
        <Button variant="primary" onClick={() => setShowModal(true)}>Upload</Button>
      </div>
      <Table striped bordered hover {...getTableProps()}>
        <thead>
          {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map(column => (
                <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                  {column.render('Header')}
                  <span>
                    {column.isSorted
                      ? column.isSortedDesc
                        ? ' 🔽'
                        : ' 🔼'
                      : ''}
                  </span>
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map(row => {
            prepareRow(row);
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map(cell => {
                  return <td {...cell.getCellProps()}>{cell.render('Cell')}</td>;
                })}
              </tr>
            );
          })}
        </tbody>
      </Table>

      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Upload Document</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
          <Form.Group>
              <Form.Label>Choose document</Form.Label>
              <Form.Control type="file" onChange={handleFileChange} />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>Close</Button>
          <Button variant="primary" onClick={handleUpload}>Upload</Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default Documents;