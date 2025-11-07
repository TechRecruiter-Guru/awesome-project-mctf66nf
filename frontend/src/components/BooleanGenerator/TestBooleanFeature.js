import React, { useState } from 'react';

function TestBooleanFeature({ booleanQuery, onQueryChange }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedQuery, setEditedQuery] = useState(booleanQuery);
  const [copied, setCopied] = useState(false);

  React.useEffect(() => {
    setEditedQuery(booleanQuery);
  }, [booleanQuery]);

  const handleCopyToClipboard = () => {
    navigator.clipboard.writeText(booleanQuery);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleSaveEdit = () => {
    onQueryChange(editedQuery);
    setIsEditing(false);
  };

  const handleCancelEdit = () => {
    setEditedQuery(booleanQuery);
    setIsEditing(false);
  };

  const formatQuery = (query) => {
    // Add line breaks for better readability
    return query
      .replace(/\s+AND\s+/g, '\nAND ')
      .replace(/\s+OR\s+/g, '\nOR ')
      .replace(/\s+NOT\s+/g, '\nNOT ');
  };

  return (
    <div className="bg-light-gray rounded-2xl shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-semibold text-gray-800">Boolean Query Preview</h3>
        <div className="flex gap-2">
          {!isEditing ? (
            <>
              <button
                onClick={() => setIsEditing(true)}
                className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors text-sm font-medium"
              >
                Edit
              </button>
              <button
                onClick={handleCopyToClipboard}
                className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium flex items-center gap-2"
              >
                {copied ? (
                  <>
                    ✓ Copied!
                  </>
                ) : (
                  <>
                    📋 Copy
                  </>
                )}
              </button>
            </>
          ) : (
            <>
              <button
                onClick={handleSaveEdit}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm font-medium"
              >
                Save
              </button>
              <button
                onClick={handleCancelEdit}
                className="px-4 py-2 bg-gray-400 text-white rounded-lg hover:bg-gray-500 transition-colors text-sm font-medium"
              >
                Cancel
              </button>
            </>
          )}
        </div>
      </div>

      {!isEditing ? (
        <div className="bg-gray-900 rounded-lg p-4 overflow-x-auto">
          <pre className="text-green-400 font-mono text-sm whitespace-pre-wrap">
            {booleanQuery || '// Your Boolean query will appear here...'}
          </pre>
        </div>
      ) : (
        <textarea
          value={editedQuery}
          onChange={(e) => setEditedQuery(e.target.value)}
          className="w-full h-48 bg-gray-900 text-green-400 font-mono text-sm rounded-lg p-4 focus:outline-none focus:ring-2 focus:ring-primary"
          placeholder="Edit your Boolean query..."
        />
      )}

      <div className="mt-4 flex gap-4 text-sm text-gray-600">
        <span>Lines: {booleanQuery.split('\n').length}</span>
        <span>Characters: {booleanQuery.length}</span>
      </div>
    </div>
  );
}

export default TestBooleanFeature;
