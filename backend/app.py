from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import os
import requests
import re

# Load environment variables from .env file (for local development)
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Enable SQL logging to see actual queries
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
    position = db.Column(db.String(255))  # Selected position/role (from dropdown)

    # Tracking
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_contact_date = db.Column(db.DateTime)
    interview_date = db.Column(db.DateTime)

    # Scoring (AI/ML candidate fit)
    technical_score = db.Column(db.Integer)  # 1-100
    research_score = db.Column(db.Integer)  # Based on publications, citations
    culture_fit_score = db.Column(db.Integer)  # 1-100
    overall_score = db.Column(db.Integer)  # Combined score

    # Hiring Intelligence (replaces cover letter)
    hiring_intelligence = db.Column(db.Text)  # Role-adaptive assessment response
    hidden_signal = db.Column(db.Text)  # Hidden signal candidate wants noticed

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
            'candidate_email': self.candidate.email if self.candidate else None,
            'candidate_phone': self.candidate.phone if self.candidate else None,
            'candidate_location': self.candidate.location if self.candidate else None,
            'candidate_years_experience': self.candidate.years_experience if self.candidate else None,
            'candidate_primary_expertise': self.candidate.primary_expertise if self.candidate else None,
            'candidate_linkedin': self.candidate.linkedin_url if self.candidate else None,
            'candidate_github': self.candidate.github_url if self.candidate else None,
            'candidate_portfolio': self.candidate.portfolio_url if self.candidate else None,
            'job_title': self.job.title if self.job else None,
            'status': self.status,
            'stage': self.stage,
            'source': self.source,
            'position': self.position,
            'applied_date': self.applied_date.isoformat() if self.applied_date else None,
            'last_contact_date': self.last_contact_date.isoformat() if self.last_contact_date else None,
            'interview_date': self.interview_date.isoformat() if self.interview_date else None,
            'technical_score': self.technical_score,
            'research_score': self.research_score,
            'culture_fit_score': self.culture_fit_score,
            'overall_score': self.overall_score,
            'hiring_intelligence': self.hiring_intelligence,
            'hidden_signal': self.hidden_signal,
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


# ==================== API ENDPOINTS ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "PAIP - PhysicalAIPros.com API is running",
        "version": "1.0.0"
    })


@app.route('/api/config/check', methods=['GET'])
def check_config():
    """Check environment configuration (for debugging)"""
    anthropic_key = os.environ.get('ANTHROPIC_API_KEY')
    github_token = os.environ.get('GITHUB_TOKEN')

    return jsonify({
        "anthropic_api_key_configured": bool(anthropic_key),
        "anthropic_api_key_length": len(anthropic_key) if anthropic_key else 0,
        "anthropic_api_key_preview": anthropic_key[:10] + "..." if anthropic_key else None,
        "github_token_configured": bool(github_token),
        "environment_vars_count": len(os.environ),
        "environment_vars_list": list(os.environ.keys())[:20]  # First 20 for debugging
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
                    journal='arXiv',
                    year=result.published.year,
                    citations=0,  # arXiv API doesn't provide citations
                    url=result.entry_id,
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
                    journal=pub_filled['bib'].get('venue', 'Unknown'),
                    year=int(pub_filled['bib'].get('pub_year', 0)) if pub_filled['bib'].get('pub_year') else None,
                    citations=pub_filled.get('num_citations', 0),
                    url=pub_filled.get('pub_url', pub_filled.get('eprint_url', ''))
                )
                db.session.add(publication)
                papers_added += 1

                papers_data.append({
                    'title': publication.title,
                    'year': publication.year,
                    'citations': publication.citations
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


# ==================== PHASE 3: AI/ML FEATURES ====================

# Top AI/ML conferences for tracking
TOP_CONFERENCES = [
    'NeurIPS', 'NIPS', 'ICML', 'ICLR', 'CVPR', 'ICCV', 'ECCV',
    'AAAI', 'IJCAI', 'ACL', 'EMNLP', 'NAACL', 'KDD', 'SIGIR',
    'ICRA', 'IROS', 'RSS', 'CoRL'
]

# AI/ML skills taxonomy
AI_ML_SKILLS = {
    'deep_learning': ['deep learning', 'neural network', 'cnn', 'rnn', 'lstm', 'transformer', 'gpt', 'bert', 'attention'],
    'computer_vision': ['computer vision', 'image processing', 'object detection', 'segmentation', 'yolo', 'rcnn', 'opencv'],
    'nlp': ['nlp', 'natural language processing', 'text mining', 'language model', 'tokenization', 'embedding'],
    'reinforcement_learning': ['reinforcement learning', 'rl', 'policy gradient', 'q-learning', 'dqn', 'ppo', 'actor-critic'],
    'robotics': ['robotics', 'robot', 'manipulation', 'navigation', 'slam', 'ros', 'motion planning'],
    'ml_frameworks': ['pytorch', 'tensorflow', 'keras', 'jax', 'scikit-learn', 'pandas', 'numpy'],
    'programming': ['python', 'c++', 'java', 'javascript', 'go', 'rust', 'cuda'],
    'ml_ops': ['docker', 'kubernetes', 'mlflow', 'wandb', 'aws', 'gcp', 'azure']
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
        venue = pub.journal.upper() if pub.journal else ''
        for conf in TOP_CONFERENCES:
            if conf in venue:
                conference_pubs += 1
                break
    score_breakdown['conference_score'] = min(conference_pubs * 3, 15)

    # Calculate total (out of 100)
    score_breakdown['total_score'] = round(sum([
        score_breakdown['h_index_score'],
        score_breakdown['citation_score'],
        score_breakdown['publication_score'],
        score_breakdown['github_score'],
        score_breakdown['conference_score']
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
            "top_conference_pubs": conference_pubs
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
        venue = pub.journal.upper() if pub.journal else ''

        # Check if it's a top conference
        for conf in TOP_CONFERENCES:
            if conf in venue:
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
                    'citations': pub.citations,
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


# ==================== HIRING INTELLIGENCE MODELS ====================

class RoleQuestion(db.Model):
    """Role-specific intelligence questions for hiring assessment"""
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=True)  # Null = template question

    # Question Details
    role_title = db.Column(db.String(200), nullable=False)  # e.g., "Robotics Engineer"
    label = db.Column(db.String(200), nullable=False)  # e.g., "Robotics Systems Intelligence"
    question = db.Column(db.Text, nullable=False)  # The actual question text

    # Metadata
    is_template = db.Column(db.Boolean, default=False)  # True = pre-populated template
    is_active = db.Column(db.Boolean, default=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    responses = db.relationship('IntelligenceResponse', backref='question', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'role_title': self.role_title,
            'label': self.label,
            'question': self.question,
            'is_template': self.is_template,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class CandidateLink(db.Model):
    """Work artifact links submitted by candidates"""
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)

    # Link Details
    link_type = db.Column(db.String(50), nullable=False)  # github, portfolio, paper, linkedin, other
    url = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(300))  # Optional title/description

    # Timestamps
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


class IntelligenceResponse(db.Model):
    """Candidate responses to intelligence questions"""
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('role_question.id'), nullable=False)

    # Response
    response_text = db.Column(db.Text, nullable=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        question = RoleQuestion.query.get(self.question_id)
        return {
            'id': self.id,
            'application_id': self.application_id,
            'question_id': self.question_id,
            'question_label': question.label if question else None,
            'question_text': question.question if question else None,
            'response_text': self.response_text,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class HiringIntelligenceSubmission(db.Model):
    """Compiled Hiring Intelligence Submission document"""
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)

    # Submission Data (JSON containing the full intelligence document)
    submission_data = db.Column(db.Text)  # JSON string

    # Status
    status = db.Column(db.String(50), default='pending')  # pending, generated, reviewed, advanced, rejected

    # Recruiter Feedback
    missing_signal = db.Column(db.String(200))  # The 1 word/phrase that was missing
    recruiter_notes = db.Column(db.Text)

    # Funnel Tracking
    passed_to_screen = db.Column(db.Boolean)
    passed_to_interview = db.Column(db.Boolean)
    received_offer = db.Column(db.Boolean)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)

    # AI Analysis Fields (for hiring manager's eye automation)
    extracted_skills = db.Column(db.Text)  # JSON array of technical skills
    key_phrases = db.Column(db.Text)  # JSON array of {phrase, context, importance}
    ai_assessment = db.Column(db.Text)  # JSON object with strengths, gaps, depth_score, recommendation
    artifact_analysis = db.Column(db.Text)  # JSON array of {url, summary, quality, relevance}

    # Analysis Metadata
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
            # AI Analysis fields
            'extracted_skills': self.extracted_skills,
            'key_phrases': self.key_phrases,
            'ai_assessment': self.ai_assessment,
            'artifact_analysis': self.artifact_analysis,
            'ai_analyzed': self.ai_analyzed,
            'ai_analyzed_at': self.ai_analyzed_at.isoformat() if self.ai_analyzed_at else None
        }


# Pre-populated Physical AI role questions (from hiring intelligence research)
PHYSICAL_AI_ROLE_QUESTIONS = {
    "Robotics Engineer": {
        "label": "Robotics Systems Intelligence",
        "question": "When integrating perception, control, and actuation, what is the earliest indicator you monitor to detect system-wide instability—and how do you intervene before the issue compounds?"
    },
    "Humanoid Roboticist": {
        "label": "Embodied Dynamics Insight",
        "question": "Describe a time when human biomechanics understanding guided a breakthrough in humanoid stability, manipulation, or locomotion. Which non-obvious signal shaped your approach?"
    },
    "Autonomous Vehicle Engineer": {
        "label": "Autonomy Arbitration Intelligence",
        "question": "When an AV faces conflicting inputs (e.g., perception noise vs motion planning constraints), how do you determine which subsystem receives priority? Share your decision logic and the signals that drove it."
    },
    "Computer Vision Engineer (Robotics)": {
        "label": "CV-for-Robotics Intelligence",
        "question": "What is the most critical vision failure mode you design against in physical environments, and which early signal reveals it before overall performance degrades?"
    },
    "Perception Engineer": {
        "label": "Perception Systems Insight",
        "question": "How do you distinguish true environmental features from sensor artifacts in complex scenes? Describe the signal or test that helps you decide."
    },
    "Motion Planning Engineer": {
        "label": "Trajectory Intelligence",
        "question": "When your planner yields a feasible but suboptimal trajectory, what is the first constraint you interrogate to unlock a more efficient or safer path?"
    },
    "SLAM Engineer": {
        "label": "Spatial Intelligence Diagnostic",
        "question": "In SLAM drift scenarios, what is your go-to method for isolating root cause—and which cue tells you whether the issue is map quality, loop closure, or sensor bias?"
    },
    "Autonomous Systems Engineer": {
        "label": "System Autonomy Insight",
        "question": "How do you architect decision-making when subsystems report uncertain or contradictory outputs? Describe the governing principle and an example."
    },
    "Robot Control Engineer": {
        "label": "Control Loop Judgment",
        "question": "When tuning controllers, what early signal indicates imminent stability loss—and what immediate corrective pattern do you apply?"
    },
    "Reinforcement Learning Engineer": {
        "label": "RL Signal Intelligence",
        "question": "When training an RL agent, what hidden metric or behavioral cue do you monitor that predicts long-term policy success before reward curves show it?"
    },
    "Computer Vision Engineer": {
        "label": "Vision Modeling Insight",
        "question": "When a vision model misclassifies or misses detections, what visual or dataset signal do you check first to determine whether the root cause is labeling noise, domain shift, or architecture limits?"
    },
    "Deep Learning Engineer": {
        "label": "Model Behavior Intelligence",
        "question": "Which model behavior (beyond accuracy) reveals deeper problems—something you watch early to detect future failure—and how do you act on it?"
    },
    "ML Systems Engineer": {
        "label": "Systems-Level ML Intelligence",
        "question": "When scaling ML pipelines, which system bottleneck do you diagnose first—and which early indicator tells you the pipeline will fail under production load?"
    },
    "AI/ML Engineer": {
        "label": "AI Solutioning Insight",
        "question": "When balancing performance, latency, and cost, which constraint becomes your anchor—and how do you determine and enforce that anchor in architecture or process?"
    },
    "Sensor Fusion Engineer": {
        "label": "Fusion Signal Intelligence",
        "question": "When sensor streams diverge, what earliest cue tells you which modality is unreliable, and how do you reconcile conflicting estimates in real time?"
    },
    "Embedded AI Engineer": {
        "label": "On-Device Intelligence Insight",
        "question": "When deploying models at the edge, which signal first tells you the hardware-software interface will be the limiting factor—and how do you mitigate it?"
    },
    "Robotics Software Engineer": {
        "label": "Software Integration Intelligence",
        "question": "When debugging heterogeneous robotic stacks, what cross-component signal do you examine first to determine whether the root cause is software logic, timing, or hardware interaction?"
    },
    "Machine Learning Engineer": {
        "label": "ML Insight Diagnostic",
        "question": "What is your highest-leverage early indicator that a training pipeline is learning the wrong patterns—even before validation metrics degrade?"
    },
    "Deep Learning Researcher": {
        "label": "Research Intelligence Signal",
        "question": "What subtle model behavior—beyond raw accuracy—signals that a research direction has deep potential and deserves further investment?"
    }
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


# ==================== HIRING INTELLIGENCE ENDPOINTS ====================

@app.route('/api/role-questions/templates', methods=['GET'])
def get_role_question_templates():
    """Get all pre-populated Physical AI role question templates"""
    templates = []
    for role_title, data in PHYSICAL_AI_ROLE_QUESTIONS.items():
        templates.append({
            'role_title': role_title,
            'label': data['label'],
            'question': data['question']
        })
    return jsonify({
        'templates': templates,
        'total': len(templates)
    })


@app.route('/api/role-questions/seed-templates', methods=['POST'])
def seed_role_question_templates():
    """Seed the database with pre-populated Physical AI role question templates"""
    created = 0
    for role_title, data in PHYSICAL_AI_ROLE_QUESTIONS.items():
        # Check if template already exists
        existing = RoleQuestion.query.filter_by(
            role_title=role_title,
            is_template=True
        ).first()

        if not existing:
            question = RoleQuestion(
                role_title=role_title,
                label=data['label'],
                question=data['question'],
                is_template=True,
                is_active=True
            )
            db.session.add(question)
            created += 1

    db.session.commit()
    return jsonify({
        'message': f'Seeded {created} role question templates',
        'created': created,
        'total_templates': len(PHYSICAL_AI_ROLE_QUESTIONS)
    })


@app.route('/api/jobs/<int:job_id>/questions', methods=['GET'])
def get_job_questions(job_id):
    """Get intelligence questions for a specific job"""
    job = Job.query.get_or_404(job_id)

    # First check for job-specific questions
    questions = RoleQuestion.query.filter_by(job_id=job_id, is_active=True).all()

    # If no job-specific questions, look for template matching job title
    if not questions:
        questions = RoleQuestion.query.filter_by(
            role_title=job.title,
            is_template=True,
            is_active=True
        ).all()

    # If still no questions, check PHYSICAL_AI_ROLE_QUESTIONS directly
    if not questions and job.title in PHYSICAL_AI_ROLE_QUESTIONS:
        data = PHYSICAL_AI_ROLE_QUESTIONS[job.title]
        return jsonify({
            'questions': [{
                'id': None,
                'job_id': job_id,
                'role_title': job.title,
                'label': data['label'],
                'question': data['question'],
                'is_template': True,
                'source': 'built_in'
            }],
            'total': 1
        })

    return jsonify({
        'questions': [q.to_dict() for q in questions],
        'total': len(questions)
    })


@app.route('/api/jobs/<int:job_id>/questions', methods=['POST'])
def create_job_question(job_id):
    """Create a custom intelligence question for a job"""
    job = Job.query.get_or_404(job_id)
    data = request.get_json()

    if not data or 'question' not in data:
        return jsonify({"error": "Question text is required"}), 400

    question = RoleQuestion(
        job_id=job_id,
        role_title=data.get('role_title', job.title),
        label=data.get('label', 'Custom Intelligence Question'),
        question=data['question'],
        is_template=False,
        is_active=True
    )

    db.session.add(question)
    db.session.commit()

    return jsonify(question.to_dict()), 201


@app.route('/api/role-questions/<int:question_id>', methods=['PUT'])
def update_role_question(question_id):
    """Update a role question"""
    question = RoleQuestion.query.get_or_404(question_id)
    data = request.get_json()

    for field in ['role_title', 'label', 'question', 'is_active']:
        if field in data:
            setattr(question, field, data[field])

    db.session.commit()
    return jsonify(question.to_dict())


@app.route('/api/role-questions/<int:question_id>', methods=['DELETE'])
def delete_role_question(question_id):
    """Delete a role question"""
    question = RoleQuestion.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Question deleted successfully"})


# ==================== CANDIDATE LINKS ENDPOINTS ====================

@app.route('/api/candidates/<int:candidate_id>/links', methods=['GET'])
def get_candidate_links(candidate_id):
    """Get all work artifact links for a candidate"""
    candidate = Candidate.query.get_or_404(candidate_id)
    links = CandidateLink.query.filter_by(candidate_id=candidate_id).all()
    return jsonify({
        'links': [link.to_dict() for link in links],
        'total': len(links)
    })


@app.route('/api/candidates/<int:candidate_id>/links', methods=['POST'])
def add_candidate_link(candidate_id):
    """Add a work artifact link to a candidate"""
    candidate = Candidate.query.get_or_404(candidate_id)
    data = request.get_json()

    if not data or 'url' not in data or 'link_type' not in data:
        return jsonify({"error": "URL and link_type are required"}), 400

    link = CandidateLink(
        candidate_id=candidate_id,
        link_type=data['link_type'],
        url=data['url'],
        title=data.get('title')
    )

    db.session.add(link)
    db.session.commit()

    return jsonify(link.to_dict()), 201


@app.route('/api/candidate-links/<int:link_id>', methods=['DELETE'])
def delete_candidate_link(link_id):
    """Delete a candidate link"""
    link = CandidateLink.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    return jsonify({"message": "Link deleted successfully"})


# ==================== INTELLIGENCE RESPONSES ENDPOINTS ====================

@app.route('/api/applications/<int:application_id>/intelligence', methods=['GET'])
def get_application_intelligence(application_id):
    """Get intelligence responses for an application"""
    application = Application.query.get_or_404(application_id)
    responses = IntelligenceResponse.query.filter_by(application_id=application_id).all()

    return jsonify({
        'responses': [r.to_dict() for r in responses],
        'total': len(responses)
    })


@app.route('/api/applications/<int:application_id>/intelligence', methods=['POST'])
def add_intelligence_response(application_id):
    """Add an intelligence response to an application"""
    application = Application.query.get_or_404(application_id)
    data = request.get_json()

    if not data or 'response_text' not in data:
        return jsonify({"error": "Response text is required"}), 400

    # Get or create question
    question_id = data.get('question_id')

    if not question_id:
        # Check if we should use a template question
        job = Job.query.get(application.job_id)
        if job and job.title in PHYSICAL_AI_ROLE_QUESTIONS:
            # Create a question from template
            template_data = PHYSICAL_AI_ROLE_QUESTIONS[job.title]
            question = RoleQuestion(
                job_id=application.job_id,
                role_title=job.title,
                label=template_data['label'],
                question=template_data['question'],
                is_template=False,
                is_active=True
            )
            db.session.add(question)
            db.session.flush()
            question_id = question.id
        else:
            return jsonify({"error": "Question ID is required"}), 400

    response = IntelligenceResponse(
        application_id=application_id,
        question_id=question_id,
        response_text=data['response_text']
    )

    db.session.add(response)
    db.session.commit()

    return jsonify(response.to_dict()), 201


# ==================== HIRING INTELLIGENCE SUBMISSIONS ENDPOINTS ====================

@app.route('/api/intelligence-submissions', methods=['GET'])
def get_intelligence_submissions():
    """Get all hiring intelligence submissions"""
    try:
        status = request.args.get('status')

        # Check if table exists first
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        if 'hiring_intelligence_submission' not in inspector.get_table_names():
            print("⚠️  hiring_intelligence_submission table does not exist yet")
            return jsonify({
                'submissions': [],
                'total': 0,
                'message': 'Intelligence submissions table not created yet'
            })

        query = HiringIntelligenceSubmission.query
        if status:
            query = query.filter_by(status=status)

        # Try different ordering strategies based on available columns
        table_columns = [c['name'] for c in inspector.get_columns('hiring_intelligence_submission')]
        print(f"📊 Available columns in hiring_intelligence_submission: {table_columns}")

        if 'created_at' in table_columns:
            print("✅ Ordering by created_at")
            submissions = query.order_by(HiringIntelligenceSubmission.created_at.desc()).all()
        elif 'generated_at' in table_columns:
            print("✅ Ordering by generated_at")
            submissions = query.order_by(HiringIntelligenceSubmission.generated_at.desc()).all()
        else:
            print("✅ Ordering by id (no timestamp columns found)")
            submissions = query.order_by(HiringIntelligenceSubmission.id.desc()).all()

        return jsonify({
            'submissions': [s.to_dict() for s in submissions],
            'total': len(submissions)
        })
    except Exception as e:
        import traceback
        print(f"❌ ERROR in get_intelligence_submissions:")
        print(f"   Error: {str(e)}")
        print(f"   Traceback:\n{traceback.format_exc()}")

        # Return empty list instead of error to prevent UI breakage
        return jsonify({
            'submissions': [],
            'total': 0,
            'error': str(e)
        }), 200  # Return 200 with empty data instead of 500


@app.route('/api/intelligence-submissions/<int:submission_id>', methods=['GET'])
def get_intelligence_submission(submission_id):
    """Get a single hiring intelligence submission"""
    submission = HiringIntelligenceSubmission.query.get_or_404(submission_id)
    return jsonify(submission.to_dict())


@app.route('/api/applications/<int:application_id>/generate-submission', methods=['POST'])
def generate_intelligence_submission(application_id):
    """Generate a Hiring Intelligence Submission for an application"""
    import json

    application = Application.query.get_or_404(application_id)
    candidate = Candidate.query.get(application.candidate_id)
    job = Job.query.get(application.job_id)

    if not candidate or not job:
        return jsonify({"error": "Invalid application"}), 400

    # Get intelligence responses
    responses = IntelligenceResponse.query.filter_by(application_id=application_id).all()

    # Get candidate links
    links = CandidateLink.query.filter_by(candidate_id=candidate.id).all()

    # Compile the submission data
    submission_data = {
        'candidate': {
            'id': candidate.id,
            'name': f"{candidate.first_name} {candidate.last_name}",
            'email': candidate.email,
            'location': candidate.location,
            'github_url': candidate.github_url,
            'portfolio_url': candidate.portfolio_url,
            'linkedin_url': candidate.linkedin_url,
            'primary_expertise': candidate.primary_expertise,
            'skills': candidate.skills,
            'years_experience': candidate.years_experience
        },
        'job': {
            'id': job.id,
            'title': job.title,
            'company': job.company
        },
        'work_links': [link.to_dict() for link in links],
        'intelligence_responses': [response.to_dict() for response in responses],
        'generated_at': datetime.utcnow().isoformat()
    }

    # Check if submission already exists
    existing = HiringIntelligenceSubmission.query.filter_by(application_id=application_id).first()

    if existing:
        existing.submission_data = json.dumps(submission_data)
        existing.status = 'generated'
        existing.generated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(existing.to_dict())

    # Create new submission
    submission = HiringIntelligenceSubmission(
        application_id=application_id,
        submission_data=json.dumps(submission_data),
        status='generated'
    )

    db.session.add(submission)
    db.session.commit()

    return jsonify(submission.to_dict()), 201


@app.route('/api/intelligence-submissions/<int:submission_id>', methods=['PUT'])
def update_intelligence_submission(submission_id):
    """Update a hiring intelligence submission (for recruiter feedback)"""
    submission = HiringIntelligenceSubmission.query.get_or_404(submission_id)
    data = request.get_json()

    for field in ['status', 'missing_signal', 'recruiter_notes',
                  'passed_to_screen', 'passed_to_interview', 'received_offer']:
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
    """
    AI-powered analysis of hiring intelligence submission
    Uses Claude API to extract skills, key phrases, and generate hiring manager assessment
    """
    import json as json_module

    try:
        # Get submission
        submission = HiringIntelligenceSubmission.query.get_or_404(submission_id)
        submission_data = json_module.loads(submission.submission_data) if submission.submission_data else {}

        # Get application and job details
        application = Application.query.get(submission.application_id)
        if not application:
            return jsonify({"error": "Application not found"}), 404

        job = application.job
        candidate = application.candidate

        # Prepare data for AI analysis
        work_links = submission_data.get('work_links', [])
        intelligence_response = submission_data.get('intelligence_response', {})
        position = submission_data.get('position', job.title if job else '')

        # Check for Anthropic API key with detailed debugging
        print("🔍 Checking for ANTHROPIC_API_KEY...")
        print(f"   Environment variables available: {list(os.environ.keys())}")

        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if api_key:
            print(f"✅ ANTHROPIC_API_KEY found (length: {len(api_key)}, starts with: {api_key[:10]}...)")
        else:
            print("❌ ANTHROPIC_API_KEY not found in environment!")
            print(f"   Checking case variations...")
            print(f"   - anthropic_api_key: {os.environ.get('anthropic_api_key', 'NOT FOUND')}")
            print(f"   - Anthropic_API_Key: {os.environ.get('Anthropic_API_Key', 'NOT FOUND')}")
            return jsonify({
                "error": "ANTHROPIC_API_KEY not configured",
                "debug_info": "API key not found in environment variables. Please ensure ANTHROPIC_API_KEY is set in Render environment settings and the service has been restarted."
            }), 500

        # Import Anthropic SDK
        try:
            from anthropic import Anthropic
        except ImportError:
            return jsonify({"error": "Anthropic SDK not installed. Run: pip install anthropic"}), 500

        # Initialize Claude API
        client = Anthropic(api_key=api_key)

        # Build analysis prompt
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
  "extracted_skills": [
    "skill1", "skill2", "skill3", ...
  ],
  "key_phrases": [
    {{
      "phrase": "the exact phrase or concept",
      "context": "why this matters for the role",
      "importance": "high/medium/low"
    }},
    ...
  ],
  "artifact_analysis": [
    {{
      "url": "the artifact URL",
      "type": "github/linkedin/portfolio/paper/project/other",
      "summary": "2-3 sentence summary of what this demonstrates",
      "quality_indicators": "what stands out about quality/depth",
      "relevance": "how relevant to role requirements (high/medium/low)"
    }},
    ...
  ],
  "ai_assessment": {{
    "strengths": [
      "Specific strength 1 with evidence",
      "Specific strength 2 with evidence",
      "Specific strength 3 with evidence"
    ],
    "potential_gaps": [
      "Gap or concern 1",
      "Gap or concern 2"
    ],
    "technical_depth": "Junior/Mid/Senior/Staff - with brief justification",
    "systems_thinking": "Strong/Moderate/Limited - with evidence",
    "recommendation": "STRONG_PASS/PASS/MAYBE/PASS_WITH_CONCERNS - with reasoning",
    "next_steps": "Suggested interview focus areas or screening questions"
  }}
}}

Focus on:
1. Technical skills (languages, frameworks, tools, methodologies)
2. Physical AI-specific expertise (robotics, perception, control, planning, etc.)
3. Systems-level thinking vs pure implementation
4. Evidence of production experience, not just academic
5. Judgment and decision-making patterns revealed in intelligence response
6. Code quality and documentation practices (if GitHub links provided)

Return ONLY the JSON, no additional text."""

        print(f"🤖 Sending analysis request to Claude API for submission {submission_id}...")

        # Call Claude API
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": analysis_prompt
            }]
        )

        # Parse response
        response_text = message.content[0].text
        print(f"✅ Received Claude API response")

        # Extract JSON from response (in case Claude adds any extra text)
        try:
            # Try to find JSON in response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                analysis_result = json_module.loads(json_match.group())
            else:
                analysis_result = json_module.loads(response_text)
        except Exception as parse_error:
            print(f"⚠️  Error parsing Claude response: {str(parse_error)}")
            print(f"   Raw response: {response_text[:500]}...")
            return jsonify({
                "error": "Failed to parse AI analysis response",
                "raw_response": response_text
            }), 500

        # Save analysis to database
        submission.extracted_skills = json_module.dumps(analysis_result.get('extracted_skills', []))
        submission.key_phrases = json_module.dumps(analysis_result.get('key_phrases', []))
        submission.ai_assessment = json_module.dumps(analysis_result.get('ai_assessment', {}))
        submission.artifact_analysis = json_module.dumps(analysis_result.get('artifact_analysis', []))
        submission.ai_analyzed = True
        submission.ai_analyzed_at = datetime.utcnow()

        db.session.commit()

        print(f"✅ AI analysis saved for submission {submission_id}")

        return jsonify({
            "message": "AI analysis completed successfully",
            "submission": submission.to_dict()
        })

    except Exception as e:
        import traceback
        print(f"❌ ERROR in AI analysis:")
        print(f"   Error: {str(e)}")
        print(f"   Traceback:\n{traceback.format_exc()}")
        db.session.rollback()
        return jsonify({"error": f"AI analysis failed: {str(e)}"}), 500


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
    """Submit an application from the public landing page with Hiring Intelligence data"""
    import json as json_module

    try:
        data = request.json

        print(f"\n📤 RECEIVED APPLICATION DATA:")
        print(f"   First Name: {data.get('first_name')}")
        print(f"   Last Name: {data.get('last_name')}")
        print(f"   Email: {data.get('email')}")
        print(f"   Phone: {data.get('phone')}")
        print(f"   Location: {data.get('location')}")
        print(f"   Years Experience: {data.get('years_experience')}")
        print(f"   Primary Expertise: {data.get('primary_expertise')}")
        print(f"   LinkedIn: {data.get('linkedin_url')}")
        print(f"   GitHub: {data.get('github_url')}")
        print(f"   Portfolio: {data.get('portfolio_url')}")
        print(f"   Position: {data.get('position')}")
        print(f"   Hiring Intelligence: {data.get('hiring_intelligence')[:50] if data.get('hiring_intelligence') else 'EMPTY'}...")
        print(f"   Hidden Signal: {data.get('hidden_signal')}")

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
            # Update candidate info if provided - ALWAYS update, even if empty
            candidate.phone = data.get('phone', '')
            candidate.linkedin_url = data.get('linkedin_url', '')
            candidate.github_url = data.get('github_url', '')
            candidate.portfolio_url = data.get('portfolio_url', '')
            candidate.location = data.get('location', '')
            candidate.years_experience = data.get('years_experience')
            candidate.primary_expertise = data.get('primary_expertise', '')
        else:
            # Create new candidate
            candidate = Candidate(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email'),
                phone=data.get('phone', ''),
                location=data.get('location', ''),
                linkedin_url=data.get('linkedin_url', ''),
                github_url=data.get('github_url', ''),
                portfolio_url=data.get('portfolio_url', ''),
                resume_url=data.get('resume_url', ''),
                years_experience=data.get('years_experience'),
                primary_expertise=data.get('primary_expertise', ''),
                status='new'
            )
            db.session.add(candidate)
            try:
                db.session.flush()  # Get candidate ID
                print(f"✅ Candidate flushed successfully - ID will be: {candidate.id}")
            except Exception as e:
                import traceback
                print(f"❌ ERROR FLUSHING CANDIDATE:")
                print(f"   Error: {str(e)}")
                print(f"   Traceback:\n{traceback.format_exc()}")
                db.session.rollback()
                return jsonify({"error": f"Failed to create candidate: {str(e)}"}), 500

        # Process work artifact links (Hiring Intelligence)
        work_links = data.get('work_links', [])
        print(f"📦 Received {len(work_links)} work links")

        # Check if candidate_link table exists before trying to use it
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        table_exists = 'candidate_link' in inspector.get_table_names()

        if not table_exists:
            print("⚠️  candidate_link table does not exist yet - skipping work links")
            print("   Work links will be available after database migration")
        elif len(work_links) > 0:
            for i, link in enumerate(work_links):
                print(f"   Link {i+1}: type={link.get('link_type')}, url={link.get('url')[:50] if link.get('url') else 'EMPTY'}, title={link.get('title', 'N/A')}")

            try:
                links_added = 0
                for link_data in work_links:
                    # Validate link has both URL and type, and URL is not empty
                    url = link_data.get('url', '').strip()
                    link_type = link_data.get('link_type', '').strip()

                    if not url or not link_type:
                        print(f"⚠️  Skipping invalid link: url='{url}', type='{link_type}'")
                        continue

                    if len(url) > 500:
                        print(f"⚠️  URL too long ({len(url)} chars), truncating to 500")
                        url = url[:500]

                    link = CandidateLink(
                        candidate_id=candidate.id,
                        link_type=link_type,
                        url=url,
                        title=link_data.get('title', '')[:300] if link_data.get('title') else None
                    )
                    db.session.add(link)
                    links_added += 1

                if links_added > 0:
                    print(f"✅ Added {links_added} work artifact links")
                else:
                    print(f"ℹ️  No valid work links to add")
            except Exception as e:
                import traceback
                print(f"⚠️  Error saving work links: {str(e)}")
                print(f"   Traceback:\n{traceback.format_exc()}")
                # Roll back the bad objects to prevent tainting the session
                db.session.rollback()
                # Re-add the candidate since we rolled back
                if candidate.id is None:
                    db.session.add(candidate)
                    db.session.flush()
                print("   Continuing without work links...")
        else:
            print("ℹ️  No work links provided")

        # Create application (store position, hiring intelligence + hidden signal)
        application = Application(
            candidate_id=candidate.id,
            job_id=job_id,
            status='applied',
            source='hiring_intelligence',
            position=data.get('position', ''),
            hiring_intelligence=data.get('hiring_intelligence', ''),
            hidden_signal=data.get('hidden_signal', ''),
            notes=data.get('cover_letter', '')
        )
        db.session.add(application)
        db.session.flush()  # Get application ID

        # Process intelligence response (Hiring Intelligence)
        intelligence_response = data.get('intelligence_response')
        if intelligence_response and intelligence_response.get('response_text'):
            # Check if intelligence tables exist
            intelligence_tables_exist = (
                'role_question' in inspector.get_table_names() and
                'intelligence_response' in inspector.get_table_names() and
                'hiring_intelligence_submission' in inspector.get_table_names()
            )

            if not intelligence_tables_exist:
                print("⚠️  Hiring intelligence tables do not exist yet - skipping intelligence data")
                print("   Intelligence data stored in Application.hiring_intelligence field as fallback")
            else:
                try:
                    # Get or create the question
                    question_id = intelligence_response.get('question_id')

                    if not question_id and job.title in PHYSICAL_AI_ROLE_QUESTIONS:
                        # Create question from template
                        template_data = PHYSICAL_AI_ROLE_QUESTIONS[job.title]
                        question = RoleQuestion(
                            job_id=job_id,
                            role_title=job.title,
                            label=template_data['label'],
                            question=template_data['question'],
                            is_template=False,
                            is_active=True
                        )
                        db.session.add(question)
                        db.session.flush()
                        question_id = question.id
                        print(f"✅ Created RoleQuestion for {job.title}")

                    if question_id:
                        response = IntelligenceResponse(
                            application_id=application.id,
                            question_id=question_id,
                            response_text=intelligence_response['response_text']
                        )
                        db.session.add(response)
                        print(f"✅ Added IntelligenceResponse")

                        # Auto-generate Hiring Intelligence Submission
                        submission_data = {
                            'candidate_name': f"{candidate.first_name} {candidate.last_name}",
                            'candidate_email': candidate.email,
                            'position': data.get('position', job.title),
                            'hidden_signal': data.get('hidden_signal', ''),
                            'work_links': [{'link_type': l.get('link_type'), 'url': l.get('url'), 'title': l.get('title')} for l in work_links],
                            'intelligence_response': {
                                'question_label': PHYSICAL_AI_ROLE_QUESTIONS.get(job.title, {}).get('label', 'Custom Question'),
                                'question_text': PHYSICAL_AI_ROLE_QUESTIONS.get(job.title, {}).get('question', ''),
                                'response_text': intelligence_response['response_text']
                            },
                            'generated_at': datetime.utcnow().isoformat()
                        }

                        submission = HiringIntelligenceSubmission(
                            application_id=application.id,
                            submission_data=json_module.dumps(submission_data),
                            status='pending'
                        )
                        db.session.add(submission)
                        print(f"✅ Created HiringIntelligenceSubmission")
                except Exception as e:
                    import traceback
                    print(f"⚠️  Error saving intelligence data: {str(e)}")
                    print(f"   Traceback:\n{traceback.format_exc()}")
                    # Roll back to prevent session tainting
                    db.session.rollback()
                    # Re-add what we need
                    if candidate.id is None:
                        db.session.add(candidate)
                        db.session.flush()
                    db.session.add(application)
                    db.session.flush()
                    print("   Continuing without intelligence data...")

        # Commit the transaction
        print(f"🔄 Attempting to commit (Candidate ID: {candidate.id}, Application: {application.id})...")
        db.session.commit()
        print(f"✅ COMMIT SUCCEEDED")

        # VERIFY DATA WAS ACTUALLY SAVED
        print(f"🔍 VERIFYING DATA IN DATABASE...")

        # Check if candidate exists
        verify_candidate = Candidate.query.get(candidate.id)
        if verify_candidate:
            print(f"   ✅ Candidate {candidate.id} verified in database: {verify_candidate.first_name} {verify_candidate.last_name}")
        else:
            print(f"   ❌ CANDIDATE {candidate.id} NOT FOUND IN DATABASE!")

        # Check if application exists
        verify_app = Application.query.get(application.id)
        if verify_app:
            print(f"   ✅ Application {application.id} verified in database")
            print(f"      Hiring Intelligence: {verify_app.hiring_intelligence[:50] if verify_app.hiring_intelligence else 'EMPTY'}...")
        else:
            print(f"   ❌ APPLICATION {application.id} NOT FOUND IN DATABASE!")

        return jsonify({
            "message": "Hiring Intelligence Submission received successfully!",
            "application_id": application.id,
            "candidate_id": candidate.id,
            "has_intelligence_data": bool(intelligence_response)
        }), 201
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ ERROR IN /api/public/apply:")
        print(f"   Error Type: {type(e).__name__}")
        print(f"   Error Message: {str(e)}")
        print(f"   Full Traceback:\n{error_trace}")
        db.session.rollback()
        return jsonify({"error": f"{type(e).__name__}: {str(e)}"}), 500


@app.route('/api/public/jobs/<int:job_id>/question', methods=['GET'])
def get_public_job_question(job_id):
    """Get the intelligence question for a public job application"""
    try:
        job = Job.query.get_or_404(job_id)

        # Only show for open jobs
        if job.status != 'open':
            return jsonify({"error": "This position is no longer accepting applications"}), 404

        # Check for job-specific question
        try:
            question = RoleQuestion.query.filter_by(job_id=job_id, is_active=True).first()
        except Exception as db_error:
            print(f"⚠️  RoleQuestion table may not exist yet: {str(db_error)}")
            question = None

        # If no job-specific, look for template
        if not question:
            try:
                question = RoleQuestion.query.filter_by(
                    role_title=job.title,
                    is_template=True,
                    is_active=True
                ).first()
            except Exception as db_error:
                print(f"⚠️  RoleQuestion template query failed: {str(db_error)}")
                question = None

        # If still none, check built-in templates
        if not question and job.title in PHYSICAL_AI_ROLE_QUESTIONS:
            template = PHYSICAL_AI_ROLE_QUESTIONS[job.title]
            print(f"✅ Using built-in template for {job.title}")
            return jsonify({
                'question_id': None,
                'role_title': job.title,
                'label': template['label'],
                'question': template['question'],
                'source': 'built_in'
            })

        if question:
            return jsonify({
                'question_id': question.id,
                'role_title': question.role_title,
                'label': question.label,
                'question': question.question,
                'source': 'database'
            })

        # No question available for this role
        print(f"⚠️  No intelligence question found for job {job_id} ({job.title})")
        return jsonify({
            'message': 'No intelligence question configured for this role',
            'question': None
        })
    except Exception as e:
        import traceback
        print(f"❌ ERROR in get_public_job_question:")
        print(f"   Job ID: {job_id}")
        print(f"   Error: {str(e)}")
        print(f"   Traceback:\n{traceback.format_exc()}")
        return jsonify({"error": f"Failed to fetch intelligence question: {str(e)}"}), 500


# ==================== DATABASE INITIALIZATION ====================
# IMPORTANT: Must be AFTER all model definitions so SQLAlchemy knows about them
print("🔧 Initializing database tables...")
with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
