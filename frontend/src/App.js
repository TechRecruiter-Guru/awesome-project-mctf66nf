import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import BooleanGenerator from './components/BooleanGenerator';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [candidates, setCandidates] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState('checking...');
  const [showCandidateForm, setShowCandidateForm] = useState(false);
  const [showJobForm, setShowJobForm] = useState(false);

  useEffect(() => {
    checkApiHealth();
    fetchStats();
    if (activeTab === 'candidates') {
      fetchCandidates();
    } else if (activeTab === 'jobs') {
      fetchJobs();
    }
  }, [activeTab]);

  const checkApiHealth = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/health`);
      setApiStatus(response.data.status);
    } catch (err) {
      setApiStatus('unhealthy');
      console.error('API health check failed:', err);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/stats`);
      setStats(response.data);
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  };

  const fetchCandidates = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/api/candidates`);
      setCandidates(response.data.candidates || []);
    } catch (err) {
      console.error('Error fetching candidates:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/api/jobs`);
      setJobs(response.data.jobs || []);
    } catch (err) {
      console.error('Error fetching jobs:', err);
    } finally {
      setLoading(false);
    }
  };

  const deleteCandidate = async (id) => {
    if (!window.confirm('Are you sure you want to delete this candidate?')) return;
    try {
      await axios.delete(`${API_URL}/api/candidates/${id}`);
      fetchCandidates();
      fetchStats();
    } catch (err) {
      console.error('Error deleting candidate:', err);
    }
  };

  const deleteJob = async (id) => {
    if (!window.confirm('Are you sure you want to delete this job?')) return;
    try {
      await axios.delete(`${API_URL}/api/jobs/${id}`);
      fetchJobs();
      fetchStats();
    } catch (err) {
      console.error('Error deleting job:', err);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <h1>🤖 AI/ML Applicant Tracking System</h1>
          <div className={`api-status ${apiStatus === 'healthy' ? 'healthy' : 'unhealthy'}`}>
            API: {apiStatus}
          </div>
        </div>
        <p className="tagline">Track candidates with research profiles, publications & academic credentials</p>
      </header>

      <nav className="nav-tabs">
        <button
          className={activeTab === 'dashboard' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('dashboard')}
        >
          📊 Dashboard
        </button>
        <button
          className={activeTab === 'candidates' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('candidates')}
        >
          👥 Candidates ({stats.total_candidates || 0})
        </button>
        <button
          className={activeTab === 'jobs' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('jobs')}
        >
          💼 Jobs ({stats.total_jobs || 0})
        </button>
        <button
          className={activeTab === 'analytics' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('analytics')}
        >
          📈 Analytics
        </button>
        <button
          className={activeTab === 'campaigns' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('campaigns')}
        >
          📧 Campaigns
        </button>
        <button
          className={activeTab === 'interviews' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('interviews')}
        >
          🗓️ Interviews
        </button>
        <button
          className={activeTab === 'offers' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('offers')}
        >
          💰 Offers
        </button>
        <button
          className={activeTab === 'boolean' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('boolean')}
        >
          🔍 Search
        </button>
      </nav>

      <main className="main-content">
        {activeTab === 'dashboard' && <DashboardView stats={stats} />}
        {activeTab === 'candidates' && (
          <CandidatesView
            candidates={candidates}
            loading={loading}
            onDelete={deleteCandidate}
            showForm={showCandidateForm}
            setShowForm={setShowCandidateForm}
            onRefresh={fetchCandidates}
          />
        )}
        {activeTab === 'jobs' && (
          <JobsView
            jobs={jobs}
            loading={loading}
            onDelete={deleteJob}
            showForm={showJobForm}
            setShowForm={setShowJobForm}
            onRefresh={fetchJobs}
          />
        )}
        {activeTab === 'analytics' && <AnalyticsView />}
        {activeTab === 'campaigns' && <CampaignsView />}
        {activeTab === 'interviews' && <InterviewsView />}
        {activeTab === 'offers' && <OffersView />}
        {activeTab === 'boolean' && <BooleanGenerator onStatsRefresh={fetchStats} />}
      </main>

      <footer className="app-footer">
        <p>Built for recruiting AI/ML talent through research profiles 🎓 | Open Source Project</p>
      </footer>
    </div>
  );
}

// Dashboard View
function DashboardView({ stats }) {
  return (
    <div className="dashboard">
      <h2>Dashboard Overview</h2>
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{stats.total_candidates || 0}</div>
          <div className="stat-label">Total Candidates</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.total_jobs || 0}</div>
          <div className="stat-label">Open Positions</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.total_applications || 0}</div>
          <div className="stat-label">Applications</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.active_candidates || 0}</div>
          <div className="stat-label">Active Candidates</div>
        </div>
      </div>

      <div className="unique-features">
        <h3>🌟 Unique ATS Features</h3>
        <ul>
          <li>📄 <strong>Research Paper Tracking</strong> - Track publications from arXiv, Google Scholar</li>
          <li>🎓 <strong>Academic Profiles</strong> - H-index, citations, ORCID integration</li>
          <li>🔬 <strong>Research Focus Areas</strong> - Computer Vision, NLP, RL, etc.</li>
          <li>📚 <strong>Publication History</strong> - Link candidates to their research papers</li>
          <li>🏆 <strong>Research Scoring</strong> - Evaluate candidates based on research impact</li>
        </ul>
      </div>
    </div>
  );
}

// Candidates View
function CandidatesView({ candidates, loading, onDelete, showForm, setShowForm, onRefresh }) {
  const [newCandidate, setNewCandidate] = useState({
    first_name: '',
    last_name: '',
    email: '',
    primary_expertise: '',
    google_scholar_url: '',
    github_url: '',
    orcid_id: ''
  });
  const [enriching, setEnriching] = useState({});
  const [impactScores, setImpactScores] = useState({});

  // Enrich candidate from various sources
  const enrichCandidate = async (candidateId, source) => {
    setEnriching(prev => ({ ...prev, [`${candidateId}-${source}`]: true }));
    try {
      const response = await axios.post(`${API_URL}/api/candidates/${candidateId}/enrich/${source}`);
      alert(`✅ ${response.data.message}`);
      onRefresh();
    } catch (err) {
      alert(`❌ Error: ${err.response?.data?.error || err.message}`);
    } finally {
      setEnriching(prev => ({ ...prev, [`${candidateId}-${source}`]: false }));
    }
  };

  // Extract skills from candidate
  const extractSkills = async (candidateId) => {
    setEnriching(prev => ({ ...prev, [`${candidateId}-skills`]: true }));
    try {
      const response = await axios.post(`${API_URL}/api/candidates/${candidateId}/extract-skills`);
      alert(`✅ Extracted ${response.data.skills_extracted} skills!`);
      onRefresh();
    } catch (err) {
      alert(`❌ Error: ${err.response?.data?.error || err.message}`);
    } finally {
      setEnriching(prev => ({ ...prev, [`${candidateId}-skills`]: false }));
    }
  };

  // Get impact score for candidate
  const getImpactScore = async (candidateId) => {
    try {
      const response = await axios.get(`${API_URL}/api/candidates/${candidateId}/impact-score`);
      setImpactScores(prev => ({ ...prev, [candidateId]: response.data }));
    } catch (err) {
      alert(`❌ Error: ${err.response?.data?.error || err.message}`);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/api/candidates`, newCandidate);
      setNewCandidate({ first_name: '', last_name: '', email: '', primary_expertise: '', google_scholar_url: '', github_url: '', orcid_id: '' });
      setShowForm(false);
      onRefresh();
    } catch (err) {
      alert('Error creating candidate: ' + (err.response?.data?.error || err.message));
    }
  };

  return (
    <div className="candidates-view">
      <div className="view-header">
        <h2>AI/ML Candidates</h2>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Add Candidate'}
        </button>
      </div>

      {showForm && (
        <form className="candidate-form" onSubmit={handleSubmit}>
          <h3>Add New Candidate</h3>
          <div className="form-row">
            <input
              type="text"
              placeholder="First Name *"
              value={newCandidate.first_name}
              onChange={(e) => setNewCandidate({ ...newCandidate, first_name: e.target.value })}
              required
            />
            <input
              type="text"
              placeholder="Last Name *"
              value={newCandidate.last_name}
              onChange={(e) => setNewCandidate({ ...newCandidate, last_name: e.target.value })}
              required
            />
          </div>
          <input
            type="email"
            placeholder="Email *"
            value={newCandidate.email}
            onChange={(e) => setNewCandidate({ ...newCandidate, email: e.target.value })}
            required
          />
          <input
            type="text"
            placeholder="Primary Expertise (e.g., Computer Vision, NLP)"
            value={newCandidate.primary_expertise}
            onChange={(e) => setNewCandidate({ ...newCandidate, primary_expertise: e.target.value })}
          />
          <input
            type="url"
            placeholder="GitHub URL"
            value={newCandidate.github_url}
            onChange={(e) => setNewCandidate({ ...newCandidate, github_url: e.target.value })}
          />
          <input
            type="url"
            placeholder="Google Scholar URL"
            value={newCandidate.google_scholar_url}
            onChange={(e) => setNewCandidate({ ...newCandidate, google_scholar_url: e.target.value })}
          />
          <input
            type="text"
            placeholder="ORCID ID (e.g., 0000-0002-1234-5678)"
            value={newCandidate.orcid_id}
            onChange={(e) => setNewCandidate({ ...newCandidate, orcid_id: e.target.value })}
          />
          <button type="submit" className="btn-primary">Create Candidate</button>
        </form>
      )}

      {loading ? (
        <div className="loading">Loading candidates...</div>
      ) : candidates.length === 0 ? (
        <div className="empty-state">
          <p>No candidates yet. Add your first AI/ML candidate!</p>
        </div>
      ) : (
        <div className="candidates-list">
          {candidates.map((candidate) => (
            <div key={candidate.id} className="candidate-card">
              <div className="candidate-header">
                <h3>{candidate.full_name}</h3>
                <span className={`status-badge ${candidate.status}`}>{candidate.status}</span>
              </div>
              <p className="email">{candidate.email}</p>

              {candidate.bio && (
                <p className="bio" style={{ fontStyle: 'italic', color: '#666', marginTop: '8px', marginBottom: '8px' }}>
                  "{candidate.bio}"
                </p>
              )}

              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '8px', marginBottom: '8px' }}>
                {candidate.location && (
                  <span style={{ fontSize: '0.85rem', padding: '4px 8px', background: '#f0f0f0', borderRadius: '4px' }}>
                    📍 {candidate.location}
                  </span>
                )}
                {candidate.company && (
                  <span style={{ fontSize: '0.85rem', padding: '4px 8px', background: '#f0f0f0', borderRadius: '4px' }}>
                    🏢 {candidate.company}
                  </span>
                )}
              </div>

              {candidate.primary_expertise && (
                <p className="expertise">🎯 {candidate.primary_expertise}</p>
              )}

              {candidate.skills && (
                <div style={{ marginTop: '8px', marginBottom: '8px' }}>
                  <strong style={{ fontSize: '0.85rem', color: '#666' }}>Languages:</strong>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginTop: '4px' }}>
                    {candidate.skills.split(',').map((skill, i) => (
                      <span key={i} style={{ fontSize: '0.8rem', padding: '3px 8px', background: '#2563eb', color: 'white', borderRadius: '4px' }}>
                        💻 {skill.trim()}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <div className="candidate-details">
                {candidate.google_scholar_url && (
                  <a href={candidate.google_scholar_url} target="_blank" rel="noopener noreferrer">
                    🎓 Google Scholar
                  </a>
                )}
                {candidate.github_url && (
                  <a href={candidate.github_url} target="_blank" rel="noopener noreferrer">
                    💻 GitHub
                  </a>
                )}
              </div>

              <div className="research-stats">
                {candidate.github_followers > 0 && <span>👥 {candidate.github_followers} followers</span>}
                {candidate.github_repos > 0 && <span>📦 {candidate.github_repos} repos</span>}
                {candidate.h_index && <span>H-index: {candidate.h_index}</span>}
                {candidate.citation_count && <span>Citations: {candidate.citation_count}</span>}
                {candidate.publication_count > 0 && <span>Publications: {candidate.publication_count}</span>}
              </div>
              {/* Impact Score Display */}
              {impactScores[candidate.id] && (
                <div style={{ background: '#f0fdf4', padding: '12px', borderRadius: '8px', marginTop: '12px', marginBottom: '12px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <strong style={{ color: '#166534' }}>🏆 Impact Score: {impactScores[candidate.id].impact_score}/100</strong>
                    <span style={{ background: '#dcfce7', padding: '4px 8px', borderRadius: '4px', fontSize: '0.8rem', color: '#166534' }}>
                      {impactScores[candidate.id].tier}
                    </span>
                  </div>
                </div>
              )}

              {/* Enrichment Actions */}
              <div style={{ background: '#f8fafc', padding: '12px', borderRadius: '8px', marginTop: '12px' }}>
                <div style={{ fontSize: '0.85rem', fontWeight: '600', marginBottom: '8px', color: '#475569' }}>
                  🔄 Auto-Enrich Profile
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {candidate.github_url && (
                    <button
                      onClick={() => enrichCandidate(candidate.id, 'github')}
                      disabled={enriching[`${candidate.id}-github`]}
                      style={{ fontSize: '0.75rem', padding: '4px 8px', background: '#1f2937', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
                    >
                      {enriching[`${candidate.id}-github`] ? '...' : '💻 GitHub'}
                    </button>
                  )}
                  <button
                    onClick={() => enrichCandidate(candidate.id, 'arxiv')}
                    disabled={enriching[`${candidate.id}-arxiv`]}
                    style={{ fontSize: '0.75rem', padding: '4px 8px', background: '#b91c1c', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
                  >
                    {enriching[`${candidate.id}-arxiv`] ? '...' : '📄 arXiv'}
                  </button>
                  {candidate.orcid_id && (
                    <button
                      onClick={() => enrichCandidate(candidate.id, 'orcid')}
                      disabled={enriching[`${candidate.id}-orcid`]}
                      style={{ fontSize: '0.75rem', padding: '4px 8px', background: '#a3e635', color: '#1a2e05', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
                    >
                      {enriching[`${candidate.id}-orcid`] ? '...' : '🆔 ORCID'}
                    </button>
                  )}
                  {candidate.google_scholar_url && (
                    <button
                      onClick={() => enrichCandidate(candidate.id, 'scholar')}
                      disabled={enriching[`${candidate.id}-scholar`]}
                      style={{ fontSize: '0.75rem', padding: '4px 8px', background: '#4285f4', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
                    >
                      {enriching[`${candidate.id}-scholar`] ? '...' : '🎓 Scholar'}
                    </button>
                  )}
                  <button
                    onClick={() => extractSkills(candidate.id)}
                    disabled={enriching[`${candidate.id}-skills`]}
                    style={{ fontSize: '0.75rem', padding: '4px 8px', background: '#7c3aed', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
                  >
                    {enriching[`${candidate.id}-skills`] ? '...' : '🧠 Extract Skills'}
                  </button>
                  <button
                    onClick={() => getImpactScore(candidate.id)}
                    style={{ fontSize: '0.75rem', padding: '4px 8px', background: '#059669', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
                  >
                    📊 Impact Score
                  </button>
                </div>
              </div>

              <div className="card-actions">
                <button className="btn-delete" onClick={() => onDelete(candidate.id)}>Delete</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// Jobs View
function JobsView({ jobs, loading, onDelete, showForm, setShowForm, onRefresh }) {
  const [newJob, setNewJob] = useState({
    title: '',
    company: '',
    required_expertise: '',
    required_skills: '',
    education_required: '',
    confidential: false
  });
  const [matchResults, setMatchResults] = useState({});
  const [matching, setMatching] = useState({});

  // Match candidates to a job
  const matchCandidates = async (jobId) => {
    setMatching(prev => ({ ...prev, [jobId]: true }));
    try {
      const response = await axios.post(`${API_URL}/api/jobs/${jobId}/match-candidates`, {
        min_score: 0,
        top_n: 5
      });
      setMatchResults(prev => ({ ...prev, [jobId]: response.data }));
    } catch (err) {
      alert(`❌ Error: ${err.response?.data?.error || err.message}`);
    } finally {
      setMatching(prev => ({ ...prev, [jobId]: false }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/api/jobs`, newJob);
      setNewJob({ title: '', company: '', required_expertise: '', required_skills: '', education_required: '', confidential: false });
      setShowForm(false);
      onRefresh();
    } catch (err) {
      alert('Error creating job: ' + (err.response?.data?.error || err.message));
    }
  };

  return (
    <div className="jobs-view">
      <div className="view-header">
        <h2>AI/ML Job Positions</h2>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Add Job'}
        </button>
      </div>

      {showForm && (
        <form className="job-form" onSubmit={handleSubmit}>
          <h3>Add New Job</h3>
          <input
            type="text"
            placeholder="Job Title *"
            value={newJob.title}
            onChange={(e) => setNewJob({ ...newJob, title: e.target.value })}
            required
          />
          <input
            type="text"
            placeholder="Company *"
            value={newJob.company}
            onChange={(e) => setNewJob({ ...newJob, company: e.target.value })}
            required
          />
          <input
            type="text"
            placeholder="Required Expertise (e.g., Deep Learning, MLOps)"
            value={newJob.required_expertise}
            onChange={(e) => setNewJob({ ...newJob, required_expertise: e.target.value })}
          />
          <input
            type="text"
            placeholder="Required Skills (comma-separated: python, pytorch, tensorflow)"
            value={newJob.required_skills}
            onChange={(e) => setNewJob({ ...newJob, required_skills: e.target.value })}
          />
          <select
            value={newJob.education_required}
            onChange={(e) => setNewJob({ ...newJob, education_required: e.target.value })}
          >
            <option value="">Education Required</option>
            <option value="PhD">PhD</option>
            <option value="Masters">Masters</option>
            <option value="Bachelors">Bachelors</option>
          </select>
          <div className="checkbox-container">
            <label>
              <input
                type="checkbox"
                checked={newJob.confidential}
                onChange={(e) => setNewJob({ ...newJob, confidential: e.target.checked })}
              />
              <span className="checkbox-label">🔒 Confidential (Stealth Mode) - Hide company name from candidates</span>
            </label>
          </div>
          <button type="submit" className="btn-primary">Create Job</button>
        </form>
      )}

      {loading ? (
        <div className="loading">Loading jobs...</div>
      ) : jobs.length === 0 ? (
        <div className="empty-state">
          <p>No job positions yet. Add your first AI/ML role!</p>
        </div>
      ) : (
        <div className="jobs-list">
          {jobs.map((job) => (
            <div key={job.id} className={`job-card ${job.confidential ? 'confidential' : ''}`}>
              <div className="job-header">
                <h3>{job.title}</h3>
                <span className={`status-badge ${job.status}`}>{job.status}</span>
              </div>
              <p className="company">
                {job.confidential && '🔒 '}
                🏢 {job.company}
                {job.confidential && ' (Confidential)'}
              </p>
              {job.required_expertise && <p>🎯 {job.required_expertise}</p>}
              {job.education_required && <p>🎓 {job.education_required} required</p>}
              {job.confidential && (
                <p className="stealth-notice">⚠️ Company name hidden until interest shown</p>
              )}
              {job.application_count > 0 && (
                <p className="applications-count">📋 {job.application_count} applications</p>
              )}

              {/* AI Matching Section */}
              <div style={{ background: '#f0f9ff', padding: '12px', borderRadius: '8px', marginTop: '12px' }}>
                <button
                  onClick={() => matchCandidates(job.id)}
                  disabled={matching[job.id]}
                  style={{
                    fontSize: '0.85rem',
                    padding: '8px 16px',
                    background: '#2563eb',
                    color: 'white',
                    border: 'none',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    width: '100%',
                    fontWeight: '600'
                  }}
                >
                  {matching[job.id] ? '🔄 Matching...' : '🎯 AI Match Candidates'}
                </button>

                {/* Match Results */}
                {matchResults[job.id] && (
                  <div style={{ marginTop: '12px' }}>
                    <div style={{ fontSize: '0.85rem', fontWeight: '600', color: '#1e40af', marginBottom: '8px' }}>
                      Found {matchResults[job.id].matches_found} matches:
                    </div>
                    {matchResults[job.id].top_matches.length === 0 ? (
                      <p style={{ fontSize: '0.8rem', color: '#64748b' }}>No matching candidates found.</p>
                    ) : (
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        {matchResults[job.id].top_matches.map((match, i) => (
                          <div key={i} style={{
                            background: 'white',
                            padding: '8px',
                            borderRadius: '6px',
                            border: '1px solid #e2e8f0',
                            fontSize: '0.8rem'
                          }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                              <strong>{match.candidate_name}</strong>
                              <span style={{
                                background: match.match_score >= 50 ? '#dcfce7' : '#fef3c7',
                                color: match.match_score >= 50 ? '#166534' : '#92400e',
                                padding: '2px 6px',
                                borderRadius: '4px',
                                fontWeight: '600'
                              }}>
                                {match.match_score}%
                              </span>
                            </div>
                            {match.primary_expertise && (
                              <div style={{ color: '#64748b', marginTop: '4px' }}>
                                🎯 {match.primary_expertise}
                              </div>
                            )}
                            {(match.h_index || match.citations) && (
                              <div style={{ color: '#64748b', marginTop: '2px' }}>
                                {match.h_index && `H-index: ${match.h_index}`}
                                {match.h_index && match.citations && ' • '}
                                {match.citations && `Citations: ${match.citations}`}
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>

              <div className="card-actions">
                <button className="btn-delete" onClick={() => onDelete(job.id)}>Delete</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// About View
function AboutView() {
  return (
    <div className="about-view">
      <h2>About This ATS</h2>
      <p>
        This is an <strong>AI/ML-focused Applicant Tracking System</strong> designed specifically
        for recruiting researchers, scientists, and AI/ML practitioners.
      </p>

      <h3>What Makes This ATS Different?</h3>
      <p>
        Traditional ATS platforms miss critical information when recruiting AI/ML talent.
        This system integrates with:
      </p>
      <ul>
        <li><strong>Google Scholar</strong> - Track publications and citations</li>
        <li><strong>arXiv</strong> - Research paper preprints</li>
        <li><strong>ResearchGate</strong> - Academic networking profiles</li>
        <li><strong>ORCID</strong> - Persistent digital identifiers for researchers</li>
      </ul>

      <h3>Key Features</h3>
      <ul>
        <li>Track candidates' research profiles and publications</li>
        <li>H-index and citation metrics</li>
        <li>Research area categorization (Computer Vision, NLP, RL, etc.)</li>
        <li>Publication history linked to candidates</li>
        <li>Research-based scoring system</li>
        <li>Integration-ready for academic APIs</li>
      </ul>

      <h3>Future Integrations (Roadmap)</h3>
      <ul>
        <li>🔄 Google Scholar API integration</li>
        <li>🔄 arXiv API for automatic paper fetching</li>
        <li>🔄 AI-powered candidate-job matching</li>
        <li>🔄 Research impact scoring algorithm</li>
        <li>🔄 Conference publication tracking (NeurIPS, ICML, CVPR, etc.)</li>
      </ul>

      <div className="cta-section">
        <h3>Open Source & Contributor-Friendly</h3>
        <p>
          This project is open source and welcomes contributions! Check out the GitHub repository
          to contribute features, integrations, or improvements.
        </p>
      </div>
    </div>
  );
}

// Analytics View
function AnalyticsView() {
  const [analytics, setAnalytics] = useState(null);
  const [funnel, setFunnel] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const [overviewRes, funnelRes] = await Promise.all([
        axios.get(`${API_URL}/api/analytics/overview`),
        axios.get(`${API_URL}/api/analytics/pipeline-funnel`)
      ]);
      setAnalytics(overviewRes.data);
      setFunnel(funnelRes.data);
    } catch (err) {
      console.error('Error fetching analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading analytics...</div>;
  if (!analytics) return <div className="error">Failed to load analytics</div>;

  return (
    <div className="analytics-view">
      <h2>📈 Analytics Dashboard</h2>

      {/* Pipeline Overview */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{analytics.pipeline.total_candidates}</div>
          <div className="stat-label">Total Candidates</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{analytics.pipeline.total_jobs}</div>
          <div className="stat-label">Total Jobs</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{analytics.interviews.upcoming}</div>
          <div className="stat-label">Upcoming Interviews</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{analytics.offers.pending}</div>
          <div className="stat-label">Pending Offers</div>
        </div>
      </div>

      {/* Conversion Rates */}
      <div style={{ marginTop: '24px', background: '#f8fafc', padding: '20px', borderRadius: '12px' }}>
        <h3 style={{ marginBottom: '16px' }}>📊 Conversion Rates</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
          <div style={{ textAlign: 'center', padding: '16px', background: 'white', borderRadius: '8px' }}>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#2563eb' }}>
              {analytics.conversion_rates.interview_rate}%
            </div>
            <div style={{ color: '#64748b' }}>Interview Rate</div>
          </div>
          <div style={{ textAlign: 'center', padding: '16px', background: 'white', borderRadius: '8px' }}>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#7c3aed' }}>
              {analytics.conversion_rates.offer_rate}%
            </div>
            <div style={{ color: '#64748b' }}>Offer Rate</div>
          </div>
          <div style={{ textAlign: 'center', padding: '16px', background: 'white', borderRadius: '8px' }}>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#059669' }}>
              {analytics.conversion_rates.hire_rate}%
            </div>
            <div style={{ color: '#64748b' }}>Hire Rate</div>
          </div>
        </div>
      </div>

      {/* Pipeline Funnel */}
      {funnel && (
        <div style={{ marginTop: '24px', background: '#f0fdf4', padding: '20px', borderRadius: '12px' }}>
          <h3 style={{ marginBottom: '16px' }}>🎯 Pipeline Funnel</h3>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            {Object.entries(funnel.funnel).map(([stage, count], i) => (
              <div key={stage} style={{ textAlign: 'center', flex: 1 }}>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#166534' }}>{count}</div>
                <div style={{ fontSize: '0.8rem', color: '#166534', textTransform: 'capitalize' }}>{stage}</div>
                {i < Object.keys(funnel.funnel).length - 1 && (
                  <span style={{ position: 'absolute', marginLeft: '20px' }}>→</span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Candidate Status Breakdown */}
      <div style={{ marginTop: '24px', background: 'white', padding: '20px', borderRadius: '12px', border: '1px solid #e2e8f0' }}>
        <h3 style={{ marginBottom: '16px' }}>👥 Candidate Status Breakdown</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px' }}>
          {Object.entries(analytics.candidate_statuses).map(([status, count]) => (
            <div key={status} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px', background: '#f8fafc', borderRadius: '6px' }}>
              <span style={{ textTransform: 'capitalize' }}>{status}</span>
              <strong>{count}</strong>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// Campaigns View
function CampaignsView() {
  const [campaigns, setCampaigns] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [newCampaign, setNewCampaign] = useState({ name: '', subject: '', body: '' });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCampaigns();
  }, []);

  const fetchCampaigns = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/campaigns`);
      setCampaigns(response.data.campaigns || []);
    } catch (err) {
      console.error('Error fetching campaigns:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/api/campaigns`, newCampaign);
      setNewCampaign({ name: '', subject: '', body: '' });
      setShowForm(false);
      fetchCampaigns();
    } catch (err) {
      alert('Error creating campaign: ' + (err.response?.data?.error || err.message));
    }
  };

  const sendCampaign = async (campaignId) => {
    if (!window.confirm('Send this campaign to all active candidates?')) return;
    try {
      const response = await axios.post(`${API_URL}/api/campaigns/${campaignId}/send`);
      alert(`✅ ${response.data.message}`);
      fetchCampaigns();
    } catch (err) {
      alert('Error sending campaign: ' + (err.response?.data?.error || err.message));
    }
  };

  const deleteCampaign = async (id) => {
    if (!window.confirm('Delete this campaign?')) return;
    try {
      await axios.delete(`${API_URL}/api/campaigns/${id}`);
      fetchCampaigns();
    } catch (err) {
      alert('Error deleting campaign: ' + err.message);
    }
  };

  return (
    <div className="campaigns-view">
      <div className="view-header">
        <h2>📧 Email Campaigns</h2>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Create Campaign'}
        </button>
      </div>

      {showForm && (
        <form className="campaign-form" onSubmit={handleSubmit} style={{ background: '#f8fafc', padding: '20px', borderRadius: '12px', marginBottom: '20px' }}>
          <h3>Create New Campaign</h3>
          <input
            type="text"
            placeholder="Campaign Name *"
            value={newCampaign.name}
            onChange={(e) => setNewCampaign({ ...newCampaign, name: e.target.value })}
            required
            style={{ width: '100%', padding: '10px', marginBottom: '10px', borderRadius: '6px', border: '1px solid #e2e8f0' }}
          />
          <input
            type="text"
            placeholder="Email Subject *"
            value={newCampaign.subject}
            onChange={(e) => setNewCampaign({ ...newCampaign, subject: e.target.value })}
            required
            style={{ width: '100%', padding: '10px', marginBottom: '10px', borderRadius: '6px', border: '1px solid #e2e8f0' }}
          />
          <textarea
            placeholder="Email Body *"
            value={newCampaign.body}
            onChange={(e) => setNewCampaign({ ...newCampaign, body: e.target.value })}
            required
            rows={6}
            style={{ width: '100%', padding: '10px', marginBottom: '10px', borderRadius: '6px', border: '1px solid #e2e8f0' }}
          />
          <button type="submit" className="btn-primary">Create Campaign</button>
        </form>
      )}

      {loading ? (
        <div className="loading">Loading campaigns...</div>
      ) : campaigns.length === 0 ? (
        <div className="empty-state">
          <p>No campaigns yet. Create your first email campaign!</p>
        </div>
      ) : (
        <div className="campaigns-list" style={{ display: 'grid', gap: '16px' }}>
          {campaigns.map((campaign) => (
            <div key={campaign.id} style={{ background: 'white', padding: '20px', borderRadius: '12px', border: '1px solid #e2e8f0' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                <h3 style={{ margin: 0 }}>{campaign.name}</h3>
                <span style={{
                  padding: '4px 12px',
                  borderRadius: '20px',
                  fontSize: '0.8rem',
                  background: campaign.status === 'sent' ? '#dcfce7' : campaign.status === 'draft' ? '#f3f4f6' : '#fef3c7',
                  color: campaign.status === 'sent' ? '#166534' : campaign.status === 'draft' ? '#374151' : '#92400e'
                }}>
                  {campaign.status}
                </span>
              </div>
              <p style={{ color: '#64748b', marginBottom: '8px' }}>📬 {campaign.subject}</p>
              {campaign.status === 'sent' && (
                <div style={{ display: 'flex', gap: '16px', fontSize: '0.85rem', color: '#64748b', marginBottom: '12px' }}>
                  <span>📤 {campaign.sent_count} sent</span>
                  <span>👁️ {campaign.open_rate}% opened</span>
                  <span>🖱️ {campaign.click_rate}% clicked</span>
                  <span>💬 {campaign.reply_rate}% replied</span>
                </div>
              )}
              <div style={{ display: 'flex', gap: '8px' }}>
                {campaign.status === 'draft' && (
                  <button
                    onClick={() => sendCampaign(campaign.id)}
                    style={{ padding: '6px 12px', background: '#2563eb', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}
                  >
                    📤 Send Campaign
                  </button>
                )}
                <button
                  onClick={() => deleteCampaign(campaign.id)}
                  style={{ padding: '6px 12px', background: '#fee2e2', color: '#991b1b', border: 'none', borderRadius: '6px', cursor: 'pointer' }}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// Interviews View
function InterviewsView() {
  const [interviews, setInterviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchInterviews();
  }, []);

  const fetchInterviews = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/interviews`);
      setInterviews(response.data.interviews || []);
    } catch (err) {
      console.error('Error fetching interviews:', err);
    } finally {
      setLoading(false);
    }
  };

  const updateStatus = async (id, status) => {
    try {
      await axios.put(`${API_URL}/api/interviews/${id}`, { status });
      fetchInterviews();
    } catch (err) {
      alert('Error updating interview: ' + err.message);
    }
  };

  const deleteInterview = async (id) => {
    if (!window.confirm('Delete this interview?')) return;
    try {
      await axios.delete(`${API_URL}/api/interviews/${id}`);
      fetchInterviews();
    } catch (err) {
      alert('Error deleting interview: ' + err.message);
    }
  };

  return (
    <div className="interviews-view">
      <div className="view-header">
        <h2>🗓️ Interview Schedule</h2>
      </div>

      {loading ? (
        <div className="loading">Loading interviews...</div>
      ) : interviews.length === 0 ? (
        <div className="empty-state">
          <p>No interviews scheduled yet. Schedule interviews from candidate profiles.</p>
        </div>
      ) : (
        <div className="interviews-list" style={{ display: 'grid', gap: '16px' }}>
          {interviews.map((interview) => (
            <div key={interview.id} style={{ background: 'white', padding: '20px', borderRadius: '12px', border: '1px solid #e2e8f0' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                <div>
                  <h3 style={{ margin: 0 }}>{interview.candidate_name}</h3>
                  <p style={{ color: '#64748b', margin: '4px 0' }}>for {interview.job_title}</p>
                </div>
                <span style={{
                  padding: '4px 12px',
                  borderRadius: '20px',
                  fontSize: '0.8rem',
                  background: interview.status === 'completed' ? '#dcfce7' : interview.status === 'scheduled' ? '#dbeafe' : '#fee2e2',
                  color: interview.status === 'completed' ? '#166534' : interview.status === 'scheduled' ? '#1e40af' : '#991b1b'
                }}>
                  {interview.status}
                </span>
              </div>
              <div style={{ display: 'flex', gap: '16px', fontSize: '0.85rem', color: '#64748b', marginBottom: '12px' }}>
                <span>📅 {new Date(interview.scheduled_at).toLocaleDateString()}</span>
                <span>🕐 {new Date(interview.scheduled_at).toLocaleTimeString()}</span>
                <span>⏱️ {interview.duration_minutes} min</span>
                <span>📹 {interview.interview_type}</span>
              </div>
              {interview.location && <p style={{ fontSize: '0.85rem', color: '#64748b' }}>📍 {interview.location}</p>}
              {interview.rating && <p style={{ fontSize: '0.85rem' }}>⭐ Rating: {interview.rating}/5</p>}
              <div style={{ display: 'flex', gap: '8px', marginTop: '12px' }}>
                {interview.status === 'scheduled' && (
                  <>
                    <button
                      onClick={() => updateStatus(interview.id, 'completed')}
                      style={{ padding: '6px 12px', background: '#059669', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}
                    >
                      ✅ Complete
                    </button>
                    <button
                      onClick={() => updateStatus(interview.id, 'cancelled')}
                      style={{ padding: '6px 12px', background: '#f59e0b', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}
                    >
                      ❌ Cancel
                    </button>
                  </>
                )}
                <button
                  onClick={() => deleteInterview(interview.id)}
                  style={{ padding: '6px 12px', background: '#fee2e2', color: '#991b1b', border: 'none', borderRadius: '6px', cursor: 'pointer' }}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// Offers View
function OffersView() {
  const [offers, setOffers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOffers();
  }, []);

  const fetchOffers = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/offers`);
      setOffers(response.data.offers || []);
    } catch (err) {
      console.error('Error fetching offers:', err);
    } finally {
      setLoading(false);
    }
  };

  const updateStatus = async (id, status) => {
    try {
      await axios.put(`${API_URL}/api/offers/${id}`, { status });
      fetchOffers();
    } catch (err) {
      alert('Error updating offer: ' + err.message);
    }
  };

  const deleteOffer = async (id) => {
    if (!window.confirm('Delete this offer?')) return;
    try {
      await axios.delete(`${API_URL}/api/offers/${id}`);
      fetchOffers();
    } catch (err) {
      alert('Error deleting offer: ' + err.message);
    }
  };

  const formatSalary = (salary) => {
    if (!salary) return 'N/A';
    return '$' + salary.toLocaleString();
  };

  return (
    <div className="offers-view">
      <div className="view-header">
        <h2>💰 Job Offers</h2>
      </div>

      {loading ? (
        <div className="loading">Loading offers...</div>
      ) : offers.length === 0 ? (
        <div className="empty-state">
          <p>No offers yet. Create offers for candidates who passed interviews.</p>
        </div>
      ) : (
        <div className="offers-list" style={{ display: 'grid', gap: '16px' }}>
          {offers.map((offer) => (
            <div key={offer.id} style={{ background: 'white', padding: '20px', borderRadius: '12px', border: '1px solid #e2e8f0' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                <div>
                  <h3 style={{ margin: 0 }}>{offer.candidate_name}</h3>
                  <p style={{ color: '#64748b', margin: '4px 0' }}>for {offer.job_title}</p>
                </div>
                <span style={{
                  padding: '4px 12px',
                  borderRadius: '20px',
                  fontSize: '0.8rem',
                  background: offer.status === 'accepted' ? '#dcfce7' : offer.status === 'sent' ? '#dbeafe' : offer.status === 'declined' ? '#fee2e2' : '#f3f4f6',
                  color: offer.status === 'accepted' ? '#166534' : offer.status === 'sent' ? '#1e40af' : offer.status === 'declined' ? '#991b1b' : '#374151'
                }}>
                  {offer.status}
                </span>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px', marginBottom: '12px' }}>
                <div style={{ background: '#f8fafc', padding: '12px', borderRadius: '8px', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#059669' }}>{formatSalary(offer.salary)}</div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Base Salary</div>
                </div>
                <div style={{ background: '#f8fafc', padding: '12px', borderRadius: '8px', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#7c3aed' }}>{offer.equity || 'N/A'}</div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Equity</div>
                </div>
                <div style={{ background: '#f8fafc', padding: '12px', borderRadius: '8px', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#2563eb' }}>{formatSalary(offer.signing_bonus)}</div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Signing Bonus</div>
                </div>
              </div>
              {offer.start_date && <p style={{ fontSize: '0.85rem', color: '#64748b' }}>📅 Start Date: {offer.start_date}</p>}
              <div style={{ display: 'flex', gap: '8px', marginTop: '12px' }}>
                {offer.status === 'draft' && (
                  <button
                    onClick={() => updateStatus(offer.id, 'sent')}
                    style={{ padding: '6px 12px', background: '#2563eb', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}
                  >
                    📤 Send Offer
                  </button>
                )}
                {offer.status === 'sent' && (
                  <>
                    <button
                      onClick={() => updateStatus(offer.id, 'accepted')}
                      style={{ padding: '6px 12px', background: '#059669', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}
                    >
                      ✅ Accepted
                    </button>
                    <button
                      onClick={() => updateStatus(offer.id, 'declined')}
                      style={{ padding: '6px 12px', background: '#dc2626', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}
                    >
                      ❌ Declined
                    </button>
                  </>
                )}
                <button
                  onClick={() => deleteOffer(offer.id)}
                  style={{ padding: '6px 12px', background: '#fee2e2', color: '#991b1b', border: 'none', borderRadius: '6px', cursor: 'pointer' }}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
