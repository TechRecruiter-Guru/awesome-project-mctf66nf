import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useParams } from 'react-router-dom';
import axios from 'axios';
import './App.css';
import BooleanGenerator from './components/BooleanGenerator';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// ==================== CANDIDATE LANDING PAGE ====================

function CandidateLandingPage() {
  const { jobId } = useParams();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    location: '',
    linkedin_url: '',
    github_url: '',
    portfolio_url: '',
    years_experience: '',
    primary_expertise: '',
    cover_letter: ''
  });

  useEffect(() => {
    fetchJob();
  }, [jobId]);

  const fetchJob = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/public/jobs/${jobId}`);
      setJob(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load job posting');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      await axios.post(`${API_URL}/api/public/apply`, {
        ...formData,
        job_id: parseInt(jobId),
        years_experience: formData.years_experience ? parseInt(formData.years_experience) : null
      });
      setSubmitted(true);
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to submit application');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="landing-page">
        <div className="landing-container">
          <div className="loading-spinner">Loading...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="landing-page">
        <div className="landing-container">
          <div className="error-message">
            <h2>Position Not Available</h2>
            <p>{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (submitted) {
    return (
      <div className="landing-page">
        <div className="landing-container">
          <div className="success-message">
            <div className="success-icon">✓</div>
            <h2>Application Submitted!</h2>
            <p>Thank you for applying for the <strong>{job.title}</strong> position.</p>
            <p>We'll review your application and get back to you soon.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="landing-page">
      <div className="landing-container">
        <div className="job-header">
          <div className="company-badge">
            {job.confidential ? '🔒 Stealth Mode' : job.company}
          </div>
          <h1>{job.title}</h1>
          <div className="job-meta">
            {job.location && <span>📍 {job.location}</span>}
            {job.job_type && <span>💼 {job.job_type}</span>}
            {job.salary_min && job.salary_max && (
              <span>💰 ${job.salary_min.toLocaleString()} - ${job.salary_max.toLocaleString()}</span>
            )}
          </div>
        </div>

        <div className="job-details">
          {job.description && (
            <div className="detail-section">
              <h3>About the Role</h3>
              <p>{job.description}</p>
            </div>
          )}

          {job.required_expertise && (
            <div className="detail-section">
              <h3>Required Expertise</h3>
              <p>{job.required_expertise}</p>
            </div>
          )}

          {job.requirements && (
            <div className="detail-section">
              <h3>Requirements</h3>
              <p>{job.requirements}</p>
            </div>
          )}

          {job.responsibilities && (
            <div className="detail-section">
              <h3>Responsibilities</h3>
              <p>{job.responsibilities}</p>
            </div>
          )}

          {job.research_focus && (
            <div className="detail-section">
              <h3>Research Focus</h3>
              <p>{job.research_focus}</p>
            </div>
          )}

          {job.education_required && (
            <div className="detail-section">
              <h3>Education</h3>
              <p>{job.education_required}</p>
            </div>
          )}
        </div>

        <div className="application-form">
          <h2>Apply Now</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label>First Name *</label>
                <input
                  type="text"
                  name="first_name"
                  value={formData.first_name}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Last Name *</label>
                <input
                  type="text"
                  name="last_name"
                  value={formData.last_name}
                  onChange={handleInputChange}
                  required
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Email *</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Phone</label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Location</label>
                <input
                  type="text"
                  name="location"
                  value={formData.location}
                  onChange={handleInputChange}
                  placeholder="City, Country"
                />
              </div>
              <div className="form-group">
                <label>Years of Experience</label>
                <input
                  type="number"
                  name="years_experience"
                  value={formData.years_experience}
                  onChange={handleInputChange}
                  min="0"
                  max="50"
                />
              </div>
            </div>

            <div className="form-group">
              <label>Primary Expertise</label>
              <select
                name="primary_expertise"
                value={formData.primary_expertise}
                onChange={handleInputChange}
              >
                <option value="">Select your expertise</option>
                <option value="Deep Learning">Deep Learning</option>
                <option value="Computer Vision">Computer Vision</option>
                <option value="NLP">Natural Language Processing</option>
                <option value="Reinforcement Learning">Reinforcement Learning</option>
                <option value="Robotics">Robotics</option>
                <option value="MLOps">MLOps</option>
                <option value="Data Science">Data Science</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div className="form-group">
              <label>LinkedIn URL</label>
              <input
                type="url"
                name="linkedin_url"
                value={formData.linkedin_url}
                onChange={handleInputChange}
                placeholder="https://linkedin.com/in/yourprofile"
              />
            </div>

            <div className="form-group">
              <label>GitHub URL</label>
              <input
                type="url"
                name="github_url"
                value={formData.github_url}
                onChange={handleInputChange}
                placeholder="https://github.com/yourusername"
              />
            </div>

            <div className="form-group">
              <label>Portfolio URL</label>
              <input
                type="url"
                name="portfolio_url"
                value={formData.portfolio_url}
                onChange={handleInputChange}
                placeholder="https://yourportfolio.com"
              />
            </div>

            <div className="form-group">
              <label>Cover Letter / Why This Role?</label>
              <textarea
                name="cover_letter"
                value={formData.cover_letter}
                onChange={handleInputChange}
                rows="5"
                placeholder="Tell us why you're interested in this position and what makes you a great fit..."
              />
            </div>

            <button
              type="submit"
              className="submit-btn"
              disabled={submitting}
            >
              {submitting ? 'Submitting...' : 'Submit Application'}
            </button>
          </form>
        </div>

        <div className="landing-footer">
          <p>Powered by AI/ML ATS</p>
        </div>
      </div>
    </div>
  );
}

// ==================== MAIN ATS APP ====================

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
          className={activeTab === 'boolean' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('boolean')}
        >
          🔍 Boolean Search
        </button>
        <button
          className={activeTab === 'about' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('about')}
        >
          ℹ️ About
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
        {activeTab === 'boolean' && <BooleanGenerator onStatsRefresh={fetchStats} />}
        {activeTab === 'about' && <AboutView />}
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

// ==================== APP WITH ROUTING ====================

function AppWithRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/apply/:jobId" element={<CandidateLandingPage />} />
        <Route path="/*" element={<App />} />
      </Routes>
    </Router>
  );
}

export default AppWithRouter;
