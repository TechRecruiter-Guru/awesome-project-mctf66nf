import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function SavedSearchesList({ onLoadSearch, refreshTrigger }) {
  const [savedSearches, setSavedSearches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [expanded, setExpanded] = useState(true);

  useEffect(() => {
    fetchSavedSearches();
  }, [refreshTrigger]);

  const fetchSavedSearches = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`${API_URL}/api/saved-searches`);
      setSavedSearches(response.data);
    } catch (err) {
      setError('Failed to load saved searches');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this saved search?')) {
      return;
    }

    try {
      await axios.delete(`${API_URL}/api/saved-searches/${id}`);
      setSavedSearches(savedSearches.filter(search => search.id !== id));
    } catch (err) {
      alert('Failed to delete search');
      console.error(err);
    }
  };

  const handleLoad = (search) => {
    if (onLoadSearch) {
      onLoadSearch(search);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="bg-light-gray rounded-2xl shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-semibold text-gray-800 flex items-center gap-2">
          📚 Saved Searches
          {savedSearches.length > 0 && (
            <span className="text-sm font-normal text-gray-600">
              ({savedSearches.length})
            </span>
          )}
        </h3>
        <button
          onClick={() => setExpanded(!expanded)}
          className="text-gray-600 hover:text-gray-800 transition-colors"
        >
          {expanded ? '▼' : '▶'}
        </button>
      </div>

      {expanded && (
        <>
          {loading && (
            <div className="text-center py-4 text-gray-600">
              Loading saved searches...
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
              {error}
            </div>
          )}

          {!loading && !error && savedSearches.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              <div className="text-4xl mb-2">🔍</div>
              <p>No saved searches yet.</p>
              <p className="text-sm mt-1">Execute a search and click "Save Search" to save it.</p>
            </div>
          )}

          {!loading && !error && savedSearches.length > 0 && (
            <div className="space-y-3">
              {savedSearches.map((search) => (
                <div
                  key={search.id}
                  className="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <h4 className="font-semibold text-gray-800 mb-1">
                        {search.name}
                      </h4>
                      <p className="text-sm text-gray-600 mb-2 font-mono bg-gray-50 p-2 rounded">
                        {search.query}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-4 text-xs text-gray-500 mb-3">
                    <span>📅 {formatDate(search.created_at)}</span>
                    <span>📊 {search.total_results} results</span>
                    {search.data_sources && search.data_sources.length > 0 && (
                      <span>🔗 {search.data_sources.join(', ')}</span>
                    )}
                  </div>

                  <div className="flex gap-2">
                    <button
                      onClick={() => handleLoad(search)}
                      className="px-3 py-1.5 bg-primary text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                    >
                      Load Search
                    </button>
                    <button
                      onClick={() => handleDelete(search.id)}
                      className="px-3 py-1.5 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors text-sm font-medium"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default SavedSearchesList;
