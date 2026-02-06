# ATS Backend Deployment Guide - Render + Supabase

## Quick Deploy (15 minutes)

### Step 1: Set Up Supabase Database (FREE - 5 min)

1. Go to https://supabase.com and sign up / log in
2. Click **"New Project"**
3. Set:
   - **Name**: `ats-recruiting-db`
   - **Database Password**: Choose a strong password (SAVE THIS!)
   - **Region**: US West (Oregon) - matches Render
4. Wait for project to provision (~2 min)
5. Go to **Settings → Database**
6. Under **Connection string → URI**, copy the **connection pooler** URI (port 6543)
   - It looks like: `postgresql://postgres.[project-ref]:[password]@aws-0-us-west-2.pooler.supabase.com:6543/postgres`
   - **IMPORTANT**: Use the **Transaction pooler** (port 6543), NOT direct connection (5432)

### Step 2: Deploy Backend on Render (FREE - 10 min)

1. Go to https://render.com and sign up / log in
2. Click **"New" → "Web Service"**
3. Connect your GitHub repo: `TechRecruiter-Guru/awesome-project-mctf66nf`
4. Configure:
   - **Name**: `ats-recruiting-backend`
   - **Region**: Oregon (US West)
   - **Branch**: `claude/ats-critical-issues-whCxA`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --preload app:app`
   - **Instance Type**: Free
5. Add Environment Variables:
   - `DATABASE_URL` = your Supabase connection pooler URI from Step 1
   - `PYTHON_VERSION` = `3.11.0`
   - `GITHUB_TOKEN` = (optional, for higher GitHub API limits)
6. Click **"Create Web Service"**
7. Wait for build to complete (~3-5 min)

### Step 3: Verify Deployment

Once deployed, test these endpoints:

```bash
# Replace with your Render URL
BACKEND_URL="https://ats-recruiting-backend.onrender.com"

# 1. Health check (should show database: postgresql, status: connected)
curl $BACKEND_URL/api/health

# 2. Initialize database tables (run ONCE after first deploy)
curl -X POST $BACKEND_URL/api/init-db

# 3. Check stats (should show 0 candidates initially)
curl $BACKEND_URL/api/stats

# 4. Populate sample data
cd backend && python populate_sample_data.py
# OR manually create your first candidate:
curl -X POST $BACKEND_URL/api/candidates \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Test","email":"test@example.com"}'
```

### Step 4: Connect Frontend

Update your Next.js frontend to point to the Render backend:

In your frontend code, update the API base URL:
```
NEXT_PUBLIC_ATS_API_URL=https://ats-recruiting-backend.onrender.com
```

---

## Troubleshooting

### "Boot timeout" error on Render
- This is FIXED. Tables now initialize lazily on first request instead of blocking startup.

### "relation does not exist" error
- Hit the `/api/init-db` endpoint: `curl -X POST YOUR_URL/api/init-db`

### Data disappearing after deploy
- This is FIXED. PostgreSQL on Supabase persists data permanently.
- SQLite data loss only happens with SQLite (local dev mode).

### Connection errors
- Make sure you're using the **connection pooler** URI (port 6543)
- NOT the direct connection (port 5432)
- Double check your DATABASE_URL has no typos

### Build fails with psycopg2 error
- Render automatically installs system dependencies for psycopg2-binary
- If issues persist, the Dockerfile includes libpq-dev for manual builds

---

## Architecture

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   Next.js UI     │────▶│  Flask Backend    │────▶│  Supabase        │
│   (Vercel)       │     │  (Render)         │     │  PostgreSQL      │
│   /recruiter     │     │  /api/*           │     │  (Persistent!)   │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | YES | Supabase PostgreSQL connection pooler URI |
| `PYTHON_VERSION` | YES | Set to `3.11.0` |
| `GITHUB_TOKEN` | No | GitHub Personal Access Token for higher API rate limits |
| `PORT` | Auto | Set by Render automatically |
