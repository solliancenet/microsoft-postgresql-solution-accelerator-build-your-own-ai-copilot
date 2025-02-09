import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { Row, Col, Button } from 'react-bootstrap';
import api from '../api/Api'; // Adjust the path as necessary

const CopilotChat = () => {
  const [sessionId, setSessionId] = useState(-1);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);
  const [error, setError] = useState('');
  const [isThinking, setIsThinking] = useState(false);

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

      // only update the messages if the session ID is the same
      // This keeps a processing completion from updating messages after a new session is created
      if (sessionId === -1 || sessionId === output.sessionId) {
        // Update the session ID
        setSessionId(output.sessionId);

        // Add the assistant's response to the messages
        const assistantMessage = { role: 'assistant', content: output.content };
        setMessages([...messages, userMessage, assistantMessage]);
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
      const response = await api.completions.getHistory();
      setSessions(response);
    } catch (error) {
      console.error('Error loading session history:', error);
      setError('Error loading session history. Please try again.');
    }
  }

  const loadSession = async (id) => {
    try {
      setSessionId(id);
      const response = await api.completions.getHistory(id);
      setMessages(response.history);
    } catch (error) {
      console.error('Error loading session history:', error);
      setError('Error loading session history. Please try again.');
    }
  }

  useEffect(() => {
    refreshSessionList();
  }, [sessionId]);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  useEffect(() => {
    refreshSessionList();
  }, []);

  return (
    <div className="ai-chat container mt-4">
      <Row>
        <Col style={{ width: '10%', maxWidth: '8em' }}>
          <Row>
            <Button area-label="New Session" alt="New Session" onClick={createNewSession}>
              <i className="fas fa-plus"></i> Session
            </Button>
          </Row>
          <Row className="mt-3">
            <strong>History</strong>

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
    </div>
  );
};

export default CopilotChat;