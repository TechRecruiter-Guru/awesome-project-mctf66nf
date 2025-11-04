import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [items, setItems] = useState([]);
  const [newItem, setNewItem] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [apiStatus, setApiStatus] = useState('checking...');

  useEffect(() => {
    checkApiHealth();
    fetchItems();
  }, []);

  const checkApiHealth = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/health`);
      setApiStatus(response.data.status);
    } catch (err) {
      setApiStatus('unhealthy');
      console.error('API health check failed:', err);
    }
  };

  const fetchItems = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.get(`${API_URL}/api/items`);
      setItems(response.data.items || []);
    } catch (err) {
      setError('Failed to fetch items: ' + err.message);
      console.error('Error fetching items:', err);
    } finally {
      setLoading(false);
    }
  };

  const addItem = async (e) => {
    e.preventDefault();
    if (!newItem.trim()) return;

    setLoading(true);
    setError('');
    try {
      const response = await axios.post(`${API_URL}/api/items`, {
        text: newItem
      });
      setItems([...items, response.data.item]);
      setNewItem('');
    } catch (err) {
      setError('Failed to add item: ' + err.message);
      console.error('Error adding item:', err);
    } finally {
      setLoading(false);
    }
  };

  const deleteItem = async (id) => {
    setLoading(true);
    setError('');
    try {
      await axios.delete(`${API_URL}/api/items/${id}`);
      setItems(items.filter(item => item.id !== id));
    } catch (err) {
      setError('Failed to delete item: ' + err.message);
      console.error('Error deleting item:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleComplete = async (id) => {
    const item = items.find(i => i.id === id);
    if (!item) return;

    setLoading(true);
    setError('');
    try {
      const response = await axios.put(`${API_URL}/api/items/${id}`, {
        completed: !item.completed
      });
      setItems(items.map(i => i.id === id ? response.data.item : i));
    } catch (err) {
      setError('Failed to update item: ' + err.message);
      console.error('Error updating item:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>📝 Task Manager MVP</h1>
        <p className="subtitle">A full-stack web application built with React & Flask</p>
        <div className={`status-badge ${apiStatus === 'healthy' ? 'healthy' : 'unhealthy'}`}>
          API Status: {apiStatus}
        </div>
      </header>

      <main className="App-main">
        {error && <div className="error-message">{error}</div>}

        <form onSubmit={addItem} className="add-item-form">
          <input
            type="text"
            value={newItem}
            onChange={(e) => setNewItem(e.target.value)}
            placeholder="Add a new task..."
            disabled={loading}
            className="item-input"
          />
          <button type="submit" disabled={loading || !newItem.trim()} className="btn btn-primary">
            Add Task
          </button>
        </form>

        <div className="items-container">
          {loading && items.length === 0 ? (
            <div className="loading">Loading...</div>
          ) : items.length === 0 ? (
            <div className="empty-state">
              <p>No tasks yet! Add one above to get started.</p>
            </div>
          ) : (
            <ul className="items-list">
              {items.map((item) => (
                <li key={item.id} className={`item ${item.completed ? 'completed' : ''}`}>
                  <div className="item-content">
                    <input
                      type="checkbox"
                      checked={item.completed}
                      onChange={() => toggleComplete(item.id)}
                      disabled={loading}
                    />
                    <span className="item-text">{item.text}</span>
                  </div>
                  <button
                    onClick={() => deleteItem(item.id)}
                    disabled={loading}
                    className="btn btn-danger"
                  >
                    Delete
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="stats">
          <p>Total: {items.length} | Completed: {items.filter(i => i.completed).length}</p>
        </div>
      </main>
    </div>
  );
}

export default App;