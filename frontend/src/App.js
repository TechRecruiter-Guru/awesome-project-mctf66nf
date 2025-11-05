import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

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
    google_scholar_url: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/api/candidates`, newCandidate);
      setNewCandidate({ first_name: '', last_name: '', email: '', primary_expertise: '', google_scholar_url: '' });
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
            placeholder="Google Scholar URL"
            value={newCandidate.google_scholar_url}
            onChange={(e) => setNewCandidate({ ...newCandidate, google_scholar_url: e.target.value })}
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
              {candidate.primary_expertise && (
                <p className="expertise">🎯 {candidate.primary_expertise}</p>
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
                {candidate.h_index && <span>H-index: {candidate.h_index}</span>}
                {candidate.citation_count && <span>Citations: {candidate.citation_count}</span>}
                {candidate.publication_count > 0 && <span>Publications: {candidate.publication_count}</span>}
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
    education_required: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/api/jobs`, newJob);
      setNewJob({ title: '', company: '', required_expertise: '', education_required: '' });
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
          <select
            value={newJob.education_required}
            onChange={(e) => setNewJob({ ...newJob, education_required: e.target.value })}
          >
            <option value="">Education Required</option>
            <option value="PhD">PhD</option>
            <option value="Masters">Masters</option>
            <option value="Bachelors">Bachelors</option>
          </select>
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
            <div key={job.id} className="job-card">
              <div className="job-header">
                <h3>{job.title}</h3>
                <span className={`status-badge ${job.status}`}>{job.status}</span>
              </div>
              <p className="company">🏢 {job.company}</p>
              {job.required_expertise && <p>🎯 {job.required_expertise}</p>}
              {job.education_required && <p>🎓 {job.education_required} required</p>}
              {job.application_count > 0 && (
                <p className="applications-count">📋 {job.application_count} applications</p>
              )}
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

export default App;
