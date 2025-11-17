# 🚀 Quick Redeploy to Render

This guide helps you redeploy your ATS (Task Manager) project to Render.

---

## ⚡ TL;DR - Fastest Redeploy

**Already deployed to Render before?** Just push to GitHub:

```bash
git add .
git commit -m "Redeploy to Render"
git push origin main
```

Render will automatically redeploy. Check status at: https://dashboard.render.com

**Manual trigger**: Dashboard → Your Service → "Manual Deploy" → "Deploy latest commit"

---

## 🔄 Redeploying an Existing Render Service

If you've already deployed to Render before and just need to redeploy:

### Option A: Automatic Redeploy (Easiest)

1. **Push your latest code to GitHub**:
   ```bash
   git add .
   git commit -m "Update for redeployment"
   git push origin main
   ```

2. **Trigger automatic deployment**:
   - Render automatically deploys when you push to GitHub
   - Check your Render dashboard: https://dashboard.render.com
   - Look for your service (e.g., "task-manager-api")
   - You'll see "Deploying..." status
   - Wait 2-5 minutes for completion

### Option B: Manual Redeploy

1. **Go to Render Dashboard**:
   - Visit: https://dashboard.render.com
   - Log in with your account

2. **Find your service**:
   - Click on your web service (e.g., "task-manager-api")

3. **Trigger manual deploy**:
   - Click "Manual Deploy" button (top right)
   - Select "Deploy latest commit"
   - Click "Deploy"
   - Wait 2-5 minutes

4. **Check deployment status**:
   - Watch the logs in real-time
   - Wait for "Build successful" message
   - Service will restart automatically

---

## 🆕 First-Time Deployment to Render

If you're deploying to Render for the first time:

### Part A: Deploy Backend to Render

#### Step 1: Create a Render Account
1. Go to https://render.com
2. Sign up for a free account (use GitHub to sign in)

#### Step 2: Prepare Backend for Render

**Check if `gunicorn` is in `backend/requirements.txt`**:

Your `backend/requirements.txt` should include:
```
Flask==2.3.2
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.0.5
python-dotenv==1.0.0
gunicorn==21.2.0
```

If `gunicorn` is missing, add it:
```bash
echo "gunicorn==21.2.0" >> backend/requirements.txt
git add backend/requirements.txt
git commit -m "Add gunicorn for Render deployment"
git push origin main
```

#### Step 3: Deploy on Render
1. **Go to Render Dashboard**: https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. **Connect GitHub**: Click "Connect account" if not connected
4. **Select your repository**: Choose `TechRecruiter-Guru/awesome-project-mctf66nf`
5. **Configure the service**:
   - **Name**: `task-manager-api` (or any name you want)
   - **Region**: Choose closest to you
   - **Branch**: `main` (or your deployment branch)
   - **Root Directory**: Leave blank (or specify `backend` if needed)
   - **Environment**: **Python 3**
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && gunicorn app:app`
   - **Instance Type**: **Free** (or paid if you want faster performance)

6. **Environment Variables** (if needed):
   Click "Add Environment Variable":
   - `FLASK_ENV` = `production`
   - `DATABASE_URL` = (if using PostgreSQL)

7. Click **"Create Web Service"**

8. **Wait for deployment** (2-5 minutes):
   - Watch the build logs
   - Wait for "Build successful"
   - Service will start automatically

9. **Copy your API URL**:
   - Example: `https://task-manager-api.onrender.com`
   - Save this for frontend configuration

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

## 🐛 Common Render Deployment Issues

### Issue 1: Build Fails - "gunicorn: command not found"

**Problem**: `gunicorn` is not in your `requirements.txt`

**Solution**:
```bash
echo "gunicorn==21.2.0" >> backend/requirements.txt
git add backend/requirements.txt
git commit -m "Add gunicorn"
git push origin main
```

Render will auto-redeploy with the fix.

### Issue 2: Build Succeeds but Service Fails to Start

**Problem**: Incorrect start command or wrong directory

**Solution**:
1. Go to Render Dashboard → Your Service → Settings
2. Check "Start Command" is: `cd backend && gunicorn app:app`
3. Or try: `gunicorn app:app` (if backend is root directory)
4. Click "Save Changes"
5. Manual Deploy → Deploy latest commit

### Issue 3: "Application failed to respond"

**Problem**: Flask app is not binding to 0.0.0.0 or correct port

**Solution**:
Check your `backend/app.py` has:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

Render sets the `PORT` environment variable automatically.

### Issue 4: Service Keeps Restarting

**Problem**: Free tier goes to sleep after 15 minutes of inactivity

**What's happening**:
- Free Render services "spin down" after 15 minutes of no activity
- First request after sleep takes 30-60 seconds (cold start)
- This is normal behavior for free tier

**Solutions**:
1. **Accept it**: Free tier limitation, nothing to fix
2. **Keep alive**: Use a service like UptimeRobot to ping every 10 minutes (not recommended, uses resources)
3. **Upgrade**: Use paid tier ($7/month) for always-on service

### Issue 5: Database Not Persisting Data

**Problem**: Using SQLite on Render free tier

**Why it happens**: Free tier containers are ephemeral - filesystem resets on each deploy

**Solution**: Upgrade to PostgreSQL:

1. **Create Render PostgreSQL database**:
   - Render Dashboard → New + → PostgreSQL
   - Copy the "Internal Database URL"

2. **Add to environment variables**:
   - Your web service → Environment
   - Add: `DATABASE_URL` = (paste internal URL)

3. **Update backend/app.py**:
   ```python
   import os
   app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///tasks.db')
   ```

4. **Add to requirements.txt**:
   ```
   psycopg2-binary==2.9.9
   ```

5. Push and redeploy.

### Issue 6: Automatic Deploys Not Working

**Problem**: Pushed to GitHub but Render didn't deploy

**Solutions**:
1. **Check Auto-Deploy is enabled**:
   - Dashboard → Your Service → Settings
   - Find "Auto-Deploy" section
   - Make sure it's set to "Yes"

2. **Check correct branch**:
   - Make sure you're pushing to the branch Render is watching
   - Default is usually `main` or `master`

3. **Manual deploy**:
   - Dashboard → Your Service → Manual Deploy
   - Click "Deploy latest commit"

### Issue 7: CORS Errors After Deployment

**Problem**: Frontend can't connect to backend API

**Solution**:
Check your `backend/app.py` has proper CORS configuration:
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins
# Or restrict to your frontend:
# CORS(app, origins=["https://your-frontend.vercel.app"])
```

---

## 🆘 General Troubleshooting

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

### Vercel: "No Output Directory named 'build' found"
This happens if the Root Directory is not set correctly:
1. Go to your Vercel project → Settings → General
2. Find "Root Directory"
3. Click "Edit" and enter: `frontend`
4. Click "Save"
5. Go to Deployments tab and redeploy
6. Alternatively, the repository includes `vercel.json` configs to help with this

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
