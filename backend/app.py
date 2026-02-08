from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import requests
import re

app = Flask(__name__)
CORS(app)

# ==================== DATABASE CONFIGURATION ====================
# PostgreSQL (Supabase) for production, SQLite fallback for local dev
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL or DATABASE_URL == 'sqlite:///ats.db':
    # Check for Supabase-specific env vars as alternative
    SUPABASE_DB_URL = os.environ.get('SUPABASE_DB_URL')
    if SUPABASE_DB_URL:
        DATABASE_URL = SUPABASE_DB_URL
    else:
        # Local development fallback
        DATABASE_URL = 'sqlite:///ats.db'
        print("INFO: No DATABASE_URL set. Using SQLite for local development.")
        print("      Set DATABASE_URL env var for PostgreSQL (Supabase) in production.")

# Fix Render/Heroku postgres:// -> postgresql:// (required by SQLAlchemy 1.4+)
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Production-ready connection pooling (only for PostgreSQL)
if DATABASE_URL and 'postgresql' in DATABASE_URL:
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {
            'connect_timeout': 10,
            'options': '-c statement_timeout=30000'
        },
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 5,
        'max_overflow': 10
    }
    print(f"DATABASE: Connected to PostgreSQL")
else:
    print(f"DATABASE: Using SQLite (local development mode)")

db = SQLAlchemy(app)

# Track whether tables have been initialized
_tables_initialized = False

# ==================== DATA MODELS ====================

class Candidate(db.Model):
    """AI/ML Candidate with research profile"""
    id = db.Column(db.Integer, primary_key=True)

    # Basic Info
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    phone = db.Column(db.String(50))
    location = db.Column(db.String(200))

    # Professional Info
    linkedin_url = db.Column(db.String(300))
    github_url = db.Column(db.String(300))
    portfolio_url = db.Column(db.String(300))
    resume_url = db.Column(db.String(300))
    company = db.Column(db.String(200))
    bio = db.Column(db.Text)

    # GitHub Metrics
    github_followers = db.Column(db.Integer)
    github_repos = db.Column(db.Integer)

    # Academic/Research Profile (THE UNIQUE PART!)
    google_scholar_url = db.Column(db.String(300))
    research_gate_url = db.Column(db.String(300))
    arxiv_author_id = db.Column(db.String(100))
    orcid_id = db.Column(db.String(100))
    h_index = db.Column(db.Integer)
    citation_count = db.Column(db.Integer)

    # Expanded Sourcing - Where Physical AI / Robotics talent actually lives
    huggingface_url = db.Column(db.String(300))       # HuggingFace profile - models, datasets, spaces
    semantic_scholar_id = db.Column(db.String(100))    # Semantic Scholar author ID
    papers_with_code_url = db.Column(db.String(300))   # Papers With Code profile
    kaggle_url = db.Column(db.String(300))             # Kaggle profile - competitions, notebooks
    devpost_url = db.Column(db.String(300))            # Devpost - hackathon projects

    # Hugging Face Metrics
    hf_models_count = db.Column(db.Integer, default=0)
    hf_datasets_count = db.Column(db.Integer, default=0)
    hf_spaces_count = db.Column(db.Integer, default=0)
    hf_likes = db.Column(db.Integer, default=0)

    # Semantic Scholar Metrics
    s2_paper_count = db.Column(db.Integer, default=0)
    s2_citation_count = db.Column(db.Integer, default=0)
    s2_h_index = db.Column(db.Integer, default=0)

    # AI/ML Specific
    primary_expertise = db.Column(db.String(200))  # e.g., "Computer Vision", "NLP", "Reinforcement Learning"
    skills = db.Column(db.Text)  # JSON array of skills
    years_experience = db.Column(db.Integer)

    # Status
    status = db.Column(db.String(50), default='new')  # new, reviewing, interviewing, offer, hired, rejected
    rating = db.Column(db.Integer)  # 1-5 star rating
    notes = db.Column(db.Text)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    applications = db.relationship('Application', backref='candidate', lazy=True, cascade='all, delete-orphan')
    publications = db.relationship('Publication', backref='candidate', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': f"{self.first_name} {self.last_name}",
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'linkedin_url': self.linkedin_url,
            'github_url': self.github_url,
            'portfolio_url': self.portfolio_url,
            'resume_url': self.resume_url,
            'company': self.company,
            'bio': self.bio,
            'github_followers': self.github_followers,
            'github_repos': self.github_repos,
            'google_scholar_url': self.google_scholar_url,
            'research_gate_url': self.research_gate_url,
            'arxiv_author_id': self.arxiv_author_id,
            'orcid_id': self.orcid_id,
            'h_index': self.h_index,
            'citation_count': self.citation_count,
            'huggingface_url': self.huggingface_url,
            'semantic_scholar_id': self.semantic_scholar_id,
            'papers_with_code_url': self.papers_with_code_url,
            'kaggle_url': self.kaggle_url,
            'devpost_url': self.devpost_url,
            'hf_models_count': self.hf_models_count,
            'hf_datasets_count': self.hf_datasets_count,
            'hf_spaces_count': self.hf_spaces_count,
            'hf_likes': self.hf_likes,
            's2_paper_count': self.s2_paper_count,
            's2_citation_count': self.s2_citation_count,
            's2_h_index': self.s2_h_index,
            'primary_expertise': self.primary_expertise,
            'skills': self.skills,
            'years_experience': self.years_experience,
            'status': self.status,
            'rating': self.rating,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'application_count': len(self.applications),
            'publication_count': len(self.publications)
        }


class Job(db.Model):
    """AI/ML Job Positions"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    job_type = db.Column(db.String(50))  # full-time, contract, internship

    # Job Details
    description = db.Column(db.Text)
    requirements = db.Column(db.Text)
    responsibilities = db.Column(db.Text)

    # AI/ML Specific
    required_expertise = db.Column(db.String(200))  # e.g., "Deep Learning", "MLOps"
    required_skills = db.Column(db.Text)  # JSON array
    education_required = db.Column(db.String(100))  # PhD, Masters, Bachelors
    research_focus = db.Column(db.String(200))  # Specific research areas

    # Compensation
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    currency = db.Column(db.String(10), default='USD')

    # Status
    status = db.Column(db.String(50), default='open')  # open, closed, on-hold
    confidential = db.Column(db.Boolean, default=False)  # Stealth mode - hide company name
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)
    closing_date = db.Column(db.DateTime)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    applications = db.relationship('Application', backref='job', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, show_company=False):
        """
        Convert job to dict. If confidential and show_company is False,
        hide the company name (stealth mode for candidates)
        """
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company if (not self.confidential or show_company) else 'Confidential Company',
            'location': self.location,
            'job_type': self.job_type,
            'description': self.description,
            'requirements': self.requirements,
            'responsibilities': self.responsibilities,
            'required_expertise': self.required_expertise,
            'required_skills': self.required_skills,
            'education_required': self.education_required,
            'research_focus': self.research_focus,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'currency': self.currency,
            'status': self.status,
            'confidential': self.confidential,
            'posted_date': self.posted_date.isoformat() if self.posted_date else None,
            'closing_date': self.closing_date.isoformat() if self.closing_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'application_count': len(self.applications)
        }


class Application(db.Model):
    """Links Candidates to Jobs"""
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)

    # Application Details
    status = db.Column(db.String(50), default='applied')  # applied, screening, interview, offer, hired, rejected
    stage = db.Column(db.String(100))  # phone screen, technical interview, on-site, etc.
    source = db.Column(db.String(100))  # linkedin, referral, google_scholar, arxiv, etc.

    # Tracking
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_contact_date = db.Column(db.DateTime)
    interview_date = db.Column(db.DateTime)

    # Scoring (AI/ML candidate fit)
    technical_score = db.Column(db.Integer)  # 1-100
    research_score = db.Column(db.Integer)  # Based on publications, citations
    culture_fit_score = db.Column(db.Integer)  # 1-100
    overall_score = db.Column(db.Integer)  # Combined score

    notes = db.Column(db.Text)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'job_id': self.job_id,
            'candidate_name': f"{self.candidate.first_name} {self.candidate.last_name}" if self.candidate else None,
            'job_title': self.job.title if self.job else None,
            'status': self.status,
            'stage': self.stage,
            'source': self.source,
            'applied_date': self.applied_date.isoformat() if self.applied_date else None,
            'last_contact_date': self.last_contact_date.isoformat() if self.last_contact_date else None,
            'interview_date': self.interview_date.isoformat() if self.interview_date else None,
            'technical_score': self.technical_score,
            'research_score': self.research_score,
            'culture_fit_score': self.culture_fit_score,
            'overall_score': self.overall_score,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Publication(db.Model):
    """Research Papers and Publications (UNIQUE FEATURE!)"""
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)

    # Publication Details
    title = db.Column(db.String(500), nullable=False)
    authors = db.Column(db.Text)  # All authors
    venue = db.Column(db.String(300))  # Conference/Journal name
    year = db.Column(db.Integer)

    # Links
    paper_url = db.Column(db.String(500))
    arxiv_id = db.Column(db.String(100))
    doi = db.Column(db.String(200))

    # Metrics
    citation_count = db.Column(db.Integer, default=0)

    # Categorization
    research_area = db.Column(db.String(200))  # Computer Vision, NLP, etc.
    keywords = db.Column(db.Text)  # JSON array

    abstract = db.Column(db.Text)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'title': self.title,
            'authors': self.authors,
            'venue': self.venue,
            'year': self.year,
            'paper_url': self.paper_url,
            'arxiv_id': self.arxiv_id,
            'doi': self.doi,
            'citation_count': self.citation_count,
            'research_area': self.research_area,
            'keywords': self.keywords,
            'abstract': self.abstract,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class SavedSearch(db.Model):
    """Saved Boolean Searches"""
    id = db.Column(db.Integer, primary_key=True)

    # Search Details
    search_query = db.Column(db.Text, nullable=False)  # Renamed from 'query' to avoid conflict
    data_sources = db.Column(db.String(500))  # Comma-separated list

    # Metadata
    name = db.Column(db.String(200))  # Optional user-given name
    description = db.Column(db.Text)

    # Results summary
    total_results = db.Column(db.Integer, default=0)
    github_results_count = db.Column(db.Integer, default=0)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_executed = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'query': self.search_query,  # Return as 'query' for API
            'data_sources': self.data_sources.split(',') if self.data_sources else [],
            'name': self.name,
            'description': self.description,
            'total_results': self.total_results,
            'github_results_count': self.github_results_count,
            'created_at': self.created_at.isoformat(),
            'last_executed': self.last_executed.isoformat()
        }


class CandidateLink(db.Model):
    """Work artifact links submitted by candidates"""
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    link_type = db.Column(db.String(50), nullable=False)  # github, portfolio, paper, linkedin, other
    url = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'link_type': self.link_type,
            'url': self.url,
            'title': self.title,
            'created_at': self.created_at.isoformat()
        }


class HiringIntelligenceSubmission(db.Model):
    """Compiled Hiring Intelligence Submission document — the AI hiring manager report"""
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    submission_data = db.Column(db.Text)  # JSON string with full intelligence document
    status = db.Column(db.String(50), default='pending')  # pending, generated, reviewed, advanced, rejected
    missing_signal = db.Column(db.String(200))
    recruiter_notes = db.Column(db.Text)
    passed_to_screen = db.Column(db.Boolean)
    passed_to_interview = db.Column(db.Boolean)
    received_offer = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    # AI Analysis Fields
    extracted_skills = db.Column(db.Text)  # JSON array of technical skills
    key_phrases = db.Column(db.Text)  # JSON array of {phrase, context, importance}
    ai_assessment = db.Column(db.Text)  # JSON object with strengths, gaps, recommendation
    artifact_analysis = db.Column(db.Text)  # JSON array of {url, summary, quality, relevance}
    ai_analyzed = db.Column(db.Boolean, default=False)
    ai_analyzed_at = db.Column(db.DateTime)

    def to_dict(self):
        application = Application.query.get(self.application_id)
        return {
            'id': self.id,
            'application_id': self.application_id,
            'candidate_name': f"{application.candidate.first_name} {application.candidate.last_name}" if application and application.candidate else None,
            'job_title': application.job.title if application and application.job else None,
            'submission_data': self.submission_data,
            'status': self.status,
            'missing_signal': self.missing_signal,
            'recruiter_notes': self.recruiter_notes,
            'passed_to_screen': self.passed_to_screen,
            'passed_to_interview': self.passed_to_interview,
            'received_offer': self.received_offer,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'extracted_skills': self.extracted_skills,
            'key_phrases': self.key_phrases,
            'ai_assessment': self.ai_assessment,
            'artifact_analysis': self.artifact_analysis,
            'ai_analyzed': self.ai_analyzed,
            'ai_analyzed_at': self.ai_analyzed_at.isoformat() if self.ai_analyzed_at else None
        }


# Physical AI role-specific hiring intelligence questions
PHYSICAL_AI_ROLE_QUESTIONS = {
    "Robotics Engineer": {"label": "Robotics Systems Intelligence", "question": "When integrating perception, control, and actuation, what is the earliest indicator you monitor to detect system-wide instability\u2014and how do you intervene before the issue compounds?"},
    "Humanoid Roboticist": {"label": "Embodied Dynamics Insight", "question": "Describe a time when human biomechanics understanding guided a breakthrough in humanoid stability, manipulation, or locomotion. Which non-obvious signal shaped your approach?"},
    "Autonomous Vehicle Engineer": {"label": "Autonomy Arbitration Intelligence", "question": "When an AV faces conflicting inputs (e.g., perception noise vs motion planning constraints), how do you determine which subsystem receives priority? Share your decision logic and the signals that drove it."},
    "Computer Vision Engineer (Robotics)": {"label": "CV-for-Robotics Intelligence", "question": "What is the most critical vision failure mode you design against in physical environments, and which early signal reveals it before overall performance degrades?"},
    "Perception Engineer": {"label": "Perception Systems Insight", "question": "How do you distinguish true environmental features from sensor artifacts in complex scenes? Describe the signal or test that helps you decide."},
    "Motion Planning Engineer": {"label": "Trajectory Intelligence", "question": "When your planner yields a feasible but suboptimal trajectory, what is the first constraint you interrogate to unlock a more efficient or safer path?"},
    "SLAM Engineer": {"label": "Spatial Intelligence Diagnostic", "question": "In SLAM drift scenarios, what is your go-to method for isolating root cause\u2014and which cue tells you whether the issue is map quality, loop closure, or sensor bias?"},
    "Autonomous Systems Engineer": {"label": "System Autonomy Insight", "question": "How do you architect decision-making when subsystems report uncertain or contradictory outputs? Describe the governing principle and an example."},
    "Robot Control Engineer": {"label": "Control Loop Judgment", "question": "When tuning controllers, what early signal indicates imminent stability loss\u2014and what immediate corrective pattern do you apply?"},
    "Reinforcement Learning Engineer": {"label": "RL Signal Intelligence", "question": "When training an RL agent, what hidden metric or behavioral cue do you monitor that predicts long-term policy success before reward curves show it?"},
    "Computer Vision Engineer": {"label": "Vision Modeling Insight", "question": "When a vision model misclassifies or misses detections, what visual or dataset signal do you check first to determine whether the root cause is labeling noise, domain shift, or architecture limits?"},
    "Deep Learning Engineer": {"label": "Model Behavior Intelligence", "question": "Which model behavior (beyond accuracy) reveals deeper problems\u2014something you watch early to detect future failure\u2014and how do you act on it?"},
    "ML Systems Engineer": {"label": "Systems-Level ML Intelligence", "question": "When scaling ML pipelines, which system bottleneck do you diagnose first\u2014and which early indicator tells you the pipeline will fail under production load?"},
    "AI/ML Engineer": {"label": "AI Solutioning Insight", "question": "When balancing performance, latency, and cost, which constraint becomes your anchor\u2014and how do you determine and enforce that anchor in architecture or process?"},
    "Sensor Fusion Engineer": {"label": "Fusion Signal Intelligence", "question": "When sensor streams diverge, what earliest cue tells you which modality is unreliable, and how do you reconcile conflicting estimates in real time?"},
    "Embedded AI Engineer": {"label": "On-Device Intelligence Insight", "question": "When deploying models at the edge, which signal first tells you the hardware-software interface will be the limiting factor\u2014and how do you mitigate it?"},
    "Robotics Software Engineer": {"label": "Software Integration Intelligence", "question": "When debugging heterogeneous robotic stacks, what cross-component signal do you examine first to determine whether the root cause is software logic, timing, or hardware interaction?"},
    "Machine Learning Engineer": {"label": "ML Insight Diagnostic", "question": "What is your highest-leverage early indicator that a training pipeline is learning the wrong patterns\u2014even before validation metrics degrade?"},
    "Deep Learning Researcher": {"label": "Research Intelligence Signal", "question": "What subtle model behavior\u2014beyond raw accuracy\u2014signals that a research direction has deep potential and deserves further investment?"}
}


# ==================== LAZY TABLE INITIALIZATION ====================
# Instead of blocking startup with db.create_all(), we initialize on first request
# This prevents boot timeouts on Render/Railway/Heroku

def ensure_tables():
    """Create tables if they haven't been created yet (lazy initialization)"""
    global _tables_initialized
    if not _tables_initialized:
        try:
            db.create_all()
            # Auto-migrate: add new columns to existing tables
            _run_migrations()
            _tables_initialized = True
            print("DATABASE: Tables initialized successfully")
        except Exception as e:
            print(f"DATABASE: Table initialization error (may already exist): {e}")
            _tables_initialized = True  # Don't retry on every request


def _run_migrations():
    """Add missing columns to existing tables (SQLAlchemy create_all won't do this)"""
    new_columns = [
        ("candidate", "huggingface_url", "VARCHAR(300)"),
        ("candidate", "semantic_scholar_id", "VARCHAR(100)"),
        ("candidate", "papers_with_code_url", "VARCHAR(300)"),
        ("candidate", "kaggle_url", "VARCHAR(300)"),
        ("candidate", "devpost_url", "VARCHAR(300)"),
        ("candidate", "hf_models_count", "INTEGER DEFAULT 0"),
        ("candidate", "hf_datasets_count", "INTEGER DEFAULT 0"),
        ("candidate", "hf_spaces_count", "INTEGER DEFAULT 0"),
        ("candidate", "hf_likes", "INTEGER DEFAULT 0"),
        ("candidate", "s2_paper_count", "INTEGER DEFAULT 0"),
        ("candidate", "s2_citation_count", "INTEGER DEFAULT 0"),
        ("candidate", "s2_h_index", "INTEGER DEFAULT 0"),
    ]
    for table, column, col_type in new_columns:
        try:
            db.session.execute(db.text(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}"))
            db.session.commit()
            print(f"MIGRATION: Added {table}.{column}")
        except Exception:
            db.session.rollback()  # Column already exists, skip

@app.before_request
def before_request():
    """Ensure database tables exist before handling any request"""
    ensure_tables()


# ==================== API ENDPOINTS ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint - also reports database status"""
    db_status = "connected"
    db_type = "postgresql" if 'postgresql' in (app.config.get('SQLALCHEMY_DATABASE_URI') or '') else "sqlite"
    try:
        db.session.execute(db.text('SELECT 1'))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return jsonify({
        "status": "healthy",
        "message": "AI/ML ATS API is running",
        "version": "2.0.0",
        "database": db_type,
        "database_status": db_status,
        "tables_initialized": _tables_initialized
    })


@app.route('/api/init-db', methods=['POST'])
def init_database():
    """Manually trigger database table creation (useful after fresh deploy)"""
    try:
        db.create_all()
        return jsonify({
            "success": True,
            "message": "Database tables created successfully",
            "database": app.config.get('SQLALCHEMY_DATABASE_URI', '').split('@')[-1] if 'postgresql' in (app.config.get('SQLALCHEMY_DATABASE_URI') or '') else 'sqlite'
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==================== CANDIDATES ====================

@app.route('/api/candidates', methods=['GET'])
def get_candidates():
    """Get all candidates with optional filtering"""
    status = request.args.get('status')
    expertise = request.args.get('expertise')

    query = Candidate.query

    if status:
        query = query.filter_by(status=status)
    if expertise:
        query = query.filter(Candidate.primary_expertise.contains(expertise))

    candidates = query.order_by(Candidate.created_at.desc()).all()
    return jsonify({
        "candidates": [c.to_dict() for c in candidates],
        "total": len(candidates)
    })


@app.route('/api/candidates/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    """Get single candidate with full details"""
    candidate = Candidate.query.get_or_404(candidate_id)
    data = candidate.to_dict()

    # Include applications and publications
    data['applications'] = [app.to_dict() for app in candidate.applications]
    data['publications'] = [pub.to_dict() for pub in candidate.publications]

    return jsonify(data)


@app.route('/api/candidates', methods=['POST'])
def create_candidate():
    """Create new candidate"""
    data = request.get_json()

    if not data or 'email' not in data or 'first_name' not in data or 'last_name' not in data:
        return jsonify({"error": "First name, last name, and email are required"}), 400

    # Check if email already exists
    existing = Candidate.query.filter_by(email=data['email']).first()
    if existing:
        return jsonify({"error": "Candidate with this email already exists"}), 409

    candidate = Candidate(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data.get('phone'),
        location=data.get('location'),
        linkedin_url=data.get('linkedin_url'),
        github_url=data.get('github_url'),
        portfolio_url=data.get('portfolio_url'),
        resume_url=data.get('resume_url'),
        google_scholar_url=data.get('google_scholar_url'),
        research_gate_url=data.get('research_gate_url'),
        arxiv_author_id=data.get('arxiv_author_id'),
        orcid_id=data.get('orcid_id'),
        h_index=data.get('h_index'),
        citation_count=data.get('citation_count'),
        primary_expertise=data.get('primary_expertise'),
        skills=data.get('skills'),
        years_experience=data.get('years_experience'),
        status=data.get('status', 'new'),
        rating=data.get('rating'),
        notes=data.get('notes')
    )

    db.session.add(candidate)
    db.session.commit()

    return jsonify(candidate.to_dict()), 201


@app.route('/api/candidates/<int:candidate_id>', methods=['PUT'])
def update_candidate(candidate_id):
    """Update candidate"""
    candidate = Candidate.query.get_or_404(candidate_id)
    data = request.get_json()

    # Update all fields that are present in the request
    for field in ['first_name', 'last_name', 'email', 'phone', 'location',
                  'linkedin_url', 'github_url', 'portfolio_url', 'resume_url',
                  'google_scholar_url', 'research_gate_url', 'arxiv_author_id', 'orcid_id',
                  'h_index', 'citation_count', 'primary_expertise', 'skills',
                  'years_experience', 'status', 'rating', 'notes']:
        if field in data:
            setattr(candidate, field, data[field])

    db.session.commit()
    return jsonify(candidate.to_dict())


@app.route('/api/candidates/<int:candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id):
    """Delete candidate"""
    candidate = Candidate.query.get_or_404(candidate_id)
    db.session.delete(candidate)
    db.session.commit()
    return jsonify({"message": "Candidate deleted successfully"})


# ==================== CANDIDATE ENRICHMENT APIs ====================

@app.route('/api/candidates/<int:candidate_id>/enrich/github', methods=['POST'])
def enrich_from_github(candidate_id):
    """Auto-enrich candidate profile from GitHub API"""
    candidate = Candidate.query.get_or_404(candidate_id)

    if not candidate.github_url:
        return jsonify({"error": "No GitHub URL provided for this candidate"}), 400

    try:
        # Extract username from GitHub URL
        # Handles: https://github.com/username or github.com/username
        username = candidate.github_url.rstrip('/').split('/')[-1]

        # Fetch from GitHub API
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'ATS-Recruiter'
        }

        # Add GitHub token if available for higher rate limits
        github_token = os.environ.get('GITHUB_TOKEN')
        if github_token:
            headers['Authorization'] = f'token {github_token}'

        response = requests.get(f'https://api.github.com/users/{username}', headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()

            # Update candidate with GitHub data
            candidate.github_followers = data.get('followers', 0)
            candidate.github_repos = data.get('public_repos', 0)
            candidate.bio = data.get('bio') or candidate.bio  # Keep existing if GitHub has none
            candidate.location = data.get('location') or candidate.location
            candidate.company = data.get('company') or candidate.company

            # Fetch top programming languages from repos
            languages = get_user_languages(username, headers)
            if languages:
                # Store as comma-separated string in skills field
                existing_skills = candidate.skills or ''
                new_skills = ', '.join(languages)
                if existing_skills:
                    candidate.skills = f"{existing_skills}, {new_skills}"
                else:
                    candidate.skills = new_skills

            db.session.commit()

            return jsonify({
                "success": True,
                "message": f"Enriched profile from GitHub user: {username}",
                "data": {
                    "followers": candidate.github_followers,
                    "repos": candidate.github_repos,
                    "languages": languages,
                    "bio": candidate.bio,
                    "location": candidate.location,
                    "company": candidate.company
                }
            })
        elif response.status_code == 404:
            return jsonify({"error": f"GitHub user '{username}' not found"}), 404
        elif response.status_code == 403:
            return jsonify({"error": "GitHub API rate limit exceeded. Add GITHUB_TOKEN to environment variables."}), 429
        else:
            return jsonify({"error": f"GitHub API error: {response.status_code}"}), 500

    except Exception as e:
        return jsonify({"error": f"Failed to enrich from GitHub: {str(e)}"}), 500


@app.route('/api/candidates/<int:candidate_id>/enrich/arxiv', methods=['POST'])
def enrich_from_arxiv(candidate_id):
    """Auto-fetch publications from arXiv API"""
    candidate = Candidate.query.get_or_404(candidate_id)

    # Need either arXiv author ID or name to search
    author_query = None
    if candidate.arxiv_author_id:
        author_query = candidate.arxiv_author_id
    else:
        # Try searching by name
        author_query = f"{candidate.first_name} {candidate.last_name}"

    try:
        import arxiv

        # Search arXiv for author's papers
        search = arxiv.Search(
            query=f'au:{author_query}',
            max_results=20,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        papers_added = 0
        papers_data = []

        for result in search.results():
            # Check if publication already exists
            arxiv_id = result.entry_id.split('/')[-1]  # Extract ID from URL
            existing = Publication.query.filter_by(
                candidate_id=candidate_id,
                arxiv_id=arxiv_id
            ).first()

            if not existing:
                # Add new publication
                publication = Publication(
                    candidate_id=candidate_id,
                    title=result.title,
                    authors=', '.join([author.name for author in result.authors]),
                    venue='arXiv',
                    year=result.published.year,
                    citation_count=0,  # arXiv API doesn't provide citations
                    paper_url=result.entry_id,
                    arxiv_id=arxiv_id,
                    abstract=result.summary[:500] if result.summary else None  # Truncate abstract
                )
                db.session.add(publication)
                papers_added += 1

                papers_data.append({
                    'title': result.title,
                    'year': result.published.year,
                    'arxiv_id': arxiv_id,
                    'url': result.entry_id
                })

        db.session.commit()

        return jsonify({
            "success": True,
            "message": f"Found {papers_added} new papers from arXiv",
            "papers_added": papers_added,
            "total_publications": len(candidate.publications),
            "papers": papers_data
        })

    except ImportError:
        return jsonify({"error": "arXiv library not installed. Run: pip install arxiv"}), 500
    except Exception as e:
        return jsonify({"error": f"Failed to fetch from arXiv: {str(e)}"}), 500


@app.route('/api/candidates/<int:candidate_id>/enrich/orcid', methods=['POST'])
def enrich_from_orcid(candidate_id):
    """Auto-enrich candidate profile from ORCID API"""
    candidate = Candidate.query.get_or_404(candidate_id)

    if not candidate.orcid_id:
        return jsonify({"error": "No ORCID ID provided for this candidate"}), 400

    try:
        # ORCID public API endpoint
        orcid_id = candidate.orcid_id.replace('https://orcid.org/', '').replace('http://orcid.org/', '')
        url = f'https://pub.orcid.org/v3.0/{orcid_id}/record'

        headers = {
            'Accept': 'application/json'
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()

            # Extract researcher information
            person = data.get('person', {})
            bio = person.get('biography', {})

            # Update candidate bio if available
            if bio and bio.get('content'):
                candidate.bio = bio['content']

            # Extract employment/affiliation
            activities = data.get('activities-summary', {})
            employments = activities.get('employments', {}).get('affiliation-group', [])

            if employments:
                # Get most recent employment
                latest = employments[0].get('summaries', [{}])[0].get('employment-summary', {})
                org = latest.get('organization', {})
                if org.get('name'):
                    candidate.company = org['name']
                if org.get('address', {}).get('city'):
                    city = org['address']['city']
                    country = org['address'].get('country', '')
                    candidate.location = f"{city}, {country}" if country else city

            # Count publications from ORCID
            works = activities.get('works', {}).get('group', [])
            orcid_publication_count = len(works)

            db.session.commit()

            return jsonify({
                "success": True,
                "message": f"Enriched profile from ORCID: {orcid_id}",
                "data": {
                    "orcid_id": orcid_id,
                    "bio": candidate.bio,
                    "company": candidate.company,
                    "location": candidate.location,
                    "orcid_publications": orcid_publication_count
                }
            })
        elif response.status_code == 404:
            return jsonify({"error": f"ORCID ID '{orcid_id}' not found"}), 404
        else:
            return jsonify({"error": f"ORCID API error: {response.status_code}"}), 500

    except Exception as e:
        return jsonify({"error": f"Failed to enrich from ORCID: {str(e)}"}), 500


@app.route('/api/candidates/<int:candidate_id>/enrich/scholar', methods=['POST'])
def enrich_from_scholar(candidate_id):
    """Auto-enrich candidate profile from Google Scholar"""
    candidate = Candidate.query.get_or_404(candidate_id)

    # Need either Google Scholar URL or name to search
    if not candidate.google_scholar_url and not (candidate.first_name and candidate.last_name):
        return jsonify({"error": "Need Google Scholar URL or candidate name"}), 400

    try:
        from scholarly import scholarly, ProxyGenerator

        # Optional: Use a proxy to avoid rate limiting (requires free-proxy package)
        # pg = ProxyGenerator()
        # pg.FreeProxies()
        # scholarly.use_proxy(pg)

        author = None

        if candidate.google_scholar_url:
            # Extract scholar ID from URL
            # Format: https://scholar.google.com/citations?user=SCHOLAR_ID
            if 'user=' in candidate.google_scholar_url:
                scholar_id = candidate.google_scholar_url.split('user=')[1].split('&')[0]
                author = scholarly.search_author_id(scholar_id)
            else:
                return jsonify({"error": "Invalid Google Scholar URL format"}), 400
        else:
            # Search by name
            search_query = f"{candidate.first_name} {candidate.last_name}"
            search_results = scholarly.search_author(search_query)
            author = next(search_results, None)  # Get first result

        if not author:
            return jsonify({"error": "Author not found on Google Scholar"}), 404

        # Fill in author details
        author = scholarly.fill(author)

        # Update candidate with Scholar metrics
        candidate.h_index = author.get('hindex', 0)
        candidate.citation_count = author.get('citedby', 0)

        # Update affiliation if available
        if author.get('affiliation'):
            candidate.company = author['affiliation']

        # Update research interests/expertise
        if author.get('interests'):
            candidate.primary_expertise = author['interests'][0] if author['interests'] else None

        # Fetch publications
        publications = author.get('publications', [])
        papers_added = 0
        papers_data = []

        for pub in publications[:20]:  # Limit to 20 most recent
            pub_filled = scholarly.fill(pub)

            # Check if publication already exists by title
            existing = Publication.query.filter_by(
                candidate_id=candidate_id,
                title=pub_filled['bib'].get('title', '')
            ).first()

            if not existing and pub_filled['bib'].get('title'):
                publication = Publication(
                    candidate_id=candidate_id,
                    title=pub_filled['bib']['title'],
                    authors=pub_filled['bib'].get('author', ''),
                    venue=pub_filled['bib'].get('venue', 'Unknown'),
                    year=int(pub_filled['bib'].get('pub_year', 0)) if pub_filled['bib'].get('pub_year') else None,
                    citation_count=pub_filled.get('num_citations', 0),
                    paper_url=pub_filled.get('pub_url', pub_filled.get('eprint_url', ''))
                )
                db.session.add(publication)
                papers_added += 1

                papers_data.append({
                    'title': publication.title,
                    'year': publication.year,
                    'citations': publication.citation_count
                })

        db.session.commit()

        return jsonify({
            "success": True,
            "message": f"Enriched profile from Google Scholar",
            "data": {
                "h_index": candidate.h_index,
                "citations": candidate.citation_count,
                "affiliation": candidate.company,
                "expertise": candidate.primary_expertise,
                "papers_added": papers_added,
                "total_publications": len(candidate.publications)
            },
            "papers": papers_data[:5]  # Return first 5 papers
        })

    except ImportError:
        return jsonify({"error": "scholarly library not installed. Run: pip install scholarly"}), 500
    except StopIteration:
        return jsonify({"error": "No Google Scholar profile found for this author"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to fetch from Google Scholar: {str(e)}"}), 500


# ==================== EXPANDED SOURCING: HUGGING FACE ====================

@app.route('/api/candidates/<int:candidate_id>/enrich/huggingface', methods=['POST'])
def enrich_from_huggingface(candidate_id):
    """Auto-enrich candidate from Hugging Face - models, datasets, spaces"""
    candidate = Candidate.query.get_or_404(candidate_id)

    if not candidate.huggingface_url:
        return jsonify({"error": "No Hugging Face URL provided for this candidate"}), 400

    try:
        # Extract username from URL: https://huggingface.co/username
        username = candidate.huggingface_url.rstrip('/').split('/')[-1]

        headers = {'User-Agent': 'ATS-Recruiter/2.0'}

        # Fetch user info
        user_resp = requests.get(f'https://huggingface.co/api/users/{username}/overview', headers=headers, timeout=10)

        models = []
        datasets = []
        spaces = []

        # Fetch models by this user
        models_resp = requests.get(f'https://huggingface.co/api/models?author={username}&limit=100', headers=headers, timeout=10)
        if models_resp.status_code == 200:
            models = models_resp.json()

        # Fetch datasets by this user
        datasets_resp = requests.get(f'https://huggingface.co/api/datasets?author={username}&limit=100', headers=headers, timeout=10)
        if datasets_resp.status_code == 200:
            datasets = datasets_resp.json()

        # Fetch spaces by this user
        spaces_resp = requests.get(f'https://huggingface.co/api/spaces?author={username}&limit=100', headers=headers, timeout=10)
        if spaces_resp.status_code == 200:
            spaces = spaces_resp.json()

        # Calculate total likes across all artifacts
        total_likes = sum(m.get('likes', 0) for m in models) + \
                      sum(d.get('likes', 0) for d in datasets) + \
                      sum(s.get('likes', 0) for s in spaces)

        # Update candidate metrics
        candidate.hf_models_count = len(models)
        candidate.hf_datasets_count = len(datasets)
        candidate.hf_spaces_count = len(spaces)
        candidate.hf_likes = total_likes

        # Extract tags/skills from models (pipeline_tag, library_name)
        hf_skills = set()
        for m in models:
            if m.get('pipeline_tag'):
                hf_skills.add(m['pipeline_tag'].replace('-', ' '))
            if m.get('library_name'):
                hf_skills.add(m['library_name'])
            for tag in m.get('tags', []):
                if tag in ['pytorch', 'tensorflow', 'jax', 'transformers', 'diffusers',
                           'reinforcement-learning', 'robotics', 'computer-vision',
                           'object-detection', 'image-segmentation', 'depth-estimation']:
                    hf_skills.add(tag.replace('-', ' '))

        # Merge HF skills into candidate skills
        if hf_skills:
            existing = candidate.skills.split(', ') if candidate.skills else []
            combined = list(set(existing + list(hf_skills)))
            candidate.skills = ', '.join(combined)

        # Extract top models info for response
        top_models = sorted(models, key=lambda m: m.get('downloads', 0), reverse=True)[:5]
        top_model_names = [{'id': m.get('modelId', ''), 'downloads': m.get('downloads', 0),
                            'likes': m.get('likes', 0), 'pipeline': m.get('pipeline_tag', '')}
                           for m in top_models]

        db.session.commit()

        return jsonify({
            "success": True,
            "message": f"Enriched from Hugging Face: {username} — {len(models)} models, {len(datasets)} datasets, {len(spaces)} spaces",
            "data": {
                "username": username,
                "models_count": len(models),
                "datasets_count": len(datasets),
                "spaces_count": len(spaces),
                "total_likes": total_likes,
                "skills_found": list(hf_skills),
                "top_models": top_model_names
            }
        })

    except Exception as e:
        return jsonify({"error": f"Failed to enrich from Hugging Face: {str(e)}"}), 500


# ==================== EXPANDED SOURCING: SEMANTIC SCHOLAR ====================

@app.route('/api/candidates/<int:candidate_id>/enrich/semantic-scholar', methods=['POST'])
def enrich_from_semantic_scholar(candidate_id):
    """Auto-enrich candidate from Semantic Scholar - free API, covers ICRA/IROS/RSS/CoRL"""
    candidate = Candidate.query.get_or_404(candidate_id)

    try:
        headers = {'User-Agent': 'ATS-Recruiter/2.0'}
        s2_api_key = os.environ.get('SEMANTIC_SCHOLAR_API_KEY')
        if s2_api_key:
            headers['x-api-key'] = s2_api_key

        author_id = candidate.semantic_scholar_id
        author_data = None

        if author_id:
            # Direct lookup by Semantic Scholar ID
            resp = requests.get(
                f'https://api.semanticscholar.org/graph/v1/author/{author_id}?fields=name,hIndex,citationCount,paperCount,affiliations,homepage,papers.title,papers.year,papers.citationCount,papers.venue,papers.externalIds,papers.url',
                headers=headers, timeout=15
            )
            if resp.status_code == 200:
                author_data = resp.json()
        else:
            # Search by name
            search_name = f"{candidate.first_name} {candidate.last_name}"
            search_resp = requests.get(
                f'https://api.semanticscholar.org/graph/v1/author/search?query={search_name}&limit=5&fields=name,hIndex,citationCount,paperCount,affiliations',
                headers=headers, timeout=15
            )
            if search_resp.status_code == 200:
                results = search_resp.json().get('data', [])
                if results:
                    # Use the first match
                    best = results[0]
                    author_id = best['authorId']
                    candidate.semantic_scholar_id = author_id

                    # Now fetch full details
                    resp = requests.get(
                        f'https://api.semanticscholar.org/graph/v1/author/{author_id}?fields=name,hIndex,citationCount,paperCount,affiliations,homepage,papers.title,papers.year,papers.citationCount,papers.venue,papers.externalIds,papers.url',
                        headers=headers, timeout=15
                    )
                    if resp.status_code == 200:
                        author_data = resp.json()

        if not author_data:
            return jsonify({"error": "Author not found on Semantic Scholar"}), 404

        # Update candidate metrics
        candidate.s2_paper_count = author_data.get('paperCount', 0)
        candidate.s2_citation_count = author_data.get('citationCount', 0)
        candidate.s2_h_index = author_data.get('hIndex', 0)

        # Update main metrics if they're better than existing
        s2_h = author_data.get('hIndex', 0) or 0
        s2_cite = author_data.get('citationCount', 0) or 0
        if s2_h > (candidate.h_index or 0):
            candidate.h_index = s2_h
        if s2_cite > (candidate.citation_count or 0):
            candidate.citation_count = s2_cite

        # Update affiliation
        affiliations = author_data.get('affiliations', [])
        if affiliations and not candidate.company:
            candidate.company = affiliations[0]

        # Import publications — especially robotics conference papers
        papers = author_data.get('papers', [])
        papers_added = 0
        robotics_papers = 0
        papers_data = []

        for paper in papers[:30]:  # Process top 30
            if not paper.get('title'):
                continue

            # Check if already exists
            existing = Publication.query.filter_by(
                candidate_id=candidate_id,
                title=paper['title']
            ).first()

            if not existing:
                venue = paper.get('venue', '') or ''
                ext_ids = paper.get('externalIds', {}) or {}

                pub = Publication(
                    candidate_id=candidate_id,
                    title=paper['title'],
                    venue=venue,
                    year=paper.get('year'),
                    citation_count=paper.get('citationCount', 0),
                    paper_url=paper.get('url', ''),
                    arxiv_id=ext_ids.get('ArXiv', ''),
                    doi=ext_ids.get('DOI', '')
                )
                db.session.add(pub)
                papers_added += 1

                # Track robotics conference papers
                venue_upper = venue.upper()
                if any(c in venue_upper for c in ['ICRA', 'IROS', 'RSS', 'CORL', 'HUMANOID', 'ROBOT']):
                    robotics_papers += 1

                papers_data.append({
                    'title': paper['title'],
                    'venue': venue,
                    'year': paper.get('year'),
                    'citations': paper.get('citationCount', 0)
                })

        db.session.commit()

        return jsonify({
            "success": True,
            "message": f"Enriched from Semantic Scholar: {candidate.s2_paper_count} papers, h-index {candidate.s2_h_index}, {candidate.s2_citation_count} citations",
            "data": {
                "author_id": author_id,
                "paper_count": candidate.s2_paper_count,
                "citation_count": candidate.s2_citation_count,
                "h_index": candidate.s2_h_index,
                "affiliations": affiliations,
                "papers_added": papers_added,
                "robotics_conference_papers": robotics_papers,
                "papers": papers_data[:10]
            }
        })

    except Exception as e:
        return jsonify({"error": f"Failed to enrich from Semantic Scholar: {str(e)}"}), 500


# ==================== EXPANDED SOURCING: PAPERS WITH CODE ====================

@app.route('/api/candidates/<int:candidate_id>/enrich/papers-with-code', methods=['POST'])
def enrich_from_papers_with_code(candidate_id):
    """Find candidate's papers that have code implementations on Papers With Code"""
    candidate = Candidate.query.get_or_404(candidate_id)

    try:
        headers = {'User-Agent': 'ATS-Recruiter/2.0'}

        # Search Papers With Code by candidate name
        search_name = f"{candidate.first_name} {candidate.last_name}"

        # Papers With Code API - search papers
        resp = requests.get(
            f'https://paperswithcode.com/api/v1/papers/?q={search_name}',
            headers=headers, timeout=15
        )

        if resp.status_code != 200:
            return jsonify({"error": f"Papers With Code API error: {resp.status_code}"}), 500

        data = resp.json()
        results = data.get('results', [])

        papers_found = 0
        papers_with_repos = 0
        papers_data = []
        tasks_found = set()

        for paper in results[:20]:
            title = paper.get('title', '')
            paper_url = paper.get('url_abs', '') or paper.get('url_pdf', '')
            arxiv_id = paper.get('arxiv_id', '')

            # Check if this paper is by our candidate (author matching)
            authors = paper.get('authors', [])
            author_names = [a.lower() for a in authors] if authors else []
            candidate_name_lower = search_name.lower()

            # Flexible name matching
            is_author = any(candidate_name_lower in a or
                           candidate.last_name.lower() in a
                           for a in author_names) if author_names else True

            if not is_author:
                continue

            papers_found += 1

            # Fetch code repositories for this paper
            paper_id = paper.get('id', '')
            repos = []
            if paper_id:
                repo_resp = requests.get(
                    f'https://paperswithcode.com/api/v1/papers/{paper_id}/repositories/',
                    headers=headers, timeout=10
                )
                if repo_resp.status_code == 200:
                    repo_data = repo_resp.json()
                    repos = repo_data.get('results', [])
                    if repos:
                        papers_with_repos += 1

            # Fetch tasks/benchmarks this paper addresses
            if paper_id:
                task_resp = requests.get(
                    f'https://paperswithcode.com/api/v1/papers/{paper_id}/tasks/',
                    headers=headers, timeout=10
                )
                if task_resp.status_code == 200:
                    task_data = task_resp.json()
                    for task in task_data.get('results', []):
                        task_name = task.get('name', '')
                        if task_name:
                            tasks_found.add(task_name)

            # Add to existing publications if not already there
            if title:
                existing = Publication.query.filter_by(
                    candidate_id=candidate_id,
                    title=title
                ).first()

                if not existing:
                    pub = Publication(
                        candidate_id=candidate_id,
                        title=title,
                        authors=', '.join(authors) if authors else '',
                        venue=paper.get('conference', '') or 'Papers With Code',
                        year=int(paper.get('published', '0000')[:4]) if paper.get('published') else None,
                        paper_url=paper_url,
                        arxiv_id=arxiv_id
                    )
                    db.session.add(pub)

            papers_data.append({
                'title': title,
                'arxiv_id': arxiv_id,
                'has_code': len(repos) > 0,
                'repo_count': len(repos),
                'top_repo': repos[0].get('url', '') if repos else None,
                'stars': repos[0].get('stars', 0) if repos else 0,
                'tasks': [t.get('name', '') for t in task_data.get('results', [])] if paper_id else []
            })

        # Extract robotics/physical AI related tasks as skills
        robotics_tasks = [t for t in tasks_found if any(kw in t.lower() for kw in
                         ['robot', 'navigation', 'slam', 'object detection', 'depth estimation',
                          'point cloud', 'pose estimation', 'motion', 'autonomous', 'segmentation',
                          'visual', '3d', 'lidar', 'manipulation', 'grasping'])]

        if robotics_tasks:
            existing = candidate.skills.split(', ') if candidate.skills else []
            combined = list(set(existing + robotics_tasks))
            candidate.skills = ', '.join(combined)

        db.session.commit()

        return jsonify({
            "success": True,
            "message": f"Found {papers_found} papers, {papers_with_repos} with code implementations",
            "data": {
                "papers_found": papers_found,
                "papers_with_code": papers_with_repos,
                "tasks": list(tasks_found),
                "robotics_tasks": robotics_tasks,
                "papers": papers_data[:10]
            }
        })

    except Exception as e:
        return jsonify({"error": f"Failed to search Papers With Code: {str(e)}"}), 500


# ==================== PHASE 3: AI/ML FEATURES ====================

# Top AI/ML conferences for tracking
TOP_CONFERENCES = [
    'NeurIPS', 'NIPS', 'ICML', 'ICLR', 'CVPR', 'ICCV', 'ECCV',
    'AAAI', 'IJCAI', 'ACL', 'EMNLP', 'NAACL', 'KDD', 'SIGIR',
    'ICRA', 'IROS', 'RSS', 'CoRL'
]

# AI/ML + Physical AI skills taxonomy
AI_ML_SKILLS = {
    'deep_learning': ['deep learning', 'neural network', 'cnn', 'rnn', 'lstm', 'transformer', 'gpt', 'bert', 'attention', 'diffusion'],
    'computer_vision': ['computer vision', 'image processing', 'object detection', 'segmentation', 'yolo', 'rcnn', 'opencv', 'depth estimation', 'point cloud', '3d reconstruction', 'stereo vision'],
    'nlp': ['nlp', 'natural language processing', 'text mining', 'language model', 'tokenization', 'embedding'],
    'reinforcement_learning': ['reinforcement learning', 'rl', 'policy gradient', 'q-learning', 'dqn', 'ppo', 'actor-critic', 'sac', 'sim-to-real', 'domain randomization', 'isaac gym'],
    'robotics': ['robotics', 'robot', 'manipulation', 'navigation', 'slam', 'ros', 'ros2', 'motion planning', 'humanoid', 'bipedal', 'quadruped', 'legged', 'locomotion', 'grasping', 'dexterous'],
    'autonomous_systems': ['autonomous', 'self-driving', 'lidar', 'sensor fusion', 'kalman filter', 'path planning', 'trajectory optimization', 'multi-robot', 'swarm'],
    'simulation': ['mujoco', 'isaac sim', 'gazebo', 'carla', 'pybullet', 'drake', 'unity', 'unreal'],
    'ml_frameworks': ['pytorch', 'tensorflow', 'keras', 'jax', 'scikit-learn', 'pandas', 'numpy', 'huggingface', 'transformers', 'diffusers'],
    'programming': ['python', 'c++', 'java', 'javascript', 'go', 'rust', 'cuda', 'tensorrt', 'onnx'],
    'edge_ai': ['jetson', 'edge ai', 'embedded', 'real-time', 'tensorrt', 'onnx', 'quantization', 'pruning', 'model compression'],
    'ml_ops': ['docker', 'kubernetes', 'mlflow', 'wandb', 'aws', 'gcp', 'azure', 'weights & biases']
}


@app.route('/api/candidates/<int:candidate_id>/extract-skills', methods=['POST'])
def extract_skills_from_candidate(candidate_id):
    """Auto-extract AI/ML skills from candidate's bio, publications, and GitHub"""
    candidate = Candidate.query.get_or_404(candidate_id)

    # Collect all text sources
    text_sources = []

    if candidate.bio:
        text_sources.append(candidate.bio.lower())
    if candidate.primary_expertise:
        text_sources.append(candidate.primary_expertise.lower())

    # Add publication titles and abstracts
    for pub in candidate.publications:
        if pub.title:
            text_sources.append(pub.title.lower())
        if hasattr(pub, 'abstract') and pub.abstract:
            text_sources.append(pub.abstract.lower())

    # Combine all text
    combined_text = ' '.join(text_sources)

    # Extract skills by category
    extracted_skills = {}
    skill_count = 0

    for category, keywords in AI_ML_SKILLS.items():
        found_skills = []
        for keyword in keywords:
            if keyword in combined_text:
                found_skills.append(keyword)
                skill_count += 1

        if found_skills:
            extracted_skills[category] = list(set(found_skills))  # Remove duplicates

    # Update candidate skills field
    all_skills = []
    for category_skills in extracted_skills.values():
        all_skills.extend(category_skills)

    if all_skills:
        # Merge with existing skills
        existing = candidate.skills.split(', ') if candidate.skills else []
        combined = list(set(existing + all_skills))
        candidate.skills = ', '.join(combined)
        db.session.commit()

    return jsonify({
        "success": True,
        "skills_extracted": skill_count,
        "skills_by_category": extracted_skills,
        "total_skills": len(all_skills),
        "updated_skills": candidate.skills
    })


@app.route('/api/candidates/<int:candidate_id>/impact-score', methods=['GET'])
def calculate_research_impact_score(candidate_id):
    """Calculate research impact score based on multiple factors"""
    candidate = Candidate.query.get_or_404(candidate_id)

    # Initialize score components
    score_breakdown = {
        'h_index_score': 0,
        'citation_score': 0,
        'publication_score': 0,
        'github_score': 0,
        'conference_score': 0,
        'huggingface_score': 0,
        'total_score': 0
    }

    # H-Index Score (0-25 points)
    # h-index of 20+ is excellent, scale accordingly
    if candidate.h_index:
        score_breakdown['h_index_score'] = min(candidate.h_index * 1.25, 25)

    # Citation Score (0-25 points)
    # 1000+ citations is excellent
    if candidate.citation_count:
        score_breakdown['citation_score'] = min(candidate.citation_count / 40, 25)

    # Publication Score (0-20 points)
    # 20+ publications is excellent
    pub_count = len(candidate.publications)
    score_breakdown['publication_score'] = min(pub_count, 20)

    # GitHub Activity Score (0-15 points)
    # Followers (0-10 points), Repos (0-5 points)
    if candidate.github_followers:
        score_breakdown['github_score'] += min(candidate.github_followers / 100, 10)
    if candidate.github_repos:
        score_breakdown['github_score'] += min(candidate.github_repos / 20, 5)

    # Top Conference Publications (0-15 points)
    # Publications in NeurIPS, ICML, CVPR, etc.
    conference_pubs = 0
    for pub in candidate.publications:
        venue = pub.venue.upper() if pub.venue else ''
        for conf in TOP_CONFERENCES:
            if conf in venue:
                conference_pubs += 1
                break
    score_breakdown['conference_score'] = min(conference_pubs * 3, 15)

    # Hugging Face Builder Score (0-10 points)
    # Models (0-5), Datasets+Spaces (0-3), Likes (0-2)
    hf_model_pts = min((candidate.hf_models_count or 0) * 1.0, 5)
    hf_other_pts = min(((candidate.hf_datasets_count or 0) + (candidate.hf_spaces_count or 0)) * 0.5, 3)
    hf_likes_pts = min((candidate.hf_likes or 0) / 50, 2)
    score_breakdown['huggingface_score'] = round(hf_model_pts + hf_other_pts + hf_likes_pts, 2)

    # Calculate total (out of 110 — normalized to show builders get credit)
    score_breakdown['total_score'] = round(sum([
        score_breakdown['h_index_score'],
        score_breakdown['citation_score'],
        score_breakdown['publication_score'],
        score_breakdown['github_score'],
        score_breakdown['conference_score'],
        score_breakdown['huggingface_score']
    ]), 2)

    # Determine tier
    total = score_breakdown['total_score']
    if total >= 80:
        tier = 'World-Class Researcher'
    elif total >= 60:
        tier = 'Senior Researcher'
    elif total >= 40:
        tier = 'Established Researcher'
    elif total >= 20:
        tier = 'Emerging Researcher'
    else:
        tier = 'Early Career'

    return jsonify({
        "candidate_id": candidate_id,
        "candidate_name": f"{candidate.first_name} {candidate.last_name}",
        "impact_score": score_breakdown['total_score'],
        "tier": tier,
        "breakdown": score_breakdown,
        "metrics": {
            "h_index": candidate.h_index,
            "citations": candidate.citation_count,
            "publications": pub_count,
            "github_followers": candidate.github_followers,
            "github_repos": candidate.github_repos,
            "top_conference_pubs": conference_pubs,
            "hf_models": candidate.hf_models_count,
            "hf_datasets": candidate.hf_datasets_count,
            "hf_spaces": candidate.hf_spaces_count,
            "hf_likes": candidate.hf_likes
        }
    })


@app.route('/api/jobs/<int:job_id>/match-candidates', methods=['POST'])
def match_candidates_to_job(job_id):
    """AI-powered candidate matching for a job"""
    job = Job.query.get_or_404(job_id)

    # Get match parameters
    data = request.get_json() or {}
    min_score = data.get('min_score', 0)
    top_n = data.get('top_n', 10)

    # Get all candidates
    candidates = Candidate.query.all()

    # Calculate match score for each candidate
    matches = []

    for candidate in candidates:
        match_score = 0
        score_details = {}

        # 1. Expertise Match (0-30 points)
        expertise_score = 0
        if job.required_expertise and candidate.primary_expertise:
            job_expertise = job.required_expertise.lower()
            candidate_expertise = candidate.primary_expertise.lower()

            # Exact match
            if candidate_expertise in job_expertise or job_expertise in candidate_expertise:
                expertise_score = 30
            # Partial match
            elif any(word in job_expertise for word in candidate_expertise.split()):
                expertise_score = 15

        score_details['expertise_match'] = expertise_score
        match_score += expertise_score

        # 2. Skills Match (0-25 points)
        skills_score = 0
        if job.required_skills and candidate.skills:
            job_skills = set(job.required_skills.lower().split(','))
            candidate_skills = set(candidate.skills.lower().split(','))

            # Count overlapping skills
            overlap = len(job_skills.intersection(candidate_skills))
            total_required = len(job_skills)

            if total_required > 0:
                skills_score = (overlap / total_required) * 25

        score_details['skills_match'] = round(skills_score, 2)
        match_score += skills_score

        # 3. Research Impact (0-20 points)
        # Use h-index and citations as proxy
        impact_score = 0
        if candidate.h_index:
            impact_score += min(candidate.h_index, 10)
        if candidate.citation_count:
            impact_score += min(candidate.citation_count / 100, 10)

        score_details['research_impact'] = round(impact_score, 2)
        match_score += impact_score

        # 4. Experience Level (0-15 points)
        experience_score = 0
        if candidate.years_experience:
            # Assume job requires 5 years (adjust based on job.experience_required if available)
            target_years = 5
            if hasattr(job, 'experience_required') and job.experience_required:
                target_years = job.experience_required

            # Perfect match at target, decay above/below
            diff = abs(candidate.years_experience - target_years)
            experience_score = max(15 - diff * 2, 0)

        score_details['experience_match'] = round(experience_score, 2)
        match_score += experience_score

        # 5. GitHub Activity (0-10 points)
        github_score = 0
        if candidate.github_repos:
            github_score += min(candidate.github_repos / 10, 5)
        if candidate.github_followers:
            github_score += min(candidate.github_followers / 50, 5)

        score_details['github_activity'] = round(github_score, 2)
        match_score += github_score

        # Total score (out of 100)
        total_score = round(match_score, 2)

        # Only include if above minimum score
        if total_score >= min_score:
            matches.append({
                'candidate_id': candidate.id,
                'candidate_name': f"{candidate.first_name} {candidate.last_name}",
                'email': candidate.email,
                'match_score': total_score,
                'score_breakdown': score_details,
                'primary_expertise': candidate.primary_expertise,
                'h_index': candidate.h_index,
                'citations': candidate.citation_count,
                'github_url': candidate.github_url
            })

    # Sort by match score (descending)
    matches.sort(key=lambda x: x['match_score'], reverse=True)

    # Return top N matches
    top_matches = matches[:top_n]

    return jsonify({
        "job_id": job_id,
        "job_title": job.title,
        "total_candidates_evaluated": len(candidates),
        "matches_found": len(matches),
        "top_matches": top_matches
    })


@app.route('/api/publications/analyze-conferences', methods=['GET'])
def analyze_conference_publications():
    """Analyze all publications to identify top conference papers"""
    all_publications = Publication.query.all()

    conference_stats = {}
    top_conference_papers = []

    for pub in all_publications:
        venue_name = pub.venue.upper() if pub.venue else ''

        # Check if it's a top conference
        for conf in TOP_CONFERENCES:
            if conf in venue_name:
                # Track conference stats
                if conf not in conference_stats:
                    conference_stats[conf] = 0
                conference_stats[conf] += 1

                # Add to top conference papers
                candidate = Candidate.query.get(pub.candidate_id)
                top_conference_papers.append({
                    'publication_id': pub.id,
                    'title': pub.title,
                    'conference': conf,
                    'year': pub.year,
                    'citations': pub.citation_count,
                    'candidate_name': f"{candidate.first_name} {candidate.last_name}" if candidate else 'Unknown',
                    'candidate_id': pub.candidate_id
                })
                break

    # Sort conferences by paper count
    sorted_conferences = sorted(conference_stats.items(), key=lambda x: x[1], reverse=True)

    # Sort papers by citations
    top_conference_papers.sort(key=lambda x: x['citations'] or 0, reverse=True)

    return jsonify({
        "total_publications": len(all_publications),
        "top_conference_papers": len(top_conference_papers),
        "conference_breakdown": dict(sorted_conferences),
        "papers": top_conference_papers[:50]  # Return top 50
    })


# ==================== JOBS ====================

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get all jobs"""
    status = request.args.get('status')

    query = Job.query
    if status:
        query = query.filter_by(status=status)

    jobs = query.order_by(Job.posted_date.desc()).all()
    return jsonify({
        "jobs": [j.to_dict() for j in jobs],
        "total": len(jobs)
    })


@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get single job"""
    job = Job.query.get_or_404(job_id)
    data = job.to_dict()
    data['applications'] = [app.to_dict() for app in job.applications]
    return jsonify(data)


@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Create new job"""
    data = request.get_json()

    if not data or 'title' not in data or 'company' not in data:
        return jsonify({"error": "Title and company are required"}), 400

    job = Job(
        title=data['title'],
        company=data['company'],
        location=data.get('location'),
        job_type=data.get('job_type'),
        description=data.get('description'),
        requirements=data.get('requirements'),
        responsibilities=data.get('responsibilities'),
        required_expertise=data.get('required_expertise'),
        required_skills=data.get('required_skills'),
        education_required=data.get('education_required'),
        research_focus=data.get('research_focus'),
        salary_min=data.get('salary_min'),
        salary_max=data.get('salary_max'),
        currency=data.get('currency', 'USD'),
        status=data.get('status', 'open'),
        confidential=data.get('confidential', False)
    )

    db.session.add(job)
    db.session.commit()

    return jsonify(job.to_dict()), 201


@app.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    """Update job"""
    job = Job.query.get_or_404(job_id)
    data = request.get_json()

    for field in ['title', 'company', 'location', 'job_type', 'description',
                  'requirements', 'responsibilities', 'required_expertise',
                  'required_skills', 'education_required', 'research_focus',
                  'salary_min', 'salary_max', 'currency', 'status', 'confidential']:
        if field in data:
            setattr(job, field, data[field])

    db.session.commit()
    return jsonify(job.to_dict())


@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Delete job"""
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return jsonify({"message": "Job deleted successfully"})


@app.route('/api/jobs/<int:job_id>/reveal', methods=['POST'])
def reveal_job_company(job_id):
    """Reveal company name for confidential job (when company shows interest)"""
    job = Job.query.get_or_404(job_id)
    return jsonify(job.to_dict(show_company=True))


# ==================== APPLICATIONS ====================

@app.route('/api/applications', methods=['GET'])
def get_applications():
    """Get all applications"""
    applications = Application.query.order_by(Application.applied_date.desc()).all()
    return jsonify({
        "applications": [a.to_dict() for a in applications],
        "total": len(applications)
    })


@app.route('/api/applications', methods=['POST'])
def create_application():
    """Create new application"""
    data = request.get_json()

    if not data or 'candidate_id' not in data or 'job_id' not in data:
        return jsonify({"error": "Candidate ID and Job ID are required"}), 400

    # Prevent duplicate applications
    existing = Application.query.filter_by(
        candidate_id=data['candidate_id'],
        job_id=data['job_id']
    ).first()
    if existing:
        return jsonify({"error": "This candidate has already applied for this position"}), 409

    application = Application(
        candidate_id=data['candidate_id'],
        job_id=data['job_id'],
        status=data.get('status', 'applied'),
        stage=data.get('stage'),
        source=data.get('source'),
        technical_score=data.get('technical_score'),
        research_score=data.get('research_score'),
        culture_fit_score=data.get('culture_fit_score'),
        overall_score=data.get('overall_score'),
        notes=data.get('notes')
    )

    db.session.add(application)
    db.session.commit()

    return jsonify(application.to_dict()), 201


@app.route('/api/applications/<int:application_id>', methods=['PUT'])
def update_application(application_id):
    """Update application"""
    application = Application.query.get_or_404(application_id)
    data = request.get_json()

    for field in ['status', 'stage', 'source', 'technical_score', 'research_score',
                  'culture_fit_score', 'overall_score', 'notes']:
        if field in data:
            setattr(application, field, data[field])

    db.session.commit()
    return jsonify(application.to_dict())


@app.route('/api/applications/<int:application_id>', methods=['DELETE'])
def delete_application(application_id):
    """Delete application"""
    application = Application.query.get_or_404(application_id)
    db.session.delete(application)
    db.session.commit()
    return jsonify({"message": "Application deleted successfully"})


# ==================== PUBLICATIONS ====================

@app.route('/api/candidates/<int:candidate_id>/publications', methods=['GET'])
def get_candidate_publications(candidate_id):
    """Get all publications for a candidate"""
    candidate = Candidate.query.get_or_404(candidate_id)
    publications = Publication.query.filter_by(candidate_id=candidate_id).order_by(Publication.year.desc()).all()
    return jsonify({
        "publications": [p.to_dict() for p in publications],
        "total": len(publications)
    })


@app.route('/api/publications', methods=['POST'])
def create_publication():
    """Add publication to candidate"""
    data = request.get_json()

    if not data or 'candidate_id' not in data or 'title' not in data:
        return jsonify({"error": "Candidate ID and title are required"}), 400

    publication = Publication(
        candidate_id=data['candidate_id'],
        title=data['title'],
        authors=data.get('authors'),
        venue=data.get('venue'),
        year=data.get('year'),
        paper_url=data.get('paper_url'),
        arxiv_id=data.get('arxiv_id'),
        doi=data.get('doi'),
        citation_count=data.get('citation_count', 0),
        research_area=data.get('research_area'),
        keywords=data.get('keywords'),
        abstract=data.get('abstract')
    )

    db.session.add(publication)
    db.session.commit()

    return jsonify(publication.to_dict()), 201


@app.route('/api/publications/<int:publication_id>', methods=['DELETE'])
def delete_publication(publication_id):
    """Delete publication"""
    publication = Publication.query.get_or_404(publication_id)
    db.session.delete(publication)
    db.session.commit()
    return jsonify({"message": "Publication deleted successfully"})


# ==================== STATS & DASHBOARD ====================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    total_candidates = Candidate.query.count()
    total_jobs = Job.query.count()
    total_applications = Application.query.count()

    active_candidates = Candidate.query.filter(Candidate.status.in_(['reviewing', 'interviewing'])).count()
    open_jobs = Job.query.filter_by(status='open').count()

    # Top expertise areas
    candidates = Candidate.query.all()
    expertise_counts = {}
    for c in candidates:
        if c.primary_expertise:
            expertise_counts[c.primary_expertise] = expertise_counts.get(c.primary_expertise, 0) + 1

    return jsonify({
        "total_candidates": total_candidates,
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "active_candidates": active_candidates,
        "open_jobs": open_jobs,
        "top_expertise_areas": expertise_counts
    })


# ==================== BOOLEAN SEARCH API ====================

@app.route('/api/boolean-search', methods=['POST'])
def execute_boolean_search():
    """Execute Boolean search across multiple platforms"""
    data = request.get_json()

    if not data or 'query' not in data:
        return jsonify({"error": "Query is required"}), 400

    query = data['query']
    data_sources = data.get('data_sources', ['GitHub'])
    execution_mode = data.get('execution_mode', 'on-demand')

    results = {
        'query': query,
        'sources': data_sources,
        'timestamp': datetime.utcnow().isoformat(),
        'results': {}
    }

    # GitHub Search
    if 'GitHub' in data_sources:
        try:
            github_results = search_github(query)
            results['results']['GitHub'] = github_results
        except Exception as e:
            results['results']['GitHub'] = {'error': str(e), 'results': []}

    # LinkedIn Search (requires API credentials)
    if 'LinkedIn' in data_sources:
        results['results']['LinkedIn'] = {
            'message': 'LinkedIn search requires API credentials. Use the Copy button to paste the query into LinkedIn manually.',
            'query_url': f'https://www.linkedin.com/search/results/people/?keywords={query.replace(" ", "%20")}',
            'results': []
        }

    # Google Scholar Search (no official API)
    if 'Google Scholar' in data_sources:
        results['results']['Google Scholar'] = {
            'message': 'Google Scholar has no official API. Use the Copy button to paste the query into Google Scholar manually.',
            'query_url': f'https://scholar.google.com/scholar?q={query.replace(" ", "+")}',
            'results': []
        }

    return jsonify(results), 200


def get_user_languages(username, headers):
    """Fetch top programming languages from user's repositories"""
    try:
        repos_url = f'https://api.github.com/users/{username}/repos?sort=updated&per_page=10'
        repos_response = requests.get(repos_url, headers=headers, timeout=5)

        if repos_response.status_code == 200:
            repos = repos_response.json()
            languages = {}

            # Collect languages from repos
            for repo in repos:
                if repo.get('language'):
                    lang = repo['language']
                    languages[lang] = languages.get(lang, 0) + 1

            # Sort by frequency and return top 5
            sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
            return [lang[0] for lang in sorted_langs[:5]]

        return []
    except Exception as e:
        print(f"Error fetching languages for {username}: {e}")
        return []


def get_user_details(user_url, headers):
    """Fetch detailed user profile from GitHub API"""
    try:
        response = requests.get(user_url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            print(f"GitHub API rate limit exceeded! Status: {response.status_code}")
            print(f"Rate limit info: {response.headers.get('X-RateLimit-Remaining', 'N/A')} remaining")
            return None
        elif response.status_code == 429:
            print(f"GitHub API rate limit - too many requests: {response.status_code}")
            return None
        else:
            print(f"GitHub API error fetching user details: Status {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching user details: {e}")
        return None


def search_github(query):
    """Search GitHub for users matching the Boolean query with detailed profiles"""
    # Extract keywords from Boolean query for GitHub API
    # GitHub API doesn't support full Boolean syntax, so we extract key terms
    keywords = extract_keywords_from_boolean(query)

    # GitHub API endpoint
    search_query = ' '.join(keywords[:5])  # Limit to 5 keywords
    url = f'https://api.github.com/search/users?q={search_query}&per_page=10'

    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'AI-ML-ATS-BooleanSearch'
    }

    # Add GitHub token if available
    github_token = os.environ.get('GITHUB_TOKEN')
    if github_token:
        headers['Authorization'] = f'token {github_token}'

    response = requests.get(url, headers=headers, timeout=10)

    # Check rate limit status
    if response.status_code == 200:
        rate_limit_remaining = response.headers.get('X-RateLimit-Remaining', 'Unknown')
        print(f"GitHub API rate limit remaining: {rate_limit_remaining}")

    if response.status_code == 200:
        data = response.json()
        users = data.get('items', [])

        # Fetch detailed info for each user
        enriched_users = []
        rate_limited = False
        for user in users[:10]:
            # Get detailed profile
            user_details = get_user_details(user.get('url'), headers)

            if user_details:
                # Get top programming languages
                languages = get_user_languages(user.get('login'), headers)

                enriched_users.append({
                    'username': user_details.get('login'),
                    'name': user_details.get('name') or user_details.get('login'),
                    'profile_url': user_details.get('html_url'),
                    'avatar': user_details.get('avatar_url'),
                    'bio': user_details.get('bio'),
                    'location': user_details.get('location'),
                    'company': user_details.get('company'),
                    'email': user_details.get('email'),
                    'followers': user_details.get('followers', 0),
                    'following': user_details.get('following', 0),
                    'public_repos': user_details.get('public_repos', 0),
                    'languages': languages,
                    'type': user_details.get('type'),
                    'score': user.get('score')
                })
            else:
                # Fallback to basic info if detailed fetch fails
                rate_limited = True
                print(f"WARNING: Falling back to basic profile for {user.get('login')} - detailed fetch failed")
                enriched_users.append({
                    'username': user.get('login'),
                    'name': user.get('login'),
                    'profile_url': user.get('html_url'),
                    'avatar': user.get('avatar_url'),
                    'bio': None,
                    'location': None,
                    'company': None,
                    'email': None,
                    'followers': 0,
                    'following': 0,
                    'public_repos': 0,
                    'languages': [],
                    'type': user.get('type'),
                    'score': user.get('score')
                })

        message = f'Found {len(enriched_users)} GitHub users with detailed profiles'
        if rate_limited:
            message += ' (⚠️ Some profiles may have limited data due to GitHub API rate limits. Add a GITHUB_TOKEN environment variable for higher limits.)'

        return {
            'total_count': data.get('total_count', 0),
            'results': enriched_users,
            'search_query': search_query,
            'message': message,
            'rate_limited': rate_limited
        }
    else:
        return {
            'error': f'GitHub API error: {response.status_code}',
            'message': 'GitHub search failed. You may need to add a GITHUB_TOKEN.',
            'results': []
        }


def extract_keywords_from_boolean(query):
    """Extract searchable keywords from Boolean query"""
    # Remove Boolean operators and special characters
    cleaned = re.sub(r'\(|\)|AND|OR|NOT|"', ' ', query, flags=re.IGNORECASE)
    # Remove comments
    cleaned = re.sub(r'#.*', '', cleaned)
    # Split into words and filter
    keywords = [word.strip() for word in cleaned.split() if len(word.strip()) > 2]
    return keywords


@app.route('/api/saved-searches', methods=['POST'])
def save_search():
    """Save a Boolean search"""
    data = request.get_json()

    if not data or 'query' not in data:
        return jsonify({"error": "Query is required"}), 400

    saved_search = SavedSearch(
        search_query=data['query'],
        data_sources=','.join(data.get('data_sources', [])),
        name=data.get('name'),
        description=data.get('description'),
        total_results=data.get('total_results', 0),
        github_results_count=data.get('github_results_count', 0)
    )

    db.session.add(saved_search)
    db.session.commit()

    return jsonify(saved_search.to_dict()), 201


@app.route('/api/saved-searches', methods=['GET'])
def get_saved_searches():
    """Get all saved searches"""
    searches = SavedSearch.query.order_by(SavedSearch.last_executed.desc()).all()
    return jsonify([search.to_dict() for search in searches])


@app.route('/api/saved-searches/<int:search_id>', methods=['DELETE'])
def delete_saved_search(search_id):
    """Delete a saved search"""
    search = SavedSearch.query.get_or_404(search_id)
    db.session.delete(search)
    db.session.commit()
    return jsonify({"message": "Search deleted successfully"})


@app.route('/api/export-candidates', methods=['POST'])
def export_candidates():
    """Export GitHub users to candidates"""
    data = request.get_json()

    if not data or 'candidates' not in data:
        return jsonify({"error": "Candidates list is required"}), 400

    candidates_data = data['candidates']
    created_candidates = []
    skipped_candidates = []

    for candidate_data in candidates_data:
        # Check if candidate already exists by GitHub URL
        github_url = candidate_data.get('profile_url')
        if github_url:
            existing = Candidate.query.filter_by(github_url=github_url).first()
            if existing:
                skipped_candidates.append({
                    'name': candidate_data.get('name'),
                    'reason': 'Already exists'
                })
                continue

        # Get data from enriched GitHub profile
        username = candidate_data.get('username', 'unknown')
        full_name = candidate_data.get('name', username)
        github_email = candidate_data.get('email')

        # Generate email - use GitHub email if available, otherwise placeholder
        if github_email:
            email = github_email
        else:
            email = f"{username}@github.user"

        # Check if email exists
        if Candidate.query.filter_by(email=email).first():
            email = f"{username}_{int(datetime.utcnow().timestamp())}@github.user"

        # Smart expertise detection based on languages
        languages = candidate_data.get('languages', [])
        expertise = candidate_data.get('expertise')
        if not expertise and languages:
            # Map languages to expertise areas
            lang_map = {
                'Python': 'Machine Learning / Data Science',
                'JavaScript': 'Full Stack Development',
                'TypeScript': 'Full Stack Development',
                'Java': 'Backend Development',
                'Go': 'Backend / Systems Programming',
                'Rust': 'Systems Programming',
                'C++': 'Systems / High Performance Computing',
                'C': 'Systems Programming',
                'Swift': 'iOS Development',
                'Kotlin': 'Android Development',
                'Ruby': 'Backend Development',
                'PHP': 'Web Development'
            }
            expertise = lang_map.get(languages[0], 'Software Engineering')

        # Build bio/notes with imported info
        bio_parts = []
        if candidate_data.get('bio'):
            bio_parts.append(candidate_data['bio'])
        bio_parts.append(f"Imported from Boolean search on {datetime.utcnow().strftime('%Y-%m-%d')}")
        if languages:
            bio_parts.append(f"Languages: {', '.join(languages)}")

        # Create new candidate with enriched data
        try:
            candidate = Candidate(
                first_name=full_name.split()[0] if ' ' in full_name else full_name,
                last_name=full_name.split()[-1] if ' ' in full_name and len(full_name.split()) > 1 else 'User',
                email=email,
                github_url=github_url,
                location=candidate_data.get('location'),
                company=candidate_data.get('company'),
                bio=candidate_data.get('bio'),
                github_followers=candidate_data.get('followers', 0),
                github_repos=candidate_data.get('public_repos', 0),
                primary_expertise=expertise or 'Software Engineering',
                skills=','.join(languages) if languages else None,
                status='new',
                notes=' | '.join(bio_parts)
            )

            db.session.add(candidate)
            db.session.commit()
            created_candidates.append(candidate.to_dict())
        except Exception as e:
            skipped_candidates.append({
                'name': full_name,
                'reason': str(e)
            })

    return jsonify({
        'created': len(created_candidates),
        'skipped': len(skipped_candidates),
        'candidates': created_candidates,
        'skipped_details': skipped_candidates
    }), 201


# ==================== PHASE 4: ADVANCED FEATURES ====================

# Email Campaign Model
class EmailCampaign(db.Model):
    """Email campaign for candidate outreach"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(500), nullable=False)
    body = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='draft')  # draft, scheduled, sent, paused
    scheduled_at = db.Column(db.DateTime)
    sent_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Stats
    total_recipients = db.Column(db.Integer, default=0)
    sent_count = db.Column(db.Integer, default=0)
    opened_count = db.Column(db.Integer, default=0)
    clicked_count = db.Column(db.Integer, default=0)
    replied_count = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'subject': self.subject,
            'body': self.body,
            'status': self.status,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'created_at': self.created_at.isoformat(),
            'total_recipients': self.total_recipients,
            'sent_count': self.sent_count,
            'opened_count': self.opened_count,
            'clicked_count': self.clicked_count,
            'replied_count': self.replied_count,
            'open_rate': round((self.opened_count / self.sent_count * 100), 1) if self.sent_count > 0 else 0,
            'click_rate': round((self.clicked_count / self.sent_count * 100), 1) if self.sent_count > 0 else 0,
            'reply_rate': round((self.replied_count / self.sent_count * 100), 1) if self.sent_count > 0 else 0
        }


# Interview Model
class Interview(db.Model):
    """Interview scheduling"""
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)

    interview_type = db.Column(db.String(100))  # phone, video, onsite, technical
    scheduled_at = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, default=60)
    location = db.Column(db.String(300))  # Zoom link, office address, etc.

    interviewers = db.Column(db.Text)  # JSON array of interviewer names/emails
    notes = db.Column(db.Text)

    status = db.Column(db.String(50), default='scheduled')  # scheduled, completed, cancelled, no_show
    feedback = db.Column(db.Text)
    rating = db.Column(db.Integer)  # 1-5 rating

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        candidate = Candidate.query.get(self.candidate_id)
        job = Job.query.get(self.job_id)
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'candidate_name': f"{candidate.first_name} {candidate.last_name}" if candidate else 'Unknown',
            'job_id': self.job_id,
            'job_title': job.title if job else 'Unknown',
            'interview_type': self.interview_type,
            'scheduled_at': self.scheduled_at.isoformat(),
            'duration_minutes': self.duration_minutes,
            'location': self.location,
            'interviewers': self.interviewers,
            'notes': self.notes,
            'status': self.status,
            'feedback': self.feedback,
            'rating': self.rating,
            'created_at': self.created_at.isoformat()
        }


# Offer Model
class Offer(db.Model):
    """Job offer management"""
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)

    salary = db.Column(db.Integer)
    equity = db.Column(db.String(100))  # e.g., "0.1%"
    signing_bonus = db.Column(db.Integer)
    start_date = db.Column(db.Date)

    status = db.Column(db.String(50), default='draft')  # draft, sent, negotiating, accepted, declined, expired
    sent_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)
    responded_at = db.Column(db.DateTime)

    notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        candidate = Candidate.query.get(self.candidate_id)
        job = Job.query.get(self.job_id)
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'candidate_name': f"{candidate.first_name} {candidate.last_name}" if candidate else 'Unknown',
            'job_id': self.job_id,
            'job_title': job.title if job else 'Unknown',
            'salary': self.salary,
            'equity': self.equity,
            'signing_bonus': self.signing_bonus,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'status': self.status,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'responded_at': self.responded_at.isoformat() if self.responded_at else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }


# ==================== EMAIL CAMPAIGN ENDPOINTS ====================

@app.route('/api/campaigns', methods=['GET'])
def get_campaigns():
    """Get all email campaigns"""
    campaigns = EmailCampaign.query.order_by(EmailCampaign.created_at.desc()).all()
    return jsonify({
        'campaigns': [c.to_dict() for c in campaigns],
        'total': len(campaigns)
    })


@app.route('/api/campaigns', methods=['POST'])
def create_campaign():
    """Create new email campaign"""
    data = request.get_json()

    if not data or 'name' not in data or 'subject' not in data or 'body' not in data:
        return jsonify({"error": "Name, subject, and body are required"}), 400

    campaign = EmailCampaign(
        name=data['name'],
        subject=data['subject'],
        body=data['body'],
        status='draft'
    )

    db.session.add(campaign)
    db.session.commit()

    return jsonify(campaign.to_dict()), 201


@app.route('/api/campaigns/<int:campaign_id>', methods=['PUT'])
def update_campaign(campaign_id):
    """Update email campaign"""
    campaign = EmailCampaign.query.get_or_404(campaign_id)
    data = request.get_json()

    for field in ['name', 'subject', 'body', 'status']:
        if field in data:
            setattr(campaign, field, data[field])

    if 'scheduled_at' in data and data['scheduled_at']:
        campaign.scheduled_at = datetime.fromisoformat(data['scheduled_at'].replace('Z', '+00:00'))
        campaign.status = 'scheduled'

    db.session.commit()
    return jsonify(campaign.to_dict())


@app.route('/api/campaigns/<int:campaign_id>/send', methods=['POST'])
def send_campaign(campaign_id):
    """Simulate sending campaign to candidates"""
    campaign = EmailCampaign.query.get_or_404(campaign_id)
    data = request.get_json() or {}

    # Get target candidates
    candidate_ids = data.get('candidate_ids', [])

    if not candidate_ids:
        # If no specific IDs, get all active candidates
        candidates = Candidate.query.filter(Candidate.status.in_(['new', 'reviewing', 'interviewing'])).all()
        candidate_ids = [c.id for c in candidates]

    # Simulate sending (in production, integrate with email service)
    campaign.total_recipients = len(candidate_ids)
    campaign.sent_count = len(candidate_ids)
    campaign.sent_at = datetime.utcnow()
    campaign.status = 'sent'

    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Campaign sent to {len(candidate_ids)} recipients",
        "campaign": campaign.to_dict()
    })


@app.route('/api/campaigns/<int:campaign_id>', methods=['DELETE'])
def delete_campaign(campaign_id):
    """Delete email campaign"""
    campaign = EmailCampaign.query.get_or_404(campaign_id)
    db.session.delete(campaign)
    db.session.commit()
    return jsonify({"message": "Campaign deleted successfully"})


# ==================== INTERVIEW SCHEDULING ENDPOINTS ====================

@app.route('/api/interviews', methods=['GET'])
def get_interviews():
    """Get all interviews"""
    status = request.args.get('status')
    candidate_id = request.args.get('candidate_id')

    query = Interview.query
    if status:
        query = query.filter_by(status=status)
    if candidate_id:
        query = query.filter_by(candidate_id=candidate_id)

    interviews = query.order_by(Interview.scheduled_at.desc()).all()
    return jsonify({
        'interviews': [i.to_dict() for i in interviews],
        'total': len(interviews)
    })


@app.route('/api/interviews', methods=['POST'])
def create_interview():
    """Schedule new interview"""
    data = request.get_json()

    required = ['candidate_id', 'job_id', 'scheduled_at']
    if not data or not all(field in data for field in required):
        return jsonify({"error": "candidate_id, job_id, and scheduled_at are required"}), 400

    interview = Interview(
        candidate_id=data['candidate_id'],
        job_id=data['job_id'],
        interview_type=data.get('interview_type', 'video'),
        scheduled_at=datetime.fromisoformat(data['scheduled_at'].replace('Z', '+00:00')),
        duration_minutes=data.get('duration_minutes', 60),
        location=data.get('location'),
        interviewers=data.get('interviewers'),
        notes=data.get('notes'),
        status='scheduled'
    )

    db.session.add(interview)
    db.session.commit()

    return jsonify(interview.to_dict()), 201


@app.route('/api/interviews/<int:interview_id>', methods=['PUT'])
def update_interview(interview_id):
    """Update interview"""
    interview = Interview.query.get_or_404(interview_id)
    data = request.get_json()

    for field in ['interview_type', 'duration_minutes', 'location', 'interviewers', 'notes', 'status', 'feedback', 'rating']:
        if field in data:
            setattr(interview, field, data[field])

    if 'scheduled_at' in data:
        interview.scheduled_at = datetime.fromisoformat(data['scheduled_at'].replace('Z', '+00:00'))

    db.session.commit()
    return jsonify(interview.to_dict())


@app.route('/api/interviews/<int:interview_id>', methods=['DELETE'])
def delete_interview(interview_id):
    """Delete interview"""
    interview = Interview.query.get_or_404(interview_id)
    db.session.delete(interview)
    db.session.commit()
    return jsonify({"message": "Interview deleted successfully"})


# ==================== OFFER MANAGEMENT ENDPOINTS ====================

@app.route('/api/offers', methods=['GET'])
def get_offers():
    """Get all offers"""
    status = request.args.get('status')

    query = Offer.query
    if status:
        query = query.filter_by(status=status)

    offers = query.order_by(Offer.created_at.desc()).all()
    return jsonify({
        'offers': [o.to_dict() for o in offers],
        'total': len(offers)
    })


@app.route('/api/offers', methods=['POST'])
def create_offer():
    """Create new job offer"""
    data = request.get_json()

    if not data or 'candidate_id' not in data or 'job_id' not in data:
        return jsonify({"error": "candidate_id and job_id are required"}), 400

    offer = Offer(
        candidate_id=data['candidate_id'],
        job_id=data['job_id'],
        salary=data.get('salary'),
        equity=data.get('equity'),
        signing_bonus=data.get('signing_bonus'),
        notes=data.get('notes'),
        status='draft'
    )

    if data.get('start_date'):
        offer.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()

    db.session.add(offer)
    db.session.commit()

    return jsonify(offer.to_dict()), 201


@app.route('/api/offers/<int:offer_id>', methods=['PUT'])
def update_offer(offer_id):
    """Update offer"""
    offer = Offer.query.get_or_404(offer_id)
    data = request.get_json()

    for field in ['salary', 'equity', 'signing_bonus', 'notes', 'status']:
        if field in data:
            setattr(offer, field, data[field])

    if 'start_date' in data and data['start_date']:
        offer.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()

    # Track status changes
    if data.get('status') == 'sent' and offer.status != 'sent':
        offer.sent_at = datetime.utcnow()
    elif data.get('status') in ['accepted', 'declined']:
        offer.responded_at = datetime.utcnow()

    db.session.commit()
    return jsonify(offer.to_dict())


@app.route('/api/offers/<int:offer_id>', methods=['DELETE'])
def delete_offer(offer_id):
    """Delete offer"""
    offer = Offer.query.get_or_404(offer_id)
    db.session.delete(offer)
    db.session.commit()
    return jsonify({"message": "Offer deleted successfully"})


# ==================== ANALYTICS DASHBOARD ENDPOINTS ====================

@app.route('/api/analytics/overview', methods=['GET'])
def get_analytics_overview():
    """Get comprehensive analytics overview"""

    # Pipeline metrics
    total_candidates = Candidate.query.count()
    total_jobs = Job.query.count()
    total_applications = Application.query.count()

    # Candidate status breakdown
    candidate_statuses = {}
    for status in ['new', 'reviewing', 'interviewing', 'offer', 'hired', 'rejected']:
        count = Candidate.query.filter_by(status=status).count()
        candidate_statuses[status] = count

    # Job status breakdown
    job_statuses = {}
    for status in ['open', 'closed', 'filled', 'on_hold']:
        count = Job.query.filter_by(status=status).count()
        job_statuses[status] = count

    # Interview stats
    total_interviews = Interview.query.count()
    completed_interviews = Interview.query.filter_by(status='completed').count()
    upcoming_interviews = Interview.query.filter(
        Interview.scheduled_at > datetime.utcnow(),
        Interview.status == 'scheduled'
    ).count()

    # Offer stats
    total_offers = Offer.query.count()
    accepted_offers = Offer.query.filter_by(status='accepted').count()
    pending_offers = Offer.query.filter(Offer.status.in_(['sent', 'negotiating'])).count()

    # Calculate conversion rates
    interview_rate = round((completed_interviews / total_candidates * 100), 1) if total_candidates > 0 else 0
    offer_rate = round((total_offers / total_candidates * 100), 1) if total_candidates > 0 else 0
    hire_rate = round((accepted_offers / total_offers * 100), 1) if total_offers > 0 else 0

    # Top expertise areas
    expertise_counts = {}
    candidates = Candidate.query.all()
    for c in candidates:
        if c.primary_expertise:
            expertise_counts[c.primary_expertise] = expertise_counts.get(c.primary_expertise, 0) + 1

    top_expertise = sorted(expertise_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    return jsonify({
        'pipeline': {
            'total_candidates': total_candidates,
            'total_jobs': total_jobs,
            'total_applications': total_applications
        },
        'candidate_statuses': candidate_statuses,
        'job_statuses': job_statuses,
        'interviews': {
            'total': total_interviews,
            'completed': completed_interviews,
            'upcoming': upcoming_interviews
        },
        'offers': {
            'total': total_offers,
            'accepted': accepted_offers,
            'pending': pending_offers
        },
        'conversion_rates': {
            'interview_rate': interview_rate,
            'offer_rate': offer_rate,
            'hire_rate': hire_rate
        },
        'top_expertise': dict(top_expertise)
    })


@app.route('/api/analytics/pipeline-funnel', methods=['GET'])
def get_pipeline_funnel():
    """Get pipeline funnel metrics"""

    funnel = {
        'sourced': Candidate.query.filter_by(status='new').count(),
        'screening': Candidate.query.filter_by(status='reviewing').count(),
        'interviewing': Candidate.query.filter_by(status='interviewing').count(),
        'offer': Candidate.query.filter_by(status='offer').count(),
        'hired': Candidate.query.filter_by(status='hired').count()
    }

    return jsonify({
        'funnel': funnel,
        'total_in_pipeline': sum(funnel.values())
    })


@app.route('/api/analytics/time-to-hire', methods=['GET'])
def get_time_to_hire():
    """Get average time-to-hire metrics"""

    # Calculate average time from candidate creation to hire
    hired_candidates = Candidate.query.filter_by(status='hired').all()

    if not hired_candidates:
        return jsonify({
            'average_days': 0,
            'total_hired': 0,
            'message': 'No hired candidates yet'
        })

    total_days = 0
    for candidate in hired_candidates:
        days = (candidate.updated_at - candidate.created_at).days
        total_days += days

    avg_days = round(total_days / len(hired_candidates), 1)

    return jsonify({
        'average_days': avg_days,
        'total_hired': len(hired_candidates),
        'message': f'Average time to hire: {avg_days} days'
    })


@app.route('/api/analytics/source-effectiveness', methods=['GET'])
def get_source_effectiveness():
    """Analyze effectiveness of different candidate sources"""

    # Group candidates by source
    sources = {}
    candidates = Candidate.query.all()

    for c in candidates:
        source = 'Direct' if not c.notes else 'Boolean Search' if 'Boolean' in (c.notes or '') else 'Other'
        if source not in sources:
            sources[source] = {'total': 0, 'hired': 0}
        sources[source]['total'] += 1
        if c.status == 'hired':
            sources[source]['hired'] += 1

    # Calculate conversion rates
    for source in sources:
        total = sources[source]['total']
        hired = sources[source]['hired']
        sources[source]['conversion_rate'] = round((hired / total * 100), 1) if total > 0 else 0

    return jsonify({
        'sources': sources
    })


# ==================== PUBLIC CANDIDATE ENDPOINTS ====================

@app.route('/api/public/jobs/<int:job_id>', methods=['GET'])
def get_public_job(job_id):
    """Get job details for public candidate landing page (respects stealth mode)"""
    job = Job.query.get_or_404(job_id)

    # Only show open jobs publicly
    if job.status != 'open':
        return jsonify({"error": "This position is no longer accepting applications"}), 404

    # Return job with stealth mode respected (company hidden if confidential)
    return jsonify(job.to_dict(show_company=False))


@app.route('/api/public/apply', methods=['POST'])
def submit_public_application():
    """Submit an application from the public landing page"""
    data = request.json

    # Validate required fields
    required_fields = ['job_id', 'first_name', 'last_name', 'email']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400

    job_id = data.get('job_id')

    # Verify job exists and is open
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    if job.status != 'open':
        return jsonify({"error": "This position is no longer accepting applications"}), 400

    # Check if candidate already exists
    existing_candidate = Candidate.query.filter_by(email=data.get('email')).first()

    if existing_candidate:
        # Check if already applied to this job
        existing_application = Application.query.filter_by(
            candidate_id=existing_candidate.id,
            job_id=job_id
        ).first()

        if existing_application:
            return jsonify({"error": "You have already applied for this position"}), 400

        candidate = existing_candidate
        # Update candidate info if provided
        if data.get('phone'):
            candidate.phone = data.get('phone')
        if data.get('linkedin_url'):
            candidate.linkedin_url = data.get('linkedin_url')
        if data.get('github_url'):
            candidate.github_url = data.get('github_url')
        if data.get('portfolio_url'):
            candidate.portfolio_url = data.get('portfolio_url')
        if data.get('location'):
            candidate.location = data.get('location')
        if data.get('years_experience'):
            candidate.years_experience = data.get('years_experience')
        if data.get('primary_expertise'):
            candidate.primary_expertise = data.get('primary_expertise')
        # Expanded sourcing fields
        if data.get('huggingface_url'):
            candidate.huggingface_url = data.get('huggingface_url')
        if data.get('kaggle_url'):
            candidate.kaggle_url = data.get('kaggle_url')
        if data.get('papers_with_code_url'):
            candidate.papers_with_code_url = data.get('papers_with_code_url')
        if data.get('devpost_url'):
            candidate.devpost_url = data.get('devpost_url')
    else:
        # Create new candidate
        candidate = Candidate(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            location=data.get('location'),
            linkedin_url=data.get('linkedin_url'),
            github_url=data.get('github_url'),
            portfolio_url=data.get('portfolio_url'),
            resume_url=data.get('resume_url'),
            years_experience=data.get('years_experience'),
            primary_expertise=data.get('primary_expertise'),
            huggingface_url=data.get('huggingface_url'),
            kaggle_url=data.get('kaggle_url'),
            papers_with_code_url=data.get('papers_with_code_url'),
            devpost_url=data.get('devpost_url'),
            status='new'
        )
        db.session.add(candidate)
        db.session.flush()  # Get candidate ID

    # Create application
    application = Application(
        candidate_id=candidate.id,
        job_id=job_id,
        status='applied',
        source='landing_page',
        notes=data.get('cover_letter', '')
    )
    db.session.add(application)
    db.session.flush()  # Get application ID

    # Store work artifact links
    import json as json_module
    work_links_data = []
    link_fields = [
        ('github_url', 'github'), ('linkedin_url', 'linkedin'),
        ('portfolio_url', 'portfolio'), ('huggingface_url', 'huggingface'),
        ('kaggle_url', 'kaggle'), ('papers_with_code_url', 'paper'),
        ('devpost_url', 'other')
    ]
    for field, link_type in link_fields:
        url = data.get(field)
        if url:
            link = CandidateLink(candidate_id=candidate.id, link_type=link_type, url=url, title=field.replace('_url', '').replace('_', ' ').title())
            db.session.add(link)
            work_links_data.append({'link_type': link_type, 'url': url, 'title': link.title})

    # Process additional dynamic links from the frontend
    additional_links = data.get('additional_links', [])
    for al in additional_links:
        if al.get('url'):
            link = CandidateLink(
                candidate_id=candidate.id,
                link_type=al.get('link_type', 'other'),
                url=al['url'],
                title=al.get('title', '')
            )
            db.session.add(link)
            work_links_data.append({
                'link_type': al.get('link_type', 'other'),
                'url': al['url'],
                'title': al.get('title', '')
            })

    # Auto-generate Hiring Intelligence Submission
    hiring_intelligence = data.get('hiring_intelligence', '')
    position = data.get('position', job.title if job else '')
    role_q = PHYSICAL_AI_ROLE_QUESTIONS.get(position, PHYSICAL_AI_ROLE_QUESTIONS.get(job.title, {}))

    submission_data = {
        'candidate_name': f"{candidate.first_name} {candidate.last_name}",
        'candidate_email': candidate.email,
        'position': position,
        'hidden_signal': data.get('hidden_signal', ''),
        'work_links': work_links_data,
        'intelligence_response': {
            'question_label': role_q.get('label', 'Hiring Intelligence'),
            'question_text': role_q.get('question', ''),
            'response_text': hiring_intelligence
        },
        'generated_at': datetime.utcnow().isoformat()
    }

    submission = HiringIntelligenceSubmission(
        application_id=application.id,
        submission_data=json_module.dumps(submission_data),
        status='pending'
    )
    db.session.add(submission)

    try:
        db.session.commit()
        return jsonify({
            "message": "Application submitted successfully!",
            "application_id": application.id,
            "candidate_id": candidate.id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ==================== HIRING INTELLIGENCE SUBMISSIONS ====================

@app.route('/api/intelligence-submissions', methods=['GET'])
def get_intelligence_submissions():
    """Get all hiring intelligence submissions"""
    try:
        status = request.args.get('status')
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        if 'hiring_intelligence_submission' not in inspector.get_table_names():
            return jsonify({'submissions': [], 'total': 0, 'message': 'Intelligence submissions table not created yet'})

        query = HiringIntelligenceSubmission.query
        if status:
            query = query.filter_by(status=status)

        submissions = query.order_by(HiringIntelligenceSubmission.id.desc()).all()
        return jsonify({'submissions': [s.to_dict() for s in submissions], 'total': len(submissions)})
    except Exception as e:
        return jsonify({'submissions': [], 'total': 0, 'error': str(e)}), 200


@app.route('/api/intelligence-submissions/<int:submission_id>', methods=['GET'])
def get_intelligence_submission(submission_id):
    """Get a single hiring intelligence submission"""
    submission = HiringIntelligenceSubmission.query.get_or_404(submission_id)
    return jsonify(submission.to_dict())


@app.route('/api/intelligence-submissions/<int:submission_id>', methods=['PUT'])
def update_intelligence_submission(submission_id):
    """Update a hiring intelligence submission (recruiter feedback)"""
    submission = HiringIntelligenceSubmission.query.get_or_404(submission_id)
    data = request.get_json()
    for field in ['status', 'missing_signal', 'recruiter_notes', 'passed_to_screen', 'passed_to_interview', 'received_offer', 'submission_data']:
        if field in data:
            setattr(submission, field, data[field])
    if data.get('status') == 'reviewed' and not submission.reviewed_at:
        submission.reviewed_at = datetime.utcnow()
    db.session.commit()
    return jsonify(submission.to_dict())


@app.route('/api/intelligence-submissions/<int:submission_id>', methods=['DELETE'])
def delete_intelligence_submission(submission_id):
    """Delete a hiring intelligence submission"""
    submission = HiringIntelligenceSubmission.query.get_or_404(submission_id)
    db.session.delete(submission)
    db.session.commit()
    return jsonify({"message": "Submission deleted successfully"})


@app.route('/api/intelligence-submissions/<int:submission_id>/analyze', methods=['POST'])
def analyze_intelligence_submission(submission_id):
    """AI-powered analysis using Claude API — generates the hiring manager report"""
    import json as json_module

    try:
        submission = HiringIntelligenceSubmission.query.get_or_404(submission_id)
        submission_data = json_module.loads(submission.submission_data) if submission.submission_data else {}

        application = Application.query.get(submission.application_id)
        if not application:
            return jsonify({"error": "Application not found"}), 404

        job = application.job
        candidate = application.candidate

        work_links = submission_data.get('work_links', [])
        intelligence_response = submission_data.get('intelligence_response', {})
        position = submission_data.get('position', job.title if job else '')

        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            return jsonify({"error": "ANTHROPIC_API_KEY not configured. Set it in Render environment variables."}), 500

        try:
            from anthropic import Anthropic
            import httpx
        except ImportError:
            return jsonify({"error": "Anthropic SDK not installed. Add 'anthropic' to requirements.txt"}), 500

        http_client = httpx.Client(timeout=60.0, follow_redirects=True)
        client = Anthropic(api_key=api_key, http_client=http_client)

        analysis_prompt = f"""You are an expert technical recruiter and hiring manager for Physical AI roles (robotics, autonomous systems, computer vision, etc.).

Analyze this hiring intelligence submission and provide structured insights:

**CANDIDATE:** {candidate.first_name} {candidate.last_name}
**POSITION:** {position}

**WORK ARTIFACTS:**
{json_module.dumps(work_links, indent=2) if work_links else "None provided"}

**INTELLIGENCE RESPONSE:**
Question: {intelligence_response.get('question_text', 'N/A')}
Response: {intelligence_response.get('response_text', 'N/A')}

**CANDIDATE BACKGROUND:**
- Years Experience: {candidate.years_experience if candidate.years_experience else 'Not specified'}
- Primary Expertise: {candidate.primary_expertise if candidate.primary_expertise else 'Not specified'}
- Location: {candidate.location if candidate.location else 'Not specified'}

---

Provide a comprehensive analysis in the following JSON format:

{{
  "extracted_skills": ["skill1", "skill2", "skill3"],
  "key_phrases": [{{"phrase": "the exact phrase", "context": "why it matters", "importance": "high/medium/low"}}],
  "artifact_analysis": [{{"url": "the URL", "type": "github/linkedin/portfolio/paper/other", "summary": "2-3 sentence summary", "quality_indicators": "what stands out", "relevance": "high/medium/low"}}],
  "ai_assessment": {{
    "strengths": ["Strength 1 with evidence", "Strength 2 with evidence", "Strength 3 with evidence"],
    "potential_gaps": ["Gap or concern 1", "Gap or concern 2"],
    "technical_depth": "Junior/Mid/Senior/Staff - with brief justification",
    "systems_thinking": "Strong/Moderate/Limited - with evidence",
    "recommendation": "HIGHLY RECOMMEND/RECOMMEND/CONSIDER/RECOMMEND WITH CAUTION - with reasoning",
    "next_steps": "Suggested interview focus areas or screening questions"
  }}
}}

Focus on:
1. Technical skills (languages, frameworks, tools, methodologies)
2. Physical AI-specific expertise (robotics, perception, control, planning)
3. Systems-level thinking vs pure implementation
4. Evidence of production experience, not just academic
5. Judgment and decision-making patterns in intelligence response
6. Code quality and documentation practices (if GitHub links provided)

Return ONLY the JSON, no additional text."""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": analysis_prompt}]
        )

        response_text = message.content[0].text

        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                analysis_result = json_module.loads(json_match.group())
            else:
                analysis_result = json_module.loads(response_text)
        except Exception:
            return jsonify({"error": "Failed to parse AI analysis response", "raw_response": response_text}), 500

        submission.extracted_skills = json_module.dumps(analysis_result.get('extracted_skills', []))
        submission.key_phrases = json_module.dumps(analysis_result.get('key_phrases', []))
        submission.ai_assessment = json_module.dumps(analysis_result.get('ai_assessment', {}))
        submission.artifact_analysis = json_module.dumps(analysis_result.get('artifact_analysis', []))
        submission.ai_analyzed = True
        submission.ai_analyzed_at = datetime.utcnow()

        db.session.commit()

        return jsonify({"message": "AI analysis completed successfully", "submission": submission.to_dict()})

    except Exception as e:
        import traceback
        print(f"AI analysis error: {traceback.format_exc()}")
        db.session.rollback()
        return jsonify({"error": f"AI analysis failed: {str(e)}"}), 500


# ==================== SEED DATA ENDPOINT ====================

@app.route('/api/seed-data', methods=['POST'])
def seed_sample_data():
    """One-click seed: populate database with sample candidates, jobs, and publications"""

    # Check if data already exists
    if Candidate.query.count() > 0:
        return jsonify({
            "message": "Database already has data. Delete existing data first or use /api/stats to check.",
            "candidates": Candidate.query.count(),
            "jobs": Job.query.count()
        }), 409

    try:
        # Sample Candidates — Physical AI, Robotics, Autonomous Systems talent
        candidates_data = [
            {"first_name": "Anika", "last_name": "Patel", "email": "anika.patel@example.edu",
             "primary_expertise": "Humanoid Robotics", "h_index": 28, "citation_count": 4200,
             "years_experience": 7, "location": "Pittsburgh, PA",
             "github_url": "https://github.com/anikapatel",
             "huggingface_url": "https://huggingface.co/anikapatel",
             "bio": "Humanoid locomotion researcher. Built bipedal walking controllers using deep RL. Published at ICRA, IROS, and CoRL. Open-sourced a ROS2 whole-body control stack with 800+ GitHub stars.",
             "skills": "Python, C++, ROS/ROS2, PyTorch, SLAM Algorithms, Motion Planning, Reinforcement Learning, MuJoCo, Isaac Sim",
             "status": "new"},
            {"first_name": "Jin", "last_name": "Nakamura", "email": "jin.nakamura@example.edu",
             "primary_expertise": "Computer Vision & SLAM",
             "h_index": 18, "citation_count": 2800, "years_experience": 5,
             "location": "San Francisco, CA",
             "github_url": "https://github.com/jinnakamura",
             "huggingface_url": "https://huggingface.co/jinnakamura",
             "bio": "Perception engineer focused on real-time 3D scene understanding for autonomous systems. Created a visual SLAM pipeline that runs at 60fps on edge devices. Active contributor to Open3D.",
             "skills": "Python, C++, CUDA, OpenCV, LIDAR Processing, Point Cloud Processing, Depth Estimation, TensorRT, ONNX, Docker",
             "status": "reviewing"},
            {"first_name": "Sofia", "last_name": "Andersen", "email": "sofia.andersen@example.edu",
             "primary_expertise": "Autonomous Vehicles",
             "h_index": 35, "citation_count": 7600, "years_experience": 9,
             "location": "Munich, Germany",
             "github_url": "https://github.com/sofiaandersen",
             "google_scholar_url": "https://scholar.google.com/citations?user=example123",
             "bio": "AV perception lead. Developed multi-sensor fusion architecture combining LiDAR, camera, and radar for L4 autonomy. 12 papers at CVPR/ICRA/IROS. Previously at Waymo, now advising 2 robotics startups.",
             "skills": "Python, C++, PyTorch, TensorFlow, Sensor Fusion, LIDAR Processing, CARLA, Object Detection, Kalman Filters, ROS/ROS2",
             "status": "interviewing"},
            {"first_name": "Kwame", "last_name": "Osei", "email": "kwame.osei@example.edu",
             "primary_expertise": "Reinforcement Learning",
             "h_index": 12, "citation_count": 1500, "years_experience": 4,
             "location": "Austin, TX",
             "github_url": "https://github.com/kwameosei",
             "huggingface_url": "https://huggingface.co/kwameosei",
             "arxiv_author_id": "kwame_osei",
             "bio": "Deep RL researcher building sim-to-real transfer for robotic manipulation. Published at CoRL and RSS. Created an open-source dexterous hand manipulation benchmark with 2k+ downloads on HuggingFace.",
             "skills": "Python, PyTorch, JAX, Isaac Gym, MuJoCo, Robotic Manipulation, Sim-to-Real, PPO, SAC, Docker, Kubernetes",
             "hf_models_count": 4, "hf_datasets_count": 2, "hf_spaces_count": 1, "hf_likes": 85,
             "status": "new"},
            {"first_name": "Mei", "last_name": "Zhang", "email": "mei.zhang@example.edu",
             "primary_expertise": "Robot Control & Dynamics",
             "h_index": 42, "citation_count": 9800, "years_experience": 11,
             "location": "Boston, MA",
             "github_url": "https://github.com/meizhang",
             "google_scholar_url": "https://scholar.google.com/citations?user=example456",
             "orcid_id": "0000-0002-1234-5678",
             "bio": "Control theory meets learning. Built the locomotion stack for a quadruped robot that won the DARPA SubT challenge. 20+ papers at ICRA/IROS/RSS. Co-created the Legged Gym framework.",
             "skills": "Python, C++, MATLAB, Control Theory, Dynamics Simulation, Gazebo, Isaac Sim, ROS/ROS2, Motion Planning, Real-time Systems",
             "status": "reviewing"},
            {"first_name": "Diego", "last_name": "Ramirez", "email": "diego.ramirez@example.edu",
             "primary_expertise": "Edge AI & Embedded Systems",
             "h_index": 8, "citation_count": 650, "years_experience": 3,
             "location": "Remote (Mexico City)",
             "github_url": "https://github.com/diegoramirez",
             "huggingface_url": "https://huggingface.co/diegoramirez",
             "kaggle_url": "https://kaggle.com/diegoramirez",
             "bio": "Edge AI specialist. Deployed real-time object detection models on NVIDIA Jetson for warehouse robots. Kaggle competitions master. Published 3 HuggingFace models for robotics perception optimized for edge deployment.",
             "skills": "Python, C++, TensorRT, ONNX, CUDA, YOLO, Docker, Linux, Real-time Systems, Edge AI, NVIDIA Jetson, Raspberry Pi",
             "hf_models_count": 3, "hf_datasets_count": 1, "hf_spaces_count": 2, "hf_likes": 42,
             "status": "new"},
            {"first_name": "Priya", "last_name": "Sharma", "email": "priya.sharma@example.edu",
             "primary_expertise": "Perception & Sensor Fusion",
             "h_index": 22, "citation_count": 3100, "years_experience": 6,
             "location": "Seattle, WA",
             "github_url": "https://github.com/priyasharma",
             "bio": "Built perception pipelines for 3 autonomous robot platforms. Specializes in multi-modal sensor fusion (LiDAR + stereo + IMU). Created ROS2 packages downloaded 15k+ times. Active RSS/ICRA reviewer.",
             "skills": "Python, C++, ROS/ROS2, Sensor Fusion, LIDAR Processing, Kalman Filters, Particle Filters, OpenCV, PCL, Docker, Git/GitHub",
             "status": "new"},
            {"first_name": "Alex", "last_name": "Kowalski", "email": "alex.kowalski@example.edu",
             "primary_expertise": "Motion Planning & Navigation",
             "h_index": 15, "citation_count": 1900, "years_experience": 5,
             "location": "Boulder, CO",
             "github_url": "https://github.com/alexkowalski",
             "arxiv_author_id": "alex_kowalski",
             "bio": "Motion planning researcher. Developed a real-time trajectory optimization framework for multi-robot coordination. Open-sourced a path planning library (RRT*, A*, PRM) with 1.2k GitHub stars. 2 best paper nominations at IROS.",
             "skills": "Python, C++, ROS/ROS2, Path Planning (RRT, A*), Motion Planning, Optimization, Gazebo, OMPL, Multi-robot Systems, Linux",
             "status": "reviewing"}
        ]

        created_candidates = []
        for c in candidates_data:
            candidate = Candidate(**c)
            db.session.add(candidate)
            created_candidates.append(c['first_name'] + ' ' + c['last_name'])

        db.session.flush()  # Get IDs assigned

        # Sample Jobs — Physical AI, Robotics, Autonomous Systems
        jobs_data = [
            {"title": "Humanoid Roboticist", "company": "Figure AI",
             "location": "Sunnyvale, CA", "job_type": "full-time",
             "description": "Design and implement whole-body control for our humanoid robot. You'll work on locomotion, manipulation, and human-robot interaction using deep RL and model-based control.",
             "requirements": "MS/PhD in Robotics/ME/CS, experience with bipedal locomotion, published at ICRA/IROS/RSS/CoRL, hands-on with real robot hardware",
             "required_expertise": "Humanoid Robotics", "education_required": "Masters",
             "research_focus": "Bipedal Locomotion and Whole-Body Control",
             "salary_min": 220000, "salary_max": 400000, "confidential": False},
            {"title": "Perception Engineer", "company": "Stealth Robotics Startup",
             "location": "San Francisco, CA", "job_type": "full-time",
             "description": "Build the perception stack for next-gen autonomous robots. Multi-sensor fusion (LiDAR, stereo, radar), real-time 3D scene understanding, and object tracking. $80M Series B.",
             "requirements": "3+ years in robotics perception, C++/Python, experience with ROS2, real-time constraints, CUDA/TensorRT",
             "required_expertise": "Perception & Sensor Fusion", "education_required": "Masters",
             "research_focus": "3D Scene Understanding and Sensor Fusion",
             "salary_min": 200000, "salary_max": 350000, "confidential": True},
            {"title": "Reinforcement Learning Engineer", "company": "NVIDIA Robotics",
             "location": "Santa Clara, CA (Hybrid)", "job_type": "full-time",
             "description": "Develop sim-to-real RL pipelines using Isaac Sim/Gym for robotic manipulation and locomotion. Push the frontier of what robots can learn in simulation and transfer to the real world.",
             "requirements": "Strong RL background (PPO, SAC, model-based), experience with Isaac Gym or MuJoCo, publications preferred, PyTorch",
             "required_expertise": "Reinforcement Learning", "education_required": "Masters",
             "research_focus": "Sim-to-Real Transfer for Robotic Manipulation",
             "salary_min": 250000, "salary_max": 420000, "confidential": False},
            {"title": "SLAM Engineer", "company": "Confidential - Autonomous Delivery",
             "location": "Pittsburgh, PA", "job_type": "full-time",
             "description": "Build robust visual-inertial SLAM for outdoor autonomous delivery robots. Must work in rain, snow, and GPS-denied environments. Founding robotics team.",
             "requirements": "Deep SLAM experience (ORB-SLAM, VINS-Mono, or similar), C++, real-time systems, published work preferred",
             "required_expertise": "Computer Vision & SLAM", "education_required": "Masters",
             "research_focus": "Visual SLAM for Outdoor Autonomy",
             "salary_min": 180000, "salary_max": 300000, "confidential": True},
            {"title": "Motion Planning Engineer", "company": "Boston Dynamics",
             "location": "Waltham, MA", "job_type": "full-time",
             "description": "Design and implement motion planning algorithms for legged robots navigating complex, unstructured environments. Work with Spot and Atlas platforms.",
             "requirements": "MS/PhD, strong C++, experience with trajectory optimization, OMPL or custom planners, ROS",
             "required_expertise": "Motion Planning & Navigation", "education_required": "Masters",
             "research_focus": "Trajectory Optimization for Legged Robots",
             "salary_min": 200000, "salary_max": 380000, "confidential": False},
            {"title": "Autonomous Systems Engineer", "company": "Confidential - Defense/Space",
             "location": "Remote (US Clearance Required)", "job_type": "full-time",
             "description": "Build autonomous navigation and decision-making systems for unmanned vehicles operating in contested environments. Multi-robot coordination and edge AI deployment.",
             "requirements": "5+ years autonomous systems, C++/Python, ROS2, real-time embedded, US citizenship required",
             "required_expertise": "Autonomous Navigation", "education_required": "Masters",
             "research_focus": "Multi-Robot Coordination and Autonomous Decision Making",
             "salary_min": 190000, "salary_max": 320000, "confidential": True},
            {"title": "Computer Vision Engineer (Robotics)", "company": "Agility Robotics",
             "location": "Corvallis, OR (Hybrid)", "job_type": "full-time",
             "description": "Build real-time vision systems for Digit, our bipedal humanoid. Object detection, semantic segmentation, and spatial reasoning for warehouse environments.",
             "requirements": "3+ years CV experience, YOLO/segmentation models, deployment on edge (Jetson/TensorRT), ROS2",
             "required_expertise": "Computer Vision & SLAM", "education_required": "Bachelors",
             "research_focus": "Real-time Vision for Humanoid Robots",
             "salary_min": 170000, "salary_max": 280000, "confidential": False},
            {"title": "Embedded AI Engineer", "company": "Stealth Humanoid Startup",
             "location": "Bay Area, CA", "job_type": "full-time",
             "description": "Deploy ML models on custom robot hardware. Optimize perception and control models for real-time inference on resource-constrained platforms. $200M+ funding.",
             "requirements": "C++/CUDA, TensorRT/ONNX, edge deployment experience, understanding of robot control loops",
             "required_expertise": "Edge AI & Embedded Systems", "education_required": "Bachelors",
             "research_focus": "On-Device ML for Robotics",
             "salary_min": 180000, "salary_max": 300000, "confidential": True}
        ]

        created_jobs = []
        for j in jobs_data:
            job = Job(**j)
            db.session.add(job)
            created_jobs.append(j['title'])

        db.session.flush()

        # Sample Publications — Robotics conference papers
        candidates_list = Candidate.query.order_by(Candidate.id).all()
        pubs_data = [
            # Anika Patel - Humanoid Robotics
            {"candidate_id": candidates_list[0].id, "title": "Deep Reinforcement Learning for Bipedal Locomotion on Uneven Terrain",
             "authors": "A. Patel, J. Hwang, S. Kim", "venue": "ICRA 2024",
             "year": 2024, "citation_count": 45, "research_area": "Humanoid Robotics",
             "abstract": "We present a deep RL framework for robust bipedal walking that transfers from simulation to a real humanoid robot, achieving stable locomotion over uneven terrain."},
            {"candidate_id": candidates_list[0].id, "title": "Whole-Body Control for Humanoid Manipulation Using Hierarchical RL",
             "authors": "A. Patel, M. Zhang", "venue": "CoRL 2023",
             "year": 2023, "citation_count": 72, "research_area": "Humanoid Robotics"},
            # Jin Nakamura - SLAM
            {"candidate_id": candidates_list[1].id, "title": "Real-Time Visual SLAM on Edge Devices for Mobile Robots",
             "authors": "J. Nakamura, L. Chen, R. Patel", "venue": "IROS 2024",
             "year": 2024, "citation_count": 28, "research_area": "Computer Vision & SLAM",
             "abstract": "A lightweight visual SLAM pipeline achieving 60fps on NVIDIA Jetson Orin with comparable accuracy to desktop methods."},
            # Sofia Andersen - AV Perception
            {"candidate_id": candidates_list[2].id, "title": "Multi-Modal Sensor Fusion for Robust Autonomous Driving in Adverse Weather",
             "authors": "S. Andersen, T. Mueller, K. Yamamoto", "venue": "CVPR 2023",
             "year": 2023, "citation_count": 156, "research_area": "Autonomous Vehicles"},
            {"candidate_id": candidates_list[2].id, "title": "LiDAR-Camera Fusion with Learned Uncertainty for 3D Object Detection",
             "authors": "S. Andersen, R. Gupta", "venue": "ICRA 2024",
             "year": 2024, "citation_count": 38, "research_area": "Autonomous Vehicles"},
            # Kwame Osei - RL Manipulation
            {"candidate_id": candidates_list[3].id, "title": "Sim-to-Real Transfer for Dexterous Robotic Manipulation via Domain Randomization",
             "authors": "K. Osei, P. Sharma, A. Kowalski", "venue": "RSS 2024",
             "year": 2024, "citation_count": 31, "research_area": "Reinforcement Learning",
             "abstract": "We demonstrate sim-to-real transfer for a 16-DOF dexterous hand using massive domain randomization in Isaac Gym."},
            # Mei Zhang - Control
            {"candidate_id": candidates_list[4].id, "title": "Adaptive Model Predictive Control for Legged Robot Locomotion",
             "authors": "M. Zhang, J. Di Carlo, S. Kim", "venue": "RSS 2022",
             "year": 2022, "citation_count": 210, "research_area": "Robot Control & Dynamics"},
            {"candidate_id": candidates_list[4].id, "title": "Learning Agile Locomotion via Adversarial Training in Simulation",
             "authors": "M. Zhang, A. Patel", "venue": "ICRA 2023",
             "year": 2023, "citation_count": 95, "research_area": "Robot Control & Dynamics"},
            # Alex Kowalski - Motion Planning
            {"candidate_id": candidates_list[7].id, "title": "Real-Time Multi-Robot Trajectory Optimization in Dynamic Environments",
             "authors": "A. Kowalski, M. Zhang, P. Sharma", "venue": "IROS 2023",
             "year": 2023, "citation_count": 52, "research_area": "Motion Planning & Navigation"}
        ]

        for p in pubs_data:
            pub = Publication(**p)
            db.session.add(pub)

        db.session.flush()

        # ==================== SEED APPLICATIONS + INTELLIGENCE SUBMISSIONS ====================
        import json as json_module

        jobs_list = Job.query.order_by(Job.id).all()

        # Create sample applications with intelligence submissions for demo
        intelligence_seeds = [
            {
                "candidate_idx": 0, "job_idx": 0,  # Anika Patel -> Humanoid Roboticist @ Figure AI
                "work_links": [
                    {"link_type": "github", "url": "https://github.com/anikapatel/bipedal-rl", "title": "Bipedal RL Controller"},
                    {"link_type": "paper", "url": "https://arxiv.org/abs/2024.12345", "title": "Deep RL for Bipedal Locomotion on Uneven Terrain"},
                    {"link_type": "paper", "url": "https://arxiv.org/abs/2023.98765", "title": "Whole-Body Control for Humanoid Manipulation"},
                    {"link_type": "demo", "url": "https://youtube.com/watch?v=demo123", "title": "Figure 01 Walking Demo"}
                ],
                "response_text": "When integrating perception, control, and actuation for humanoid systems, the earliest indicator I monitor is the divergence between predicted and actual joint torque profiles during the first 50ms of a new motion primitive. This reveals cascading instability before it propagates to higher-level controllers. In my bipedal locomotion work, I noticed that ankle torque prediction errors above 15% reliably predicted full-body instability within 200ms. My intervention pattern: immediately shift to a conservative stance controller while the learning system adapts its internal model. This saved us from 3 hardware-damaging falls during real-robot testing at Stanford.",
                "hidden_signal": "I rebuilt Figure's sim-to-real pipeline from scratch after the original failed on uneven terrain",
                "extracted_skills": ["PyTorch", "Isaac Gym", "MuJoCo", "Bipedal Control", "Reinforcement Learning", "Sim-to-Real Transfer", "ROS2", "Whole-Body Control", "C++", "Python", "Trajectory Optimization"],
                "key_phrases": [
                    {"phrase": "joint torque profile divergence", "importance": "high", "context": "Candidate identifies a specific, non-obvious early indicator for system instability - shows deep domain expertise"},
                    {"phrase": "conservative stance controller", "importance": "high", "context": "Demonstrates graceful degradation thinking - prioritizes hardware safety over performance"},
                    {"phrase": "sim-to-real pipeline from scratch", "importance": "high", "context": "Hidden signal reveals initiative and ability to rebuild critical infrastructure"}
                ],
                "artifact_analysis": [
                    {"type": "github", "url": "https://github.com/anikapatel/bipedal-rl", "summary": "Well-structured RL codebase for bipedal locomotion with clear documentation, comprehensive tests, and modular architecture. 847 stars, 12 contributors.", "relevance": "high", "quality_indicators": "Clean code architecture, CI/CD pipeline, extensive README with math notation"},
                    {"type": "paper", "url": "https://arxiv.org/abs/2024.12345", "summary": "ICRA 2024 paper on deep RL for bipedal locomotion. Strong experimental section with real-robot validation.", "relevance": "high", "quality_indicators": "Top-tier venue, 45 citations, real-world validation"},
                    {"type": "demo", "url": "https://youtube.com/watch?v=demo123", "summary": "Video demonstration of bipedal walking on various terrains including gravel, slopes, and stairs.", "relevance": "medium", "quality_indicators": "Real hardware demo, not simulation only"}
                ],
                "ai_assessment": {
                    "recommendation": "HIGHLY RECOMMEND - FAST TRACK",
                    "strengths": [
                        "Deep systems-level understanding of humanoid control - identifies non-obvious failure indicators",
                        "Proven sim-to-real transfer experience with real hardware",
                        "Strong publication record at top robotics venues (ICRA, CoRL)",
                        "Open-source contributions demonstrate code quality and collaboration ability",
                        "Initiative shown in rebuilding critical infrastructure (hidden signal)"
                    ],
                    "potential_gaps": [
                        "Limited mention of manipulation tasks - focus appears primarily on locomotion",
                        "No explicit mention of production deployment at scale"
                    ],
                    "technical_depth": "Expert - Demonstrates mastery of both theoretical foundations and practical implementation",
                    "systems_thinking": "Exceptional - Identifies cross-system failure propagation patterns and designs graceful degradation strategies",
                    "next_steps": "Schedule technical deep-dive on whole-body manipulation. Ask about experience with hardware failure recovery and production-grade safety systems."
                }
            },
            {
                "candidate_idx": 1, "job_idx": 2,  # Jin Nakamura -> Perception/SLAM @ Boston Dynamics
                "work_links": [
                    {"link_type": "github", "url": "https://github.com/jnakamura/edge-slam", "title": "Edge SLAM Framework"},
                    {"link_type": "paper", "url": "https://arxiv.org/abs/2023.54321", "title": "Real-Time Visual SLAM on Edge Devices"},
                    {"link_type": "dataset", "url": "https://huggingface.co/datasets/jnakamura/indoor-slam-benchmark", "title": "Indoor SLAM Benchmark Dataset"}
                ],
                "response_text": "In SLAM drift scenarios, my go-to method is analyzing the information matrix eigenvalue spectrum of the factor graph. When the smallest eigenvalue drops below a threshold I've empirically determined for each sensor configuration, it tells me the system is becoming under-constrained. The critical cue for differentiating root cause: if eigenvalue degradation is uniform across spatial dimensions, it's typically sensor bias (IMU drift). If it's directionally biased, it's usually map quality degradation from repetitive environments. If it's sudden and localized, it's a missed loop closure. At Toyota Research, this diagnostic saved us 2 weeks of debugging on the warehouse mapping project.",
                "hidden_signal": "I optimized our SLAM pipeline to run on Jetson Orin at 30fps - the team said it was impossible",
                "extracted_skills": ["Visual SLAM", "LiDAR SLAM", "Factor Graphs", "GTSAM", "Edge Computing", "Jetson Orin", "C++", "CUDA", "TensorRT", "ROS2", "Point Cloud Processing"],
                "key_phrases": [
                    {"phrase": "information matrix eigenvalue spectrum", "importance": "high", "context": "Highly specific SLAM diagnostic - indicates deep mathematical understanding beyond surface-level SLAM usage"},
                    {"phrase": "directionally biased degradation", "importance": "high", "context": "Shows systematic root cause analysis methodology for spatial mapping failures"},
                    {"phrase": "30fps on Jetson Orin", "importance": "medium", "context": "Hidden signal reveals edge optimization capability - critical for mobile robots"}
                ],
                "artifact_analysis": [
                    {"type": "github", "url": "https://github.com/jnakamura/edge-slam", "summary": "Production-quality SLAM framework optimized for edge devices. Impressive benchmarks against ORB-SLAM3 and RTAB-Map.", "relevance": "high", "quality_indicators": "2.3k stars, used by 3 robotics companies, comprehensive benchmarks"},
                    {"type": "paper", "url": "https://arxiv.org/abs/2023.54321", "summary": "Novel approach to visual SLAM optimization for resource-constrained hardware. Real-time performance on embedded GPUs.", "relevance": "high", "quality_indicators": "IROS 2023, 89 citations, reproducible results"}
                ],
                "ai_assessment": {
                    "recommendation": "HIGHLY RECOMMEND",
                    "strengths": [
                        "Exceptional diagnostic methodology for SLAM systems - goes beyond standard tooling",
                        "Proven edge deployment experience (Jetson Orin optimization)",
                        "Strong mathematical foundations in factor graph optimization",
                        "Open-source SLAM framework with real industry adoption"
                    ],
                    "potential_gaps": [
                        "Experience appears focused on indoor/warehouse environments - unclear about outdoor/adverse weather SLAM",
                        "No mention of multi-robot SLAM or collaborative mapping"
                    ],
                    "technical_depth": "Expert - Deep understanding of SLAM mathematical foundations and practical optimization",
                    "systems_thinking": "Strong - Systematic root cause isolation methodology across sensor, map, and algorithm domains",
                    "next_steps": "Schedule hands-on SLAM challenge. Explore experience with outdoor environments and dynamic obstacle handling."
                }
            },
            {
                "candidate_idx": 2, "job_idx": 4,  # Sofia Andersen -> AV Engineer @ Stealth AV
                "work_links": [
                    {"link_type": "github", "url": "https://github.com/sandersen/lidar-camera-fusion", "title": "LiDAR-Camera Fusion Library"},
                    {"link_type": "paper", "url": "https://arxiv.org/abs/2024.67890", "title": "Multi-Modal Sensor Fusion for Robust AV Perception"},
                    {"link_type": "project", "url": "https://sandersen.dev/av-perception-demo", "title": "AV Perception Pipeline Demo"}
                ],
                "response_text": "When an AV faces conflicting inputs between perception and motion planning, I anchor my decision hierarchy on a risk-weighted confidence framework. The motion planner gets priority when: perception confidence drops below a tuned threshold AND the planner has a valid safe trajectory from its last high-confidence cycle. Perception gets priority when: multiple sensor modalities agree on a novel obstacle even if it contradicts the prior map. The non-obvious signal I watch: the rate of change of the perception-planner disagreement score. A sudden spike (not gradual drift) usually indicates a real environmental change rather than sensor noise. At Waymo, this framework reduced our false emergency stops by 34% while maintaining safety margins.",
                "hidden_signal": "I discovered a critical sensor calibration drift that was causing 12% of our false positives - fixed it and it became standard protocol",
                "extracted_skills": ["LiDAR Processing", "Camera-LiDAR Fusion", "3D Object Detection", "Sensor Calibration", "Python", "C++", "TensorRT", "CUDA", "Point Cloud Processing", "ROS2"],
                "key_phrases": [
                    {"phrase": "risk-weighted confidence framework", "importance": "high", "context": "Structured decision-making methodology for safety-critical autonomous systems"},
                    {"phrase": "rate of change of disagreement score", "importance": "high", "context": "Novel meta-signal for distinguishing real events from noise - systems-level thinking"},
                    {"phrase": "reduced false emergency stops by 34%", "importance": "medium", "context": "Quantified impact at Waymo - demonstrates measurable engineering outcomes"}
                ],
                "artifact_analysis": [
                    {"type": "github", "url": "https://github.com/sandersen/lidar-camera-fusion", "summary": "Robust sensor fusion library with uncertainty-aware fusion pipeline. Good test coverage.", "relevance": "high", "quality_indicators": "340 stars, well-documented API, unit tests"},
                    {"type": "paper", "url": "https://arxiv.org/abs/2024.67890", "summary": "CVPR 2024 paper on multi-modal perception for adverse weather driving. State-of-the-art results on nuScenes.", "relevance": "high", "quality_indicators": "Top-tier venue, strong experimental methodology"}
                ],
                "ai_assessment": {
                    "recommendation": "RECOMMEND - STRONG CANDIDATE",
                    "strengths": [
                        "Structured safety-critical decision framework - essential for AV development",
                        "Quantified impact at Waymo (34% reduction in false emergency stops)",
                        "Strong sensor fusion expertise across LiDAR and camera modalities",
                        "Initiative in identifying and fixing systematic calibration issues"
                    ],
                    "potential_gaps": [
                        "Heavy focus on perception - less evidence of end-to-end planning integration",
                        "No mention of V2X or infrastructure-aware perception"
                    ],
                    "technical_depth": "Advanced - Strong combination of theoretical understanding and practical deployment",
                    "systems_thinking": "Strong - Risk-weighted confidence framework shows mature systems engineering approach",
                    "next_steps": "Explore experience with planning integration and safety validation frameworks. Ask about scaling from prototype to production fleet."
                }
            }
        ]

        intelligence_created = 0
        for seed in intelligence_seeds:
            cand = candidates_list[seed['candidate_idx']]
            job_obj = jobs_list[seed['job_idx']] if seed['job_idx'] < len(jobs_list) else jobs_list[0]
            role_q = PHYSICAL_AI_ROLE_QUESTIONS.get(job_obj.title, {})

            # Create Application
            app_record = Application(
                job_id=job_obj.id,
                candidate_id=cand.id,
                status='screening',
                source='landing_page',
                overall_score=85
            )
            db.session.add(app_record)
            db.session.flush()

            # Create CandidateLinks
            for wl in seed['work_links']:
                cl = CandidateLink(candidate_id=cand.id, link_type=wl['link_type'], url=wl['url'], title=wl.get('title', ''))
                db.session.add(cl)

            # Create HiringIntelligenceSubmission with full AI analysis
            submission_data = {
                'candidate_name': f"{cand.first_name} {cand.last_name}",
                'candidate_email': cand.email,
                'position': job_obj.title,
                'hidden_signal': seed.get('hidden_signal', ''),
                'work_links': seed['work_links'],
                'intelligence_response': {
                    'question_label': role_q.get('label', 'Hiring Intelligence'),
                    'question_text': role_q.get('question', ''),
                    'response_text': seed['response_text']
                },
                'generated_at': datetime.utcnow().isoformat()
            }

            his = HiringIntelligenceSubmission(
                application_id=app_record.id,
                submission_data=json_module.dumps(submission_data),
                status='reviewed',
                missing_signal='hardware testing',
                passed_to_screen=True,
                passed_to_interview=seed['candidate_idx'] < 2,
                received_offer=seed['candidate_idx'] == 0,
                extracted_skills=json_module.dumps(seed.get('extracted_skills', [])),
                key_phrases=json_module.dumps(seed.get('key_phrases', [])),
                artifact_analysis=json_module.dumps(seed.get('artifact_analysis', [])),
                ai_assessment=json_module.dumps(seed.get('ai_assessment', {})),
                ai_analyzed=True,
                ai_analyzed_at=datetime.utcnow()
            )
            db.session.add(his)
            intelligence_created += 1

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Sample data loaded successfully!",
            "candidates_created": created_candidates,
            "jobs_created": created_jobs,
            "publications_created": len(pubs_data),
            "intelligence_submissions_created": intelligence_created,
            "stealth_jobs": 4
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/seed-intelligence', methods=['POST'])
def seed_intelligence_data():
    """Seed intelligence submissions for existing candidates/jobs — works even when DB already has data"""
    import json as json_module

    # Check if intelligence submissions already exist
    try:
        existing = HiringIntelligenceSubmission.query.count()
        if existing > 0:
            return jsonify({
                "message": f"Intelligence submissions already exist ({existing} records). Delete them first to re-seed.",
                "existing_count": existing
            }), 409
    except Exception:
        pass  # Table may not exist yet, create_all will handle it

    candidates_list = Candidate.query.order_by(Candidate.id).all()
    jobs_list = Job.query.order_by(Job.id).all()

    if len(candidates_list) < 3 or len(jobs_list) < 3:
        return jsonify({"error": "Need at least 3 candidates and 3 jobs. Run /api/seed-data first."}), 400

    try:
        intelligence_seeds = [
            {
                "candidate_idx": 0, "job_idx": 0,
                "work_links": [
                    {"link_type": "github", "url": "https://github.com/anikapatel/bipedal-rl", "title": "Bipedal RL Controller"},
                    {"link_type": "paper", "url": "https://arxiv.org/abs/2024.12345", "title": "Deep RL for Bipedal Locomotion on Uneven Terrain"},
                    {"link_type": "paper", "url": "https://arxiv.org/abs/2023.98765", "title": "Whole-Body Control for Humanoid Manipulation"},
                    {"link_type": "demo", "url": "https://youtube.com/watch?v=demo123", "title": "Figure 01 Walking Demo"}
                ],
                "response_text": "When integrating perception, control, and actuation for humanoid systems, the earliest indicator I monitor is the divergence between predicted and actual joint torque profiles during the first 50ms of a new motion primitive. This reveals cascading instability before it propagates to higher-level controllers. In my bipedal locomotion work, I noticed that ankle torque prediction errors above 15% reliably predicted full-body instability within 200ms. My intervention pattern: immediately shift to a conservative stance controller while the learning system adapts its internal model. This saved us from 3 hardware-damaging falls during real-robot testing at Stanford.",
                "hidden_signal": "I rebuilt Figure's sim-to-real pipeline from scratch after the original failed on uneven terrain",
                "extracted_skills": ["PyTorch", "Isaac Gym", "MuJoCo", "Bipedal Control", "Reinforcement Learning", "Sim-to-Real Transfer", "ROS2", "Whole-Body Control", "C++", "Python", "Trajectory Optimization"],
                "key_phrases": [
                    {"phrase": "joint torque profile divergence", "importance": "high", "context": "Identifies a specific, non-obvious early indicator for system instability - deep domain expertise"},
                    {"phrase": "conservative stance controller", "importance": "high", "context": "Demonstrates graceful degradation thinking - prioritizes hardware safety over performance"},
                    {"phrase": "sim-to-real pipeline from scratch", "importance": "high", "context": "Hidden signal reveals initiative and ability to rebuild critical infrastructure"}
                ],
                "artifact_analysis": [
                    {"type": "github", "url": "https://github.com/anikapatel/bipedal-rl", "summary": "Well-structured RL codebase for bipedal locomotion with clear documentation, comprehensive tests, and modular architecture. 847 stars, 12 contributors.", "relevance": "high", "quality_indicators": "Clean code architecture, CI/CD pipeline, extensive README with math notation"},
                    {"type": "paper", "url": "https://arxiv.org/abs/2024.12345", "summary": "ICRA 2024 paper on deep RL for bipedal locomotion. Strong experimental section with real-robot validation.", "relevance": "high", "quality_indicators": "Top-tier venue, 45 citations, real-world validation"},
                    {"type": "demo", "url": "https://youtube.com/watch?v=demo123", "summary": "Video demonstration of bipedal walking on various terrains including gravel, slopes, and stairs.", "relevance": "medium", "quality_indicators": "Real hardware demo, not simulation only"}
                ],
                "ai_assessment": {
                    "recommendation": "HIGHLY RECOMMEND - FAST TRACK",
                    "strengths": [
                        "Deep systems-level understanding of humanoid control - identifies non-obvious failure indicators",
                        "Proven sim-to-real transfer experience with real hardware",
                        "Strong publication record at top robotics venues (ICRA, CoRL)",
                        "Open-source contributions demonstrate code quality and collaboration ability",
                        "Initiative shown in rebuilding critical infrastructure (hidden signal)"
                    ],
                    "potential_gaps": [
                        "Limited mention of manipulation tasks - focus appears primarily on locomotion",
                        "No explicit mention of production deployment at scale"
                    ],
                    "technical_depth": "Expert - Demonstrates mastery of both theoretical foundations and practical implementation",
                    "systems_thinking": "Exceptional - Identifies cross-system failure propagation patterns and designs graceful degradation strategies",
                    "next_steps": "Schedule technical deep-dive on whole-body manipulation. Ask about experience with hardware failure recovery and production-grade safety systems."
                }
            },
            {
                "candidate_idx": 1, "job_idx": min(2, len(jobs_list) - 1),
                "work_links": [
                    {"link_type": "github", "url": "https://github.com/jnakamura/edge-slam", "title": "Edge SLAM Framework"},
                    {"link_type": "paper", "url": "https://arxiv.org/abs/2023.54321", "title": "Real-Time Visual SLAM on Edge Devices"},
                    {"link_type": "dataset", "url": "https://huggingface.co/datasets/jnakamura/indoor-slam-benchmark", "title": "Indoor SLAM Benchmark Dataset"}
                ],
                "response_text": "In SLAM drift scenarios, my go-to method is analyzing the information matrix eigenvalue spectrum of the factor graph. When the smallest eigenvalue drops below a threshold I've empirically determined for each sensor configuration, it tells me the system is becoming under-constrained. The critical cue for differentiating root cause: if eigenvalue degradation is uniform across spatial dimensions, it's typically sensor bias (IMU drift). If it's directionally biased, it's usually map quality degradation from repetitive environments. If it's sudden and localized, it's a missed loop closure. At Toyota Research, this diagnostic saved us 2 weeks of debugging on the warehouse mapping project.",
                "hidden_signal": "I optimized our SLAM pipeline to run on Jetson Orin at 30fps - the team said it was impossible",
                "extracted_skills": ["Visual SLAM", "LiDAR SLAM", "Factor Graphs", "GTSAM", "Edge Computing", "Jetson Orin", "C++", "CUDA", "TensorRT", "ROS2", "Point Cloud Processing"],
                "key_phrases": [
                    {"phrase": "information matrix eigenvalue spectrum", "importance": "high", "context": "Highly specific SLAM diagnostic - indicates deep mathematical understanding beyond surface-level SLAM usage"},
                    {"phrase": "directionally biased degradation", "importance": "high", "context": "Shows systematic root cause analysis methodology for spatial mapping failures"},
                    {"phrase": "30fps on Jetson Orin", "importance": "medium", "context": "Hidden signal reveals edge optimization capability - critical for mobile robots"}
                ],
                "artifact_analysis": [
                    {"type": "github", "url": "https://github.com/jnakamura/edge-slam", "summary": "Production-quality SLAM framework optimized for edge devices. Impressive benchmarks against ORB-SLAM3 and RTAB-Map.", "relevance": "high", "quality_indicators": "2.3k stars, used by 3 robotics companies, comprehensive benchmarks"},
                    {"type": "paper", "url": "https://arxiv.org/abs/2023.54321", "summary": "Novel approach to visual SLAM optimization for resource-constrained hardware. Real-time performance on embedded GPUs.", "relevance": "high", "quality_indicators": "IROS 2023, 89 citations, reproducible results"}
                ],
                "ai_assessment": {
                    "recommendation": "HIGHLY RECOMMEND",
                    "strengths": [
                        "Exceptional diagnostic methodology for SLAM systems - goes beyond standard tooling",
                        "Proven edge deployment experience (Jetson Orin optimization)",
                        "Strong mathematical foundations in factor graph optimization",
                        "Open-source SLAM framework with real industry adoption"
                    ],
                    "potential_gaps": [
                        "Experience appears focused on indoor/warehouse environments - unclear about outdoor/adverse weather SLAM",
                        "No mention of multi-robot SLAM or collaborative mapping"
                    ],
                    "technical_depth": "Expert - Deep understanding of SLAM mathematical foundations and practical optimization",
                    "systems_thinking": "Strong - Systematic root cause isolation methodology across sensor, map, and algorithm domains",
                    "next_steps": "Schedule hands-on SLAM challenge. Explore experience with outdoor environments and dynamic obstacle handling."
                }
            },
            {
                "candidate_idx": 2, "job_idx": min(4, len(jobs_list) - 1),
                "work_links": [
                    {"link_type": "github", "url": "https://github.com/sandersen/lidar-camera-fusion", "title": "LiDAR-Camera Fusion Library"},
                    {"link_type": "paper", "url": "https://arxiv.org/abs/2024.67890", "title": "Multi-Modal Sensor Fusion for Robust AV Perception"},
                    {"link_type": "project", "url": "https://sandersen.dev/av-perception-demo", "title": "AV Perception Pipeline Demo"}
                ],
                "response_text": "When an AV faces conflicting inputs between perception and motion planning, I anchor my decision hierarchy on a risk-weighted confidence framework. The motion planner gets priority when: perception confidence drops below a tuned threshold AND the planner has a valid safe trajectory from its last high-confidence cycle. Perception gets priority when: multiple sensor modalities agree on a novel obstacle even if it contradicts the prior map. The non-obvious signal I watch: the rate of change of the perception-planner disagreement score. A sudden spike (not gradual drift) usually indicates a real environmental change rather than sensor noise. At Waymo, this framework reduced our false emergency stops by 34% while maintaining safety margins.",
                "hidden_signal": "I discovered a critical sensor calibration drift causing 12% of false positives - fixed it and it became standard protocol",
                "extracted_skills": ["LiDAR Processing", "Camera-LiDAR Fusion", "3D Object Detection", "Sensor Calibration", "Python", "C++", "TensorRT", "CUDA", "Point Cloud Processing", "ROS2"],
                "key_phrases": [
                    {"phrase": "risk-weighted confidence framework", "importance": "high", "context": "Structured decision-making methodology for safety-critical autonomous systems"},
                    {"phrase": "rate of change of disagreement score", "importance": "high", "context": "Novel meta-signal for distinguishing real events from noise - systems-level thinking"},
                    {"phrase": "reduced false emergency stops by 34%", "importance": "medium", "context": "Quantified impact at Waymo - demonstrates measurable engineering outcomes"}
                ],
                "artifact_analysis": [
                    {"type": "github", "url": "https://github.com/sandersen/lidar-camera-fusion", "summary": "Robust sensor fusion library with uncertainty-aware fusion pipeline. Good test coverage.", "relevance": "high", "quality_indicators": "340 stars, well-documented API, unit tests"},
                    {"type": "paper", "url": "https://arxiv.org/abs/2024.67890", "summary": "CVPR 2024 paper on multi-modal perception for adverse weather driving. State-of-the-art results on nuScenes.", "relevance": "high", "quality_indicators": "Top-tier venue, strong experimental methodology"}
                ],
                "ai_assessment": {
                    "recommendation": "RECOMMEND - STRONG CANDIDATE",
                    "strengths": [
                        "Structured safety-critical decision framework - essential for AV development",
                        "Quantified impact at Waymo (34% reduction in false emergency stops)",
                        "Strong sensor fusion expertise across LiDAR and camera modalities",
                        "Initiative in identifying and fixing systematic calibration issues"
                    ],
                    "potential_gaps": [
                        "Heavy focus on perception - less evidence of end-to-end planning integration",
                        "No mention of V2X or infrastructure-aware perception"
                    ],
                    "technical_depth": "Advanced - Strong combination of theoretical understanding and practical deployment",
                    "systems_thinking": "Strong - Risk-weighted confidence framework shows mature systems engineering approach",
                    "next_steps": "Explore experience with planning integration and safety validation frameworks. Ask about scaling from prototype to production fleet."
                }
            }
        ]

        intelligence_created = 0
        for seed in intelligence_seeds:
            cand = candidates_list[seed['candidate_idx']]
            job_obj = jobs_list[seed['job_idx']]
            role_q = PHYSICAL_AI_ROLE_QUESTIONS.get(job_obj.title, {})

            # Check for existing application
            existing_app = Application.query.filter_by(candidate_id=cand.id, job_id=job_obj.id).first()
            if existing_app:
                continue

            app_record = Application(
                job_id=job_obj.id,
                candidate_id=cand.id,
                status='screening',
                source='landing_page',
                overall_score=85
            )
            db.session.add(app_record)
            db.session.flush()

            for wl in seed['work_links']:
                cl = CandidateLink(candidate_id=cand.id, link_type=wl['link_type'], url=wl['url'], title=wl.get('title', ''))
                db.session.add(cl)

            submission_data = {
                'candidate_name': f"{cand.first_name} {cand.last_name}",
                'candidate_email': cand.email,
                'position': job_obj.title,
                'hidden_signal': seed.get('hidden_signal', ''),
                'work_links': seed['work_links'],
                'intelligence_response': {
                    'question_label': role_q.get('label', 'Hiring Intelligence'),
                    'question_text': role_q.get('question', ''),
                    'response_text': seed['response_text']
                },
                'generated_at': datetime.utcnow().isoformat()
            }

            his = HiringIntelligenceSubmission(
                application_id=app_record.id,
                submission_data=json_module.dumps(submission_data),
                status='reviewed',
                missing_signal='hardware testing',
                passed_to_screen=True,
                passed_to_interview=seed['candidate_idx'] < 2,
                received_offer=seed['candidate_idx'] == 0,
                extracted_skills=json_module.dumps(seed.get('extracted_skills', [])),
                key_phrases=json_module.dumps(seed.get('key_phrases', [])),
                artifact_analysis=json_module.dumps(seed.get('artifact_analysis', [])),
                ai_assessment=json_module.dumps(seed.get('ai_assessment', {})),
                ai_analyzed=True,
                ai_analyzed_at=datetime.utcnow()
            )
            db.session.add(his)
            intelligence_created += 1

        db.session.commit()
        return jsonify({
            "success": True,
            "message": f"Intelligence submissions seeded successfully!",
            "intelligence_submissions_created": intelligence_created
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    is_dev = 'sqlite' in (app.config.get('SQLALCHEMY_DATABASE_URI') or '')
    app.run(debug=is_dev, host='0.0.0.0', port=port)
