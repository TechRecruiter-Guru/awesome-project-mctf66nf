# 🔧 RENDER DEPLOYMENT FIX - Free Tier Database Limit

## ⚠️ Issue Detected

```
Error: "cannot have more than one active free tier database"
```

**Cause**: Render.com free tier allows only **1 free PostgreSQL database per account**.
You already have one active free tier database.

---

## ✅ Solution: Use Your Existing Database

I've updated `render.yaml` to skip database creation. You'll link to your existing database manually.

---

## 🚀 Deploy Now (Updated Steps)

### Step 1: Deploy Web Service Only

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"** (or manual Web Service)
3. Select: **TechRecruiter-Guru/awesome-project-mctf66nf**
4. Branch: **claude/setup-new-project-branch-3ywS9**
5. Click **"Apply"** or **"Create Web Service"**

The service will deploy but won't have a database connection yet.

### Step 2: Link Your Existing Database

1. Go to **Render Dashboard** → **institutional-memory-api**
2. Click **"Environment"** (left sidebar)
3. Click **"Add Environment Variable"**
4. Add:
   ```
   Key: DATABASE_URL
   Value: [Click dropdown and select your existing database]
   ```
5. If dropdown doesn't work, manually copy the **Internal Database URL** from your existing database

### Step 3: Redeploy

1. Go to **institutional-memory-api** → **Manual Deploy**
2. Click **"Deploy latest commit"**
3. Wait ~3 minutes for deployment

### Step 4: Initialize Database Tables

1. Go to **institutional-memory-api** → **Shell**
2. Run:
   ```bash
   python backend/init_db.py
   ```
3. You should see:
   ```
   Creating database tables...
   ✓ Database tables created successfully!
   ```

**Done!** Your API is now live! 🎉

---

## 🎯 Alternative: Manual Web Service (Skip Blueprint)

If Blueprint still has issues:

### Create Web Service Manually

1. **Dashboard** → **"New +"** → **"Web Service"**
2. Connect repository: **TechRecruiter-Guru/awesome-project-mctf66nf**
3. Branch: **claude/setup-new-project-branch-3ywS9**

### Configure:

```
Name: institutional-memory-api
Environment: Python 3
Region: Oregon (or your preferred region)
Branch: claude/setup-new-project-branch-3ywS9

Build Command:
pip install -r backend/requirements.txt

Start Command:
cd backend && gunicorn app:app --bind 0.0.0.0:$PORT
```

### Add Environment Variables:

```
Key: DATABASE_URL
Value: [Internal Database URL from your existing database]

Key: FLASK_ENV
Value: production
```

### Set Health Check:

```
Health Check Path: /api/health
```

### Click "Create Web Service"

---

## 💡 Option 2: Upgrade Database to Paid (If You Want Separate DB)

If you want a dedicated database for this project:

1. Go to your existing database
2. Click **"Upgrade"**
3. Choose **Starter Plan** ($7/month)
4. This frees up your free tier slot

Then you can deploy with the original render.yaml.

**Cost**: $7/month for the existing database + Free for new database

---

## 🔍 Find Your Existing Database

To locate your existing free tier database:

1. Go to https://dashboard.render.com
2. Click **"Databases"** in left sidebar
3. Look for a database with **"Free"** plan
4. Click it to view details
5. Copy the **"Internal Database URL"**

Format will be:
```
postgresql://user:password@dpg-xxxxx/database
```

---

## ✅ Verification After Fix

Test your deployed API:

```bash
# Health check
curl https://institutional-memory-api.onrender.com/api/health

# Should return:
{
  "status": "healthy",
  "message": "AI/ML ATS API is running"
}
```

---

## 📝 What Changed in render.yaml

**Before**: Tried to create a new free database
```yaml
databases:
  - name: institutional-memory-db
    plan: free  # ❌ Failed - already have one
```

**After**: Uses your existing database
```yaml
# Database section commented out
# You'll link manually in dashboard ✓
```

---

## 🎊 Current Deployment Status

- [x] Code pushed to GitHub ✓
- [x] render.yaml updated for existing database ✓
- [ ] Deploy web service ← **YOU ARE HERE**
- [ ] Link existing database via dashboard
- [ ] Initialize database tables
- [ ] Test API endpoints

---

## 📞 Still Having Issues?

### Database Not Showing in Dropdown?

**Solution**: Copy the database URL manually:
1. Go to your database → **"Connect"**
2. Copy **"Internal Database URL"**
3. Paste into DATABASE_URL environment variable

### Web Service Won't Start?

**Check**:
1. DATABASE_URL is set correctly
2. URL starts with `postgresql://` (not `postgres://`)
3. Check logs for specific error

### Tables Not Created?

**Run**:
```bash
python backend/init_db.py
```

In the Render Shell (not locally).

---

## 🚀 Ready to Deploy Again

Your render.yaml is now fixed. Try deploying again:

```
👉 https://dashboard.render.com
👉 New + → Blueprint (or Web Service)
👉 Deploy!
```

This time it will work! 💪
