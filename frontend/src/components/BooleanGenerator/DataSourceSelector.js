import React, { useState } from 'react';

function DataSourceSelector({ onDataSourceChange }) {
  const [selectedSources, setSelectedSources] = useState(['LinkedIn']);
  const [customSource, setCustomSource] = useState('');
  const [showCustomInput, setShowCustomInput] = useState(false);

  const predefinedSources = [
    { name: 'LinkedIn', icon: '💼' },
    { name: 'GitHub', icon: '💻' },
    { name: 'Google Scholar', icon: '🎓' },
  ];

  const handleToggleSource = (source) => {
    let newSources;
    if (selectedSources.includes(source)) {
      newSources = selectedSources.filter(s => s !== source);
    } else {
      newSources = [...selectedSources, source];
    }
    setSelectedSources(newSources);
    onDataSourceChange(newSources);
  };

  const handleAddCustomSource = () => {
    if (customSource.trim() && !selectedSources.includes(customSource.trim())) {
      const newSources = [...selectedSources, customSource.trim()];
      setSelectedSources(newSources);
      setCustomSource('');
      setShowCustomInput(false);
      onDataSourceChange(newSources);
    }
  };

  return (
    <div className="bg-light-gray rounded-2xl shadow-md p-6">
      <h3 className="text-xl font-semibold mb-4 text-gray-800">Data Source</h3>

      <div className="space-y-3">
        {predefinedSources.map((source) => (
          <label
            key={source.name}
            className="flex items-center p-3 bg-white rounded-lg hover:shadow-md transition-shadow cursor-pointer"
          >
            <input
              type="checkbox"
              checked={selectedSources.includes(source.name)}
              onChange={() => handleToggleSource(source.name)}
              className="w-5 h-5 text-primary focus:ring-2 focus:ring-primary rounded"
            />
            <span className="ml-3 text-2xl">{source.icon}</span>
            <span className="ml-2 text-gray-800 font-medium">{source.name}</span>
          </label>
        ))}

        {selectedSources
          .filter(s => !predefinedSources.some(ps => ps.name === s))
          .map((source, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-3 bg-white rounded-lg"
            >
              <span className="text-gray-800 font-medium">🔗 {source}</span>
              <button
                onClick={() => {
                  const newSources = selectedSources.filter(s => s !== source);
                  setSelectedSources(newSources);
                  onDataSourceChange(newSources);
                }}
                className="text-red-500 hover:text-red-700 font-bold"
              >
                ×
              </button>
            </div>
          ))}
      </div>

      {!showCustomInput ? (
        <button
          onClick={() => setShowCustomInput(true)}
          className="mt-4 w-full py-2 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-primary hover:text-primary transition-colors"
        >
          + Add Custom Source
        </button>
      ) : (
        <div className="mt-4 flex gap-2">
          <input
            type="text"
            value={customSource}
            onChange={(e) => setCustomSource(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleAddCustomSource()}
            placeholder="Enter custom source..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            autoFocus
          />
          <button
            onClick={handleAddCustomSource}
            className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-blue-700"
          >
            Add
          </button>
          <button
            onClick={() => {
              setShowCustomInput(false);
              setCustomSource('');
            }}
            className="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400"
          >
            Cancel
          </button>
        </div>
      )}

      <p className="mt-4 text-sm text-gray-600">
        Query formatting will adjust based on selected platform syntax
      </p>
    </div>
  );
}

export default DataSourceSelector;
