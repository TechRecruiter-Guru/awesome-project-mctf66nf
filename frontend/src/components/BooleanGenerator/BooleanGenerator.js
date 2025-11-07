import React, { useState, useEffect } from 'react';
import JobTitleInput from './JobTitleInput';
import SkillsKeywordsInput from './SkillsKeywordsInput';
import ExclusionsInput from './ExclusionsInput';
import DataSourceSelector from './DataSourceSelector';
import TestBooleanFeature from './TestBooleanFeature';
import SearchExecutionMode from './SearchExecutionMode';
import CustomSchedulingPanel from './CustomSchedulingPanel';
import ExecuteSearchButton from './ExecuteSearchButton';

function BooleanGenerator() {
  const [jobTitles, setJobTitles] = useState([]);
  const [skills, setSkills] = useState([]);
  const [exclusions, setExclusions] = useState([]);
  const [dataSources, setDataSources] = useState(['LinkedIn']);
  const [executionMode, setExecutionMode] = useState('on-demand');
  const [schedule, setSchedule] = useState(null);
  const [booleanQuery, setBooleanQuery] = useState('');

  // Generate Boolean query whenever inputs change
  useEffect(() => {
    generateBooleanQuery();
  }, [jobTitles, skills, exclusions, dataSources]);

  const generateBooleanQuery = () => {
    let query = '';

    // Job Titles (OR logic)
    if (jobTitles.length > 0) {
      const titlesQuery = jobTitles.map(title => `"${title}"`).join(' OR ');
      query += `(${titlesQuery})`;
    }

    // Skills (AND logic)
    if (skills.length > 0) {
      const skillsQuery = skills.map(skill => `"${skill.name}"`).join(' AND ');
      if (query) query += ' AND ';
      query += `(${skillsQuery})`;
    }

    // Exclusions (NOT logic)
    if (exclusions.length > 0) {
      const exclusionsQuery = exclusions.map(exclusion => `NOT "${exclusion}"`).join(' AND ');
      if (query) query += ' AND ';
      query += `(${exclusionsQuery})`;
    }

    // Add platform-specific formatting notes
    if (query) {
      const platformNote = dataSources.length > 0
        ? `\n\n// Optimized for: ${dataSources.join(', ')}`
        : '';
      query += platformNote;
    } else {
      query = '// Add job titles, skills, or keywords to generate a Boolean query';
    }

    setBooleanQuery(query);
  };

  const handleExecuteSearch = async (query) => {
    // Simulate API call
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          success: true,
          query: query,
          timestamp: new Date().toISOString(),
        });
      }, 1500);
    });
  };

  return (
    <div className="boolean-generator-container">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            Boolean Query Generator
          </h1>
          <p className="text-gray-200">
            Build powerful Boolean search queries for recruiting and talent sourcing
          </p>
        </div>

        {/* Main Grid Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Column */}
          <div className="space-y-6">
            <JobTitleInput onJobTitlesChange={setJobTitles} />
            <SkillsKeywordsInput onSkillsChange={setSkills} />
            <ExclusionsInput onExclusionsChange={setExclusions} />
            <DataSourceSelector onDataSourceChange={setDataSources} />
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            <TestBooleanFeature
              booleanQuery={booleanQuery}
              onQueryChange={setBooleanQuery}
            />
            <SearchExecutionMode onModeChange={setExecutionMode} />
            <CustomSchedulingPanel
              visible={executionMode === 'auto-run'}
              onScheduleChange={setSchedule}
            />
            <ExecuteSearchButton
              booleanQuery={booleanQuery}
              onExecute={handleExecuteSearch}
              disabled={!booleanQuery || booleanQuery.includes('//')}
            />
          </div>
        </div>

        {/* Info Section */}
        <div className="mt-8 bg-white bg-opacity-10 rounded-2xl p-6 backdrop-blur-sm">
          <h3 className="text-xl font-semibold text-white mb-3">
            How to Use This Tool
          </h3>
          <ul className="text-gray-200 space-y-2">
            <li>• <strong>Job Titles:</strong> Add one or more job titles (combined with OR)</li>
            <li>• <strong>Skills & Keywords:</strong> Add required skills (combined with AND)</li>
            <li>• <strong>Exclusions:</strong> Remove irrelevant results (added as NOT clauses)</li>
            <li>• <strong>Data Sources:</strong> Select platforms for optimized query formatting</li>
            <li>• <strong>Execution Mode:</strong> Run queries on-demand or schedule them</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default BooleanGenerator;
