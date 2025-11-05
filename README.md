# 🤖 AI/ML Applicant Tracking System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-green.svg)](https://flask.palletsprojects.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub issues](https://img.shields.io/github/issues/TechRecruiter-Guru/awesome-project-mctf66nf)](https://github.com/TechRecruiter-Guru/awesome-project-mctf66nf/issues)

**An Applicant Tracking System specifically designed for recruiting AI/ML talent by tracking research profiles, publications, and academic credentials that traditional ATS platforms overlook.**

## 🌟 Why This ATS is Different

Traditional ATS platforms fail to capture the most important signals when recruiting AI/ML researchers and practitioners:
- **Research publications** on arXiv, Google Scholar
- **Academic impact** measured by H-index and citations
- **Conference contributions** (NeurIPS, ICML, CVPR, etc.)
- **Open source contributions** and technical portfolios
- **Research focus areas** (Computer Vision, NLP, Reinforcement Learning, etc.)

This ATS solves that problem by putting **research credentials first**.

## 🌐 Live Demo

- **Frontend**: [Deploy to Vercel - Instructions below]
- **Backend API**: [Deploy to Render - Instructions below]
- **API Health Check**: `GET /api/health`

> **Note**: Backend may take 30-60 seconds to wake up on first request (free tier)

## ✨ Key Features

### 🎓 Academic & Research Tracking
- **Google Scholar Integration** - Track publications and citations
- **arXiv Author Profiles** - Link to research paper preprints
- **ORCID Support** - Persistent researcher identifiers
- **ResearchGate Profiles** - Academic networking presence
- **H-Index Tracking** - Measure research impact
- **Citation Metrics** - Track academic influence
- **Publication History** - Full paper cataloging with venues and citations

### 💼 Standard ATS Features
- **Candidate Management** - Full CRUD for AI/ML candidates
- **Job Posting** - AI/ML-specific job requirements
- **Application Tracking** - Link candidates to positions
- **Pipeline Management** - Track hiring stages
- **Research-Based Scoring** - Rate candidates on technical + research fit
- **Skills & Expertise** - Categorize by AI/ML specialization

### 🔍 AI/ML-Specific Fields
- **Research Focus Areas**: Computer Vision, NLP, RL, MLOps, etc.
- **Conference Publications**: NeurIPS, ICML, CVPR, ICLR, etc.
- **Education Level**: PhD, Masters, Bachelors
- **Technical Skills**: PyTorch, TensorFlow, CUDA, etc.
- **Source Tracking**: Found via LinkedIn, Google Scholar, arXiv, referral

## 🛠 Tech Stack

### Backend
- **Flask** - Lightweight Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Database (easily upgradable to PostgreSQL)
- **Flask-CORS** - Cross-origin resource sharing
- **Gunicorn** - Production WSGI server

### Frontend
- **React 18** - Modern React with Hooks
- **Axios** - HTTP client for API calls
- **CSS3** - Custom professional styling

### Data Models
- **Candidate** - With research profile fields
- **Job** - AI/ML position with research requirements
- **Application** - Candidate-job linkage with scoring
- **Publication** - Research paper tracking

### DevOps
- **Docker** - Containerization ready
- **Vercel** - Frontend hosting
- **Render** - Backend hosting
- **Git** - Version control

## 🚀 Quick Start

### Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- pip (Python package manager)
- npm (Node package manager)

### Local Development Setup

#### 1. Clone the repository

```bash
git clone https://github.com/TechRecruiter-Guru/awesome-project-mctf66nf.git
cd awesome-project-mctf66nf
```

#### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The backend server will start on `http://localhost:5000`

✅ You should see: `* Running on http://127.0.0.1:5000`

#### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend
npm install
npm start
```

The frontend will start on `http://localhost:3000` and automatically open in your browser.

✅ You should see the AI/ML ATS interface!

### 🐳 Docker Setup (Alternative)

Prefer Docker? We've got you covered:

```bash
docker-compose up
```

Both frontend and backend will start automatically!
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:5000`

## 📡 API Documentation

### Base URL
- **Local**: `http://localhost:5000`
- **Production**: `https://your-api.onrender.com`

### Core Endpoints

#### Candidates

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/api/candidates` | Get all candidates | None |
| GET | `/api/candidates/:id` | Get candidate with full details | None |
| POST | `/api/candidates` | Create new candidate | Candidate object |
| PUT | `/api/candidates/:id` | Update candidate | Updated fields |
| DELETE | `/api/candidates/:id` | Delete candidate | None |

#### Jobs

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/api/jobs` | Get all jobs | None |
| GET | `/api/jobs/:id` | Get job with applications | None |
| POST | `/api/jobs` | Create new job | Job object |
| PUT | `/api/jobs/:id` | Update job | Updated fields |
| DELETE | `/api/jobs/:id` | Delete job | None |

#### Applications

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/api/applications` | Get all applications | None |
| POST | `/api/applications` | Create application | Application object |
| PUT | `/api/applications/:id` | Update application | Updated fields |
| DELETE | `/api/applications/:id` | Delete application | None |

#### Publications

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/api/candidates/:id/publications` | Get candidate's publications | None |
| POST | `/api/publications` | Add publication | Publication object |
| DELETE | `/api/publications/:id` | Delete publication | None |

#### Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stats` | Get dashboard statistics |
| GET | `/api/health` | Health check |

### Example: Create AI/ML Candidate

```bash
curl -X POST http://localhost:5000/api/candidates \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@university.edu",
    "primary_expertise": "Computer Vision",
    "google_scholar_url": "https://scholar.google.com/citations?user=XXXXX",
    "h_index": 25,
    "citation_count": 1500,
    "years_experience": 5
  }'
```

### Example: Create AI/ML Job

```bash
curl -X POST http://localhost:5000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior ML Research Scientist",
    "company": "TechCorp AI Lab",
    "required_expertise": "Deep Learning",
    "education_required": "PhD",
    "research_focus": "Computer Vision and Multimodal Learning",
    "salary_min": 150000,
    "salary_max": 250000
  }'
```

### Example: Add Publication

```bash
curl -X POST http://localhost:5000/api/publications \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "title": "Attention Is All You Need",
    "venue": "NeurIPS 2017",
    "year": 2017,
    "arxiv_id": "1706.03762",
    "citation_count": 50000,
    "research_area": "Natural Language Processing"
  }'
```

## 📁 Project Structure

```
awesome-project-mctf66nf/
├── .github/
│   ├── ISSUE_TEMPLATE/          # Issue templates
│   └── PULL_REQUEST_TEMPLATE.md # PR template
├── frontend/
│   ├── public/
│   │   └── index.html           # HTML template
│   ├── src/
│   │   ├── App.js               # Main ATS interface
│   │   ├── App.css              # ATS styling
│   │   ├── index.js             # React entry point
│   │   └── index.css            # Global styles
│   ├── Dockerfile               # Frontend container
│   ├── package.json             # Frontend dependencies
│   └── vercel.json              # Vercel config
├── backend/
│   ├── app.py                   # Flask ATS API
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile               # Backend container
│   └── ats.db                   # SQLite database (auto-generated)
├── docker-compose.yml           # Docker orchestration
├── vercel.json                  # Vercel monorepo config
├── railway.toml                 # Railway config
├── DEPLOYMENT.md                # Deployment guide
├── CONTRIBUTING.md              # Contribution guidelines
├── CODE_OF_CONDUCT.md           # Community guidelines
├── CONTRIBUTORS.md              # List of contributors
└── README.md                    # You are here!
```

## 🎨 Data Models

### Candidate
```python
- Basic Info: first_name, last_name, email, phone, location
- Professional: linkedin_url, github_url, portfolio_url, resume_url
- Research Profile: google_scholar_url, research_gate_url, arxiv_author_id, orcid_id
- Metrics: h_index, citation_count
- AI/ML: primary_expertise, skills, years_experience
- Status: status, rating, notes
```

### Job
```python
- Basic: title, company, location, job_type
- Details: description, requirements, responsibilities
- AI/ML: required_expertise, required_skills, education_required, research_focus
- Compensation: salary_min, salary_max, currency
- Status: status, posted_date, closing_date
```

### Application
```python
- Links: candidate_id, job_id
- Status: status, stage, source
- Tracking: applied_date, last_contact_date, interview_date
- Scoring: technical_score, research_score, culture_fit_score, overall_score
```

### Publication
```python
- Details: title, authors, venue, year
- Links: paper_url, arxiv_id, doi
- Metrics: citation_count
- Categories: research_area, keywords, abstract
```

## 🚢 Deployment

Want to deploy your own instance? Check out our comprehensive [DEPLOYMENT.md](DEPLOYMENT.md) guide!

### Quick Deploy Options

- **Frontend**: Vercel (recommended) or Netlify
- **Backend**: Render (recommended) or Railway
- **Full Stack**: Railway or Docker

See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions.

## 🔧 Development

### Making Changes

**Frontend**:
- Edit files in `frontend/src/`
- The app will hot-reload automatically
- Changes appear instantly in the browser

**Backend**:
- Edit `backend/app.py`
- Restart the Python server to see changes
- Use `Ctrl+C` to stop, then `python app.py` to restart

### Adding New Features

Some ideas for contributors:

1. **Google Scholar API Integration** - Auto-fetch publications
2. **arXiv API Integration** - Automatic paper importing
3. **AI-Powered Candidate Matching** - ML-based job matching
4. **Email Integration** - Automated candidate outreach
5. **Resume Parser** - Extract info from CVs
6. **Conference Tracker** - Track accepted papers at top venues

## 🤝 Contributing

We love contributions! Whether you're fixing bugs, adding features, or improving documentation, we'd love to have you as part of our community.

### How to Contribute

1. 🍴 Fork the repository
2. 🔧 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🎉 Open a Pull Request

Check out our [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines!

### Good First Issues

New to open source? Look for issues labeled:
- `good first issue` - Perfect for beginners
- `help wanted` - We need help!
- `documentation` - Improve our docs
- `api-integration` - Add Google Scholar, arXiv APIs

### Contributors

See [CONTRIBUTORS.md](CONTRIBUTORS.md) for the list of amazing people who have contributed to this project!

## 📋 Roadmap

### Phase 1: Core ATS (✅ Complete)
- [x] Candidate management with research profiles
- [x] Job posting management
- [x] Application tracking
- [x] Publication tracking
- [x] Dashboard and statistics

### Phase 2: API Integrations (🔄 In Progress)
- [ ] Google Scholar API integration
- [ ] arXiv API for automatic paper fetching
- [ ] ORCID API integration
- [ ] GitHub API for repository analysis
- [ ] LinkedIn scraping (ethically)

### Phase 3: AI/ML Features
- [ ] AI-powered candidate-job matching
- [ ] Research impact scoring algorithm
- [ ] Resume parsing with NLP
- [ ] Automated skill extraction
- [ ] Conference publication tracking (NeurIPS, ICML, CVPR)

### Phase 4: Advanced Features
- [ ] Email campaign automation
- [ ] Interview scheduling
- [ ] Offer management
- [ ] Analytics dashboard
- [ ] Team collaboration features
- [ ] PostgreSQL support for production

Want to help with any of these? Check out [CONTRIBUTING.md](CONTRIBUTING.md)!

## 🎯 Use Cases

### For Recruiters
- Track AI/ML candidates with comprehensive research profiles
- Evaluate candidates based on research impact
- Source candidates from Google Scholar and arXiv
- Match candidates to jobs based on research expertise

### For Hiring Managers
- Review candidates' publication history
- Assess technical depth through research contributions
- Find candidates with specific AI/ML expertise
- Track candidates through interview pipeline

### For Research Labs
- Recruit PhD candidates and postdocs
- Find collaborators with specific research backgrounds
- Track candidates from academic conferences
- Evaluate research fit for lab positions

## 🐛 Known Issues

No known issues at the moment! Found a bug? Please [report it](https://github.com/TechRecruiter-Guru/awesome-project-mctf66nf/issues/new?template=bug_report.md).

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask and React teams for amazing frameworks
- The AI/ML research community for inspiration
- All our contributors!

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/TechRecruiter-Guru/awesome-project-mctf66nf/issues)
- **Discussions**: [GitHub Discussions](https://github.com/TechRecruiter-Guru/awesome-project-mctf66nf/discussions)
- **Project Maintainer**: TechRecruiter-Guru

## ⭐ Show Your Support

If you like this project, please give it a ⭐ on GitHub!

This ATS fills a critical gap in recruiting AI/ML talent by recognizing that **research credentials matter** as much as work experience.

---

## 🌍 Why This Matters

Traditional ATS platforms treat all candidates the same. But when recruiting for AI/ML roles, the most qualified candidates often have:

- **Strong publication records** rather than traditional work history
- **Open source contributions** on GitHub
- **Conference presentations** at NeurIPS, ICML, CVPR
- **Research impact** measured by citations and H-index
- **Academic credentials** from top programs

This ATS puts those signals first, making it easier to find and evaluate top AI/ML talent.

---

**Built with ❤️ by TechRecruiter-Guru and the open source community**

Ready to contribute? Start with our [Contributing Guide](CONTRIBUTING.md)!

---

## 🚀 Star History

If this project helped you, consider giving it a star! Every star motivates us to keep improving the platform.
