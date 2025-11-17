# Awesome Project Repository

This repository contains two distinct projects for different domains:

## 📋 Projects

### 1. 🤖 AI/ML Applicant Tracking System (ATS)

An Applicant Tracking System specifically designed for recruiting AI/ML talent by tracking research profiles, publications, and academic credentials that traditional ATS platforms overlook.

**Key Features:**
- Track candidates with Google Scholar profiles, H-index, and citations
- Manage publications and research papers
- Link candidates to job positions
- Boolean search generator for GitHub
- Full CRUD operations for candidates, jobs, and applications

**Tech Stack:** React + Flask + SQLite

📖 **[View Full ATS Documentation](docs/ATS_README.md)**

**Quick Start:**
```bash
# Backend
cd backend
pip install -r requirements.txt
python app.py

# Frontend (in new terminal)
cd frontend
npm install
npm start
```

---

### 2. 🛡️ SafetyCase.AI

Automated safety case website creation for Physical AI companies. Generate professional, self-contained safety case websites in minutes using AI-powered data extraction.

**Key Features:**
- 5 Industry-Specific Templates (Humanoid Robots, AMRs, Cobots, Drones, Inspection Robots)
- AI-Powered PDF data extraction using Claude API
- Zero external dependencies
- Self-contained HTML output
- Admin dashboard for order management

**Tech Stack:** Next.js 14 + TypeScript + Tailwind CSS + Anthropic Claude API

📖 **[View Full SafetyCase.AI Documentation](docs/SAFETYCASEAI_README.md)**

**Quick Start:**
```bash
# Install dependencies
npm install

# Set up environment variables
cp .env.local.example .env.local
# Edit .env.local and add your ANTHROPIC_API_KEY

# Run development server
npm run dev
```

---

## 🗂️ Repository Structure

```
awesome-project-mctf66nf/
├── docs/
│   ├── ATS_README.md              # Full ATS documentation
│   └── SAFETYCASEAI_README.md     # Full SafetyCase.AI documentation
├── frontend/                       # ATS React frontend
├── backend/                        # ATS Flask backend
├── app/                           # SafetyCase.AI Next.js app
├── components/                    # SafetyCase.AI components
├── lib/                           # SafetyCase.AI libraries
├── templates/                     # SafetyCase.AI HTML templates
├── data/                          # SafetyCase.AI data storage
├── safetycaseai/                  # SafetyCase.AI subdirectory (legacy)
└── README.md                      # This file
```

## 🚀 Deployment

### ATS Deployment
- **Frontend**: Vercel or Netlify
- **Backend**: Render or Railway
- See [docs/ATS_README.md](docs/ATS_README.md) for detailed deployment instructions

### SafetyCase.AI Deployment
- **Platform**: Vercel (recommended)
- See [docs/SAFETYCASEAI_README.md](docs/SAFETYCASEAI_README.md) for detailed deployment instructions

## 📝 Documentation

- **ATS Full Documentation**: [docs/ATS_README.md](docs/ATS_README.md)
- **SafetyCase.AI Full Documentation**: [docs/SAFETYCASEAI_README.md](docs/SAFETYCASEAI_README.md)
- **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Contributing Guidelines**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **Code of Conduct**: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## 🤝 Contributing

We welcome contributions to both projects! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

## 📞 Support

- **ATS Issues**: [GitHub Issues](https://github.com/TechRecruiter-Guru/awesome-project-mctf66nf/issues) (label: `ats`)
- **SafetyCase.AI Issues**: [GitHub Issues](https://github.com/TechRecruiter-Guru/awesome-project-mctf66nf/issues) (label: `safetycaseai`)

## 📄 License

MIT License - See LICENSE file for details

---

**Built with ❤️ by TechRecruiter-Guru and contributors**
