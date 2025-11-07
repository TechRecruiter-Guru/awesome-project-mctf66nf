import React, { useState } from 'react';

function SkillsKeywordsInput({ onSkillsChange }) {
  const [skills, setSkills] = useState([]);
  const [currentInput, setCurrentInput] = useState('');
  const [category, setCategory] = useState('Tech');

  // Predefined skill suggestions
  const skillSuggestions = {
    Tech: ['JavaScript', 'Python', 'React', 'Node.js', 'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision'],
    Soft: ['Leadership', 'Communication', 'Problem Solving', 'Teamwork', 'Critical Thinking'],
    Domain: ['Healthcare', 'Finance', 'E-commerce', 'SaaS', 'Research', 'Academia']
  };

  const [showSuggestions, setShowSuggestions] = useState(false);

  const handleAddSkill = (skill = currentInput) => {
    if (skill.trim() && !skills.some(s => s.name === skill.trim())) {
      const newSkills = [...skills, { name: skill.trim(), category }];
      setSkills(newSkills);
      setCurrentInput('');
      setShowSuggestions(false);
      onSkillsChange(newSkills);
    }
  };

  const handleRemoveSkill = (index) => {
    const newSkills = skills.filter((_, i) => i !== index);
    setSkills(newSkills);
    onSkillsChange(newSkills);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddSkill();
    }
  };

  const filteredSuggestions = currentInput.length > 0
    ? skillSuggestions[category].filter(s =>
        s.toLowerCase().includes(currentInput.toLowerCase())
      )
    : skillSuggestions[category];

  const getCategoryColor = (cat) => {
    switch(cat) {
      case 'Tech': return 'bg-blue-100 text-blue-800';
      case 'Soft': return 'bg-green-100 text-green-800';
      case 'Domain': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-light-gray rounded-2xl shadow-md p-6">
      <h3 className="text-xl font-semibold mb-4 text-gray-800">Skills & Keywords</h3>

      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Category
        </label>
        <div className="flex gap-2">
          {['Tech', 'Soft', 'Domain'].map(cat => (
            <button
              key={cat}
              onClick={() => setCategory(cat)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                category === cat
                  ? 'bg-primary text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      <div className="relative mb-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={currentInput}
            onChange={(e) => setCurrentInput(e.target.value)}
            onKeyPress={handleKeyPress}
            onFocus={() => setShowSuggestions(true)}
            placeholder="Enter skills or keywords..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
          />
          <button
            onClick={() => handleAddSkill()}
            className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            Add
          </button>
        </div>

        {showSuggestions && currentInput.length > 0 && filteredSuggestions.length > 0 && (
          <div className="absolute z-10 w-full mt-2 bg-white border border-gray-200 rounded-lg shadow-lg max-h-48 overflow-y-auto">
            {filteredSuggestions.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => handleAddSkill(suggestion)}
                className="w-full text-left px-4 py-2 hover:bg-gray-100 transition-colors"
              >
                {suggestion}
              </button>
            ))}
          </div>
        )}
      </div>

      {skills.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {skills.map((skill, index) => (
            <div
              key={index}
              className={`px-4 py-2 rounded-lg flex items-center gap-2 shadow-sm ${getCategoryColor(skill.category)}`}
            >
              <span className="text-sm font-medium">{skill.name}</span>
              <button
                onClick={() => handleRemoveSkill(index)}
                className="font-bold hover:opacity-70"
              >
                ×
              </button>
            </div>
          ))}
        </div>
      )}

      {skills.length > 1 && (
        <p className="mt-3 text-sm text-gray-600">
          Combined with AND logic
        </p>
      )}
    </div>
  );
}

export default SkillsKeywordsInput;
