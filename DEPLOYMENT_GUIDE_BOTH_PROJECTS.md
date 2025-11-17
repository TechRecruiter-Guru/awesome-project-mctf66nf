# Deployment Guide - Both Projects

This repository contains two separate projects that need independent deployments:

1. **SafetyCase.AI** (Next.js) - Root directory
2. **AI/ML ATS** (React + Flask) - /frontend and /backend directories

## 🎯 Deployment Strategy

```
┌─────────────────────────────────────────────────────────┐
│  Repository: awesome-project-mctf66nf                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────────────────────────────┐         │
│  │  SafetyCase.AI (Root)                      │         │
│  │  ├── app/                                  │         │
│  │  ├── components/                           │         │
│  │  ├── lib/                                  │         │
│  │  └── package.json (Next.js)               │         │
│  │                                            │         │
│  │  Deploy to: Vercel                        │         │
│  │  Domain: safetycaseai.vercel.app          │         │
│  └────────────────────────────────────────────┘         │
│                                                          │
│  ┌────────────────────────────────────────────┐         │
│  │  ATS Frontend (/frontend)                  │         │
│  │  ├── src/                                  │         │
│  │  ├── public/                               │         │
│  │  └── package.json (React)                 │         │
│  │                                            │         │
│  │  Deploy to: Vercel                        │         │
│  │  Domain: ats-frontend.vercel.app          │         │
│  └────────────────────────────────────────────┘         │
│                                                          │
│  ┌────────────────────────────────────────────┐         │
│  │  ATS Backend (/backend)                    │         │
│  │  ├── app.py                                │         │
│  │  ├── requirements.txt (Flask)             │         │
│  │  └── ats.db (SQLite)                      │         │
│  │                                            │         │
│  │  Deploy to: Render                        │         │
│  │  Domain: ats-backend.onrender.com         │         │
│  └────────────────────────────────────────────┘         │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Deployment 1: SafetyCase.AI (Already Deployed)

**Current Status**: ✅ Deployed to Vercel
**Domains**:
- awesome-project-mctf66n-git-71df32-techrecruiter-gurus-projects.vercel.app
- awesome-project-mctf66nf-21xy-aev99jg14.vercel.app

### Configuration
- **Framework**: Next.js 14
- **Root Directory**: `/` (repository root)
- **Build Command**: `npm run build`
- **Output Directory**: `.next`

### Environment Variables
```env
ANTHROPIC_API_KEY=your_anthropic_api_key
NEXT_PUBLIC_ADMIN_PASSWORD=Muses480!
```

### No Changes Needed
This deployment is already live and working. Keep it as-is.

---

## 📦 Deployment 2: ATS Frontend (NEW)

### Deploy to Vercel

#### Step 1: Create New Vercel Project

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import the same repository: `TechRecruiter-Guru/awesome-project-mctf66nf`
4. Click **"Import"**

#### Step 2: Configure Build Settings

In the project configuration:

```
Framework Preset:         Create React App
Root Directory:          frontend
Build Command:           npm run build
Output Directory:        build
Install Command:         npm install
```

#### Step 3: Environment Variables

Add the following environment variable (will update after backend is deployed):

```
Name:  REACT_APP_API_URL
Value: https://ats-backend.onrender.com
```

#### Step 4: Deploy

1. Click **"Deploy"**
2. Wait for build to complete (~2-3 minutes)
3. Your ATS frontend will be live!

#### Expected URL
```
https://awesome-project-mctf66nf-frontend.vercel.app
```

Or assign a custom domain like:
```
https://ats.yourcompany.com
```

---

## 📦 Deployment 3: ATS Backend (NEW)

### Deploy to Render

#### Step 1: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Grant access to your repository

#### Step 2: Create New Web Service

1. Click **"New"** → **"Web Service"**
2. Connect repository: `TechRecruiter-Guru/awesome-project-mctf66nf`
3. Click **"Connect"**

#### Step 3: Configure Service

```
Name:                ats-backend
Region:             Oregon (US West)
Branch:             main (or your default branch)
Root Directory:     backend
Runtime:            Python 3
Build Command:      pip install -r requirements.txt
Start Command:      gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app
```

#### Step 4: Environment Variables (Optional)

```
Name:  GITHUB_TOKEN
Value: your_github_personal_access_token
```

> This increases GitHub API rate limits for the Boolean search feature

#### Step 5: Choose Plan

- **Free Tier**: Good for development/testing
  - Spins down after inactivity
  - 750 hours/month free

- **Starter ($7/mo)**: Recommended for production
  - Always on
  - Better performance

#### Step 6: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (~3-5 minutes)
3. Service will be live at: `https://ats-backend.onrender.com`

#### Step 7: Test Backend

Once deployed, test the health endpoint:

```bash
curl https://ats-backend.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "AI/ML ATS API is running",
  "version": "1.0.0"
}
```

---

## 🔗 Connect Frontend to Backend

After backend deployment, update the frontend environment variable:

### In Vercel Dashboard

1. Go to your ATS Frontend project
2. Navigate to **Settings** → **Environment Variables**
3. Update `REACT_APP_API_URL`:
   ```
   Value: https://ats-backend.onrender.com
   ```
4. Click **"Save"**
5. Go to **Deployments** → Redeploy latest deployment

---

## 📊 Final Deployment URLs

After all deployments are complete:

### SafetyCase.AI
```
🌐 Production: https://awesome-project-mctf66nf.vercel.app
📁 Code:       / (root directory)
```

### ATS Frontend
```
🌐 Production: https://awesome-project-mctf66nf-frontend.vercel.app
📁 Code:       /frontend directory
🔌 API:        https://ats-backend.onrender.com
```

### ATS Backend
```
🌐 Production: https://ats-backend.onrender.com
📁 Code:       /backend directory
🗄️ Database:   SQLite (Render persistent disk)
```

---

## 🚀 Quick Deploy Commands

### Option 1: Using Vercel CLI (ATS Frontend)

```bash
cd frontend
npm install -g vercel
vercel --prod
```

### Option 2: Using Render Blueprint (ATS Backend)

The `backend/render.yaml` file enables one-click deployment:

1. Go to Render Dashboard
2. New → Blueprint
3. Connect repository
4. Select `backend/render.yaml`
5. Deploy

---

## 🔧 Post-Deployment Steps

### 1. Populate ATS Database

SSH into Render backend or use Render Shell:

```bash
# In Render Shell
python populate_sample_data.py
```

This adds:
- 6 sample candidates (Yann LeCun, Fei-Fei Li, etc.)
- 6 sample jobs (Meta, OpenAI, DeepMind, etc.)
- 4 publications

### 2. Test ATS Application

Visit your frontend URL and verify:
- ✅ Dashboard loads with statistics
- ✅ Candidates page shows 6 candidates
- ✅ Jobs page shows 6 jobs
- ✅ Stealth mode works for confidential jobs
- ✅ Boolean search generates queries

### 3. Monitor Backend

Render provides automatic monitoring:
- Health checks via `/api/health`
- Logs in Render dashboard
- Automatic restarts on failure

---

## 📱 Custom Domains (Optional)

### SafetyCase.AI
```
1. Go to Vercel project → Settings → Domains
2. Add: safetycaseai.com
3. Update DNS with provided records
```

### ATS
```
Frontend:
1. Go to Vercel project → Settings → Domains
2. Add: ats.yourcompany.com

Backend:
1. Go to Render service → Settings → Custom Domains
2. Add: api.ats.yourcompany.com
```

---

## 🔐 Security Checklist

### SafetyCase.AI
- [x] ANTHROPIC_API_KEY stored in Vercel env vars
- [x] Admin password secured
- [x] CORS configured

### ATS
- [x] REACT_APP_API_URL points to production backend
- [x] Flask CORS enabled for frontend domain
- [x] GITHUB_TOKEN (optional) secured in Render env vars
- [ ] Consider adding authentication for production

---

## 🆘 Troubleshooting

### ATS Frontend Can't Connect to Backend

**Issue**: CORS errors or API not responding

**Solution**:
1. Verify backend is deployed and healthy
2. Check REACT_APP_API_URL in Vercel env vars
3. Ensure CORS is enabled in Flask backend (already configured)
4. Redeploy frontend after env var changes

### Backend Database Reset

**Issue**: Need to reset or repopulate database

**Solution**:
```bash
# In Render Shell
rm ats.db
python app.py  # Recreates database
python populate_sample_data.py  # Repopulates data
```

### Render Free Tier Spin Down

**Issue**: Backend takes 30-60s to respond after inactivity

**Solution**:
- Upgrade to Starter plan ($7/mo)
- Or use a cron job to keep it alive:
  ```bash
  # Ping every 10 minutes
  */10 * * * * curl https://ats-backend.onrender.com/api/health
  ```

---

## 📖 Documentation Links

- **ATS README**: [docs/ATS_README.md](docs/ATS_README.md)
- **SafetyCase.AI README**: [docs/SAFETYCASEAI_README.md](docs/SAFETYCASEAI_README.md)
- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs

---

## ✅ Deployment Checklist

### SafetyCase.AI
- [x] Deployed to Vercel
- [x] Environment variables configured
- [x] Domain active

### ATS Frontend
- [ ] Create new Vercel project
- [ ] Set root directory to `frontend`
- [ ] Configure environment variables
- [ ] Deploy and verify
- [ ] Test connection to backend

### ATS Backend
- [ ] Create Render web service
- [ ] Set root directory to `backend`
- [ ] Configure start command
- [ ] Deploy and verify
- [ ] Populate sample data
- [ ] Update frontend API URL

### Final Testing
- [ ] SafetyCase.AI loads correctly
- [ ] ATS Frontend loads and connects to backend
- [ ] ATS Dashboard shows statistics
- [ ] Candidates and Jobs pages work
- [ ] Boolean search generates queries
- [ ] All CRUD operations functional

---

**Ready to deploy?** Start with the ATS Backend on Render, then deploy the ATS Frontend to Vercel!
