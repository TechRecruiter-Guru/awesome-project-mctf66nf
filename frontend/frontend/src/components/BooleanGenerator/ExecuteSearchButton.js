import React, { useState } from 'react';

function ExecuteSearchButton({ booleanQuery, onExecute, disabled }) {
  const [isExecuting, setIsExecuting] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [results, setResults] = useState(null);

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
                <pre className="text-sm text-gray-700 bg-white p-3 rounded border border-gray-200 overflow-x-auto">
                  {booleanQuery}
                </pre>
              </div>

              {results && (
                <div className="p-4 bg-blue-50 rounded-lg">
                  <h4 className="font-semibold text-gray-800 mb-2">Summary:</h4>
                  <ul className="text-sm text-gray-700 space-y-1">
                    <li>• Query generated successfully</li>
                    <li>• Ready for use in selected platforms</li>
                    <li>• Results may vary by data source</li>
                  </ul>
                </div>
              )}

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
