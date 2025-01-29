import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import api from '../api/Api'; // Adjust the path as necessary

const CopilotChat = () => {
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

    const userMessage = { role: 'user', content: prompt };
    setMessages([...messages, userMessage]);

    setError('');

    try {
      const response = await api.completions.chat(prompt, messages);

      const assistantMessage = { role: 'assistant', content: response };
      setMessages([...messages, userMessage, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      setError('Error sending message. Please try again.');
    } finally {
        setIsThinking(false);
    }

  };

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  return (
    <div className="ai-chat container mt-4">
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
        <button className="btn btn-primary" onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
};

export default CopilotChat;