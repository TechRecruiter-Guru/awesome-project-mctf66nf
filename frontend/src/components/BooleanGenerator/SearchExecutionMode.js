import React, { useState } from 'react';

function SearchExecutionMode({ onModeChange }) {
  const [selectedMode, setSelectedMode] = useState('on-demand');

  const modes = [
    {
      id: 'on-demand',
      title: 'On-Demand',
      description: 'Manual execution when ready',
      icon: '🎯'
    },
    {
      id: 'auto-run',
      title: 'Auto-Run',
      description: 'Scheduled or trigger-based',
      icon: '⚡'
    }
  ];

  const handleModeSelect = (modeId) => {
    setSelectedMode(modeId);
    onModeChange(modeId);
  };

  return (
    <div className="bg-light-gray rounded-2xl shadow-md p-6">
      <h3 className="text-xl font-semibold mb-4 text-gray-800">Search Execution Mode</h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {modes.map((mode) => (
          <button
            key={mode.id}
            onClick={() => handleModeSelect(mode.id)}
            className={`relative p-6 rounded-xl border-2 transition-all duration-300 text-left ${
              selectedMode === mode.id
                ? 'border-primary bg-blue-50 shadow-lg transform scale-105'
                : 'border-gray-300 bg-white hover:border-gray-400 hover:shadow-md'
            }`}
          >
            <div className="flex items-start gap-4">
              <span className="text-4xl">{mode.icon}</span>
              <div className="flex-1">
                <h4 className="text-lg font-semibold text-gray-800 mb-1">
                  {mode.title}
                </h4>
                <p className="text-sm text-gray-600">
                  {mode.description}
                </p>
              </div>
              {selectedMode === mode.id && (
                <div className="absolute top-3 right-3 w-6 h-6 bg-primary rounded-full flex items-center justify-center">
                  <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </div>
              )}
            </div>
          </button>
        ))}
      </div>

      {selectedMode === 'auto-run' && (
        <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <p className="text-sm text-blue-800">
            💡 Auto-run mode enabled. Configure scheduling options below.
          </p>
        </div>
      )}
    </div>
  );
}

export default SearchExecutionMode;
