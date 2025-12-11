# 🚨 CRITICAL: Database Persistence Setup Guide

## Problem: Your Data is Disappearing!

Your work disappears because **SQLite doesn't persist on cloud platforms**. Railway, Render, and similar services have **ephemeral filesystems** - any files (including SQLite databases) are **deleted when containers restart**.

## Solution: Migrate to PostgreSQL (Persistent Database)

Your code has been updated to automatically use PostgreSQL in production while keeping SQLite for local development.

---

## 🛤️ Setup for Railway (Recommended)

### Step 1: Provision PostgreSQL Database

1. Go to your Railway project dashboard
2. Click **"+ New"** → **"Database"** → **"Add PostgreSQL"**
3. Railway will automatically:
   - Create a PostgreSQL database
   - Set the `DATABASE_URL` environment variable
   - Link it to your backend service

### Step 2: Initialize Database Schema

After provisioning, you need to create the tables. Run this command in Railway's service terminal or locally with the DATABASE_URL:

```bash
# In Railway dashboard: Click your backend service → "Settings" → "Variables" → Copy DATABASE_URL
# Then run locally (replace with your actual URL):
export DATABASE_URL="postgresql://postgres:..."
cd backend
python -c "from app import db; db.create_all(); print('✅ Database initialized!')"
```

OR use Railway's built-in terminal:
1. Click your backend service
2. Go to "Deployments" tab → Click latest deployment → "View Logs"
3. The database will auto-initialize on first deployment (check logs for "🗄️ Using PostgreSQL")

### Step 3: Verify

1. Deploy your backend
2. Check logs for: `🗄️ Using PostgreSQL database (persistent)`
3. Test by creating data, waiting a few hours, and checking if it's still there

---

## 🚂 Setup for Render

### Step 1: Create PostgreSQL Database

1. Go to Render dashboard
2. Click **"New +"** → **"PostgreSQL"**
3. Choose:
   - Name: `physicalai-db` (or any name)
   - Database: `physicalai` (or any name)
   - User: Auto-generated
   - Region: Same as your backend service
   - Instance Type: **Free** (if available) or **Starter**
4. Click **"Create Database"**

### Step 2: Link Database to Backend Service

1. Go to your backend Web Service in Render
2. Go to **"Environment"** tab
3. Add environment variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Copy the **"Internal Database URL"** from your Postgres instance
   - Click **"Save Changes"**
4. Render will automatically redeploy your backend

### Step 3: Initialize Database Schema

After the service redeploys:

**Option A: Use Render Shell**
1. Go to your backend service → Click **"Shell"** in the top right
2. Run:
```bash
python -c "from app import db; db.create_all(); print('✅ Database initialized!')"
```

**Option B: Automatic on first request**
The app will auto-initialize tables on first access (check deployment logs)

### Step 4: Verify

1. Check deployment logs for: `🗄️ Using PostgreSQL database (persistent)`
2. Test by creating data and verifying persistence

---

## 🔄 Data Migration (If You Have Existing Data in SQLite)

If you have data in local SQLite that you want to migrate to production PostgreSQL:

### Option 1: Manual Export/Import (Recommended for small datasets)

**Export from SQLite:**
```bash
# Run locally
cd backend
python << EOF
from app import db, Candidate, Job, Application, IntelligenceSubmission
import json

# Export candidates
candidates = Candidate.query.all()
with open('candidates_export.json', 'w') as f:
    json.dump([c.to_dict() for c in candidates], f)

# Export jobs
jobs = Job.query.all()
with open('jobs_export.json', 'w') as f:
    json.dump([j.to_dict() for j in jobs], f)

# Export applications (if needed)
# ... similar pattern

print("✅ Data exported!")
EOF
```

**Import to PostgreSQL:**
```bash
# Set DATABASE_URL to your production Postgres
export DATABASE_URL="postgresql://..."
cd backend

python << EOF
from app import db, Candidate, Job
import json

# Create tables
db.create_all()

# Import candidates
with open('candidates_export.json', 'r') as f:
    candidates = json.load(f)
    for c_data in candidates:
        # Create candidate with data (adjust fields as needed)
        candidate = Candidate(**c_data)
        db.session.add(candidate)

db.session.commit()
print("✅ Data imported!")
EOF
```

### Option 2: Database Migration Tools (For larger datasets)

Use `pgloader` to migrate directly:
```bash
brew install pgloader  # Mac
# or: apt-get install pgloader  # Linux

pgloader sqlite://ats.db postgresql://your-database-url
```

---

## ✅ Verification Checklist

- [ ] PostgreSQL database provisioned on Railway/Render
- [ ] `DATABASE_URL` environment variable set in backend service
- [ ] Backend redeployed with updated code
- [ ] Logs show: `🗄️ Using PostgreSQL database (persistent)`
- [ ] Database tables created (check logs or manually verify)
- [ ] Test data persists after container restarts
- [ ] No more data loss!

---

## 🆘 Troubleshooting

### Error: "No module named 'psycopg2'"
**Fix**: Redeploy after pushing the updated `requirements.txt` (already updated in this commit)

### Error: "Could not connect to database"
**Fix**: Verify `DATABASE_URL` is set correctly in environment variables. Check for typos.

### Error: "relation does not exist"
**Fix**: Tables weren't created. Run `db.create_all()` manually or check the automatic initialization in app startup logs.

### Still seeing SQLite warning in logs
**Fix**: `DATABASE_URL` environment variable is not set. Go back to Step 2 of your platform setup.

---

## 📝 Notes

- **Local Development**: Still uses SQLite (no setup needed)
- **Production**: Uses PostgreSQL (persistent storage)
- **Cost**: Railway and Render both offer **free tier PostgreSQL** (limited storage)
- **Backups**: Set up automated backups in Railway/Render dashboard (recommended)

---

## 🎯 Next Steps After Setup

1. Commit and push this fix
2. Provision PostgreSQL on your platform
3. Set `DATABASE_URL` environment variable
4. Deploy and verify in logs
5. Test data persistence
6. Celebrate - your data is now safe! 🎉
