# 🚀 Render.com Deployment Guide
## Institutional Memory API - Production Deployment

---

## 📋 Prerequisites

Before deploying to Render.com, ensure:

- ✅ Code is pushed to GitHub
- ✅ You have a Render.com account (free tier works!)
- ✅ Branch: `claude/setup-new-project-branch-3ywS9` is up to date

---

## 🎯 Quick Deploy (Automatic with render.yaml)

We've included a `render.yaml` file that configures everything automatically!

### Step 1: Connect to Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub account if not already connected
4. Select repository: **TechRecruiter-Guru/awesome-project-mctf66nf**
5. Branch: **claude/setup-new-project-branch-3ywS9**

### Step 2: Render Reads render.yaml

Render will automatically detect `render.yaml` and configure:

✅ **Web Service**: Flask API (institutional-memory-api)
✅ **Database**: PostgreSQL (institutional-memory-db)
✅ **Environment Variables**: Automatically linked
✅ **Health Checks**: /api/health endpoint

### Step 3: Click "Apply"

Render will:
1. Create PostgreSQL database
2. Build your Python application
3. Install dependencies
4. Start the Gunicorn server
5. Link database to web service

**Build time**: ~3-5 minutes

### Step 4: Initialize Database

After first deployment completes:

1. Go to **Render Dashboard** → Your service → **Shell**
2. Run:
   ```bash
   python backend/init_db.py
   ```
3. You should see:
   ```
   Creating database tables...
   ✓ Database tables created successfully!
   ```

---

## 🔧 Manual Deploy (Alternative Method)

If you prefer to configure manually instead of using render.yaml:

### Create Web Service

1. **Dashboard** → **New +** → **Web Service**
2. **Repository**: TechRecruiter-Guru/awesome-project-mctf66nf
3. **Branch**: claude/setup-new-project-branch-3ywS9

### Configure Build Settings

```
Name: institutional-memory-api
Environment: Python 3
Region: Oregon (US West) or closest to you
Branch: claude/setup-new-project-branch-3ywS9

Build Command:
pip install -r backend/requirements.txt

Start Command:
cd backend && gunicorn app:app --bind 0.0.0.0:$PORT
```

### Add PostgreSQL Database

1. **Dashboard** → **New +** → **PostgreSQL**
2. **Name**: institutional-memory-db
3. **Database Name**: institutional_memory
4. **User**: institutional_memory_user
5. **Plan**: Free

### Link Database to Web Service

1. Go to your web service settings
2. **Environment** → **Environment Variables**
3. Add variable:
   ```
   Key: DATABASE_URL
   Value: [Select from database] → institutional-memory-db → Internal Database URL
   ```

---

## 🌐 Your Live API URL

After deployment completes, you'll get a URL like:

```
https://institutional-memory-api.onrender.com
```

**Important**: Free tier services spin down after 15 minutes of inactivity.
First request after downtime takes ~30 seconds to wake up.

---

## ✅ Verify Deployment

### 1. Health Check
```bash
curl https://your-service.onrender.com/api/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "message": "AI/ML ATS API is running",
  "version": "1.0.0"
}
```

### 2. Query API
```bash
curl https://your-service.onrender.com/api/ai-systems
```

**Expected Response**:
```json
{
  "ai_systems": [],
  "total": 0
}
```

### 3. Create First AI System
```bash
curl -X POST https://your-service.onrender.com/api/ai-systems \
  -H "Content-Type: application/json" \
  -d '{
    "ai_system_id": "test-system",
    "system_name": "Test AI System",
    "system_type": "screening",
    "decision_influence": "assistive",
    "deployment_date": "2025-01-07T00:00:00Z",
    "created_by": "admin@company.com"
  }'
```

---

## 🗄️ Database Management

### View Database

1. **Render Dashboard** → **institutional-memory-db**
2. Click **"Connect"** → Get connection string
3. Use with any PostgreSQL client (TablePlus, pgAdmin, etc.)

### Backup Database

Render free tier doesn't include automatic backups. To backup:

```bash
# From Render Shell
pg_dump $DATABASE_URL > backup.sql
```

### Database Connection String Format

```
postgresql://user:password@host:5432/database
```

---

## 📊 Monitor Your Deployment

### Logs

**Real-time logs**:
1. Dashboard → Your service → **Logs**
2. See all requests, errors, and system messages

**Useful for debugging**:
- API errors
- Database connection issues
- Request patterns

### Metrics

**Free tier includes**:
- CPU usage
- Memory usage
- Request count
- Response times

### Alerts

Set up email alerts for:
- Service crashes
- High error rates
- Deployment failures

---

## 🔐 Environment Variables (Production)

Add these in Render Dashboard → Service → Environment:

### Required
```
DATABASE_URL: [Automatically set when database linked]
PORT: [Automatically set by Render]
```

### Optional (for production)
```
FLASK_ENV: production
PYTHONUNBUFFERED: 1
```

---

## 🚨 Troubleshooting

### Build Fails

**Error**: `Could not find requirements.txt`
**Fix**: Make sure build command includes `backend/` path:
```
pip install -r backend/requirements.txt
```

### Database Connection Error

**Error**: `OperationalError: could not connect to server`
**Fix**:
1. Verify DATABASE_URL is set correctly
2. Check database is in same region as web service
3. Ensure database is running (not paused)

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'psycopg2'`
**Fix**: Verify `psycopg2-binary` is in requirements.txt

### Tables Not Created

**Error**: `no such table: ai_system_record`
**Fix**: Run database initialization:
```bash
python backend/init_db.py
```

### Service Won't Start

**Error**: `Web service exited with code 1`
**Fix**:
1. Check logs for specific error
2. Verify start command: `cd backend && gunicorn app:app --bind 0.0.0.0:$PORT`
3. Test locally first with same command

---

## 🔄 Continuous Deployment

### Automatic Deploys

Render automatically deploys when you push to GitHub:

```bash
git add .
git commit -m "Update API"
git push origin claude/setup-new-project-branch-3ywS9
```

**Render will**:
1. Detect the push
2. Start new build
3. Run tests (if configured)
4. Deploy if successful
5. Health check new deployment
6. Swap to new version

**Deploy time**: ~3-5 minutes

### Manual Deploy

Force a redeploy without code changes:

1. Dashboard → Your service
2. **Manual Deploy** → **Deploy latest commit**

---

## 💰 Pricing

### Free Tier Includes

**Web Service**:
- 750 hours/month
- 512 MB RAM
- Shared CPU
- Spins down after 15 min inactivity

**PostgreSQL**:
- 1 GB storage
- 90 days data retention
- No backups included

### When to Upgrade

Consider paid plans ($7-$25/month) when you need:
- Always-on service (no spin down)
- More RAM/CPU
- Automatic backups
- Multiple environments
- Custom domains with SSL

---

## 🎯 Post-Deployment Checklist

After successful deployment:

- [ ] Health check passes
- [ ] Database initialized (tables created)
- [ ] Can create AI system records
- [ ] Can query all endpoints
- [ ] Can generate audit packs
- [ ] Logs show no errors
- [ ] Response times acceptable
- [ ] Test with sample data

---

## 📚 API Documentation

Your live API will be available at:

```
Base URL: https://your-service.onrender.com/api
```

### Available Endpoints

```
GET  /api/health                          - Health check
GET  /api/ai-systems                      - List AI systems
POST /api/ai-systems                      - Register AI system
GET  /api/regulatory-contexts             - List regulations
POST /api/regulatory-contexts             - Create regulation snapshot
POST /api/disclosures/render              - Render disclosure
POST /api/disclosures/deliver             - Record delivery
POST /api/hiring-decisions                - Record decision
POST /api/decision-rationales             - Log rationale
POST /api/governance-approvals            - Record approval
POST /api/vendor-assertions               - Record vendor claim
POST /api/audit-packs/generate            - Generate evidence pack
```

**Full documentation**: See `INSTITUTIONAL_MEMORY_API.md`

---

## 🔗 Useful Links

- **Render Dashboard**: https://dashboard.render.com
- **GitHub Repository**: https://github.com/TechRecruiter-Guru/awesome-project-mctf66nf
- **Branch**: claude/setup-new-project-branch-3ywS9
- **Render Docs**: https://render.com/docs
- **Support**: https://render.com/support

---

## 🎊 Success!

Once deployed, you'll have:

✅ Production-grade institutional memory API
✅ PostgreSQL database with immutable records
✅ Automatic HTTPS with SSL certificate
✅ Global CDN for fast responses
✅ Continuous deployment from GitHub
✅ Real-time logs and metrics
✅ Free tier to start, easy to scale

**Your API is now live and ready to capture institutional memory for AI-era hiring decisions!**

---

## 📞 Need Help?

**Render Support**:
- Community: https://community.render.com
- Docs: https://render.com/docs
- Status: https://status.render.com

**Check Logs First**:
Most issues can be diagnosed from the Render logs dashboard.

---

**Last Updated**: 2026-01-07
**Documentation Version**: 1.0
**Render.yaml Version**: 1.0
