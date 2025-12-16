# 🔍 Diagnose Why Your Jobs Keep Disappearing

Your jobs disappearing the next day means the database is **ephemeral** (not persisting). Let's diagnose the issue step-by-step.

---

## ⚡ Quick Diagnostic (30 seconds)

### Step 1: Check Your Backend Database Status

Open this URL in your browser (replace with your actual backend URL):

```
https://YOUR-BACKEND-URL.onrender.com/api/health
```

**Example**: If your backend is `physicalai-backend.onrender.com`:
```
https://physicalai-backend.onrender.com/api/health
```

---

## 📊 Understanding the Results

### ✅ GOOD (PostgreSQL Connected):
```json
{
  "status": "healthy",
  "database": {
    "type": "PostgreSQL",
    "persistent": true,
    "accessible": true,
    "job_count": 5,
    "candidate_count": 12,
    "warning": null
  }
}
```
**What this means**: PostgreSQL is working! Your data **should** persist.

**If data is still disappearing with PostgreSQL**, check:
1. Is the same Postgres instance being used across deployments?
2. Are you accidentally deleting/recreating the Postgres database?
3. Is there a migration script running that drops tables?

---

### ❌ BAD (Still Using SQLite):
```json
{
  "status": "healthy",
  "database": {
    "type": "SQLite",
    "persistent": false,
    "job_count": 5,
    "warning": "⚠️ CRITICAL: Using SQLite - data will be lost on restart!"
  }
}
```
**What this means**: You're still using SQLite (ephemeral). Data **WILL** disappear on container restarts.

**Why this happens**:
- `DATABASE_URL` environment variable is **NOT** set on Render
- Backend can't find PostgreSQL connection
- Falls back to SQLite (which doesn't persist on cloud)

**Fix**: Follow Step 2 below to set up PostgreSQL properly.

---

## 🔧 Step 2: Fix SQLite → PostgreSQL (If Needed)

If the health check shows `"type": "SQLite"`, you need to set up PostgreSQL:

### On Render:

#### 2.1: Create PostgreSQL Database

1. **Render Dashboard** → **"New +"** → **"PostgreSQL"**
2. Fill in:
   - **Name**: `physicalai-db` (or any name)
   - **Database**: `physicalai`
   - **User**: Auto-generated
   - **Region**: **Same region as your backend** (important!)
   - **Plan**: **Free** (or Starter if you need more storage)
3. Click **"Create Database"**
4. Wait 2-3 minutes for provisioning

#### 2.2: Get the Database URL

1. Click on your newly created PostgreSQL instance
2. Scroll down to **"Connections"** section
3. Copy the **"Internal Database URL"** (starts with `postgres://`)
   - **Use INTERNAL, not EXTERNAL** (faster and free)

#### 2.3: Connect to Backend

1. Go to your **backend Web Service** in Render
2. Click **"Environment"** in the left sidebar
3. Click **"Add Environment Variable"**
4. Add:
   - **Key**: `DATABASE_URL`
   - **Value**: (paste the Internal Database URL you copied)
5. Click **"Save Changes"**
6. Render will **automatically redeploy** your backend

#### 2.4: Verify Connection

Wait 2-3 minutes for the redeploy to complete, then:

1. Check deployment logs for: `🗄️ Using PostgreSQL database (persistent)`
2. Visit `/api/health` again - should now show `"type": "PostgreSQL"`
3. Create a test job
4. Wait 24 hours or restart the service
5. Check if the job is still there ✅

---

## 🐛 Step 3: Check Backend Deployment Logs

If health check shows PostgreSQL but data still disappears:

### On Render:

1. Go to your backend service
2. Click **"Logs"** tab
3. Look for these indicators:

#### ✅ Good Signs:
```
🗄️ Using PostgreSQL database (persistent)
✅ Database tables created successfully
```

#### ❌ Bad Signs:
```
⚠️ Using SQLite database (local development only - DO NOT use in production!)
```
This means DATABASE_URL is not set correctly.

```
Database error: could not connect to server
```
This means PostgreSQL credentials are wrong or service is down.

```
relation "job" does not exist
```
This means database tables weren't created. Run initialization manually.

---

## 🔍 Step 4: Verify Environment Variables

### On Render:

1. Backend service → **"Environment"** tab
2. Verify you have:
   - ✅ `DATABASE_URL` = `postgres://...` (or `postgresql://...`)
   - ✅ `ANTHROPIC_API_KEY` = `sk-ant-api...`
3. If `DATABASE_URL` is missing → Go back to Step 2

---

## 🎯 Step 5: Manual Database Initialization (If Needed)

If tables aren't being created automatically:

### Using Render Shell:

1. Backend service → Click **"Shell"** button (top right)
2. Run:
```bash
python << EOF
from app import app, db
with app.app_context():
    db.create_all()
    print("✅ Tables created!")
EOF
```

---

## 📋 Common Issues & Solutions

### Issue: "Still showing SQLite after setting DATABASE_URL"

**Solutions**:
1. Make sure you saved the environment variable
2. Check that Render redeployed after adding it
3. Verify DATABASE_URL value starts with `postgres://` or `postgresql://`
4. Hard refresh the /api/health endpoint (Ctrl+Shift+R)

### Issue: "PostgreSQL connected but job count shows 0"

**Solutions**:
1. Tables might not be created yet - run manual initialization (Step 5)
2. You might be looking at a different environment (staging vs production)
3. Check Render logs for table creation errors

### Issue: "Database error: password authentication failed"

**Solutions**:
1. You copied the wrong database URL (use INTERNAL, not external)
2. You're using a different Postgres instance
3. Regenerate the password in Postgres settings and update DATABASE_URL

### Issue: "Data was there yesterday, gone today"

**Solutions**:
1. Check if you're still using SQLite (run health check)
2. Someone might have deleted the Postgres database
3. Check if you have multiple backend deployments pointing to different databases
4. Verify the Postgres instance is still running in Render dashboard

---

## 🆘 Emergency Data Recovery

If you lost data and need to recover:

### Option 1: Render Database Backups
1. Postgres instance → **"Backups"** tab
2. Find the most recent backup
3. Click **"Restore"**

### Option 2: Check Git History
If you committed any data exports:
```bash
git log --all --full-history -- "*.json"
```

---

## ✅ Final Checklist

- [ ] Visited `/api/health` endpoint
- [ ] Confirmed `"type": "PostgreSQL"` and `"persistent": true`
- [ ] Checked Render logs show `🗄️ Using PostgreSQL database (persistent)`
- [ ] Environment variable `DATABASE_URL` is set in Render
- [ ] PostgreSQL instance is running in Render dashboard
- [ ] Created test job and verified it persists after 24 hours

---

## 📞 Still Having Issues?

If jobs are **still** disappearing after following all steps:

1. Share the output of `/api/health`
2. Share Render deployment logs (last 50 lines)
3. Share Render environment variables list (screenshot)
4. Confirm PostgreSQL instance status in Render dashboard

The issue is almost certainly one of:
- DATABASE_URL not set correctly
- Using wrong database URL (external vs internal)
- Postgres instance not running
- Multiple backends using different databases
