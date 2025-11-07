import React, { useState } from 'react';

function JobTitleInput({ onJobTitlesChange }) {
  const [titles, setTitles] = useState([]);
  const [currentInput, setCurrentInput] = useState('');

  const normalizeTitle = (title) => {
    return title
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
      .join(' ');
  };

  const handleAddTitle = () => {
    if (currentInput.trim()) {
      const normalized = normalizeTitle(currentInput.trim());
      const newTitles = [...titles, normalized];
      setTitles(newTitles);
      setCurrentInput('');
      onJobTitlesChange(newTitles);
    }
  };

  const handleRemoveTitle = (index) => {
    const newTitles = titles.filter((_, i) => i !== index);
    setTitles(newTitles);
    onJobTitlesChange(newTitles);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddTitle();
    }
  };

  return (
    <div className="bg-light-gray rounded-2xl shadow-md p-6">
      <h3 className="text-xl font-semibold mb-4 text-gray-800">Job Title(s)</h3>

      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={currentInput}
          onChange={(e) => setCurrentInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Enter job title(s)..."
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
        />
        <button
          onClick={handleAddTitle}
          className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
        >
          Add
        </button>
      </div>

      {titles.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {titles.map((title, index) => (
            <div
              key={index}
              className="bg-white px-4 py-2 rounded-lg flex items-center gap-2 shadow-sm"
            >
              <span className="text-gray-700">{title}</span>
              <button
                onClick={() => handleRemoveTitle(index)}
                className="text-red-500 hover:text-red-700 font-bold"
              >
                ×
              </button>
            </div>
          ))}
        </div>
      )}

      {titles.length > 1 && (
        <p className="mt-3 text-sm text-gray-600">
          Combined with OR logic
        </p>
      )}
    </div>
  );
}

export default JobTitleInput;
