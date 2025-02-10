import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { Row, Col, Button, OverlayTrigger, Tooltip } from 'react-bootstrap';
import ConfirmModal from './ConfirmModal'; 
import api from '../api/Api'; // Adjust the path as necessary
import './CopilotChat.css';

const CopilotChat = () => {
  const [sessionId, setSessionId] = useState(-1);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);
  const [error, setError] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  
  const [sessions, setSessions] = useState([]);
  const [sessionToDelete, setSessionToDelete] = useState(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  const handleSendMessage = async () => {
    if (input.trim() === '') return;

    const prompt = input;
    setInput('');

    setIsThinking(true);

    // Add the user's message to the local mesage history
    const userMessage = { role: 'user', content: prompt };
    setMessages([...messages, userMessage]);

    setError('');

    try {
      // Get the completion from the API
      const output = await api.completions.chat(sessionId, prompt);

      // make sure request for a different session doesn't update the messages
      if (sessionId === output.session_id) {
        // Add the assistant's response to the messages
        const assistantMessage = { role: 'assistant', content: output.content };
        setMessages([...messages, userMessage, assistantMessage]);
      }

      // only update the messages if the session ID is the same
      // This keeps a processing completion from updating messages after a new session is created
      if (sessionId === -1 || sessionId !== output.session_id) {
        // Update the session ID
        setSessionId(output.session_id);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setError('Error sending message. Please try again.');
    } finally {
        setIsThinking(false);
    }

  };

  const createNewSession = async () => {
    setSessionId(-1);
    setMessages([]);
    setIsThinking(false);
    setError('');
  };

  const refreshSessionList = async () => {
    try {
      const data = await api.completions.getSessions();
      setSessions(data);
    } catch (error) {
      console.error('Error loading session history:', error);
      setError('Error loading session history. Please try again.');
    }
  }

  const loadSessionHistory = async () => {
    if (!sessionId || sessionId <= 0) {
      setMessages([]);
      return;
    }
    try {
      const data = await api.completions.getHistory(sessionId);
      setMessages(data);
    } catch (error) {
      console.error('Error loading session history:', error);
      setError('Error loading session history. Please try again.');
    }
  }

  useEffect(() => {
    refreshSessionList();
    loadSessionHistory();
  }, [sessionId]);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  useEffect(() => {
    refreshSessionList();
  }, []);

  const handleDelete = async () => {
    if (!sessionToDelete) return;

    setError(null);
    try {
      await api.completions.deleteSession(sessionToDelete);

      console.log('Session deleted:', sessionToDelete);
      console.log('Current session:', sessionId);
      if (sessionId === sessionToDelete) {
        setSessionId(-1);
      }
    } catch (err) {
      console.error('Error deleting session:', err);
      setError('Error deleting session. Please try again.');
    }
    setShowDeleteModal(false);
    refreshSessionList();
  };

  return (
    <div className="ai-chat container mt-4">
      <Row>
        <Col style={{ width: '10%', maxWidth: '10em' }}>
          <Row>
            <Button area-label="New Session" alt="New Session" onClick={createNewSession}>
              <i className="fas fa-plus"></i> Session
            </Button>
          </Row>
          <Row className="mt-3">
            <strong>Chat History</strong>
            {!sessions || sessions.length === 0 && <p>No sessions</p>}
            {sessions && sessions.length > 0 && <ul className="session-list">
              {sessions.map((session, index) => (
                  <li key={index}
                    className={`session ${sessionId === session.id ? 'selected' : ''}`}
                    style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px', borderBottom: '1px solid #ccc', cursor: 'pointer' }}
                    onClick={() => setSessionId(session.id)}
                  >
                    <OverlayTrigger
                      placement="top"
                      delay={{ show: 250, hide: 400 }}
                      overlay={<Tooltip id={`tooltip-${index}`}>{session.name.substring(0, 300)}</Tooltip>}
                    >
                      <a alt={session.name}>{session.name}</a>
                    </OverlayTrigger>
                    <div>
                      <OverlayTrigger
                        placement="top"
                        delay={{ show: 250, hide: 400 }}
                        overlay={<Tooltip id={`delete-tooltip-${index}`}>Delete Session</Tooltip>}
                      >
                        <Button className="btn-danger" style={{ marginRight: '10px' }}
                          title="Delete Session"
                          onClick={(e) => { setSessionToDelete(session.id); setShowDeleteModal(true); e.stopPropagation(); }}>
                          <i className="fas fa-trash"></i>
                        </Button>
                      </OverlayTrigger>
                    </div>
                  </li>
                ))}
              </ul>}
          </Row>
        </Col>
        <Col>
          <div className="messages mb-3 border p-3" style={{ minHeight: '20em', maxHeight: '50em', overflowY: 'scroll' }}>
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.role} mb-2 d-flex ${msg.role === 'user' ? 'justify-content-end' : 'justify-content-start'}`}>
                {!error && index === messages.length - 1 && <div ref={messagesEndRef} />}
                <div className={`alert ${msg.role === 'user' ? 'alert-primary' : 'alert-secondary'}`} style={{ maxWidth: '90%' }} role="alert">
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
              </div>
            ))}
            {error && <div className="alert alert-danger" role="alert">{error}<div ref={messagesEndRef} /></div>}
            {isThinking && <div className="d-flex justify-content-center">
                <div className="spinner-border text-info" role="status">
                  <span className="visually-hidden">Thinking...</span>
                </div>
                <div ref={messagesEndRef} />
              </div>}
          </div>
          <div className="input-container d-flex">
            <textarea className="form-control me-2"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') { handleSendMessage(e); e.preventDefault(); return false; } }}
              placeholder="Type a message..."
            ></textarea>
            <Button onClick={handleSendMessage}>Send</Button>
          </div>
        </Col>
      </Row>

      <ConfirmModal
        show={showDeleteModal}
        handleClose={() => setShowDeleteModal(false)}
        handleConfirm={handleDelete}
        message="Are you sure you want to delete this session?"
      />
    </div>
  );
};

export default CopilotChat;