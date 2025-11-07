import React, { useState } from 'react';

function ExclusionsInput({ onExclusionsChange }) {
  const [exclusions, setExclusions] = useState([]);
  const [currentInput, setCurrentInput] = useState('');

  const handleAddExclusion = () => {
    if (currentInput.trim() && !exclusions.includes(currentInput.trim())) {
      const newExclusions = [...exclusions, currentInput.trim()];
      setExclusions(newExclusions);
      setCurrentInput('');
      onExclusionsChange(newExclusions);
    }
  };

  const handleRemoveExclusion = (index) => {
    const newExclusions = exclusions.filter((_, i) => i !== index);
    setExclusions(newExclusions);
    onExclusionsChange(newExclusions);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddExclusion();
    }
  };

  return (
    <div className="bg-light-gray rounded-2xl shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-semibold text-gray-800">Exclusions</h3>
        <div className="relative group">
          <button className="text-gray-500 hover:text-gray-700">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
            </svg>
          </button>
          <div className="absolute right-0 w-64 p-3 bg-gray-800 text-white text-sm rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-10">
            Use to remove irrelevant roles or industries
          </div>
        </div>
      </div>

      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={currentInput}
          onChange={(e) => setCurrentInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Enter terms to exclude..."
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
        />
        <button
          onClick={handleAddExclusion}
          className="px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors font-medium"
        >
          Add
        </button>
      </div>

      {exclusions.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {exclusions.map((exclusion, index) => (
            <div
              key={index}
              className="bg-red-100 text-red-800 px-4 py-2 rounded-lg flex items-center gap-2 shadow-sm"
            >
              <span className="text-sm font-medium">NOT {exclusion}</span>
              <button
                onClick={() => handleRemoveExclusion(index)}
                className="font-bold hover:opacity-70"
              >
                ×
              </button>
            </div>
          ))}
        </div>
      )}

      {exclusions.length > 0 && (
        <p className="mt-3 text-sm text-gray-600">
          Adds NOT clauses to query
        </p>
      )}
    </div>
  );
}

export default ExclusionsInput;
