# ⚠️ IMPORTANT: ATS Backend Deployment Platform

## Why the Vercel Build Failed

**Error**: `/vercel/path0/backend/.next/routes-manifest.json` couldn't be found

**Reason**: Vercel is trying to build the Flask backend as a Next.js application!

## Correct Deployment Strategy

| Component | Platform | Why |
|-----------|----------|-----|
| **SafetyCase.AI** | ✅ Vercel | Next.js app - perfect for Vercel |
| **ATS Frontend** | ✅ Vercel | React static site - perfect for Vercel |
| **ATS Backend** | ❌ NOT Vercel<br>✅ USE Render | Flask API + SQLite needs persistent server |

---

## Why ATS Backend Can't Use Vercel

### 1. **Flask Needs a Persistent Server**
   - Vercel is **serverless** (functions run on-demand and shut down)
   - Flask expects to run continuously
   - Database connections need to persist

### 2. **SQLite Needs Persistent Storage**
   - Vercel filesystem is **ephemeral** (resets on each deployment)
   - Your `ats.db` file would be deleted constantly
   - Data would be lost on every deploy

### 3. **Long-Running Processes**
   - Flask dev server or gunicorn needs to stay running
   - Vercel functions have 10-60 second timeouts
   - Your API needs unlimited runtime

---

## ✅ Deploy ATS Backend to Render Instead

Render provides:
- ✅ Persistent servers (always running)
- ✅ Persistent disk storage (SQLite database survives)
- ✅ Free tier available
- ✅ Easy Python/Flask deployment

### Step-by-Step: Deploy to Render

#### 1. Create Render Account
- Go to: https://render.com
- Sign up with GitHub
- Grant access to repository: `TechRecruiter-Guru/awesome-project-mctf66nf`

#### 2. Create New Web Service
- Click **"New"** → **"Web Service"**
- Select repository: `awesome-project-mctf66nf`
- Click **"Connect"**

#### 3. Configure Service
```
Name:              ats-backend
Region:            Oregon (US West)
Branch:            main
Root Directory:    backend
Runtime:           Python 3
Build Command:     pip install -r requirements.txt
Start Command:     gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app
```

**IMPORTANT**: Make sure "Root Directory" is set to `backend`!

#### 4. Choose Plan
- **Free Tier**:
  - ✅ Good for testing/development
  - ⚠️ Spins down after 15 min inactivity (first request takes 30-60s)
  - ✅ 750 hours/month free

- **Starter ($7/month)**:
  - ✅ Always on (no spin down)
  - ✅ Better for production
  - ✅ Faster response times

#### 5. Deploy!
- Click **"Create Web Service"**
- Wait 3-5 minutes for build and deployment
- Backend will be live at: `https://ats-backend.onrender.com`

#### 6. Verify Deployment
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

#### 7. Populate Database
- In Render Dashboard → Your service → **"Shell"** tab
- Run:
  ```bash
  python populate_sample_data.py
  ```
- Adds 6 candidates, 6 jobs, 4 publications

#### 8. Connect Frontend to Backend
- Go to Vercel Dashboard
- Find your ATS Frontend project
- **Settings** → **Environment Variables**
- Add:
  ```
  Name:  REACT_APP_API_URL
  Value: https://ats-backend.onrender.com
  ```
- **Deployments** → Redeploy latest deployment

---

## Alternative Options (If You Don't Want Render)

### Option 1: Railway.app
- Similar to Render
- Deploy: https://railway.app
- Pricing: $5/month
- Same persistent storage benefits

### Option 2: Fly.io
- Global edge deployment
- Deploy: https://fly.io
- Pricing: Free tier available
- Better for global users

### Option 3: DigitalOcean App Platform
- Enterprise-grade
- Deploy: https://cloud.digitalocean.com
- Pricing: $5/month minimum
- More control over infrastructure

### Option 4: Heroku
- Classic PaaS platform
- Deploy: https://heroku.com
- Pricing: $5-7/month (no free tier anymore)
- Easy Python deployment

---

## What About Using Vercel for Everything?

### Could We Make the Backend Work on Vercel?

**Technically possible but NOT recommended** because:

1. **Would need to convert Flask to Vercel Serverless Functions**
   - Complete rewrite of backend code
   - Change from `app.py` to individual function files
   - Complex routing setup

2. **Would need to replace SQLite with Vercel KV or external DB**
   - Migrate from SQLite to PostgreSQL/MySQL
   - Add database hosting (Supabase, PlanetScale, etc.)
   - Additional monthly costs ($0-20)

3. **Would lose some Flask features**
   - No background tasks
   - Cold starts on every request
   - 60-second timeout limits

**Effort**: ~4-6 hours of work + ongoing complexity
**Cost**: Potentially more than Render
**Benefit**: Minimal (everything in one platform)

**Verdict**: ❌ Not worth it - Use Render!

---

## Summary: Final Architecture

```
┌─────────────────────────────────────────────────────────┐
│                                                          │
│  VERCEL (Good for static/serverless)                   │
│  ├── SafetyCase.AI (Next.js)                          │
│  │   https://awesome-project-mctf66nf.vercel.app      │
│  │                                                      │
│  └── ATS Frontend (React)                             │
│      https://awesome-project-...vercel.app            │
│              ↓                                          │
│              │ API Calls (HTTPS)                       │
│              ↓                                          │
│  RENDER (Good for persistent servers)                  │
│  └── ATS Backend (Flask + SQLite)                     │
│      https://ats-backend.onrender.com                 │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Deployment Checklist

- [x] SafetyCase.AI on Vercel ✅ (already done)
- [x] ATS Frontend on Vercel ✅ (already done)
- [ ] ATS Backend on Render ❌ (do this now!)
- [ ] Connect frontend to backend via env vars
- [ ] Populate database with sample data
- [ ] Test complete application

---

## Next Step

**Deploy the ATS Backend to Render now!** Follow the "Step-by-Step" section above.

Once deployed, your ATS will be fully functional with:
- ✅ 6 AI/ML candidates with research profiles
- ✅ 6 job positions with salaries
- ✅ 4 publications with citations
- ✅ Working Boolean search for GitHub
- ✅ Complete CRUD operations

**Estimated time**: 5-7 minutes total
