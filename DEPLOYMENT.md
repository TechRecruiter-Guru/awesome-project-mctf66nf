# 🚀 Deployment Guide

This guide will help you deploy your Task Manager MVP to the internet so you can access it from anywhere!

## 📋 Table of Contents
- [Option 1: Render + Vercel (Recommended for Beginners)](#option-1-render--vercel-easiest)
- [Option 2: Railway (All-in-One)](#option-2-railway-all-in-one)
- [Option 3: Heroku](#option-3-heroku)
- [Option 4: Docker Deployment](#option-4-docker-deployment)

---

## Option 1: Render + Vercel (Easiest)

This option deploys your backend on Render (free tier) and frontend on Vercel (free tier).

### Part A: Deploy Backend to Render

#### Step 1: Create a Render Account
1. Go to https://render.com
2. Sign up for a free account (use GitHub to sign in)

#### Step 2: Prepare Backend for Render
Create a `render.yaml` in the root directory:

```yaml
services:
  - type: web
    name: task-manager-api
    env: python
    buildCommand: "pip install -r backend/requirements.txt"
    startCommand: "cd backend && gunicorn app:app"
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
```

Add `gunicorn` to `backend/requirements.txt`:
```
Flask==2.3.2
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.0.5
python-dotenv==1.0.0
gunicorn==21.2.0
```

#### Step 3: Deploy on Render
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select your repository
4. Render will auto-detect Python
5. Configure:
   - **Name**: task-manager-api
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && gunicorn app:app`
6. Click "Create Web Service"
7. Wait for deployment (takes 2-5 minutes)
8. Copy your API URL (e.g., `https://task-manager-api.onrender.com`)

### Part B: Deploy Frontend to Vercel

#### Step 1: Update Frontend API URL
In `frontend/src/App.js`, update line 5:
```javascript
const API_URL = process.env.REACT_APP_API_URL || 'https://YOUR-RENDER-URL.onrender.com';
```
Replace `YOUR-RENDER-URL` with your Render URL from above.

Or create `frontend/.env.production`:
```
REACT_APP_API_URL=https://YOUR-RENDER-URL.onrender.com
```

#### Step 2: Deploy to Vercel

**🚨 IMPORTANT: You MUST set the Root Directory to `frontend`**

1. Go to https://vercel.com
2. Sign up (use GitHub)
3. Click "Add New" → "Project"
4. Import your repository
5. **Configure Build Settings** (CRITICAL):
   - **Root Directory**: Click "Edit" and type `frontend` (⚠️ This is the most important step!)
   - **Framework Preset**: Create React App (auto-detected)
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `build` (auto-detected)
6. **Add Environment Variable**:
   - Click "Environment Variables"
   - **Key**: `REACT_APP_API_URL`
   - **Value**: `https://YOUR-RENDER-URL.onrender.com`
7. Click "Deploy"
8. Wait 1-2 minutes
9. Click on your live URL!

**Alternative**: A `vercel.json` configuration file has been included in the repository root to help with deployment.

### ✅ Done! Your app is live!

---

## Option 2: Railway (All-in-One)

Railway can host both frontend and backend together.

#### Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub

#### Step 2: Prepare for Railway
Create `railway.toml` in root:
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "cd backend && gunicorn app:app"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

Add `gunicorn` to `backend/requirements.txt`

#### Step 3: Deploy
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository
4. Railway auto-deploys both services
5. Set environment variables in Railway dashboard
6. Get your public URL

---

## Option 3: Heroku

Heroku offers a straightforward deployment option.

#### Step 1: Install Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

#### Step 2: Prepare Backend
Create `backend/Procfile`:
```
web: gunicorn app:app
```

Add `gunicorn` to `backend/requirements.txt`

#### Step 3: Deploy Backend
```bash
cd backend
heroku login
heroku create your-app-name-api
git init
git add .
git commit -m "Deploy backend"
heroku git:remote -a your-app-name-api
git push heroku main
```

#### Step 4: Deploy Frontend
Update `REACT_APP_API_URL` in frontend, then:
```bash
cd frontend
npm run build
# Deploy build folder to Netlify or Vercel (see Option 1)
```

---

## Option 4: Docker Deployment

Use the existing Docker setup for deployment.

#### Step 1: Update docker-compose.yml
Already configured! Just update environment variables:

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:5000
    depends_on:
      - backend
```

#### Step 2: Deploy to Any Cloud Provider
```bash
# Build and run
docker-compose up -d

# Or deploy to:
# - AWS ECS
# - Google Cloud Run
# - DigitalOcean App Platform
# - Azure Container Instances
```

---

## 🌍 Deployment Checklist

Before deploying, ensure:

- [ ] Backend `requirements.txt` includes `gunicorn`
- [ ] Frontend `.env.production` has correct API URL
- [ ] Database is configured (SQLite works, but consider PostgreSQL for production)
- [ ] CORS is properly configured in backend
- [ ] Environment variables are set in deployment platform
- [ ] Git repository is up to date

---

## 🔒 Production Best Practices

### Security
1. **Use Environment Variables** for sensitive data
2. **Enable HTTPS** (most platforms do this automatically)
3. **Add rate limiting** to API endpoints
4. **Update dependencies** regularly

### Database
For production, consider upgrading from SQLite to PostgreSQL:
```python
# In backend/app.py, update:
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///tasks.db')
```

Add to `requirements.txt`:
```
psycopg2-binary==2.9.9
```

### Performance
1. **Enable caching** for static assets
2. **Use CDN** for frontend (Vercel/Netlify do this automatically)
3. **Optimize images** if you add any
4. **Minify JavaScript** (React Scripts does this in build)

---

## 🆘 Troubleshooting

### Frontend can't connect to Backend
- Check CORS settings in `backend/app.py`
- Verify `REACT_APP_API_URL` is correct
- Ensure backend is deployed and running

### Database errors
- SQLite works for MVP but consider PostgreSQL for production
- Check file permissions for SQLite database
- Ensure database directory exists

### Build failures
- Check Node.js version (use v16+)
- Check Python version (use 3.8+)
- Clear cache and rebuild

---

## 📞 Quick Deploy Commands

### Render (Backend)
```bash
# Add gunicorn to requirements.txt
echo "gunicorn==21.2.0" >> backend/requirements.txt
git add . && git commit -m "Add gunicorn" && git push
# Then deploy via Render dashboard
```

### Vercel (Frontend)
```bash
cd frontend
npx vercel
# Follow prompts
```

### Railway (Full Stack)
```bash
# Install Railway CLI
npm i -g @railway/cli
railway login
railway init
railway up
```

---

## 🎉 After Deployment

Once deployed, you'll get URLs like:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-api.onrender.com`

Share these with anyone to use your Task Manager!

---

## 💡 Free Tier Limits

| Platform | Limits | Best For |
|----------|--------|----------|
| **Vercel** | 100GB bandwidth/month | Frontend |
| **Render** | 750 hours/month, sleeps after 15min idle | Backend APIs |
| **Railway** | $5 free credit/month | Full stack |
| **Netlify** | 100GB bandwidth/month | Frontend |
| **Heroku** | No longer has free tier | Paid hosting |

**Pro Tip**: Render free tier "sleeps" after 15 minutes of inactivity, causing 30-60 second cold starts. Consider Railway or paid tier for production.

---

Need help? Check the platform-specific documentation or reach out!
