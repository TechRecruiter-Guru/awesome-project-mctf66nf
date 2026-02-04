# ⚡ Supabase Setup - 5 Minute Version

## 🎯 Goal
Stop losing data! Move from SQLite → PostgreSQL in 15 minutes.

---

## ✅ Checklist

### 1. Create Supabase Account (2 min)
- [ ] Go to https://supabase.com
- [ ] Sign up with GitHub
- [ ] Create new project: `ats-production`
- [ ] Save your database password!

### 2. Get Connection String (1 min)
- [ ] Supabase → Settings → Database
- [ ] Copy "Connection string" (URI format)
- [ ] Should look like:
  ```
  postgresql://postgres:YOUR_PASSWORD@db.xxx.supabase.co:5432/postgres
  ```

### 3. Add to Render (2 min)
- [ ] Render Dashboard → ats-backend service
- [ ] Environment tab
- [ ] Add variable:
  - **Key:** `DATABASE_URL`
  - **Value:** [paste Supabase connection string]
- [ ] Save (auto-redeploys)

### 4. Initialize Database (2 min)
- [ ] Wait for Render redeploy (watch logs)
- [ ] Render → Shell tab
- [ ] Run:
  ```bash
  python -c "from app import db; db.create_all(); print('Done!')"
  ```

### 5. Add Sample Data (2 min)
- [ ] Still in Shell, run:
  ```bash
  python populate_sample_data.py
  ```

### 6. Test! (1 min)
- [ ] Visit your ATS frontend
- [ ] Should see 6 candidates, 6 jobs
- [ ] Create a test candidate
- [ ] Wait 30 min, check again - **should still be there!** ✅

---

## 🔗 Quick Links

| What | Where |
|------|-------|
| Supabase Dashboard | https://app.supabase.com |
| Render Dashboard | https://dashboard.render.com |
| Get Connection String | Supabase → Settings → Database |
| View Data | Supabase → Table Editor |

---

## ⚠️ Common Mistakes

1. **Forgot to replace `[YOUR-PASSWORD]`** in connection string
   - Copy the string, manually replace the password placeholder

2. **Added `DATABASE_URL` but service didn't redeploy**
   - Manually trigger redeploy in Render

3. **Forgot to run `db.create_all()`**
   - Tables won't exist until you initialize

4. **Used wrong connection string format**
   - Must be `postgresql://` NOT `postgres://`
   - Code handles this automatically, but use `postgresql://` anyway

---

## 🎉 Done!

Total time: **~15 minutes**
Monthly cost: **$0**
Data loss: **NEVER AGAIN** ✅

---

**Full guide:** See [MIGRATE_TO_SUPABASE.md](MIGRATE_TO_SUPABASE.md)
