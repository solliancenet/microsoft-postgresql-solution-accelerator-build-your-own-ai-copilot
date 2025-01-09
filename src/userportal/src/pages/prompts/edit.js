import React, { useState, useEffect } from 'react';
import { Form, Button } from 'react-bootstrap';
import api from '../../api/Api';

const PromptEdit = () => {
    const [prompts, setPrompts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    useEffect(() => {
        // Fetch data when component mounts
        const fetchData = async () => {
        try {
            const data = await api.prompts.list();
            setPrompts(data)
            setLoading(false);
        } catch (err) {
            setError('Failed to load Prompt data');
        }
        };
        fetchData();
    }, []);

    const handleChange = (index, field, value) => {
        const newPrompts = [...prompts];
        newPrompts[index][field] = value;
        setPrompts(newPrompts);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
          await api.prompts.update(prompts);
          setSuccess('Prompts updated successfully!');
          setError(null);
        } catch (err) {
          console.error(err);
          setError('Failed to update Prompts');
          setSuccess(null);
        }
      };

    return (
    <div>
        <h1>Edit Prompts</h1>
        <hr/>
        {error && <div className="alert alert-danger">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}
        {loading && <div className="alert alert-info">Loading...</div>}
        <Form onSubmit={handleSubmit}>
        {prompts.map((prompt, index) => (
          <div key={prompt.id}>
            <Form.Group controlId={`promptText-${prompt.id}`} className="mb-3">
              <Form.Label>{prompt.name}</Form.Label>
              <Form.Control
                as="textarea"
                style={{ height: '12em' }}
                rows={3}
                value={prompt.prompt}
                onChange={(e) => handleChange(index, 'prompt', e.target.value)}
                required
                />
            </Form.Group>
          </div>
        ))}
        <Button type="submit" variant="primary">
            <i className="fas fa-save"></i> Save
        </Button>
        <Button type="button" variant="secondary" className="ms-2" onClick={() => window.location.href = '/msas' }>
            <i className="fas fa-times"></i> Cancel
        </Button>
        </Form>
    </div>
    );
};

export default PromptEdit;