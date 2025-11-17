# Deploy ATS Backend & Connect to Existing Frontend

## Current Status

✅ **SafetyCase.AI**: Deployed on Vercel (root directory)
✅ **ATS Frontend**: Deployed on Vercel at https://awesome-project-mctf66nf-techrecruiter-gurus-projects.vercel.app/
❌ **ATS Backend**: Not deployed yet (needs Render deployment)

---

## Step 1: Deploy ATS Backend to Render

### Quick Deploy Instructions

1. **Go to Render**: https://render.com/dashboard

2. **Create New Web Service**:
   - Click **"New"** → **"Web Service"**
   - Connect your GitHub: `TechRecruiter-Guru/awesome-project-mctf66nf`
   - Click **"Connect"**

3. **Configure Service**:
   ```
   Name:              ats-backend
   Region:            Oregon (US West)
   Branch:            main
   Root Directory:    backend
   Runtime:           Python 3
   Build Command:     pip install -r requirements.txt
   Start Command:     gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app
   ```

4. **Environment Variables** (Optional but recommended):
   ```
   Name:  GITHUB_TOKEN
   Value: your_github_personal_access_token
   ```
   *(This increases GitHub API rate limits for Boolean search)*

5. **Select Plan**:
   - **Free Tier**: Spins down after 15 min inactivity (good for testing)
   - **Starter ($7/mo)**: Always on (recommended for production)

6. **Deploy**:
   - Click **"Create Web Service"**
   - Wait 3-5 minutes for deployment
   - Your backend will be at: `https://ats-backend.onrender.com`

### Verify Backend Deployment

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

## Step 2: Populate Backend Database

After backend is deployed:

1. Go to Render Dashboard → Your `ats-backend` service
2. Click **"Shell"** tab (opens a terminal)
3. Run the population script:

```bash
python populate_sample_data.py
```

This adds:
- 6 AI/ML candidates (Yann LeCun, Fei-Fei Li, Yoshua Bengio, etc.)
- 6 job positions (Meta, OpenAI, DeepMind, etc.)
- 4 publications with citation counts

---

## Step 3: Connect Frontend to Backend

Now connect your existing ATS frontend deployment to the new backend:

### In Vercel Dashboard

1. Go to: https://vercel.com/dashboard
2. Find your ATS project: `awesome-project-mctf66nf-techrecruiter-gurus-projects`
3. Navigate to: **Settings** → **Environment Variables**
4. Add or update this variable:

   ```
   Name:  REACT_APP_API_URL
   Value: https://ats-backend.onrender.com
   ```

5. **Important**: Set it for all environments (Production, Preview, Development)
6. Click **"Save"**

### Redeploy Frontend

After adding the environment variable:

1. Go to **Deployments** tab
2. Find the latest deployment
3. Click the **"..."** menu → **"Redeploy"**
4. Wait 1-2 minutes for redeployment

---

## Step 4: Test the Complete ATS

Visit your ATS frontend:
```
https://awesome-project-mctf66nf-techrecruiter-gurus-projects.vercel.app/
```

### Verify Everything Works

1. **Dashboard Tab**:
   - Should show statistics: 6 candidates, 6 jobs
   - Top expertise areas displayed

2. **Candidates Tab**:
   - Should list 6 AI/ML researchers
   - Click on a candidate to see publications

3. **Jobs Tab**:
   - Should list 6 job positions
   - Some should be marked "CONFIDENTIAL" (stealth mode)

4. **Boolean Search Tab**:
   - Generate a GitHub search query
   - Click "Execute Search"
   - Should return GitHub users

5. **Test API Connection**:
   - Open browser DevTools (F12)
   - Go to Network tab
   - Navigate to Candidates page
   - Should see successful API calls to `ats-backend.onrender.com`

---

## Troubleshooting

### Frontend shows "API: unhealthy"

**Problem**: Frontend can't connect to backend

**Solutions**:
1. Verify backend is deployed and healthy:
   ```bash
   curl https://ats-backend.onrender.com/api/health
   ```
2. Check REACT_APP_API_URL in Vercel environment variables
3. Ensure you redeployed frontend after adding env var
4. Check browser console for CORS errors

### Backend returns 404 or 500 errors

**Problem**: Backend not configured correctly

**Solutions**:
1. Check Render logs for errors
2. Verify Start Command: `gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app`
3. Ensure Root Directory is set to `backend`
4. Redeploy the backend service

### Database is empty

**Problem**: Sample data not populated

**Solution**:
```bash
# In Render Shell
python populate_sample_data.py
```

### Free tier backend is slow

**Problem**: Render free tier spins down after 15 minutes

**Solution**:
- First request takes 30-60s to wake up
- Upgrade to Starter plan ($7/mo) for always-on service
- Or use a cron job to ping every 10 minutes

---

## Final Architecture

```
┌─────────────────────────────────────────────────────┐
│                                                      │
│  USER                                               │
│    │                                                │
│    ├─→ SafetyCase.AI (Vercel)                      │
│    │   https://awesome-project-mctf66nf.vercel.app │
│    │                                                │
│    └─→ ATS Frontend (Vercel)                       │
│        https://awesome-project-mctf66nf-           │
│        techrecruiter-gurus-projects.vercel.app     │
│                    ↓                                │
│                    │ API Calls                      │
│                    ↓                                │
│        ATS Backend (Render)                        │
│        https://ats-backend.onrender.com            │
│                    ↓                                │
│                SQLite Database                      │
│                (Persistent Disk)                    │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## Summary Checklist

- [ ] Deploy ATS Backend to Render (5 min)
- [ ] Test backend health endpoint
- [ ] Populate database via Render Shell (1 min)
- [ ] Add REACT_APP_API_URL to Vercel env vars
- [ ] Redeploy ATS Frontend on Vercel (2 min)
- [ ] Test complete ATS application
- [ ] Verify candidates, jobs, and Boolean search work

---

## URLs Reference

| Component | URL |
|-----------|-----|
| SafetyCase.AI | `https://awesome-project-mctf66nf.vercel.app` |
| ATS Frontend | `https://awesome-project-mctf66nf-techrecruiter-gurus-projects.vercel.app` |
| ATS Backend | `https://ats-backend.onrender.com` (after deployment) |

---

**Next Step**: Deploy the backend to Render now! Follow Step 1 above.
