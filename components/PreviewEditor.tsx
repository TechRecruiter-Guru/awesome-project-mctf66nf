'use client';

import { useState } from 'react';
import { SafetyCaseData, RiskAssessment, TestingResult } from '@/lib/types';

interface PreviewEditorProps {
  initialData: SafetyCaseData;
  templateHtml: string;
  onDataChange: (data: SafetyCaseData) => void;
}

export default function PreviewEditor({
  initialData,
  templateHtml,
  onDataChange,
}: PreviewEditorProps) {
  const [data, setData] = useState<SafetyCaseData>(initialData);
  const [activeTab, setActiveTab] = useState<'edit' | 'preview'>('edit');

  const handleChange = (field: keyof SafetyCaseData, value: any) => {
    const updatedData = { ...data, [field]: value };
    setData(updatedData);
    onDataChange(updatedData);
  };

  const addRiskAssessment = () => {
    const newAssessment: RiskAssessment = {
      scenario: 'New Scenario',
      severity: 'Low',
      likelihood: 'Low',
      riskLevel: 'Low',
      status: 'Pending',
    };
    handleChange('riskAssessments', [...(data.riskAssessments ?? []), newAssessment]);
  };

  const updateRiskAssessment = (index: number, field: keyof RiskAssessment, value: string) => {
    const updated = [...(data.riskAssessments ?? [])];
    updated[index] = { ...updated[index], [field]: value };
    handleChange('riskAssessments', updated);
  };

  const removeRiskAssessment = (index: number) => {
    handleChange('riskAssessments', (data.riskAssessments ?? []).filter((_, i) => i !== index));
  };

  const addTestingResult = () => {
    const newResult: TestingResult = {
      category: 'New Category',
      scenarios: 0,
      cycles: 0,
      passRate: 0,
    };
    handleChange('testingResults', [...(data.testingResults ?? []), newResult]);
  };

  const updateTestingResult = (index: number, field: keyof TestingResult, value: any) => {
    const updated = [...(data.testingResults ?? [])];
    updated[index] = { ...updated[index], [field]: value };
    handleChange('testingResults', updated);
  };

  const removeTestingResult = (index: number) => {
    handleChange('testingResults', (data.testingResults ?? []).filter((_, i) => i !== index));
  };

  const addStandard = () => {
    handleChange('complianceStandards', [...(data.complianceStandards ?? []), 'New Standard']);
  };

  const updateStandard = (index: number, value: string) => {
    const updated = [...(data.complianceStandards ?? [])];
    updated[index] = value;
    handleChange('complianceStandards', updated);
  };

  const removeStandard = (index: number) => {
    handleChange('complianceStandards', (data.complianceStandards ?? []).filter((_, i) => i !== index));
  };

  return (
    <div className="space-y-6">
      <div className="flex gap-4 border-b">
        <button
          onClick={() => setActiveTab('edit')}
          className={`px-6 py-3 font-semibold border-b-2 transition-colors ${
            activeTab === 'edit'
              ? 'border-primary-600 text-primary-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          Edit Data
        </button>
        <button
          onClick={() => setActiveTab('preview')}
          className={`px-6 py-3 font-semibold border-b-2 transition-colors ${
            activeTab === 'preview'
              ? 'border-primary-600 text-primary-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          Preview
        </button>
      </div>

      {activeTab === 'edit' ? (
        <div className="card space-y-6">
          <h3 className="text-xl font-bold">Basic Information</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="label">Company Name</label>
              <input
                type="text"
                value={data.companyName}
                onChange={e => handleChange('companyName', e.target.value)}
                className="input-field"
              />
            </div>
            <div>
              <label className="label">Robot Model</label>
              <input
                type="text"
                value={data.robotModel}
                onChange={e => handleChange('robotModel', e.target.value)}
                className="input-field"
              />
            </div>
            <div>
              <label className="label">SIL Rating</label>
              <input
                type="text"
                value={data.silRating}
                onChange={e => handleChange('silRating', e.target.value)}
                className="input-field"
              />
            </div>
            <div>
              <label className="label">Operational Hours</label>
              <input
                type="number"
                value={data.operationalHours}
                onChange={e => handleChange('operationalHours', parseInt(e.target.value))}
                className="input-field"
              />
            </div>
            <div>
              <label className="label">Certification Body</label>
              <input
                type="text"
                value={data.certificationBody}
                onChange={e => handleChange('certificationBody', e.target.value)}
                className="input-field"
              />
            </div>
            <div>
              <label className="label">Certificate Number</label>
              <input
                type="text"
                value={data.certificateNumber}
                onChange={e => handleChange('certificateNumber', e.target.value)}
                className="input-field"
              />
            </div>
          </div>

          <h3 className="text-xl font-bold mt-8">Safety Metrics</h3>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="label">Hazards Identified</label>
              <input
                type="number"
                value={data.hazardsIdentified}
                onChange={e => handleChange('hazardsIdentified', parseInt(e.target.value))}
                className="input-field"
              />
            </div>
            <div>
              <label className="label">Risk Score</label>
              <input
                type="number"
                value={data.riskScore}
                onChange={e => handleChange('riskScore', parseInt(e.target.value))}
                className="input-field"
              />
            </div>
            <div>
              <label className="label">Compliance Rate (%)</label>
              <input
                type="number"
                value={data.complianceRate}
                onChange={e => handleChange('complianceRate', parseInt(e.target.value))}
                className="input-field"
              />
            </div>
            <div>
              <label className="label">Test Coverage (%)</label>
              <input
                type="number"
                value={data.testCoverage}
                onChange={e => handleChange('testCoverage', parseInt(e.target.value))}
                className="input-field"
              />
            </div>
            <div>
              <label className="label">Incident Rate</label>
              <input
                type="number"
                step="0.01"
                value={data.incidentRate}
                onChange={e => handleChange('incidentRate', parseFloat(e.target.value))}
                className="input-field"
              />
            </div>
          </div>

          <h3 className="text-xl font-bold mt-8">Compliance Standards</h3>
          <div className="space-y-2">
            {(data.complianceStandards ?? []).map((standard, index) => (
              <div key={index} className="flex gap-2">
                <input
                  type="text"
                  value={standard}
                  onChange={e => updateStandard(index, e.target.value)}
                  className="input-field flex-1"
                />
                <button
                  onClick={() => removeStandard(index)}
                  className="px-4 py-2 text-red-600 hover:bg-red-50 rounded"
                >
                  Remove
                </button>
              </div>
            ))}
            <button onClick={addStandard} className="btn-secondary">
              + Add Standard
            </button>
          </div>

          <h3 className="text-xl font-bold mt-8">Risk Assessments</h3>
          <div className="space-y-4">
            {(data.riskAssessments ?? []).map((assessment, index) => (
              <div key={index} className="border p-4 rounded-lg">
                <div className="grid grid-cols-2 gap-4 mb-2">
                  <div className="col-span-2">
                    <label className="label">Scenario</label>
                    <input
                      type="text"
                      value={assessment.scenario}
                      onChange={e => updateRiskAssessment(index, 'scenario', e.target.value)}
                      className="input-field"
                    />
                  </div>
                  <div>
                    <label className="label">Severity</label>
                    <select
                      value={assessment.severity}
                      onChange={e => updateRiskAssessment(index, 'severity', e.target.value)}
                      className="input-field"
                    >
                      <option>Low</option>
                      <option>Medium</option>
                      <option>High</option>
                      <option>Critical</option>
                    </select>
                  </div>
                  <div>
                    <label className="label">Likelihood</label>
                    <select
                      value={assessment.likelihood}
                      onChange={e => updateRiskAssessment(index, 'likelihood', e.target.value)}
                      className="input-field"
                    >
                      <option>Low</option>
                      <option>Medium</option>
                      <option>High</option>
                    </select>
                  </div>
                  <div>
                    <label className="label">Risk Level</label>
                    <select
                      value={assessment.riskLevel}
                      onChange={e => updateRiskAssessment(index, 'riskLevel', e.target.value)}
                      className="input-field"
                    >
                      <option>Low</option>
                      <option>Medium</option>
                      <option>High</option>
                    </select>
                  </div>
                  <div>
                    <label className="label">Status</label>
                    <select
                      value={assessment.status}
                      onChange={e => updateRiskAssessment(index, 'status', e.target.value)}
                      className="input-field"
                    >
                      <option>Pending</option>
                      <option>In Progress</option>
                      <option>Mitigated</option>
                      <option>Approved</option>
                    </select>
                  </div>
                </div>
                <button
                  onClick={() => removeRiskAssessment(index)}
                  className="text-red-600 hover:text-red-700 text-sm"
                >
                  Remove Assessment
                </button>
              </div>
            ))}
            <button onClick={addRiskAssessment} className="btn-secondary">
              + Add Risk Assessment
            </button>
          </div>

          <h3 className="text-xl font-bold mt-8">Testing Results</h3>
          <div className="space-y-4">
            {(data.testingResults ?? []).map((result, index) => (
              <div key={index} className="border p-4 rounded-lg">
                <div className="grid grid-cols-2 gap-4 mb-2">
                  <div className="col-span-2">
                    <label className="label">Category</label>
                    <input
                      type="text"
                      value={result.category}
                      onChange={e => updateTestingResult(index, 'category', e.target.value)}
                      className="input-field"
                    />
                  </div>
                  <div>
                    <label className="label">Scenarios</label>
                    <input
                      type="number"
                      value={result.scenarios}
                      onChange={e => updateTestingResult(index, 'scenarios', parseInt(e.target.value))}
                      className="input-field"
                    />
                  </div>
                  <div>
                    <label className="label">Cycles</label>
                    <input
                      type="number"
                      value={result.cycles}
                      onChange={e => updateTestingResult(index, 'cycles', parseInt(e.target.value))}
                      className="input-field"
                    />
                  </div>
                  <div className="col-span-2">
                    <label className="label">Pass Rate (%)</label>
                    <input
                      type="number"
                      value={result.passRate}
                      onChange={e => updateTestingResult(index, 'passRate', parseFloat(e.target.value))}
                      className="input-field"
                    />
                  </div>
                </div>
                <button
                  onClick={() => removeTestingResult(index)}
                  className="text-red-600 hover:text-red-700 text-sm"
                >
                  Remove Result
                </button>
              </div>
            ))}
            <button onClick={addTestingResult} className="btn-secondary">
              + Add Testing Result
            </button>
          </div>
        </div>
      ) : (
        <div className="card">
          <h3 className="text-xl font-bold mb-4">Preview</h3>
          <div
            className="border rounded-lg p-4 bg-white"
            dangerouslySetInnerHTML={{ __html: templateHtml }}
          />
        </div>
      )}
    </div>
  );
}
