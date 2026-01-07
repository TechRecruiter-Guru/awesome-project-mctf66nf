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


# ==================== INSTITUTIONAL MEMORY MODELS (AI COMPLIANCE) ====================

class AISystemRecord(db.Model):
    """
    Immutable record of AI systems used in hiring.
    Purpose: Proves where and how AI touched hiring decisions.
    """
    __tablename__ = 'ai_system_record'

    id = db.Column(db.Integer, primary_key=True)
    ai_system_id = db.Column(db.String(100), unique=True, nullable=False)

    # System Details
    system_name = db.Column(db.String(200), nullable=False)
    vendor_name = db.Column(db.String(200))
    system_type = db.Column(db.String(100))  # screening, ranking, interview_analysis, assessment
    decision_influence = db.Column(db.String(50))  # assistive, determinative, hybrid
    data_inputs = db.Column(db.Text)  # JSON: resume text, video, assessment scores
    human_override_points = db.Column(db.Text)  # yes/no + description
    intended_use_statement = db.Column(db.Text)  # Critical for defensibility

    # Lifecycle
    deployment_date = db.Column(db.DateTime, nullable=False)
    retirement_date = db.Column(db.DateTime)

    # Immutability Fields
    created_by = db.Column(db.String(200))
    created_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    version = db.Column(db.Integer, default=1)

    # Relationships
    disclosures = db.relationship('DisclosureArtifact', backref='ai_system', lazy=True)
    decision_events = db.relationship('HiringDecisionEvent', backref='ai_system', lazy=True)
    governance_approvals = db.relationship('GovernanceApprovalRecord', backref='ai_system', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'ai_system_id': self.ai_system_id,
            'system_name': self.system_name,
            'vendor_name': self.vendor_name,
            'system_type': self.system_type,
            'decision_influence': self.decision_influence,
            'data_inputs': self.data_inputs,
            'human_override_points': self.human_override_points,
            'intended_use_statement': self.intended_use_statement,
            'deployment_date': self.deployment_date.isoformat() if self.deployment_date else None,
            'retirement_date': self.retirement_date.isoformat() if self.retirement_date else None,
            'created_by': self.created_by,
            'created_timestamp': self.created_timestamp.isoformat(),
            'version': self.version,
            'disclosure_count': len(self.disclosures) if self.disclosures else 0,
            'decision_event_count': len(self.decision_events) if self.decision_events else 0
        }


class RegulatoryContextSnapshot(db.Model):
    """
    Immutable snapshot of regulatory context at a point in time.
    Purpose: Freezes the legal environment to prevent retroactive compliance reinterpretation.
    """
    __tablename__ = 'regulatory_context_snapshot'

    id = db.Column(db.Integer, primary_key=True)
    reg_context_id = db.Column(db.String(100), unique=True, nullable=False)

    # Regulation Details
    jurisdiction = db.Column(db.String(100), nullable=False)  # state, city
    regulation_name = db.Column(db.String(200), nullable=False)
    regulation_version = db.Column(db.String(50))
    effective_start_date = db.Column(db.Date, nullable=False)
    effective_end_date = db.Column(db.Date)

    # Compliance Rules
    compliance_obligations = db.Column(db.Text)  # JSON: structured ruleset
    source_reference = db.Column(db.String(500))  # URL or citation

    # Immutability Fields
    ingested_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    disclosures = db.relationship('DisclosureArtifact', backref='regulatory_context', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'reg_context_id': self.reg_context_id,
            'jurisdiction': self.jurisdiction,
            'regulation_name': self.regulation_name,
            'regulation_version': self.regulation_version,
            'effective_start_date': self.effective_start_date.isoformat() if self.effective_start_date else None,
            'effective_end_date': self.effective_end_date.isoformat() if self.effective_end_date else None,
            'compliance_obligations': self.compliance_obligations,
            'source_reference': self.source_reference,
            'ingested_timestamp': self.ingested_timestamp.isoformat(),
            'disclosure_count': len(self.disclosures) if self.disclosures else 0
        }


class DisclosureArtifact(db.Model):
    """
    Immutable record of AI disclosures to candidates.
    Purpose: Proves what was disclosed, to whom, when, and why.
    """
    __tablename__ = 'disclosure_artifact'

    id = db.Column(db.Integer, primary_key=True)
    disclosure_id = db.Column(db.String(100), unique=True, nullable=False)

    # References
    ai_system_record_id = db.Column(db.Integer, db.ForeignKey('ai_system_record.id'), nullable=False)
    reg_context_id = db.Column(db.Integer, db.ForeignKey('regulatory_context_snapshot.id'), nullable=False)
    candidate_id_hash = db.Column(db.String(200), nullable=False)  # Hashed for privacy
    role_id = db.Column(db.Integer, db.ForeignKey('job.id'))

    # Disclosure Details
    hiring_stage = db.Column(db.String(100))  # screening, interview, offer
    disclosure_text_rendered = db.Column(db.Text, nullable=False)  # Verbatim text shown
    delivery_method = db.Column(db.String(100))  # ATS, email, portal
    delivery_timestamp = db.Column(db.DateTime, nullable=False)
    acknowledgment_status = db.Column(db.String(50))  # acknowledged, pending, not_required
    language_locale = db.Column(db.String(10))  # en-US, es-MX, etc.

    # Immutability Fields
    created_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'disclosure_id': self.disclosure_id,
            'ai_system_record_id': self.ai_system_record_id,
            'reg_context_id': self.reg_context_id,
            'candidate_id_hash': self.candidate_id_hash,
            'role_id': self.role_id,
            'hiring_stage': self.hiring_stage,
            'disclosure_text_rendered': self.disclosure_text_rendered,
            'delivery_method': self.delivery_method,
            'delivery_timestamp': self.delivery_timestamp.isoformat(),
            'acknowledgment_status': self.acknowledgment_status,
            'language_locale': self.language_locale,
            'created_timestamp': self.created_timestamp.isoformat()
        }


class HiringDecisionEvent(db.Model):
    """
    Immutable record linking AI use to employment outcomes.
    Purpose: Anchors AI influence to human accountability.
    """
    __tablename__ = 'hiring_decision_event'

    id = db.Column(db.Integer, primary_key=True)
    decision_event_id = db.Column(db.String(100), unique=True, nullable=False)

    # References
    candidate_id_hash = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    ai_system_record_id = db.Column(db.Integer, db.ForeignKey('ai_system_record.id'))

    # Decision Details
    decision_type = db.Column(db.String(50), nullable=False)  # advance, reject, score
    human_involvement_level = db.Column(db.String(100))  # full_review, override, approved_ai_recommendation
    final_decision_maker_role = db.Column(db.String(100))  # recruiter, hiring_manager, system
    decision_timestamp = db.Column(db.DateTime, nullable=False)

    # Immutability Fields
    created_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    rationales = db.relationship('DecisionRationaleLog', backref='decision_event', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'decision_event_id': self.decision_event_id,
            'candidate_id_hash': self.candidate_id_hash,
            'role_id': self.role_id,
            'ai_system_record_id': self.ai_system_record_id,
            'decision_type': self.decision_type,
            'human_involvement_level': self.human_involvement_level,
            'final_decision_maker_role': self.final_decision_maker_role,
            'decision_timestamp': self.decision_timestamp.isoformat(),
            'created_timestamp': self.created_timestamp.isoformat(),
            'rationale_count': len(self.rationales) if self.rationales else 0
        }


class DecisionRationaleLog(db.Model):
    """
    Immutable log of WHY decisions were made.
    Purpose: Most overlooked, most valuable - demonstrates human judgment.
    """
    __tablename__ = 'decision_rationale_log'

    id = db.Column(db.Integer, primary_key=True)
    rationale_id = db.Column(db.String(100), unique=True, nullable=False)

    # Reference
    decision_event_id = db.Column(db.Integer, db.ForeignKey('hiring_decision_event.id'), nullable=False)

    # Rationale Details
    rationale_type = db.Column(db.String(100))  # policy, performance, qualification, override
    rationale_summary = db.Column(db.Text, nullable=False)  # Plain language explanation
    supporting_artifacts = db.Column(db.Text)  # JSON: IDs of supporting docs, not files

    # Immutability Fields
    entered_by = db.Column(db.String(200))
    entered_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'rationale_id': self.rationale_id,
            'decision_event_id': self.decision_event_id,
            'rationale_type': self.rationale_type,
            'rationale_summary': self.rationale_summary,
            'supporting_artifacts': self.supporting_artifacts,
            'entered_by': self.entered_by,
            'entered_timestamp': self.entered_timestamp.isoformat()
        }


class GovernanceApprovalRecord(db.Model):
    """
    Immutable record of governance oversight.
    Purpose: Proves oversight existed before issues arose.
    """
    __tablename__ = 'governance_approval_record'

    id = db.Column(db.Integer, primary_key=True)
    approval_id = db.Column(db.String(100), unique=True, nullable=False)

    # Reference
    ai_system_record_id = db.Column(db.Integer, db.ForeignKey('ai_system_record.id'), nullable=False)

    # Approval Details
    approval_type = db.Column(db.String(100), nullable=False)  # legal, HR, security, ethics
    approver_role = db.Column(db.String(200), nullable=False)  # General Counsel, CHRO, etc.
    approval_decision = db.Column(db.String(50), nullable=False)  # approved, conditional, denied
    conditions_or_exceptions = db.Column(db.Text)  # Any conditions attached

    # Immutability Fields
    approval_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'approval_id': self.approval_id,
            'ai_system_record_id': self.ai_system_record_id,
            'approval_type': self.approval_type,
            'approver_role': self.approver_role,
            'approval_decision': self.approval_decision,
            'conditions_or_exceptions': self.conditions_or_exceptions,
            'approval_timestamp': self.approval_timestamp.isoformat()
        }


class VendorAssertionRecord(db.Model):
    """
    Immutable record of vendor claims and evidence.
    Purpose: Documents what vendors claimed - and what they didn't.
    """
    __tablename__ = 'vendor_assertion_record'

    id = db.Column(db.Integer, primary_key=True)
    vendor_assertion_id = db.Column(db.String(100), unique=True, nullable=False)

    # Reference
    ai_system_record_id = db.Column(db.Integer, db.ForeignKey('ai_system_record.id'), nullable=False)

    # Assertion Details
    assertion_type = db.Column(db.String(100), nullable=False)  # bias_testing, data_sourcing, accuracy
    assertion_statement = db.Column(db.Text, nullable=False)  # What vendor claimed
    evidence_provided = db.Column(db.Boolean, default=False)  # yes/no
    risk_flag = db.Column(db.String(20))  # green, amber, red

    # Immutability Fields
    recorded_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Foreign Key for AI System
    ai_system = db.relationship('AISystemRecord', backref='vendor_assertions', foreign_keys=[ai_system_record_id])

    def to_dict(self):
        return {
            'id': self.id,
            'vendor_assertion_id': self.vendor_assertion_id,
            'ai_system_record_id': self.ai_system_record_id,
            'assertion_type': self.assertion_type,
            'assertion_statement': self.assertion_statement,
            'evidence_provided': self.evidence_provided,
            'risk_flag': self.risk_flag,
            'recorded_timestamp': self.recorded_timestamp.isoformat()
        }


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


# ==================== INSTITUTIONAL MEMORY API ENDPOINTS ====================

# ==================== AI SYSTEM REGISTRY ====================

@app.route('/api/ai-systems', methods=['POST'])
def create_ai_system():
    """Register new AI system used in hiring"""
    data = request.get_json()

    if not data or 'system_name' not in data or 'ai_system_id' not in data:
        return jsonify({"error": "system_name and ai_system_id are required"}), 400

    # Check if AI system already exists
    existing = AISystemRecord.query.filter_by(ai_system_id=data['ai_system_id']).first()
    if existing:
        return jsonify({"error": "AI system with this ID already exists"}), 409

    try:
        deployment_date = datetime.fromisoformat(data['deployment_date'].replace('Z', '+00:00')) if data.get('deployment_date') else datetime.utcnow()
    except:
        deployment_date = datetime.utcnow()

    ai_system = AISystemRecord(
        ai_system_id=data['ai_system_id'],
        system_name=data['system_name'],
        vendor_name=data.get('vendor_name'),
        system_type=data.get('system_type'),
        decision_influence=data.get('decision_influence'),
        data_inputs=data.get('data_inputs'),
        human_override_points=data.get('human_override_points'),
        intended_use_statement=data.get('intended_use_statement'),
        deployment_date=deployment_date,
        created_by=data.get('created_by', 'system'),
        version=1
    )

    db.session.add(ai_system)
    db.session.commit()

    return jsonify(ai_system.to_dict()), 201


@app.route('/api/ai-systems', methods=['GET'])
def get_ai_systems():
    """Get all AI systems"""
    systems = AISystemRecord.query.order_by(AISystemRecord.created_timestamp.desc()).all()
    return jsonify({
        'ai_systems': [s.to_dict() for s in systems],
        'total': len(systems)
    })


@app.route('/api/ai-systems/<string:ai_system_id>', methods=['GET'])
def get_ai_system(ai_system_id):
    """Get specific AI system by ID"""
    system = AISystemRecord.query.filter_by(ai_system_id=ai_system_id).first_or_404()
    data = system.to_dict()

    # Include related records
    data['disclosures'] = [d.to_dict() for d in system.disclosures]
    data['decision_events'] = [e.to_dict() for e in system.decision_events]
    data['governance_approvals'] = [g.to_dict() for g in system.governance_approvals]

    return jsonify(data)


@app.route('/api/ai-systems/<int:system_id>/retire', methods=['POST'])
def retire_ai_system(system_id):
    """Mark AI system as retired (immutable - creates new version)"""
    system = AISystemRecord.query.get_or_404(system_id)

    if system.retirement_date:
        return jsonify({"error": "System already retired"}), 400

    system.retirement_date = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "message": f"AI system {system.system_name} retired successfully",
        "system": system.to_dict()
    })


# ==================== REGULATORY CONTEXT SNAPSHOT ====================

@app.route('/api/regulatory-contexts', methods=['POST'])
def create_regulatory_context():
    """Create regulatory context snapshot"""
    data = request.get_json()

    required_fields = ['reg_context_id', 'jurisdiction', 'regulation_name', 'effective_start_date']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing required fields: {required_fields}"}), 400

    try:
        effective_start = datetime.strptime(data['effective_start_date'], '%Y-%m-%d').date()
        effective_end = datetime.strptime(data['effective_end_date'], '%Y-%m-%d').date() if data.get('effective_end_date') else None
    except:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    reg_context = RegulatoryContextSnapshot(
        reg_context_id=data['reg_context_id'],
        jurisdiction=data['jurisdiction'],
        regulation_name=data['regulation_name'],
        regulation_version=data.get('regulation_version'),
        effective_start_date=effective_start,
        effective_end_date=effective_end,
        compliance_obligations=data.get('compliance_obligations'),
        source_reference=data.get('source_reference')
    )

    db.session.add(reg_context)
    db.session.commit()

    return jsonify(reg_context.to_dict()), 201


@app.route('/api/regulatory-contexts', methods=['GET'])
def get_regulatory_contexts():
    """Get all regulatory context snapshots"""
    jurisdiction = request.args.get('jurisdiction')
    date_str = request.args.get('date')

    query = RegulatoryContextSnapshot.query

    if jurisdiction:
        query = query.filter_by(jurisdiction=jurisdiction)

    if date_str:
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            query = query.filter(
                RegulatoryContextSnapshot.effective_start_date <= target_date,
                db.or_(
                    RegulatoryContextSnapshot.effective_end_date.is_(None),
                    RegulatoryContextSnapshot.effective_end_date >= target_date
                )
            )
        except:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    contexts = query.order_by(RegulatoryContextSnapshot.ingested_timestamp.desc()).all()
    return jsonify({
        'regulatory_contexts': [c.to_dict() for c in contexts],
        'total': len(contexts)
    })


@app.route('/api/regulatory-contexts/<string:reg_context_id>', methods=['GET'])
def get_regulatory_context(reg_context_id):
    """Get specific regulatory context"""
    context = RegulatoryContextSnapshot.query.filter_by(reg_context_id=reg_context_id).first_or_404()
    return jsonify(context.to_dict())


# ==================== DISCLOSURE MEMORY ====================

@app.route('/api/disclosures/render', methods=['POST'])
def render_disclosure():
    """Render disclosure text based on AI system and regulatory context"""
    data = request.get_json()

    required_fields = ['ai_system_id', 'reg_context_id', 'candidate_id', 'role_id', 'hiring_stage']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing required fields: {required_fields}"}), 400

    # Resolve AI system and regulatory context
    ai_system = AISystemRecord.query.filter_by(ai_system_id=data['ai_system_id']).first()
    reg_context = RegulatoryContextSnapshot.query.filter_by(reg_context_id=data['reg_context_id']).first()

    if not ai_system or not reg_context:
        return jsonify({"error": "AI system or regulatory context not found"}), 404

    # Generate disclosure text (simplified - in production, use template engine)
    disclosure_text = f"""
AI Hiring Disclosure

As required by {reg_context.regulation_name} ({reg_context.jurisdiction}), we inform you that:

We are using AI technology in our hiring process for this position.

AI System: {ai_system.system_name}
Vendor: {ai_system.vendor_name or 'Internal'}
Purpose: {ai_system.system_type}
Decision Role: {ai_system.decision_influence}
Stage: {data['hiring_stage']}

{ai_system.intended_use_statement or ''}

Human reviewers are involved in all final decisions.

If you have questions about this use of AI, please contact our HR team.
    """.strip()

    return jsonify({
        "disclosure_text": disclosure_text,
        "ai_system_name": ai_system.system_name,
        "regulation": reg_context.regulation_name,
        "jurisdiction": reg_context.jurisdiction
    })


@app.route('/api/disclosures/deliver', methods=['POST'])
def deliver_disclosure():
    """Record disclosure delivery to candidate"""
    data = request.get_json()

    required_fields = ['disclosure_id', 'ai_system_id', 'reg_context_id', 'candidate_id_hash', 'disclosure_text']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing required fields: {required_fields}"}), 400

    # Get AI system and regulatory context IDs
    ai_system = AISystemRecord.query.filter_by(ai_system_id=data['ai_system_id']).first()
    reg_context = RegulatoryContextSnapshot.query.filter_by(reg_context_id=data['reg_context_id']).first()

    if not ai_system or not reg_context:
        return jsonify({"error": "AI system or regulatory context not found"}), 404

    disclosure = DisclosureArtifact(
        disclosure_id=data['disclosure_id'],
        ai_system_record_id=ai_system.id,
        reg_context_id=reg_context.id,
        candidate_id_hash=data['candidate_id_hash'],
        role_id=data.get('role_id'),
        hiring_stage=data.get('hiring_stage'),
        disclosure_text_rendered=data['disclosure_text'],
        delivery_method=data.get('delivery_method', 'ATS'),
        delivery_timestamp=datetime.utcnow(),
        acknowledgment_status=data.get('acknowledgment_status', 'pending'),
        language_locale=data.get('language_locale', 'en-US')
    )

    db.session.add(disclosure)
    db.session.commit()

    return jsonify(disclosure.to_dict()), 201


@app.route('/api/disclosures/<string:disclosure_id>', methods=['GET'])
def get_disclosure(disclosure_id):
    """Get specific disclosure"""
    disclosure = DisclosureArtifact.query.filter_by(disclosure_id=disclosure_id).first_or_404()
    return jsonify(disclosure.to_dict())


@app.route('/api/disclosures', methods=['GET'])
def get_disclosures():
    """Get all disclosures"""
    candidate_hash = request.args.get('candidate_id_hash')
    role_id = request.args.get('role_id')

    query = DisclosureArtifact.query

    if candidate_hash:
        query = query.filter_by(candidate_id_hash=candidate_hash)
    if role_id:
        query = query.filter_by(role_id=role_id)

    disclosures = query.order_by(DisclosureArtifact.delivery_timestamp.desc()).all()
    return jsonify({
        'disclosures': [d.to_dict() for d in disclosures],
        'total': len(disclosures)
    })


# ==================== HIRING DECISION EVENT ====================

@app.route('/api/hiring-decisions', methods=['POST'])
def create_hiring_decision():
    """Record hiring decision event"""
    data = request.get_json()

    required_fields = ['decision_event_id', 'candidate_id_hash', 'decision_type']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing required fields: {required_fields}"}), 400

    # Get AI system if specified
    ai_system_id = None
    if data.get('ai_system_id'):
        ai_system = AISystemRecord.query.filter_by(ai_system_id=data['ai_system_id']).first()
        if ai_system:
            ai_system_id = ai_system.id

    try:
        decision_timestamp = datetime.fromisoformat(data['decision_timestamp'].replace('Z', '+00:00')) if data.get('decision_timestamp') else datetime.utcnow()
    except:
        decision_timestamp = datetime.utcnow()

    decision = HiringDecisionEvent(
        decision_event_id=data['decision_event_id'],
        candidate_id_hash=data['candidate_id_hash'],
        role_id=data.get('role_id'),
        ai_system_record_id=ai_system_id,
        decision_type=data['decision_type'],
        human_involvement_level=data.get('human_involvement_level'),
        final_decision_maker_role=data.get('final_decision_maker_role'),
        decision_timestamp=decision_timestamp
    )

    db.session.add(decision)
    db.session.commit()

    return jsonify(decision.to_dict()), 201


@app.route('/api/hiring-decisions/<string:decision_event_id>', methods=['GET'])
def get_hiring_decision(decision_event_id):
    """Get specific hiring decision"""
    decision = HiringDecisionEvent.query.filter_by(decision_event_id=decision_event_id).first_or_404()
    data = decision.to_dict()
    data['rationales'] = [r.to_dict() for r in decision.rationales]
    return jsonify(data)


@app.route('/api/hiring-decisions', methods=['GET'])
def get_hiring_decisions():
    """Get all hiring decisions"""
    candidate_hash = request.args.get('candidate_id_hash')
    role_id = request.args.get('role_id')
    decision_type = request.args.get('decision_type')

    query = HiringDecisionEvent.query

    if candidate_hash:
        query = query.filter_by(candidate_id_hash=candidate_hash)
    if role_id:
        query = query.filter_by(role_id=role_id)
    if decision_type:
        query = query.filter_by(decision_type=decision_type)

    decisions = query.order_by(HiringDecisionEvent.decision_timestamp.desc()).all()
    return jsonify({
        'hiring_decisions': [d.to_dict() for d in decisions],
        'total': len(decisions)
    })


# ==================== DECISION RATIONALE LOG ====================

@app.route('/api/decision-rationales', methods=['POST'])
def create_decision_rationale():
    """Log decision rationale"""
    data = request.get_json()

    required_fields = ['rationale_id', 'decision_event_id', 'rationale_summary']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing required fields: {required_fields}"}), 400

    # Find decision event
    decision = HiringDecisionEvent.query.get(data['decision_event_id'])
    if not decision:
        return jsonify({"error": "Decision event not found"}), 404

    rationale = DecisionRationaleLog(
        rationale_id=data['rationale_id'],
        decision_event_id=data['decision_event_id'],
        rationale_type=data.get('rationale_type'),
        rationale_summary=data['rationale_summary'],
        supporting_artifacts=data.get('supporting_artifacts'),
        entered_by=data.get('entered_by', 'system')
    )

    db.session.add(rationale)
    db.session.commit()

    return jsonify(rationale.to_dict()), 201


@app.route('/api/decision-rationales/<int:decision_event_id>', methods=['GET'])
def get_decision_rationales(decision_event_id):
    """Get rationales for specific decision event"""
    rationales = DecisionRationaleLog.query.filter_by(decision_event_id=decision_event_id).all()
    return jsonify({
        'rationales': [r.to_dict() for r in rationales],
        'total': len(rationales)
    })


# ==================== GOVERNANCE & APPROVAL ====================

@app.route('/api/governance-approvals', methods=['POST'])
def create_governance_approval():
    """Record governance approval"""
    data = request.get_json()

    required_fields = ['approval_id', 'ai_system_id', 'approval_type', 'approver_role', 'approval_decision']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing required fields: {required_fields}"}), 400

    # Get AI system
    ai_system = AISystemRecord.query.filter_by(ai_system_id=data['ai_system_id']).first()
    if not ai_system:
        return jsonify({"error": "AI system not found"}), 404

    approval = GovernanceApprovalRecord(
        approval_id=data['approval_id'],
        ai_system_record_id=ai_system.id,
        approval_type=data['approval_type'],
        approver_role=data['approver_role'],
        approval_decision=data['approval_decision'],
        conditions_or_exceptions=data.get('conditions_or_exceptions')
    )

    db.session.add(approval)
    db.session.commit()

    return jsonify(approval.to_dict()), 201


@app.route('/api/governance-approvals', methods=['GET'])
def get_governance_approvals():
    """Get all governance approvals"""
    ai_system_id = request.args.get('ai_system_id')

    query = GovernanceApprovalRecord.query

    if ai_system_id:
        ai_system = AISystemRecord.query.filter_by(ai_system_id=ai_system_id).first()
        if ai_system:
            query = query.filter_by(ai_system_record_id=ai_system.id)

    approvals = query.order_by(GovernanceApprovalRecord.approval_timestamp.desc()).all()
    return jsonify({
        'governance_approvals': [a.to_dict() for a in approvals],
        'total': len(approvals)
    })


# ==================== VENDOR ASSERTION RECORD ====================

@app.route('/api/vendor-assertions', methods=['POST'])
def create_vendor_assertion():
    """Record vendor assertion"""
    data = request.get_json()

    required_fields = ['vendor_assertion_id', 'ai_system_id', 'assertion_type', 'assertion_statement']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing required fields: {required_fields}"}), 400

    # Get AI system
    ai_system = AISystemRecord.query.filter_by(ai_system_id=data['ai_system_id']).first()
    if not ai_system:
        return jsonify({"error": "AI system not found"}), 404

    assertion = VendorAssertionRecord(
        vendor_assertion_id=data['vendor_assertion_id'],
        ai_system_record_id=ai_system.id,
        assertion_type=data['assertion_type'],
        assertion_statement=data['assertion_statement'],
        evidence_provided=data.get('evidence_provided', False),
        risk_flag=data.get('risk_flag', 'green')
    )

    db.session.add(assertion)
    db.session.commit()

    return jsonify(assertion.to_dict()), 201


@app.route('/api/vendor-assertions', methods=['GET'])
def get_vendor_assertions():
    """Get all vendor assertions"""
    ai_system_id = request.args.get('ai_system_id')

    query = VendorAssertionRecord.query

    if ai_system_id:
        ai_system = AISystemRecord.query.filter_by(ai_system_id=ai_system_id).first()
        if ai_system:
            query = query.filter_by(ai_system_record_id=ai_system.id)

    assertions = query.order_by(VendorAssertionRecord.recorded_timestamp.desc()).all()
    return jsonify({
        'vendor_assertions': [a.to_dict() for a in assertions],
        'total': len(assertions)
    })


# ==================== AUDIT EVIDENCE EXPORT ====================

@app.route('/api/audit-packs/generate', methods=['POST'])
def generate_audit_pack():
    """Generate comprehensive audit evidence bundle"""
    data = request.get_json()

    # Filters
    jurisdiction = data.get('jurisdiction')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    ai_system_id = data.get('ai_system_id')
    role_id = data.get('role_id')

    audit_pack = {
        'generated_at': datetime.utcnow().isoformat(),
        'filters': {
            'jurisdiction': jurisdiction,
            'date_range': f"{start_date} to {end_date}" if start_date and end_date else 'all',
            'ai_system_id': ai_system_id,
            'role_id': role_id
        },
        'evidence': {}
    }

    # AI Systems
    ai_systems_query = AISystemRecord.query
    if ai_system_id:
        ai_systems_query = ai_systems_query.filter_by(ai_system_id=ai_system_id)
    audit_pack['evidence']['ai_systems'] = [s.to_dict() for s in ai_systems_query.all()]

    # Regulatory Contexts
    reg_contexts_query = RegulatoryContextSnapshot.query
    if jurisdiction:
        reg_contexts_query = reg_contexts_query.filter_by(jurisdiction=jurisdiction)
    audit_pack['evidence']['regulatory_contexts'] = [c.to_dict() for c in reg_contexts_query.all()]

    # Disclosures
    disclosures_query = DisclosureArtifact.query
    if role_id:
        disclosures_query = disclosures_query.filter_by(role_id=role_id)
    if start_date and end_date:
        try:
            start = datetime.fromisoformat(start_date)
            end = datetime.fromisoformat(end_date)
            disclosures_query = disclosures_query.filter(
                DisclosureArtifact.delivery_timestamp >= start,
                DisclosureArtifact.delivery_timestamp <= end
            )
        except:
            pass
    audit_pack['evidence']['disclosures'] = [d.to_dict() for d in disclosures_query.all()]

    # Decision Events
    decisions_query = HiringDecisionEvent.query
    if role_id:
        decisions_query = decisions_query.filter_by(role_id=role_id)
    if start_date and end_date:
        try:
            start = datetime.fromisoformat(start_date)
            end = datetime.fromisoformat(end_date)
            decisions_query = decisions_query.filter(
                HiringDecisionEvent.decision_timestamp >= start,
                HiringDecisionEvent.decision_timestamp <= end
            )
        except:
            pass
    audit_pack['evidence']['decision_events'] = [d.to_dict() for d in decisions_query.all()]

    # Governance Approvals
    approvals_query = GovernanceApprovalRecord.query
    audit_pack['evidence']['governance_approvals'] = [a.to_dict() for a in approvals_query.all()]

    # Vendor Assertions
    assertions_query = VendorAssertionRecord.query
    audit_pack['evidence']['vendor_assertions'] = [a.to_dict() for a in assertions_query.all()]

    # Summary stats
    audit_pack['summary'] = {
        'total_ai_systems': len(audit_pack['evidence']['ai_systems']),
        'total_disclosures': len(audit_pack['evidence']['disclosures']),
        'total_decisions': len(audit_pack['evidence']['decision_events']),
        'total_approvals': len(audit_pack['evidence']['governance_approvals']),
        'total_vendor_assertions': len(audit_pack['evidence']['vendor_assertions'])
    }

    return jsonify(audit_pack), 200


@app.route('/api/audit-packs/<string:audit_pack_id>', methods=['GET'])
def get_audit_pack(audit_pack_id):
    """Get specific audit pack (placeholder - would be stored in production)"""
    return jsonify({
        "error": "Audit pack storage not implemented. Use /api/audit-packs/generate with filters."
    }), 501


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
