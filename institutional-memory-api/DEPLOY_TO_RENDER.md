# 🚀 DEPLOY INSTITUTIONAL MEMORY API TO RENDER.COM

## Quick Deploy Instructions

### Prerequisites
- Render.com account (free tier works!)
- Repository: TechRecruiter-Guru/awesome-project-mctf66nf
- Branch: claude/setup-new-project-branch-3ywS9

---

## Step-by-Step Deployment

### 1. Create Web Service

Go to: https://dashboard.render.com

Click: **"New +"** → **"Web Service"**

### 2. Connect Repository

- Repository: `TechRecruiter-Guru/awesome-project-mctf66nf`
- Branch: `claude/setup-new-project-branch-3ywS9`

### 3. Configure Service

```
Name:              institutional-memory-api
Environment:       Python 3
Region:            Oregon (US West) or closest to you

Root Directory:    institutional-memory-api    ⭐ CRITICAL!

Build Command:     pip install -r requirements.txt

Start Command:     gunicorn app:app --bind 0.0.0.0:$PORT

Health Check Path: /api/health
```

### 4. Environment Variables

Add these in the **Environment** section:

```
PORT:          10000
FLASK_ENV:     production
```

### 5. Create Service

Click **"Create Web Service"**

Render will:
- Clone your repository
- Install dependencies
- Start the Flask server
- Give you a URL

**Deploy time**: ~3-5 minutes

---

## After Deployment

### 1. Get Your URL

You'll receive a URL like:
```
https://institutional-memory-api.onrender.com
```

### 2. Initialize Database

1. In Render Dashboard → Your service → **Shell**
2. Run:
```bash
python init_db.py
```

You should see:
```
Creating Institutional Memory database tables...
✓ Database tables created successfully!
```

### 3. Test API

```bash
# Health check
curl https://institutional-memory-api.onrender.com/api/health

# Expected response:
{
  "status": "healthy",
  "message": "Institutional Memory API is running",
  "version": "1.0.0"
}
```

### 4. Register First Company

```bash
curl -X POST https://institutional-memory-api.onrender.com/api/company/register \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Test Company",
    "plan_type": "pro"
  }'
```

You'll get back:
```json
{
  "company_id": "comp_abc123",
  "api_key": "im_live_xyz...",
  "note": "Save this API key securely"
}
```

**SAVE THAT API KEY!**

---

## Run the Demo Against Production

After deployment, you can test with real API:

```bash
cd institutional-memory-api

# Edit demo script to use production URL
# Change: BASE_URL = "http://localhost:5001/api"
# To:     BASE_URL = "https://institutional-memory-api.onrender.com/api"

python demo_legal_challenge.py
```

---

## Troubleshooting

### Build Fails

**Error**: `Could not find requirements.txt`

**Fix**: Make sure **Root Directory** is set to `institutional-memory-api`

### Service Won't Start

**Error**: `Web service exited with code 1`

**Fix**:
1. Check logs in Render dashboard
2. Verify start command: `gunicorn app:app --bind 0.0.0.0:$PORT`

### Database Error

**Error**: `no such table: company`

**Fix**: Run `python init_db.py` in the Shell

---

## What You Get

After deployment:

✅ **Live API URL**: `https://institutional-memory-api.onrender.com`
✅ **HTTPS/SSL**: Included automatically
✅ **Health monitoring**: Automatic
✅ **Logs**: Real-time in dashboard
✅ **Free tier**: $0/month to start
✅ **Auto-deploy**: On git push

---

## Free Tier Limits

**Render Free Tier**:
- 750 hours/month (25 days)
- 512 MB RAM
- Spins down after 15 min inactivity
- First request after inactivity: ~30 seconds to wake up

**Good for**: Testing, demos, initial customers

**Upgrade when**: You have paying customers and need 24/7 uptime

---

## Next: Share Your API URL

Once deployed, you can:

1. **Demo to customers**: Send them the URL
2. **Integrate with ATS**: Share webhook endpoints
3. **Generate audit packs**: Real production data
4. **Make sales**: Show live demo, not localhost

Your API is now **LIVE and PRODUCTION-READY**! 🎉

---

## Your API Endpoints

Base URL: `https://institutional-memory-api.onrender.com/api`

```
GET  /api/health                     - Health check
POST /api/company/register           - Sign up new company
POST /api/webhook/ai-usage           - Record AI usage
POST /api/webhook/hiring-decision    - Record decision
POST /api/audit-pack/generate        - Generate evidence
```

Full docs: See `institutional-memory-api/README.md`

---

**Status**: Ready to deploy ✓
**Time to deploy**: 5 minutes ⏱️
**Cost**: $0 (free tier) 💰

**GO DEPLOY IT NOW!** 🚀
