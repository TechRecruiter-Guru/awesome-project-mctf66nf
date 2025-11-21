import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useParams } from 'react-router-dom';
import axios from 'axios';
import './App.css';
import BooleanGenerator from './components/BooleanGenerator';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// ==================== PHYSICAL AI INDUSTRY KEYWORDS ====================

const PHYSICAL_AI_JOB_TITLES = [
  'Robotics Engineer',
  'Humanoid Roboticist',
  'Autonomous Vehicle Engineer',
  'Computer Vision Engineer (Robotics)',
  'Perception Engineer',
  'Motion Planning Engineer',
  'SLAM Engineer',
  'Autonomous Systems Engineer',
  'Robot Control Engineer',
  'Reinforcement Learning Engineer',
  'Computer Vision Engineer',
  'Deep Learning Engineer',
  'ML Systems Engineer',
  'AI/ML Engineer',
  'Sensor Fusion Engineer',
  'Embedded AI Engineer',
  'Robotics Software Engineer',
  'Machine Learning Engineer',
  'Deep Learning Researcher'
];

const PHYSICAL_AI_EXPERTISE = [
  'Computer Vision & SLAM',
  'Humanoid Robotics',
  'Autonomous Vehicles',
  'Robot Control & Dynamics',
  'Perception & Sensor Fusion',
  'Motion Planning & Navigation',
  'Reinforcement Learning',
  'Deep Learning',
  'Natural Language Processing',
  'Object Detection & Tracking',
  'Path Planning Algorithms',
  'Autonomous Navigation',
  'Robotic Manipulation',
  'Bipedal Locomotion',
  'Robot Operating System (ROS)',
  'LIDAR & LiDAR Processing',
  '3D Scene Understanding',
  'Real-time Processing',
  'Edge AI & Embedded Systems'
];

const PHYSICAL_AI_SKILLS = [
  'Python',
  'C++',
  'TensorFlow',
  'PyTorch',
  'OpenCV',
  'ROS / ROS2',
  'SLAM Algorithms',
  'YOLO',
  'Computer Vision',
  'Sensor Fusion',
  'LIDAR Processing',
  'Point Cloud Processing',
  'Deep Learning',
  'Object Detection',
  'Semantic Segmentation',
  'Instance Segmentation',
  'Motion Planning',
  'Path Planning (RRT, A*)',
  'Control Theory',
  'Dynamics Simulation',
  'Gazebo',
  'CARLA (Autonomous Driving Simulator)',
  'CUDA',
  'Docker',
  'Git / GitHub',
  'Linux',
  'Real-time Systems',
  'Optimization',
  'Kalman Filters',
  'Particle Filters'
];

const PHYSICAL_AI_RESEARCH_FOCUS = [
  'Computer Vision for Robotics',
  'Humanoid Robotics',
  'Autonomous Vehicles / AVs',
  'SLAM & Localization',
  'Motion Planning',
  'Robotic Manipulation',
  'Deep Reinforcement Learning',
  'Robot Learning',
  'Semantic Understanding',
  'Real-time Perception',
  'Sensor Fusion',
  'Edge AI',
  'Embedded Systems',
  'Multi-robot Systems',
  'Human-Robot Interaction',
  'Autonomous Navigation'
];

// ==================== HIRING INTELLIGENCE ROLE PROMPTS ====================

const HIRING_INTELLIGENCE_PROMPTS = {
  'Robotics Engineer': {
    label: 'Robotics Systems Intelligence',
    question: 'When integrating perception, control, and actuation, what is the earliest indicator you monitor to detect system-wide instability—and how do you intervene before the issue compounds?'
  },
  'Humanoid Roboticist': {
    label: 'Embodied Dynamics Insight',
    question: 'Describe a time when human biomechanics understanding guided a breakthrough in humanoid stability, manipulation, or locomotion. Which non-obvious signal shaped your approach?'
  },
  'Autonomous Vehicle Engineer': {
    label: 'Autonomy Arbitration Intelligence',
    question: 'When an AV faces conflicting inputs (e.g., perception noise vs motion planning constraints), how do you determine which subsystem receives priority? Share your decision logic and the signals that drove it.'
  },
  'Computer Vision Engineer (Robotics)': {
    label: 'CV-for-Robotics Intelligence',
    question: 'What is the most critical vision failure mode you design against in physical environments, and which early signal reveals it before overall performance degrades?'
  },
  'Perception Engineer': {
    label: 'Perception Systems Insight',
    question: 'How do you distinguish true environmental features from sensor artifacts in complex scenes? Describe the signal or test that helps you decide.'
  },
  'Motion Planning Engineer': {
    label: 'Trajectory Intelligence',
    question: 'When your planner yields a feasible but suboptimal trajectory, what is the first constraint you interrogate to unlock a more efficient or safer path?'
  },
  'SLAM Engineer': {
    label: 'Spatial Intelligence Diagnostic',
    question: 'In SLAM drift scenarios, what is your go-to method for isolating root cause—and which cue tells you whether the issue is map quality, loop closure, or sensor bias?'
  },
  'Autonomous Systems Engineer': {
    label: 'System Autonomy Insight',
    question: 'How do you architect decision-making when subsystems report uncertain or contradictory outputs? Describe the governing principle and an example.'
  },
  'Robot Control Engineer': {
    label: 'Control Loop Judgment',
    question: 'When tuning controllers, what early signal indicates imminent stability loss—and what immediate corrective pattern do you apply?'
  },
  'Reinforcement Learning Engineer': {
    label: 'RL Signal Intelligence',
    question: 'When training an RL agent, what hidden metric or behavioral cue do you monitor that predicts long-term policy success before reward curves show it?'
  },
  'Computer Vision Engineer': {
    label: 'Vision Modeling Insight',
    question: 'When a vision model misclassifies or misses detections, what visual or dataset signal do you check first to determine whether the root cause is labeling noise, domain shift, or architecture limits?'
  },
  'Deep Learning Engineer': {
    label: 'Model Behavior Intelligence',
    question: 'Which model behavior (beyond accuracy) reveals deeper problems—something you watch early to detect future failure—and how do you act on it?'
  },
  'ML Systems Engineer': {
    label: 'Systems-Level ML Intelligence',
    question: 'When scaling ML pipelines, which system bottleneck do you diagnose first—and which early indicator tells you the pipeline will fail under production load?'
  },
  'AI/ML Engineer': {
    label: 'AI Solutioning Insight',
    question: 'When balancing performance, latency, and cost, which constraint becomes your anchor—and how do you determine and enforce that anchor in architecture or process?'
  },
  'Sensor Fusion Engineer': {
    label: 'Fusion Signal Intelligence',
    question: 'When sensor streams diverge, what earliest cue tells you which modality is unreliable, and how do you reconcile conflicting estimates in real time?'
  },
  'Embedded AI Engineer': {
    label: 'On-Device Intelligence Insight',
    question: 'When deploying models at the edge, which signal first tells you the hardware-software interface will be the limiting factor—and how do you mitigate it?'
  },
  'Robotics Software Engineer': {
    label: 'Software Integration Intelligence',
    question: 'When debugging heterogeneous robotic stacks, what cross-component signal do you examine first to determine whether the root cause is software logic, timing, or hardware interaction?'
  },
  'Machine Learning Engineer': {
    label: 'ML Insight Diagnostic',
    question: 'What is your highest-leverage early indicator that a training pipeline is learning the wrong patterns—even before validation metrics degrade?'
  },
  'Deep Learning Researcher': {
    label: 'Research Intelligence Signal',
    question: 'What subtle model behavior—beyond raw accuracy—signals that a research direction has deep potential and deserves further investment?'
  }
};

// ==================== PUBLIC JOBS LISTING PAGE ====================

function PublicJobsPage() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedJobId, setSelectedJobId] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchPublicJobs();
  }, []);

  const fetchPublicJobs = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/jobs`);
      // Filter to only open jobs
      const openJobs = (response.data.jobs || []).filter(job => job.status === 'open');
      setJobs(openJobs);
    } catch (err) {
      console.error('Error fetching jobs:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredJobs = jobs.filter(job =>
    job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    job.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
    job.location.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (selectedJobId) {
    return <JobDetailPage jobId={selectedJobId} onBack={() => setSelectedJobId(null)} />;
  }

  return (
    <div className="public-jobs-page">
      <div className="jobs-header">
        <h1>🚀 AI/ML Career Opportunities</h1>
        <p>Discover transformative roles in AI, Machine Learning, and Robotics at PAIP</p>
      </div>

      <div className="jobs-search">
        <input
          type="text"
          placeholder="Search by job title, company, or location..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>

      {loading ? (
        <div className="loading">Loading opportunities...</div>
      ) : filteredJobs.length === 0 ? (
        <div className="empty-state">
          <p>No opportunities match your search</p>
        </div>
      ) : (
        <div className="jobs-grid">
          {filteredJobs.map(job => (
            <div key={job.id} className="job-listing-card">
              <div className="job-listing-header">
                <h3>{job.title}</h3>
                {job.confidential && <span className="stealth-badge">🔒 Confidential</span>}
              </div>
              <p className="job-company">{job.confidential ? 'Confidential Company' : job.company}</p>

              <div className="job-meta-info">
                {job.location && <span>📍 {job.location}</span>}
                {job.job_type && <span>💼 {job.job_type}</span>}
              </div>

              {job.salary_min && job.salary_max && (
                <p className="salary" style={{ fontWeight: '700', color: '#059669', fontSize: '1.1rem' }}>
                  💰 ${job.salary_min.toLocaleString()} - ${job.salary_max.toLocaleString()}
                </p>
              )}

              {job.required_expertise && (
                <div style={{ marginTop: '8px' }}>
                  <p style={{ fontSize: '0.85rem', fontWeight: '600', color: '#666', marginBottom: '6px' }}>🎯 Expertise:</p>
                  <p style={{ fontSize: '0.9rem', color: '#2563eb', fontWeight: '500' }}>{job.required_expertise}</p>
                </div>
              )}

              {job.education_required && (
                <p style={{ fontSize: '0.85rem', color: '#7c3aed', marginTop: '6px' }}>
                  🎓 {job.education_required}
                </p>
              )}

              <p className="job-excerpt" style={{ marginTop: '10px', color: '#555', fontSize: '0.95rem' }}>
                {job.description?.substring(0, 120)}...
              </p>

              <button
                className="view-apply-btn"
                onClick={() => setSelectedJobId(job.id)}
                style={{ marginTop: '12px' }}
              >
                🔍 View Full Details & Apply
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ==================== JOB DETAIL + APPLICATION PAGE ====================

function JobDetailPage({ jobId, onBack }) {
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [intelligenceQuestion, setIntelligenceQuestion] = useState(null);
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
    position: '',
    hiring_intelligence: '',
    hidden_signal: ''
  });
  const [intelligencePrompt, setIntelligencePrompt] = useState(null);

  // Hiring Intelligence state
  const [workLinks, setWorkLinks] = useState([
    { link_type: 'github', url: '', title: '' }
  ]);
  const [intelligenceResponse, setIntelligenceResponse] = useState('');

  useEffect(() => {
    fetchJob();
    fetchIntelligenceQuestion();
  }, [jobId]);

  const fetchJob = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/jobs/${jobId}`);
      setJob(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load job posting');
    } finally {
      setLoading(false);
    }
  };

  const fetchIntelligenceQuestion = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/public/jobs/${jobId}/question`);
      setIntelligenceQuestion(response.data);
    } catch (err) {
      console.log('No intelligence question available for this role');
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  // Work Links handlers
  const addWorkLink = () => {
    setWorkLinks([...workLinks, { link_type: 'other', url: '', title: '' }]);
  };

  const removeWorkLink = (index) => {
    setWorkLinks(workLinks.filter((_, i) => i !== index));
  };

  const updateWorkLink = (index, field, value) => {
    const updated = [...workLinks];
    updated[index][field] = value;
    setWorkLinks(updated);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    // Validate hiring intelligence is provided
    if (!formData.hiring_intelligence || !formData.hiring_intelligence.trim()) {
      alert('Please provide your hiring intelligence response.');
      setSubmitting(false);
      return;
    }

    // Filter out empty work links
    const validWorkLinks = workLinks.filter(link => link.url.trim() !== '');

    const submissionData = {
      ...formData,
      job_id: parseInt(jobId),
      job_title: job.title,
      years_experience: formData.years_experience ? parseInt(formData.years_experience) : null,
      // Add work links for backend storage
      work_links: validWorkLinks,
      // Format intelligence response for backend
      intelligence_response: formData.hiring_intelligence ? {
        question_id: intelligenceQuestion?.question_id || null,
        response_text: formData.hiring_intelligence
      } : null
    };

    console.log('📤 Submitting application data:', submissionData);

    try {
      const response = await axios.post(`${API_URL}/api/public/apply`, submissionData);
      console.log('✅ Application submitted successfully:', response.data);
      setSubmitted(true);
    } catch (err) {
      console.error('❌ Submission error:', err.response?.data || err.message);
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
            <button className="btn-back" onClick={onBack}>← Back to Jobs</button>
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
            <button className="btn-back" onClick={onBack}>← Back to Jobs</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="landing-page">
      <div className="landing-container">
        <button className="btn-back-small" onClick={onBack}>← Back to Jobs</button>
        <div className="job-header">
          <div className="company-badge">
            {job.confidential ? '🔒 Confidential' : job.company}
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
                <input type="text" name="first_name" value={formData.first_name} onChange={handleInputChange} required />
              </div>
              <div className="form-group">
                <label>Last Name *</label>
                <input type="text" name="last_name" value={formData.last_name} onChange={handleInputChange} required />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Email *</label>
                <input type="email" name="email" value={formData.email} onChange={handleInputChange} required />
              </div>
              <div className="form-group">
                <label>Phone</label>
                <input type="tel" name="phone" value={formData.phone} onChange={handleInputChange} />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Location</label>
                <input type="text" name="location" value={formData.location} onChange={handleInputChange} placeholder="City, Country" />
              </div>
              <div className="form-group">
                <label>Years of Experience</label>
                <input type="number" name="years_experience" value={formData.years_experience} onChange={handleInputChange} min="0" max="50" />
              </div>
            </div>
            <div className="form-group">
              <label>Primary Expertise</label>
              <select name="primary_expertise" value={formData.primary_expertise} onChange={handleInputChange}>
                <option value="">Select your expertise</option>
                {PHYSICAL_AI_EXPERTISE.map(exp => (
                  <option key={exp} value={exp}>{exp}</option>
                ))}
                <option value="Other">Other</option>
              </select>
            </div>
            <div className="form-group">
              <label>LinkedIn URL</label>
              <input type="url" name="linkedin_url" value={formData.linkedin_url} onChange={handleInputChange} placeholder="https://linkedin.com/in/yourprofile" />
            </div>
            <div className="form-group">
              <label>GitHub URL</label>
              <input type="url" name="github_url" value={formData.github_url} onChange={handleInputChange} placeholder="https://github.com/yourusername" />
            </div>
            <div className="form-group">
              <label>Portfolio URL</label>
              <input type="url" name="portfolio_url" value={formData.portfolio_url} onChange={handleInputChange} placeholder="https://yourportfolio.com" />
            </div>

            {/* ==================== WORK ARTIFACTS SECTION ==================== */}

            <div style={{
              backgroundColor: '#f8fafc',
              borderRadius: '12px',
              border: '1px solid #e2e8f0',
              padding: '24px',
              marginTop: '30px',
              marginBottom: '20px'
            }}>
              <h2 style={{ margin: '0 0 6px 0', fontSize: '20px', color: '#0f1724' }}>
                Work Artifacts
              </h2>
              <p style={{ color: '#6b7280', margin: '0 0 18px 0', fontSize: '13px' }}>
                Share links to your work - GitHub repos, papers, projects, or any artifacts that demonstrate your capabilities.
              </p>

              {workLinks.map((link, index) => (
                <div key={index} style={{
                  display: 'grid',
                  gridTemplateColumns: '140px 1fr 1fr auto',
                  gap: '10px',
                  marginBottom: '12px',
                  alignItems: 'center'
                }}>
                  <select
                    value={link.link_type}
                    onChange={(e) => updateWorkLink(index, 'link_type', e.target.value)}
                    style={{
                      padding: '10px',
                      border: '1px solid #d1d5db',
                      borderRadius: '6px',
                      fontSize: '14px',
                      backgroundColor: 'white'
                    }}
                  >
                    <option value="github">GitHub</option>
                    <option value="paper">Paper/Publication</option>
                    <option value="portfolio">Portfolio</option>
                    <option value="project">Project</option>
                    <option value="other">Other</option>
                  </select>
                  <input
                    type="url"
                    value={link.url}
                    onChange={(e) => updateWorkLink(index, 'url', e.target.value)}
                    placeholder="https://..."
                    style={{
                      padding: '10px',
                      border: '1px solid #d1d5db',
                      borderRadius: '6px',
                      fontSize: '14px'
                    }}
                  />
                  <input
                    type="text"
                    value={link.title}
                    onChange={(e) => updateWorkLink(index, 'title', e.target.value)}
                    placeholder="Title/Description (optional)"
                    style={{
                      padding: '10px',
                      border: '1px solid #d1d5db',
                      borderRadius: '6px',
                      fontSize: '14px'
                    }}
                  />
                  {workLinks.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeWorkLink(index)}
                      style={{
                        background: '#ef4444',
                        color: 'white',
                        border: 'none',
                        borderRadius: '6px',
                        width: '36px',
                        height: '36px',
                        fontSize: '1.2rem',
                        cursor: 'pointer'
                      }}
                    >
                      ×
                    </button>
                  )}
                </div>
              ))}

              <button
                type="button"
                onClick={addWorkLink}
                style={{
                  background: 'none',
                  border: '2px dashed #667eea',
                  color: '#667eea',
                  padding: '10px 20px',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontWeight: '600',
                  marginTop: '10px'
                }}
              >
                + Add Another Link
              </button>
            </div>

            {/* ==================== PROFESSIONAL PAIP HIRING INTELLIGENCE INTAKE ==================== */}

            <div style={{
              backgroundColor: '#ffffff',
              borderRadius: '12px',
              boxShadow: '0 6px 20px rgba(15,23,36,0.06)',
              padding: '24px',
              marginTop: '30px',
              marginBottom: '20px'
            }}>
              <h2 style={{ margin: '0 0 6px 0', fontSize: '20px', color: '#0f1724' }}>
                Hiring Intelligence — Role-Aware Intake
              </h2>
              <p style={{ color: '#6b7280', margin: '0 0 18px 0', fontSize: '13px' }}>
                This captures decision-making signals and engineering judgment aligned to the {job?.title}. The question adapts to surface judgment and systems-level reasoning.
              </p>

              <div style={{
                display: 'grid',
                gridTemplateColumns: '1fr 360px',
                gap: '18px',
                marginBottom: '16px'
              }}>
                {/* LEFT COLUMN - FORM INPUTS */}
                <div>
                  {/* Position Selection Dropdown */}
                  <div style={{ marginBottom: '18px' }}>
                    <label style={{ display: 'block', fontWeight: '600', marginBottom: '8px', color: '#0f1724' }}>
                      Position <span style={{ color: '#0b63ff' }}>*</span>
                    </label>
                    <select
                      name="position"
                      value={formData.position || ''}
                      onChange={handleInputChange}
                      style={{
                        width: '100%',
                        padding: '12px',
                        borderRadius: '8px',
                        border: '1px solid #e6e9ef',
                        fontSize: '14px',
                        backgroundColor: '#fff',
                        color: '#0f1724',
                        fontWeight: '500',
                        cursor: 'pointer',
                        boxSizing: 'border-box'
                      }}
                      required
                    >
                      <option value="">— Select a Position —</option>
                      {PHYSICAL_AI_JOB_TITLES.map(title => (
                        <option key={title} value={title}>{title}</option>
                      ))}
                    </select>
                    <p style={{ color: '#6b7280', fontSize: '13px', marginTop: '6px' }}>
                      Select the role to reveal a tailored intelligence prompt
                    </p>
                  </div>

                  {/* Candidate Name */}
                  <div style={{ marginBottom: '18px' }}>
                    <label style={{ display: 'block', fontWeight: '600', marginBottom: '8px', color: '#0f1724' }}>
                      Candidate Name <span style={{ color: '#0b63ff' }}>*</span>
                    </label>
                    <input
                      type="text"
                      placeholder={formData.first_name || formData.last_name ? `${formData.first_name} ${formData.last_name}` : 'First Last'}
                      value={formData.first_name && formData.last_name ? `${formData.first_name} ${formData.last_name}` : ''}
                      readOnly
                      style={{
                        width: '100%',
                        padding: '12px',
                        borderRadius: '8px',
                        border: '1px solid #e6e9ef',
                        fontSize: '14px',
                        backgroundColor: '#f8fafc',
                        color: '#0f1724'
                      }}
                    />
                    <p style={{ color: '#6b7280', fontSize: '13px', marginTop: '6px' }}>
                      From your application profile
                    </p>
                  </div>

                  {/* Contact Email */}
                  <div style={{ marginBottom: '18px' }}>
                    <label style={{ display: 'block', fontWeight: '600', marginBottom: '8px', color: '#0f1724' }}>
                      Contact Email <span style={{ color: '#0b63ff' }}>*</span>
                    </label>
                    <input
                      type="text"
                      placeholder={formData.email || 'you@company.com'}
                      value={formData.email || ''}
                      readOnly
                      style={{
                        width: '100%',
                        padding: '12px',
                        borderRadius: '8px',
                        border: '1px solid #e6e9ef',
                        fontSize: '14px',
                        backgroundColor: '#f8fafc',
                        color: '#0f1724'
                      }}
                    />
                    <p style={{ color: '#6b7280', fontSize: '13px', marginTop: '6px' }}>
                      From your application profile
                    </p>
                  </div>
                </div>

                {/* RIGHT COLUMN - LIVE PREVIEW */}
                <div>
                  <p style={{ color: '#6b7280', fontSize: '12px', marginBottom: '6px', margin: 0 }}>
                    Live Preview — Adaptive Question
                  </p>
                  <div style={{
                    backgroundColor: '#f8fafc',
                    borderRadius: '10px',
                    padding: '12px',
                    minHeight: '200px',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'flex-start'
                  }}>
                    <div style={{ fontWeight: '700', marginBottom: '8px', color: '#0f1724' }}>
                      {(formData.position || job?.title) && HIRING_INTELLIGENCE_PROMPTS[formData.position || job?.title]
                        ? HIRING_INTELLIGENCE_PROMPTS[formData.position || job?.title].label
                        : 'Role-specific Intelligence Question'}
                    </div>
                    <div style={{ color: '#6b7280', fontSize: '14px', lineHeight: '1.45' }}>
                      {(formData.position || job?.title) && HIRING_INTELLIGENCE_PROMPTS[formData.position || job?.title]
                        ? HIRING_INTELLIGENCE_PROMPTS[formData.position || job?.title].question
                        : 'Fill out the form above to load a targeted question that surfaces judgment and system-level reasoning.'}
                    </div>
                    <div style={{ flex: 1 }} />
                    <div style={{ color: '#6b7280', fontSize: '12px', marginTop: '8px' }}>
                      Question adapts based on role; full textarea below captures your narrative.
                    </div>
                  </div>
                </div>
              </div>

              {/* FULL WIDTH - INTELLIGENCE RESPONSE TEXTAREA */}
              <div style={{ marginTop: '16px', marginBottom: '12px' }}>
                <label style={{ display: 'block', fontWeight: '600', marginBottom: '8px', color: '#0f1724' }}>
                  Hiring Intelligence Response
                  <span style={{ color: '#6b7280', fontWeight: '600', marginLeft: '8px' }}>— role-adaptive</span>
                </label>
                <textarea
                  name="hiring_intelligence"
                  value={formData.hiring_intelligence}
                  onChange={handleInputChange}
                  rows="6"
                  placeholder={(formData.position || job?.title) && HIRING_INTELLIGENCE_PROMPTS[formData.position || job?.title]
                    ? HIRING_INTELLIGENCE_PROMPTS[formData.position || job?.title].question + ' (3–6 short paragraphs recommended)'
                    : 'Select a job position to load the role-specific prompt...'}
                  style={{
                    width: '100%',
                    padding: '12px',
                    borderRadius: '8px',
                    border: '1px solid #e6e9ef',
                    fontSize: '14px',
                    backgroundColor: '#fff',
                    fontFamily: 'inherit',
                    minHeight: '130px',
                    boxSizing: 'border-box'
                  }}
                  required
                />
                <p style={{ color: '#6b7280', fontSize: '13px', marginTop: '6px' }}>
                  Provide a concise, evidence-based narrative (3–6 short paragraphs recommended). Focus on signals, tradeoffs, and the first-order decision you made.
                </p>
              </div>

              {/* HIDDEN SIGNAL FIELD */}
              <div style={{ marginTop: '12px', marginBottom: '14px' }}>
                <label style={{ display: 'block', fontWeight: '600', marginBottom: '8px', color: '#0f1724' }}>
                  Hidden Signal You Think We Should Notice
                </label>
                <input
                  type="text"
                  name="hidden_signal"
                  value={formData.hidden_signal}
                  onChange={handleInputChange}
                  placeholder="E.g., specialized toolchain, fieldwork, low-level hardware insight"
                  style={{
                    width: '100%',
                    padding: '12px',
                    borderRadius: '8px',
                    border: '1px solid #e6e9ef',
                    fontSize: '14px',
                    backgroundColor: '#fff',
                    fontFamily: 'inherit',
                    boxSizing: 'border-box'
                  }}
                />
                <p style={{ color: '#6b7280', fontSize: '13px', marginTop: '6px' }}>
                  Optional: call out unconventional capabilities often overlooked by hiring teams.
                </p>
              </div>

              {/* ACTION BUTTONS */}
              <div style={{ display: 'flex', gap: '12px', alignItems: 'center', marginTop: '14px', marginBottom: '18px' }}>
                <button
                  type="submit"
                  disabled={submitting}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '10px 14px',
                    borderRadius: '10px',
                    backgroundColor: '#0b63ff',
                    color: 'white',
                    border: 'none',
                    cursor: 'pointer',
                    fontWeight: '600',
                    opacity: submitting ? 0.6 : 1,
                    fontSize: '14px'
                  }}
                >
                  {submitting ? '⏳ Submitting...' : '✅ Submit Intelligence'}
                </button>

                <button
                  type="button"
                  onClick={() => {
                    setFormData({
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
                      hiring_intelligence: '',
                      hidden_signal: ''
                    });
                  }}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '10px 14px',
                    borderRadius: '10px',
                    backgroundColor: '#6b7280',
                    color: 'white',
                    border: 'none',
                    cursor: 'pointer',
                    fontWeight: '600',
                    fontSize: '14px'
                  }}
                >
                  🔄 Clear
                </button>

                <div style={{ flex: 1 }} />
                <div style={{ color: '#6b7280', fontSize: '13px' }} id="statusMsg" />
              </div>

              {/* JSON PAYLOAD PREVIEW */}
              <div style={{ marginTop: '18px' }}>
                <p style={{ color: '#6b7280', fontSize: '12px', marginBottom: '6px' }}>
                  Payload Preview (JSON)
                </p>
                <pre style={{
                  backgroundColor: '#0b1220',
                  color: '#e6eef8',
                  padding: '12px',
                  borderRadius: '8px',
                  overflow: 'auto',
                  fontSize: '12px',
                  lineHeight: '1.4',
                  margin: 0,
                  maxHeight: '250px',
                  boxSizing: 'border-box'
                }}>
                  {JSON.stringify({
                    submittedAt: new Date().toISOString(),
                    jobTitle: job?.title || 'Not selected',
                    candidateName: formData.first_name && formData.last_name ? `${formData.first_name} ${formData.last_name}` : null,
                    candidateEmail: formData.email || null,
                    intelligence: {
                      label: job && HIRING_INTELLIGENCE_PROMPTS[job.title] ? HIRING_INTELLIGENCE_PROMPTS[job.title].label : null,
                      question: job && HIRING_INTELLIGENCE_PROMPTS[job.title] ? HIRING_INTELLIGENCE_PROMPTS[job.title].question : null,
                      answer: formData.hiring_intelligence || '[pending response]'
                    },
                    hiddenSignal: formData.hidden_signal || null,
                    candidateProfile: {
                      location: formData.location || null,
                      yearsExperience: formData.years_experience || null,
                      primaryExpertise: formData.primary_expertise || null,
                      linkedinUrl: formData.linkedin_url || null,
                      githubUrl: formData.github_url || null,
                      portfolioUrl: formData.portfolio_url || null
                    }
                  }, null, 2)}
                </pre>
              </div>
            </div>

          </form>
        </div>

        <div className="landing-footer">
          <p>Powered by AI/ML ATS</p>
        </div>
      </div>
    </div>
  );
}

// ==================== CANDIDATE LANDING PAGE (OLD - DEPRECATED) ====================

function CandidateLandingPage() {
  const { jobId } = useParams();
  return <JobDetailPage jobId={jobId} onBack={() => window.history.back()} />;
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
          <h1>🎯 PAIP - PhysicalAIPros.com</h1>
          <div className={`api-status ${apiStatus === 'healthy' ? 'healthy' : 'unhealthy'}`}>
            API: {apiStatus}
          </div>
        </div>
        <p className="tagline">The Leader in AI/ML Early Talent Detection | Recruiter Portal</p>
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
          className={activeTab === 'applications' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('applications')}
        >
          📋 Applications ({stats.total_applications || 0})
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
        {activeTab === 'applications' && <ApplicationsView />}
        {activeTab === 'analytics' && <AnalyticsView />}
        {activeTab === 'campaigns' && <CampaignsView />}
        {activeTab === 'interviews' && <InterviewsView />}
        {activeTab === 'offers' && <OffersView />}
        {activeTab === 'boolean' && <BooleanGenerator onStatsRefresh={fetchStats} />}
        {activeTab === 'about' && <AboutView />}
      </main>

      <footer className="app-footer">
        <p>Built for recruiting AI/ML talent through research profiles 🎓 | Open Source Project</p>
      </footer>
    </div>
  );
}

// Applications View
function ApplicationsView() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterJobId, setFilterJobId] = useState('all');
  const [jobs, setJobs] = useState([]);
  const [selectedApplication, setSelectedApplication] = useState(null);

  useEffect(() => {
    fetchApplications();
    fetchJobs();
  }, []);

  const fetchApplications = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/api/applications`);
      setApplications(response.data.applications || []);
    } catch (err) {
      console.error('Error fetching applications:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchJobs = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/jobs`);
      setJobs(response.data.jobs || []);
    } catch (err) {
      console.error('Error fetching jobs:', err);
    }
  };

  const updateApplicationStatus = async (applicationId, newStatus) => {
    try {
      await axios.put(`${API_URL}/api/applications/${applicationId}`, { status: newStatus });
      fetchApplications();
    } catch (err) {
      alert('Error updating application: ' + (err.response?.data?.error || err.message));
    }
  };

  const filteredApplications = applications.filter(app => {
    const statusMatch = filterStatus === 'all' || app.status === filterStatus;
    const jobMatch = filterJobId === 'all' || app.job_id === parseInt(filterJobId);
    return statusMatch && jobMatch;
  });

  const getJobTitle = (jobId) => {
    const job = jobs.find(j => j.id === jobId);
    return job ? job.title : 'Unknown Job';
  };

  const statusColors = {
    'applied': '#3b82f6',
    'screening': '#f59e0b',
    'interview': '#8b5cf6',
    'offer': '#10b981',
    'hired': '#059669',
    'rejected': '#ef4444'
  };

  return (
    <div className="applications-view">
      <div className="view-header">
        <h2>All Applications</h2>
      </div>

      <div style={{ display: 'flex', gap: '20px', marginBottom: '20px', flexWrap: 'wrap' }}>
        <div>
          <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>Filter by Status:</label>
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            style={{ padding: '8px', borderRadius: '6px', border: '1px solid #ddd', minWidth: '150px' }}
          >
            <option value="all">All Statuses</option>
            <option value="applied">Applied</option>
            <option value="screening">Screening</option>
            <option value="interview">Interview</option>
            <option value="offer">Offer</option>
            <option value="hired">Hired</option>
            <option value="rejected">Rejected</option>
          </select>
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>Filter by Job:</label>
          <select
            value={filterJobId}
            onChange={(e) => setFilterJobId(e.target.value)}
            style={{ padding: '8px', borderRadius: '6px', border: '1px solid #ddd', minWidth: '200px' }}
          >
            <option value="all">All Jobs</option>
            {jobs.map(job => (
              <option key={job.id} value={job.id}>{job.title} ({job.company})</option>
            ))}
          </select>
        </div>

        <div>
          <p style={{ marginTop: '28px', fontWeight: '600' }}>Total: {filteredApplications.length}</p>
        </div>
      </div>

      {loading ? (
        <div className="loading">Loading applications...</div>
      ) : filteredApplications.length === 0 ? (
        <div className="empty-state">
          <p>No applications match your filters</p>
        </div>
      ) : (
        <div style={{ overflowX: 'auto' }}>
          <table style={{
            width: '100%',
            borderCollapse: 'collapse',
            backgroundColor: 'white',
            borderRadius: '8px',
            overflow: 'hidden'
          }}>
            <thead>
              <tr style={{ backgroundColor: '#f3f4f6', borderBottom: '2px solid #e5e7eb' }}>
                <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600' }}>Candidate</th>
                <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600' }}>Job Position</th>
                <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600' }}>Status</th>
                <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600' }}>Applied Date</th>
                <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600' }}>Overall Score</th>
                <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredApplications.map((app) => (
                <tr key={app.id} style={{ borderBottom: '1px solid #e5e7eb' }}>
                  <td style={{ padding: '12px' }}>
                    <strong>{app.candidate_name}</strong>
                  </td>
                  <td style={{ padding: '12px' }}>
                    {getJobTitle(app.job_id)}
                  </td>
                  <td style={{ padding: '12px' }}>
                    <select
                      value={app.status}
                      onChange={(e) => updateApplicationStatus(app.id, e.target.value)}
                      style={{
                        backgroundColor: statusColors[app.status] || '#6b7280',
                        color: 'white',
                        padding: '6px 12px',
                        borderRadius: '4px',
                        border: 'none',
                        cursor: 'pointer',
                        fontWeight: '600',
                        minWidth: '120px'
                      }}
                    >
                      <option value="applied">Applied</option>
                      <option value="screening">Screening</option>
                      <option value="interview">Interview</option>
                      <option value="offer">Offer</option>
                      <option value="hired">Hired</option>
                      <option value="rejected">Rejected</option>
                    </select>
                  </td>
                  <td style={{ padding: '12px' }}>
                    {app.applied_date ? new Date(app.applied_date).toLocaleDateString() : '-'}
                  </td>
                  <td style={{ padding: '12px' }}>
                    {app.overall_score ? (
                      <span style={{
                        backgroundColor: app.overall_score >= 70 ? '#dcfce7' : app.overall_score >= 50 ? '#fef3c7' : '#fee2e2',
                        color: app.overall_score >= 70 ? '#166534' : app.overall_score >= 50 ? '#92400e' : '#991b1b',
                        padding: '4px 8px',
                        borderRadius: '4px',
                        fontWeight: '600'
                      }}>
                        {app.overall_score}%
                      </span>
                    ) : '-'}
                  </td>
                  <td style={{ padding: '12px' }}>
                    <button
                      onClick={() => setSelectedApplication(app)}
                      style={{
                        padding: '6px 12px',
                        backgroundColor: '#2563eb',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontSize: '0.85rem'
                      }}
                    >
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* APPLICATION DETAILS MODAL */}
      {selectedApplication && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000
        }}>
          <div style={{
            backgroundColor: 'white',
            borderRadius: '12px',
            padding: '24px',
            maxWidth: '800px',
            maxHeight: '90vh',
            overflowY: 'auto',
            width: '95%'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h2 style={{ margin: 0 }}>Application Details</h2>
              <button
                onClick={() => setSelectedApplication(null)}
                style={{
                  backgroundColor: 'transparent',
                  border: '1px solid #ddd',
                  borderRadius: '4px',
                  padding: '6px 12px',
                  cursor: 'pointer',
                  fontSize: '1rem'
                }}
              >
                ✕ Close
              </button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '20px' }}>
              <div>
                <p style={{ margin: '0 0 4px 0', fontSize: '12px', color: '#6b7280', fontWeight: '600' }}>CANDIDATE</p>
                <p style={{ margin: 0, fontSize: '16px', fontWeight: '600' }}>{selectedApplication.candidate_name}</p>
              </div>
              <div>
                <p style={{ margin: '0 0 4px 0', fontSize: '12px', color: '#6b7280', fontWeight: '600' }}>JOB POSITION</p>
                <p style={{ margin: 0, fontSize: '16px', fontWeight: '600' }}>{selectedApplication.job_title}</p>
              </div>
              <div>
                <p style={{ margin: '0 0 4px 0', fontSize: '12px', color: '#6b7280', fontWeight: '600' }}>SELECTED ROLE</p>
                <p style={{ margin: 0, fontSize: '16px', fontWeight: '600' }}>{selectedApplication.position || selectedApplication.job_title}</p>
              </div>
              <div>
                <p style={{ margin: '0 0 4px 0', fontSize: '12px', color: '#6b7280', fontWeight: '600' }}>STATUS</p>
                <p style={{ margin: 0, fontSize: '16px', fontWeight: '600' }}>{selectedApplication.status}</p>
              </div>
              <div style={{ gridColumn: '1 / -1' }}>
                <p style={{ margin: '0 0 4px 0', fontSize: '12px', color: '#6b7280', fontWeight: '600' }}>OVERALL SCORE</p>
                <p style={{ margin: 0, fontSize: '16px', fontWeight: '600' }}>{selectedApplication.overall_score ? selectedApplication.overall_score + '%' : '-'}</p>
              </div>
            </div>

            <hr style={{ margin: '20px 0', borderColor: '#e5e7eb' }} />

            {/* CANDIDATE PROFILE */}
            <h3 style={{ margin: '16px 0 12px 0', color: '#0f1724', fontSize: '14px', fontWeight: '700' }}>CANDIDATE PROFILE</h3>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '20px' }}>
              {selectedApplication.candidate_email && (
                <div>
                  <p style={{ margin: '0 0 4px 0', fontSize: '12px', color: '#6b7280', fontWeight: '600' }}>EMAIL</p>
                  <p style={{ margin: 0, fontSize: '14px', color: '#0f1724' }}>
                    <a href={`mailto:${selectedApplication.candidate_email}`} style={{ color: '#0b63ff', textDecoration: 'none' }}>
                      {selectedApplication.candidate_email}
                    </a>
                  </p>
                </div>
              )}
              {selectedApplication.candidate_phone && (
                <div>
                  <p style={{ margin: '0 0 4px 0', fontSize: '12px', color: '#6b7280', fontWeight: '600' }}>PHONE</p>
                  <p style={{ margin: 0, fontSize: '14px', color: '#0f1724' }}>
                    <a href={`tel:${selectedApplication.candidate_phone}`} style={{ color: '#0b63ff', textDecoration: 'none' }}>
                      {selectedApplication.candidate_phone}
                    </a>
                  </p>
                </div>
              )}
              {selectedApplication.candidate_location && (
                <div>
                  <p style={{ margin: '0 0 4px 0', fontSize: '12px', color: '#6b7280', fontWeight: '600' }}>LOCATION</p>
                  <p style={{ margin: 0, fontSize: '14px', color: '#0f1724' }}>{selectedApplication.candidate_location}</p>
                </div>
              )}
              {selectedApplication.candidate_years_experience !== null && selectedApplication.candidate_years_experience !== '' && (
                <div>
                  <p style={{ margin: '0 0 4px 0', fontSize: '12px', color: '#6b7280', fontWeight: '600' }}>EXPERIENCE</p>
                  <p style={{ margin: 0, fontSize: '14px', color: '#0f1724' }}>{selectedApplication.candidate_years_experience} years</p>
                </div>
              )}
              {selectedApplication.candidate_primary_expertise && (
                <div>
                  <p style={{ margin: '0 0 4px 0', fontSize: '12px', color: '#6b7280', fontWeight: '600' }}>PRIMARY EXPERTISE</p>
                  <p style={{ margin: 0, fontSize: '14px', color: '#0f1724' }}>{selectedApplication.candidate_primary_expertise}</p>
                </div>
              )}
            </div>

            {/* PROFESSIONAL LINKS */}
            {(selectedApplication.candidate_linkedin || selectedApplication.candidate_github || selectedApplication.candidate_portfolio) && (
              <div style={{ marginBottom: '20px' }}>
                <h3 style={{ margin: '0 0 12px 0', color: '#0f1724', fontSize: '14px', fontWeight: '700' }}>PROFESSIONAL LINKS</h3>
                <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
                  {selectedApplication.candidate_linkedin && (
                    <a href={selectedApplication.candidate_linkedin} target="_blank" rel="noopener noreferrer" style={{
                      padding: '8px 12px',
                      backgroundColor: '#0b63ff',
                      color: 'white',
                      borderRadius: '6px',
                      textDecoration: 'none',
                      fontSize: '13px',
                      fontWeight: '600'
                    }}>
                      LinkedIn
                    </a>
                  )}
                  {selectedApplication.candidate_github && (
                    <a href={selectedApplication.candidate_github} target="_blank" rel="noopener noreferrer" style={{
                      padding: '8px 12px',
                      backgroundColor: '#1f2937',
                      color: 'white',
                      borderRadius: '6px',
                      textDecoration: 'none',
                      fontSize: '13px',
                      fontWeight: '600'
                    }}>
                      GitHub
                    </a>
                  )}
                  {selectedApplication.candidate_portfolio && (
                    <a href={selectedApplication.candidate_portfolio} target="_blank" rel="noopener noreferrer" style={{
                      padding: '8px 12px',
                      backgroundColor: '#7c3aed',
                      color: 'white',
                      borderRadius: '6px',
                      textDecoration: 'none',
                      fontSize: '13px',
                      fontWeight: '600'
                    }}>
                      Portfolio
                    </a>
                  )}
                </div>
              </div>
            )}

            <hr style={{ margin: '20px 0', borderColor: '#e5e7eb' }} />

            <div style={{ marginBottom: '20px' }}>
              <h3 style={{ margin: '0 0 12px 0', color: '#0f1724' }}>Hiring Intelligence Response</h3>
              <div style={{
                backgroundColor: '#f8fafc',
                padding: '12px',
                borderRadius: '8px',
                border: '1px solid #e6e9ef',
                fontSize: '14px',
                lineHeight: '1.6',
                color: '#0f1724',
                whiteSpace: 'pre-wrap',
                wordWrap: 'break-word'
              }}>
                {selectedApplication.hiring_intelligence || '(No hiring intelligence response provided)'}
              </div>
            </div>

            {selectedApplication.hidden_signal && (
              <div style={{ marginBottom: '20px' }}>
                <h3 style={{ margin: '0 0 12px 0', color: '#0f1724' }}>Hidden Signal</h3>
                <div style={{
                  backgroundColor: '#fef3c7',
                  padding: '12px',
                  borderRadius: '8px',
                  border: '1px solid #fcd34d',
                  fontSize: '14px',
                  lineHeight: '1.6',
                  color: '#78350f'
                }}>
                  {selectedApplication.hidden_signal}
                </div>
              </div>
            )}

            <div style={{
              backgroundColor: '#f3f4f6',
              padding: '12px',
              borderRadius: '8px',
              fontSize: '12px',
              color: '#6b7280'
            }}>
              <p style={{ margin: '0 0 6px 0' }}>
                <strong>Applied:</strong> {selectedApplication.applied_date ? new Date(selectedApplication.applied_date).toLocaleString() : '-'}
              </p>
              <p style={{ margin: 0 }}>
                <strong>Application ID:</strong> {selectedApplication.id}
              </p>
            </div>
          </div>
        </div>
      )}
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
  const [schedulingInterviewFor, setSchedulingInterviewFor] = useState(null);
  const [interviewForm, setInterviewForm] = useState({
    interview_stage: 'phone_screen',
    scheduled_date: '',
    interviewer_name: '',
    notes: ''
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

  const scheduleInterview = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/api/interviews`, {
        candidate_id: schedulingInterviewFor,
        ...interviewForm,
        status: 'scheduled'
      });
      alert('✅ Interview scheduled!');
      setSchedulingInterviewFor(null);
      setInterviewForm({ interview_stage: 'phone_screen', scheduled_date: '', interviewer_name: '', notes: '' });
      onRefresh();
    } catch (err) {
      alert('Error scheduling interview: ' + (err.response?.data?.error || err.message));
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

          {/* Primary Expertise Dropdown */}
          <select
            value={newCandidate.primary_expertise}
            onChange={(e) => setNewCandidate({ ...newCandidate, primary_expertise: e.target.value })}
            style={{ marginBottom: '10px' }}
          >
            <option value="">Select Primary Expertise</option>
            {PHYSICAL_AI_EXPERTISE.map(exp => (
              <option key={exp} value={exp}>{exp}</option>
            ))}
            <option value="Other">Other (Custom)</option>
          </select>
          {newCandidate.primary_expertise === 'Other' && (
            <input
              type="text"
              placeholder="Enter your primary expertise"
              onChange={(e) => setNewCandidate({ ...newCandidate, primary_expertise: e.target.value })}
              style={{ marginBottom: '10px' }}
            />
          )}
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
                <button className="btn-primary" onClick={() => setSchedulingInterviewFor(candidate.id)}>🗓️ Schedule Interview</button>
                <button className="btn-delete" onClick={() => onDelete(candidate.id)}>Delete</button>
              </div>
            </div>
          ))}
        </div>
      )}

      {schedulingInterviewFor && (
        <form className="candidate-form" onSubmit={scheduleInterview}>
          <h3>Schedule Interview</h3>
          <select
            value={interviewForm.interview_stage}
            onChange={(e) => setInterviewForm({ ...interviewForm, interview_stage: e.target.value })}
          >
            <option value="phone_screen">Phone Screen</option>
            <option value="technical_interview">Technical Interview</option>
            <option value="final_interview">Final Interview</option>
            <option value="offer">Offer Discussion</option>
          </select>
          <input
            type="datetime-local"
            required
            value={interviewForm.scheduled_date}
            onChange={(e) => setInterviewForm({ ...interviewForm, scheduled_date: e.target.value })}
          />
          <input
            type="text"
            placeholder="Interviewer Name"
            required
            value={interviewForm.interviewer_name}
            onChange={(e) => setInterviewForm({ ...interviewForm, interviewer_name: e.target.value })}
          />
          <textarea
            placeholder="Interview Notes / Questions"
            value={interviewForm.notes}
            onChange={(e) => setInterviewForm({ ...interviewForm, notes: e.target.value })}
            rows="4"
          />
          <div style={{ display: 'flex', gap: '10px' }}>
            <button type="submit" className="btn-primary">Schedule Interview</button>
            <button type="button" className="btn-delete" onClick={() => setSchedulingInterviewFor(null)}>Cancel</button>
          </div>
        </form>
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
  const [editingJobId, setEditingJobId] = useState(null);
  const [editJob, setEditJob] = useState({});
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

  const startEditJob = (job) => {
    setEditingJobId(job.id);
    setEditJob(job);
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.put(`${API_URL}/api/jobs/${editingJobId}`, editJob);
      setEditingJobId(null);
      onRefresh();
    } catch (err) {
      alert('Error updating job: ' + (err.response?.data?.error || err.message));
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

          {/* Job Title Dropdown */}
          <select
            value={newJob.title}
            onChange={(e) => setNewJob({ ...newJob, title: e.target.value })}
            required
            style={{ marginBottom: '10px' }}
          >
            <option value="">Select Job Title *</option>
            {PHYSICAL_AI_JOB_TITLES.map(title => (
              <option key={title} value={title}>{title}</option>
            ))}
            <option value="Other">Other (Custom Title)</option>
          </select>
          {newJob.title === 'Other' && (
            <input
              type="text"
              placeholder="Enter custom job title"
              value={newJob.title === 'Other' ? '' : newJob.title}
              onChange={(e) => setNewJob({ ...newJob, title: e.target.value })}
              style={{ marginBottom: '10px' }}
            />
          )}

          <input
            type="text"
            placeholder="Company *"
            value={newJob.company}
            onChange={(e) => setNewJob({ ...newJob, company: e.target.value })}
            required
          />

          {/* Required Expertise Dropdown */}
          <select
            value={newJob.required_expertise}
            onChange={(e) => setNewJob({ ...newJob, required_expertise: e.target.value })}
            style={{ marginBottom: '10px' }}
          >
            <option value="">Select Required Expertise</option>
            {PHYSICAL_AI_EXPERTISE.map(exp => (
              <option key={exp} value={exp}>{exp}</option>
            ))}
            <option value="Other">Other (Custom)</option>
          </select>
          {newJob.required_expertise === 'Other' && (
            <input
              type="text"
              placeholder="Enter custom expertise"
              onChange={(e) => setNewJob({ ...newJob, required_expertise: e.target.value })}
              style={{ marginBottom: '10px' }}
            />
          )}

          {/* Required Skills Dropdown */}
          <select
            value={newJob.required_skills || ''}
            onChange={(e) => setNewJob({ ...newJob, required_skills: e.target.value })}
            style={{ marginBottom: '10px' }}
          >
            <option value="">Select Primary Skill</option>
            {PHYSICAL_AI_SKILLS.map(skill => (
              <option key={skill} value={skill}>{skill}</option>
            ))}
          </select>
          <small style={{ display: 'block', marginBottom: '10px', color: '#666' }}>
            💡 Tip: Separate multiple skills with commas
          </small>
          <textarea
            placeholder="Additional required skills (comma-separated)"
            value={newJob.required_skills}
            onChange={(e) => setNewJob({ ...newJob, required_skills: e.target.value })}
            style={{ minHeight: '60px', marginBottom: '10px' }}
          />

          <select
            value={newJob.education_required}
            onChange={(e) => setNewJob({ ...newJob, education_required: e.target.value })}
          >
            <option value="">Education Required</option>
            <option value="No Degree - Just Know-How">No Degree - Just Know-How</option>
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

      {editingJobId && (
        <form className="job-form" onSubmit={handleEditSubmit}>
          <h3>Edit Job</h3>
          <input
            type="text"
            placeholder="Job Title"
            value={editJob.title || ''}
            onChange={(e) => setEditJob({ ...editJob, title: e.target.value })}
          />
          <input
            type="text"
            placeholder="Company"
            value={editJob.company || ''}
            onChange={(e) => setEditJob({ ...editJob, company: e.target.value })}
          />
          <input
            type="text"
            placeholder="Location"
            value={editJob.location || ''}
            onChange={(e) => setEditJob({ ...editJob, location: e.target.value })}
          />
          <textarea
            placeholder="Job Description"
            value={editJob.description || ''}
            onChange={(e) => setEditJob({ ...editJob, description: e.target.value })}
            rows="4"
          />
          <input
            type="text"
            placeholder="Required Expertise"
            value={editJob.required_expertise || ''}
            onChange={(e) => setEditJob({ ...editJob, required_expertise: e.target.value })}
          />
          <select
            value={editJob.status || 'open'}
            onChange={(e) => setEditJob({ ...editJob, status: e.target.value })}
          >
            <option value="open">Open</option>
            <option value="closed">Closed</option>
          </select>
          <div className="checkbox-container">
            <label>
              <input
                type="checkbox"
                checked={editJob.confidential || false}
                onChange={(e) => setEditJob({ ...editJob, confidential: e.target.checked })}
              />
              <span className="checkbox-label">🔒 Confidential (Stealth Mode)</span>
            </label>
          </div>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button type="submit" className="btn-primary">Save Changes</button>
            <button type="button" className="btn-delete" onClick={() => setEditingJobId(null)}>Cancel</button>
          </div>
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
                <button
                  onClick={() => alert(`📋 ${job.application_count} applications for ${job.title}\n\nGo to Applications tab to manage all applications for this job.`)}
                  style={{
                    display: 'block',
                    width: '100%',
                    padding: '8px 12px',
                    marginTop: '8px',
                    backgroundColor: '#e0f2fe',
                    color: '#0369a1',
                    border: '1px solid #0ea5e9',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    fontWeight: '600',
                    fontSize: '0.9rem',
                    transition: 'all 0.3s'
                  }}
                  onMouseEnter={(e) => e.target.style.backgroundColor = '#cffafe'}
                  onMouseLeave={(e) => e.target.style.backgroundColor = '#e0f2fe'}
                >
                  📋 View {job.application_count} Applications
                </button>
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
                <button className="btn-primary" onClick={() => startEditJob(job)}>✏️ Edit</button>
                <button className="btn-delete" onClick={() => onDelete(job.id)}>Delete</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// Analytics View
function AnalyticsView() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/analytics/overview`);
      setAnalytics(response.data);
    } catch (err) {
      console.error('Error fetching analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading analytics...</div>;

  return (
    <div className="view-header">
      <h2>📈 Analytics Dashboard</h2>
      {analytics && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginTop: '20px' }}>
          <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#667eea' }}>{analytics.total_candidates}</div>
            <div style={{ color: '#666', marginTop: '4px' }}>Total Candidates</div>
          </div>
          <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#667eea' }}>{analytics.total_jobs}</div>
            <div style={{ color: '#666', marginTop: '4px' }}>Total Jobs</div>
          </div>
          <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#10b981' }}>{analytics.hired_candidates}</div>
            <div style={{ color: '#666', marginTop: '4px' }}>Hired Candidates</div>
          </div>
          <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#f59e0b' }}>{analytics.avg_time_to_hire}</div>
            <div style={{ color: '#666', marginTop: '4px' }}>Avg Days to Hire</div>
          </div>
        </div>
      )}
    </div>
  );
}

// Campaigns View
function CampaignsView() {
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

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

  const sendCampaign = async (campaignId) => {
    try {
      await axios.post(`${API_URL}/api/campaigns/${campaignId}/send`);
      alert('Campaign sent successfully!');
      fetchCampaigns();
    } catch (err) {
      console.error('Error sending campaign:', err);
    }
  };

  const deleteCampaign = async (campaignId) => {
    if (!window.confirm('Delete this campaign?')) return;
    try {
      await axios.delete(`${API_URL}/api/campaigns/${campaignId}`);
      fetchCampaigns();
    } catch (err) {
      console.error('Error deleting campaign:', err);
    }
  };

  if (loading) return <div className="loading">Loading campaigns...</div>;

  return (
    <div>
      <div className="view-header">
        <h2>📧 Email Campaigns</h2>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : 'New Campaign'}
        </button>
      </div>

      {campaigns.map(campaign => (
        <div key={campaign.id} className="job-card">
          <h3>{campaign.name}</h3>
          <p>{campaign.subject}</p>
          <p style={{ color: '#666', marginTop: '8px' }}>Recipients: {campaign.recipient_count || 0}</p>
          <div className="card-actions">
            <button className="btn-primary" onClick={() => sendCampaign(campaign.id)}>Send</button>
            <button className="btn-delete" onClick={() => deleteCampaign(campaign.id)}>Delete</button>
          </div>
        </div>
      ))}
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

  const updateInterviewStatus = async (interviewId, status) => {
    try {
      await axios.put(`${API_URL}/api/interviews/${interviewId}`, { status });
      fetchInterviews();
    } catch (err) {
      console.error('Error updating interview:', err);
    }
  };

  const deleteInterview = async (interviewId) => {
    if (!window.confirm('Delete this interview?')) return;
    try {
      await axios.delete(`${API_URL}/api/interviews/${interviewId}`);
      fetchInterviews();
    } catch (err) {
      console.error('Error deleting interview:', err);
    }
  };

  if (loading) return <div className="loading">Loading interviews...</div>;

  return (
    <div>
      <div className="view-header">
        <h2>🗓️ Interviews</h2>
      </div>

      {interviews.length === 0 ? (
        <div className="empty-state">No interviews scheduled</div>
      ) : (
        interviews.map(interview => (
          <div key={interview.id} className="job-card">
            <h3>{interview.candidate_name} - {interview.interview_stage}</h3>
            <p>Status: <span className="status-badge">{interview.status}</span></p>
            <p style={{ color: '#666', marginTop: '8px' }}>Scheduled: {interview.scheduled_date}</p>
            <div className="card-actions">
              <button className="btn-primary" onClick={() => updateInterviewStatus(interview.id, 'completed')}>Mark Complete</button>
              <button className="btn-delete" onClick={() => deleteInterview(interview.id)}>Delete</button>
            </div>
          </div>
        ))
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

  const updateStatus = async (offerId, status) => {
    try {
      await axios.put(`${API_URL}/api/offers/${offerId}`, { status });
      fetchOffers();
    } catch (err) {
      console.error('Error updating offer:', err);
    }
  };

  const deleteOffer = async (offerId) => {
    if (!window.confirm('Delete this offer?')) return;
    try {
      await axios.delete(`${API_URL}/api/offers/${offerId}`);
      fetchOffers();
    } catch (err) {
      console.error('Error deleting offer:', err);
    }
  };

  if (loading) return <div className="loading">Loading offers...</div>;

  return (
    <div>
      <div className="view-header">
        <h2>💰 Offers</h2>
      </div>

      {offers.length === 0 ? (
        <div className="empty-state">No offers</div>
      ) : (
        offers.map(offer => (
          <div key={offer.id} className="job-card">
            <h3>{offer.candidate_name}</h3>
            <p>Position: {offer.position_title}</p>
            <p>Status: <span className="status-badge">{offer.status}</span></p>
            <p style={{ color: '#667eea', marginTop: '8px', fontWeight: '600' }}>Salary: ${offer.salary_offered}</p>
            <div className="card-actions">
              <button className="btn-primary" onClick={() => updateStatus(offer.id, 'accepted')}>Accept</button>
              <button className="btn-primary" onClick={() => updateStatus(offer.id, 'declined')}>Decline</button>
              <button className="btn-delete" onClick={() => deleteOffer(offer.id)}>Delete</button>
            </div>
          </div>
        ))
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

// ==================== LOGIN PAGE ====================

function LoginPage({ onLogin }) {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const RECRUITER_PASSWORD = 'recruit123';

  const handleSubmit = (e) => {
    e.preventDefault();
    if (password === RECRUITER_PASSWORD) {
      onLogin();
      setPassword('');
      setError('');
    } else {
      setError('❌ Incorrect password');
      setPassword('');
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-box">
          <h1>🔐 PAIP Recruiter Portal</h1>
          <p>The Leader in AI/ML Early Talent Detection - Login Required</p>

          <form onSubmit={handleSubmit}>
            <input
              type="password"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoFocus
            />
            <button type="submit" className="btn-primary">
              Login
            </button>
          </form>

          {error && <p className="error-message">{error}</p>}

          <p className="login-hint">Password: recruit123</p>
        </div>
      </div>
    </div>
  );
}

// ==================== PROTECTED RECRUITER ROUTE ====================

function ProtectedRecruiterRoute() {
  const [isAuthenticated, setIsAuthenticated] = useState(
    localStorage.getItem('recruiter_auth') === 'true'
  );

  const handleLogin = () => {
    setIsAuthenticated(true);
    localStorage.setItem('recruiter_auth', 'true');
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    localStorage.removeItem('recruiter_auth');
  };

  if (!isAuthenticated) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return (
    <div>
      <button
        className="logout-btn"
        onClick={handleLogout}
        style={{
          position: 'fixed',
          top: '10px',
          right: '10px',
          zIndex: 1000,
          padding: '8px 16px',
          backgroundColor: '#dc3545',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '12px'
        }}
      >
        🚪 Logout
      </button>
      <App />
    </div>
  );
}

// ==================== APP WITH ROUTING ====================

function AppWithRouter() {
  return (
    <Router>
      <Routes>
        {/* Public-facing routes - no login required */}
        <Route path="/" element={<PublicJobsPage />} />
        <Route path="/apply/:jobId" element={<CandidateLandingPage />} />

        {/* Recruiter portal - password protected */}
        <Route path="/recruiter/*" element={<ProtectedRecruiterRoute />} />
      </Routes>
    </Router>
  );
}

export default AppWithRouter;
