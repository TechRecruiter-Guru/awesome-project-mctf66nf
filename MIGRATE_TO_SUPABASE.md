# 🚀 Migrate ATS from SQLite to Supabase PostgreSQL

## 🔴 Why This Is Critical

**Your current setup LOSES DATA because:**
- ✗ SQLite file deleted on every Render container restart
- ✗ Deployments wipe the database
- ✗ Spin-down = data loss
- ✗ No persistence on cloud platforms

**After migration:**
- ✅ Data persists forever
- ✅ Automatic backups
- ✅ Zero cost (Supabase free tier)
- ✅ Better performance
- ✅ Easy to scale

---

## ⚡ Quick Migration (15 Minutes Total)

### Step 1: Create Supabase Account (2 min)

1. Go to: **https://supabase.com**
2. Click **"Start your project"**
3. Sign up with GitHub (easiest)
4. Verify your email

### Step 2: Create Database Project (3 min)

1. Click **"New Project"**
2. Fill in details:
   ```
   Name:         ats-production
   Database Password: [Generate a strong password - SAVE THIS!]
   Region:       Choose closest to your users (e.g., US West)
   Plan:         Free ($0/month)
   ```
3. Click **"Create new project"**
4. Wait ~2 minutes for provisioning

### Step 3: Get Database Connection String (1 min)

1. In your Supabase project dashboard
2. Click **Settings** (gear icon) → **Database**
3. Scroll to **Connection string** section
4. Copy the **URI** format connection string:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```
5. Replace `[YOUR-PASSWORD]` with the password you set earlier

**Example:**
```
postgresql://postgres:MyStr0ngP@ssw0rd@db.abc123xyz.supabase.co:5432/postgres
```

### Step 4: Update Render Environment Variable (2 min)

1. Go to: **https://dashboard.render.com**
2. Select your **ats-backend** service
3. Click **Environment** tab
4. Add new environment variable:
   ```
   Key:   DATABASE_URL
   Value: postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```
5. Click **Save**

**Important:** Render will automatically redeploy with the new database!

### Step 5: Initialize Database Tables (2 min)

After Render redeploys (watch the logs):

1. In Render Dashboard → Your service → **Shell** tab
2. Run this command to create all tables:
   ```bash
   python -c "from app import db; db.create_all(); print('✅ Database initialized!')"
   ```

You should see: `✅ Database initialized!`

### Step 6: Populate Database with Sample Data (2 min)

Still in the Render Shell:

```bash
python populate_sample_data.py
```

This adds:
- 6 AI/ML candidates (Yann LeCun, Fei-Fei Li, etc.)
- 6 job positions
- 4 publications

### Step 7: Verify Everything Works (3 min)

**Test the API:**
```bash
curl https://ats-backend.onrender.com/api/health
```

Expected: `{"status":"healthy"...}`

**Check candidates:**
```bash
curl https://ats-backend.onrender.com/api/candidates
```

Should return 6 candidates!

**Test persistence:**
1. Visit your ATS frontend
2. Create a new test candidate
3. Wait 30 minutes (let Render spin down if on free tier)
4. Visit frontend again
5. **Candidate should still be there!** ✅

---

## 🎯 Verification Checklist

- [ ] Supabase project created
- [ ] Database connection string copied
- [ ] DATABASE_URL added to Render
- [ ] Render service redeployed successfully
- [ ] Database tables initialized (`db.create_all()`)
- [ ] Sample data populated
- [ ] API health check passes
- [ ] Candidates endpoint returns data
- [ ] Frontend shows candidates/jobs
- [ ] **Created test data persists after 30+ minutes** ✅

---

## 📊 View Your Data in Supabase

**Supabase has a beautiful database dashboard:**

1. Go to your Supabase project
2. Click **Table Editor** (left sidebar)
3. You'll see all your tables:
   - `candidate`
   - `job`
   - `application`
   - `publication`
   - `saved_search`

**You can:**
- View all data in a spreadsheet-like interface
- Edit records directly
- Run SQL queries
- Export to CSV
- See real-time updates

---

## 🔧 Troubleshooting

### Issue: "could not connect to server"

**Problem:** Wrong connection string

**Solution:**
1. Check DATABASE_URL in Render env vars
2. Ensure password has no special URL characters (or URL-encode them)
3. Verify Supabase project is active (not paused)

### Issue: "relation 'candidate' does not exist"

**Problem:** Tables not created

**Solution:**
```bash
# In Render Shell
python -c "from app import db; db.create_all()"
```

### Issue: "password authentication failed"

**Problem:** Wrong password in connection string

**Solution:**
1. Reset password in Supabase Settings → Database
2. Update DATABASE_URL in Render with new password
3. Redeploy

### Issue: Data still disappears

**Problem:** Still using SQLite (DATABASE_URL not set)

**Solution:**
1. Check Render logs: Look for `sqlite:///ats.db` (bad) vs `postgresql://...` (good)
2. Verify DATABASE_URL environment variable is set
3. Force redeploy in Render

---

## 💰 Cost Breakdown

### Supabase Free Tier (Forever)
- **Database Storage:** 500MB (you'll use <10MB)
- **Bandwidth:** 2GB/month (plenty for ATS)
- **API Requests:** Unlimited
- **Cost:** **$0/month** ✅

### When to Upgrade ($25/month)
- 8GB storage (500x what you need now)
- 50GB bandwidth
- Point-in-time recovery (7 days)
- Daily backups

**You won't need this for a LONG time!**

---

## 🔐 Security Best Practices

### 1. Use Environment Variables (Already Done! ✅)
```python
DATABASE_URL = os.environ.get('DATABASE_URL')  # ✅ Correct
```

### 2. Never Commit Credentials
```bash
# .gitignore already has:
.env
*.db
```

### 3. Rotate Database Password Periodically
In Supabase Settings → Database → Reset Password

---

## 🚀 Performance Comparison

### Before (SQLite)
- ✗ Lost data on restart
- ✗ Single file = bottleneck
- ✗ No concurrent writes
- ✗ No backups

### After (PostgreSQL)
- ✅ Data persists forever
- ✅ 100+ concurrent connections
- ✅ Automatic backups
- ✅ Point-in-time recovery
- ✅ 10x faster on complex queries

---

## 📝 Code Changes Made

All changes are **backward compatible** - still works locally with SQLite!

### Updated Files:
1. **backend/requirements.txt** - Added `psycopg2-binary`
2. **backend/app.py** - Uses `DATABASE_URL` environment variable

### How It Works:
```python
# Local development (no DATABASE_URL set)
DATABASE_URL = 'sqlite:///ats.db'  # ✅ Works

# Production (DATABASE_URL from Render)
DATABASE_URL = 'postgresql://...'  # ✅ Uses Supabase
```

---

## 🎓 Alternative Database Options

If you prefer something else:

### Option 2: Neon (PostgreSQL Serverless)
- Free tier: 3GB
- Setup: https://neon.tech
- Same migration steps

### Option 3: PlanetScale (MySQL)
- Free tier: 5GB
- Need to change `psycopg2` to `PyMySQL`
- Setup: https://planetscale.com

### Option 4: Render PostgreSQL ($7/mo)
- Integrated with Render
- Setup in Render Dashboard → New → PostgreSQL
- Auto-generates DATABASE_URL

---

## ✅ You're Done!

**Your ATS now has:**
- ✅ Persistent database (data never lost)
- ✅ Zero cost (Supabase free tier)
- ✅ Automatic backups
- ✅ Beautiful data viewer
- ✅ Room to scale to 1000s of candidates

**Time to migrate:** ~15 minutes
**Monthly cost:** $0
**Peace of mind:** Priceless 🎉

---

## 🆘 Need Help?

**Common Questions:**

1. **Can I migrate existing data from SQLite?**
   - SQLite likely already empty due to restarts
   - Just run `populate_sample_data.py` after migration

2. **Will this work with the free Render tier?**
   - YES! Perfect combo: Free Render + Free Supabase

3. **What if I want to switch back to SQLite?**
   - Just remove `DATABASE_URL` from Render env vars
   - (But you really shouldn't - you'll lose data again!)

4. **Can I use this for local development?**
   - Yes! Set `DATABASE_URL` in your local `.env` file
   - Or leave it unset to use SQLite locally

---

**Ready to migrate?** Follow the steps above - you'll be done in 15 minutes! 🚀
