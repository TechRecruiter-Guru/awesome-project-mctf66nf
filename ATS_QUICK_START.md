# AI/ML ATS Quick Start Guide

## Backend Setup (Already Running!)

The backend is currently running at http://localhost:5000

### Start Backend
```bash
cd backend
pip3 install -r requirements.txt
python3 app.py
```

### Populate Sample Data
```bash
cd backend
python3 populate_sample_data.py
```

## Frontend Setup

### Install Dependencies
```bash
cd frontend
npm install
```

### Configure API URL
The frontend is already configured to use `http://localhost:5000` by default.

Check `frontend/src/App.js` line 6:
```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
```

### Start Frontend
```bash
cd frontend
npm start
```

The app will open at http://localhost:3000

## Sample Data

### Candidates (6)
- Yann LeCun (Computer Vision, H-index: 150)
- Fei-Fei Li (Computer Vision, H-index: 120)
- Yoshua Bengio (Deep Learning, H-index: 175)
- Andrew Ng (Machine Learning, H-index: 140)
- Emily Chen (NLP, H-index: 45)
- Marcus Rodriguez (Reinforcement Learning, H-index: 35)

### Jobs (6)
- 3 Public jobs (Meta, DeepMind, OpenAI)
- 3 Confidential jobs (Stealth mode active)

### Publications (4)
- Classic AI/ML papers linked to candidates

## API Endpoints

### Test Endpoints
```bash
# Health check
curl http://localhost:5000/api/health

# Get all candidates
curl http://localhost:5000/api/candidates

# Get all jobs
curl http://localhost:5000/api/jobs

# Get stats
curl http://localhost:5000/api/stats

# Reveal confidential job
curl -X POST http://localhost:5000/api/jobs/2/reveal
```

## Features to Explore

1. **Research Profiles** - View candidates with Google Scholar URLs, h-index, citations
2. **Publications** - Browse academic papers with citation counts
3. **Stealth Mode** - Test confidential job listings
4. **Boolean Search** - Use the search generator for GitHub/LinkedIn
5. **Filtering** - Filter candidates by expertise, status
6. **Dashboard** - View statistics and top expertise areas

## Next Steps

1. ✅ Backend running with sample data
2. ✅ All API endpoints tested and working
3. 🔄 Start frontend React app
4. 🔄 Test full end-to-end workflow
5. 🔄 Try Boolean search for GitHub candidates
6. 🔄 Create test applications linking candidates to jobs

## Troubleshooting

### Backend won't start
```bash
# Check if port 5000 is in use
lsof -i :5000

# Kill existing process if needed
kill -9 <PID>
```

### Frontend can't connect to backend
- Ensure backend is running on port 5000
- Check CORS is enabled in backend (already configured)
- Verify API_URL in frontend/.env or frontend/src/App.js

### Database is empty
```bash
cd backend
python3 populate_sample_data.py
```

## Documentation

- **Full ATS README**: [docs/ATS_README.md](docs/ATS_README.md)
- **Verification Report**: [backend/ATS_VERIFICATION.md](backend/ATS_VERIFICATION.md)
- **Repository Overview**: [README.md](README.md)

---

**Backend Status**: ✅ Running at http://localhost:5000
**Database**: ✅ Populated with 6 candidates, 6 jobs, 4 publications
**Next**: Start the frontend to see the full ATS UI!
