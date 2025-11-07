import React, { useState } from 'react';
import axios from 'axios';

function ExecuteSearchButton({ booleanQuery, onExecute, disabled, onSearchSaved, onCandidatesExported }) {
  const [isExecuting, setIsExecuting] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [results, setResults] = useState(null);
  const [isSaving, setIsSaving] = useState(false);
  const [isExporting, setIsExporting] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  const handleExecute = async () => {
    // Validate inputs
    if (!booleanQuery || booleanQuery.trim() === '') {
      alert('Please generate a Boolean query first!');
      return;
    }

    setIsExecuting(true);

    try {
      // Call the onExecute callback
      const response = await onExecute(booleanQuery);
      setResults(response);
      setShowModal(true);
    } catch (error) {
      console.error('Search execution failed:', error);
      alert('Search execution failed. Please try again.');
    } finally {
      setIsExecuting(false);
    }
  };

  const handleSaveSearch = async () => {
    if (!results) return;

    setIsSaving(true);
    try {
      const searchName = prompt('Enter a name for this search (optional):');

      const response = await axios.post(`${API_URL}/api/saved-searches`, {
        query: booleanQuery,
        data_sources: results.sources || [],
        name: searchName || `Search ${new Date().toLocaleDateString()}`,
        total_results: results.results?.GitHub?.total_count || 0,
        github_results_count: results.results?.GitHub?.results?.length || 0
      });

      alert('Search saved successfully!');

      // Trigger refresh of saved searches list
      if (onSearchSaved) {
        onSearchSaved();
      }
    } catch (error) {
      console.error('Error saving search:', error);
      alert('Failed to save search. Please try again.');
    } finally {
      setIsSaving(false);
    }
  };

  const handleExportCandidates = async () => {
    if (!results || !results.results?.GitHub?.results) {
      alert('No GitHub results to export!');
      return;
    }

    setIsExporting(true);
    try {
      const candidates = results.results.GitHub.results.map(user => ({
        name: user.name,
        github_url: user.profile_url,
        expertise: 'Software Engineering' // Default
      }));

      const response = await axios.post(`${API_URL}/api/export-candidates`, {
        candidates: candidates
      });

      alert(`Successfully exported ${response.data.created} candidates! (${response.data.skipped} skipped as duplicates)`);

      // Trigger stats refresh in parent component
      if (onCandidatesExported) {
        onCandidatesExported();
      }
    } catch (error) {
      console.error('Error exporting candidates:', error);
      alert('Failed to export candidates. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  const closeModal = () => {
    setShowModal(false);
    setResults(null);
  };

  return (
    <>
      <div className="bg-light-gray rounded-2xl shadow-md p-6">
        <div className="flex flex-col items-center gap-4">
          <h3 className="text-xl font-semibold text-gray-800">Execute Search</h3>

          <button
            onClick={handleExecute}
            disabled={disabled || isExecuting}
            className={`w-full py-4 rounded-xl font-semibold text-lg transition-all duration-300 ${
              disabled || isExecuting
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-600 to-blue-700 text-white hover:from-blue-700 hover:to-blue-800 shadow-lg hover:shadow-xl transform hover:scale-105'
            }`}
          >
            {isExecuting ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Executing Search...
              </span>
            ) : (
              '🚀 Execute Boolean Search'
            )}
          </button>

          <p className="text-sm text-gray-600 text-center">
            Click to validate inputs and run the Boolean search query
          </p>
        </div>
      </div>

      {/* Results Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[80vh] overflow-y-auto p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-2xl font-bold text-gray-800">Search Results</h3>
              <button
                onClick={closeModal}
                className="text-gray-500 hover:text-gray-700 text-2xl"
              >
                ×
              </button>
            </div>

            <div className="space-y-4">
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                <p className="text-green-800 font-semibold">✓ Search executed successfully!</p>
              </div>

              <div className="p-4 bg-gray-50 rounded-lg">
                <h4 className="font-semibold text-gray-800 mb-2">Query Executed:</h4>
                <pre className="text-sm text-gray-700 bg-white p-3 rounded border border-gray-200 overflow-x-auto whitespace-pre-wrap">
                  {booleanQuery}
                </pre>
              </div>

              {results && results.results && (
                <div className="space-y-4">
                  {/* GitHub Results */}
                  {results.results.GitHub && (
                    <div className="p-4 bg-gray-800 rounded-lg">
                      <h4 className="font-semibold text-white mb-3 flex items-center gap-2">
                        💻 GitHub Results
                      </h4>
                      {results.results.GitHub.error ? (
                        <p className="text-gray-300 text-sm">{results.results.GitHub.message}</p>
                      ) : (
                        <>
                          <p className="text-gray-300 text-sm mb-3">
                            Found {results.results.GitHub.total_count} users
                          </p>
                          <div className="space-y-2 max-h-64 overflow-y-auto">
                            {results.results.GitHub.results.map((user, idx) => (
                              <div key={idx} className="bg-gray-700 p-3 rounded flex items-center gap-3">
                                <img src={user.avatar} alt={user.name} className="w-10 h-10 rounded-full" />
                                <div className="flex-1">
                                  <a
                                    href={user.profile_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-blue-400 hover:text-blue-300 font-medium"
                                  >
                                    {user.name}
                                  </a>
                                  <p className="text-gray-400 text-xs">{user.type}</p>
                                </div>
                              </div>
                            ))}
                          </div>
                        </>
                      )}
                    </div>
                  )}

                  {/* LinkedIn Results */}
                  {results.results.LinkedIn && (
                    <div className="p-4 bg-blue-50 rounded-lg">
                      <h4 className="font-semibold text-gray-800 mb-2 flex items-center gap-2">
                        💼 LinkedIn
                      </h4>
                      <p className="text-sm text-gray-700 mb-2">{results.results.LinkedIn.message}</p>
                      {results.results.LinkedIn.query_url && (
                        <a
                          href={results.results.LinkedIn.query_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-block mt-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm"
                        >
                          Open in LinkedIn →
                        </a>
                      )}
                    </div>
                  )}

                  {/* Google Scholar Results */}
                  {results.results['Google Scholar'] && (
                    <div className="p-4 bg-red-50 rounded-lg">
                      <h4 className="font-semibold text-gray-800 mb-2 flex items-center gap-2">
                        🎓 Google Scholar
                      </h4>
                      <p className="text-sm text-gray-700 mb-2">{results.results['Google Scholar'].message}</p>
                      {results.results['Google Scholar'].query_url && (
                        <a
                          href={results.results['Google Scholar'].query_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-block mt-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 text-sm"
                        >
                          Open in Google Scholar →
                        </a>
                      )}
                    </div>
                  )}
                </div>
              )}

              {/* Action Buttons */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-4">
                <button
                  onClick={handleSaveSearch}
                  disabled={isSaving}
                  className="py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium disabled:bg-gray-300 disabled:cursor-not-allowed"
                >
                  {isSaving ? '💾 Saving...' : '💾 Save Search'}
                </button>

                <button
                  onClick={handleExportCandidates}
                  disabled={isExporting || !results?.results?.GitHub?.results}
                  className="py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors font-medium disabled:bg-gray-300 disabled:cursor-not-allowed"
                >
                  {isExporting ? '📤 Exporting...' : '📤 Export to Candidates'}
                </button>
              </div>

              <button
                onClick={closeModal}
                className="w-full py-3 bg-primary text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default ExecuteSearchButton;
