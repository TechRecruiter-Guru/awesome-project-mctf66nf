# 🚀 Quick Deploy Reference Card

## Three Separate Deployments

### 1️⃣ SafetyCase.AI ✅ (Already Deployed)
```
Platform: Vercel
Status:   ✅ LIVE
URL:      https://awesome-project-mctf66nf.vercel.app
Root:     / (repository root)
```
**No action needed** - Already deployed and working!

---

### 2️⃣ ATS Backend (Deploy First)

**Platform**: Render.com

**Quick Setup**:
```bash
1. Go to: https://render.com/dashboard
2. Click: New → Web Service
3. Repo: TechRecruiter-Guru/awesome-project-mctf66nf
4. Configure:
   - Name: ats-backend
   - Root Directory: backend
   - Build: pip install -r requirements.txt
   - Start: gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app
5. Click: Create Web Service
6. Wait ~3 minutes
7. Test: curl https://ats-backend.onrender.com/api/health
```

**Expected URL**:
```
https://ats-backend.onrender.com
```

**After Deploy**:
```bash
# Populate database via Render Shell
python populate_sample_data.py
```

---

### 3️⃣ ATS Frontend (Deploy Second)

**Platform**: Vercel

**Quick Setup**:
```bash
1. Go to: https://vercel.com/dashboard
2. Click: Add New → Project
3. Import: TechRecruiter-Guru/awesome-project-mctf66nf
4. Configure:
   - Framework: Create React App
   - Root Directory: frontend
   - Build Command: npm run build
   - Output Directory: build
5. Add Environment Variable:
   - REACT_APP_API_URL=https://ats-backend.onrender.com
6. Click: Deploy
7. Wait ~2 minutes
```

**Expected URL**:
```
https://awesome-project-mctf66nf-frontend.vercel.app
```

---

## 📋 Final URLs

| Project | URL |
|---------|-----|
| SafetyCase.AI | https://awesome-project-mctf66nf.vercel.app |
| ATS Frontend | https://awesome-project-mctf66nf-frontend.vercel.app |
| ATS Backend | https://ats-backend.onrender.com |

---

## ✅ Verification

### Test SafetyCase.AI
```bash
curl https://awesome-project-mctf66nf.vercel.app
# Should return HTML for SafetyCase.AI landing page
```

### Test ATS Backend
```bash
curl https://ats-backend.onrender.com/api/health
# Should return: {"status":"healthy","message":"AI/ML ATS API is running"}
```

### Test ATS Frontend
Visit in browser:
```
https://awesome-project-mctf66nf-frontend.vercel.app
```
Should show:
- 🤖 AI/ML Applicant Tracking System header
- Dashboard with statistics
- 6 candidates, 6 jobs

---

## 🔄 Update Frontend After Backend Deploy

If you deployed backend after frontend:

```bash
1. Go to Vercel → ATS Frontend project
2. Settings → Environment Variables
3. Update REACT_APP_API_URL to your Render backend URL
4. Deployments → Redeploy latest
```

---

## 🆘 Quick Troubleshooting

**Backend not responding?**
- Free tier spins down after 15 min
- First request takes 30-60s to wake up
- Upgrade to Starter ($7/mo) for always-on

**Frontend can't connect to backend?**
- Check REACT_APP_API_URL env var
- Verify backend is healthy
- Check browser console for CORS errors

**Database empty?**
```bash
# In Render Shell
python populate_sample_data.py
```

---

**Full Guide**: See [DEPLOYMENT_GUIDE_BOTH_PROJECTS.md](DEPLOYMENT_GUIDE_BOTH_PROJECTS.md)
