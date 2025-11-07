from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import requests
import re

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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


# Create tables
with app.app_context():
    db.create_all()


# ==================== API ENDPOINTS ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "AI/ML ATS API is running",
        "version": "1.0.0"
    })


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

    if response.status_code == 200:
        data = response.json()
        users = data.get('items', [])

        # Fetch detailed info for each user
        enriched_users = []
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

        return {
            'total_count': data.get('total_count', 0),
            'results': enriched_users,
            'search_query': search_query,
            'message': f'Found {len(enriched_users)} GitHub users with detailed profiles'
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
