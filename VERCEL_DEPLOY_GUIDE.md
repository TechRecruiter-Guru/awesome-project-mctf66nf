# 🚀 Vercel Web Dashboard Deployment Guide

## Step-by-Step Instructions for SafetyCase.AI

### Step 1: Go to Vercel New Project Page

Open this URL in your browser:
```
https://vercel.com/new
```

---

### Step 2: Import Your Repository

1. You'll see "Import Git Repository"
2. Look for: **TechRecruiter-Guru/awesome-project-mctf66nf**
3. Click the **"Import"** button next to it

*If you don't see your repo:*
- Click "Adjust GitHub App Permissions"
- Make sure this repository has access

---

### Step 3: Configure Project (MOST IMPORTANT!)

You'll see a configuration screen. Here's what to set:

#### **Framework Preset**
- Should auto-detect: **Next.js**
- ✅ Leave this as is

#### **Root Directory** ⚠️ CRITICAL STEP
1. Look for the "Root Directory" section
2. You'll see it says `./` or shows `frontend` and `backend` options
3. Click **"Edit"** or **"Include source files outside of the Root Directory in the Build Step"**
4. A text box will appear
5. Type exactly: `safetycaseai`
6. You should see: `awesome-project-mctf66nf/safetycaseai` ✓

#### **Build and Output Settings**
These should auto-fill:
- Build Command: `npm run build` ✓
- Output Directory: `.next` ✓
- Install Command: `npm install` ✓

✅ Leave these as default!

---

### Step 4: Add Environment Variables

Scroll down to **"Environment Variables"** section:

#### **Variable 1: Anthropic API Key**

1. Click "Add" or the input field
2. **Name:** `ANTHROPIC_API_KEY`
3. **Value:** `sk-ant-api03-[your-actual-key-here]`
4. **Environment:** Select all (Production, Preview, Development)

#### **Variable 2: Admin Password**

1. Click "Add" again
2. **Name:** `NEXT_PUBLIC_ADMIN_PASSWORD`
3. **Value:** `Muses480!`
4. **Environment:** Select all (Production, Preview, Development)

---

### Step 5: Deploy! 🚀

1. Double-check:
   - ✅ Root Directory = `safetycaseai`
   - ✅ Two environment variables added
   - ✅ Framework = Next.js

2. Click the big **"Deploy"** button

3. Wait 2-3 minutes while Vercel:
   - Clones your repository
   - Installs dependencies
   - Builds your Next.js app
   - Deploys to production

---

### Step 6: Get Your Live URL

Once deployment completes, you'll see:

```
🎉 Congratulations! Your project has been deployed!
```

Your URL will be something like:
```
https://awesome-project-mctf66nf-[random-hash].vercel.app
```

**Or if you have a custom domain setup:**
```
https://safetycaseai.vercel.app
```

---

## ✅ Testing Your Deployment

### Test 1: Landing Page
Go to your Vercel URL - you should see:
- SafetyCase.AI header
- 5 robot template cards
- Beautiful gradient hero section

### Test 2: Admin Login
1. Go to: `[your-url]/admin`
2. Password: `Muses480!`
3. Should see admin dashboard

### Test 3: Create Order
1. Click any template on homepage
2. Should see payment instructions
3. Note the Order ID

### Test 4: Generate Code
1. In admin dashboard
2. Find your test order
3. Click "Generate Code"
4. Should see: `UNLOCK-001`

### Test 5: Full Workflow
1. Go to `/upload`
2. Enter code: `UNLOCK-001`
3. Upload a PDF (or test without)
4. Preview and download HTML

---

## 🐛 Troubleshooting

### "Build Failed" Error

**Check the logs:**
1. Click "View Function Logs"
2. Look for error messages

**Common fixes:**
- Make sure Root Directory is `safetycaseai`
- Check environment variables are correct
- Verify no typos in API key

### "Cannot find module" Error

**This means Root Directory is wrong!**
1. Go to Project Settings
2. Click "General"
3. Find "Root Directory"
4. Edit to: `safetycaseai`
5. Redeploy

### "ANTHROPIC_API_KEY is not configured"

**Environment variable issue:**
1. Go to Project Settings
2. Click "Environment Variables"
3. Add or fix `ANTHROPIC_API_KEY`
4. Redeploy

### Root Directory Not Showing Text Box

If you only see `frontend` and `backend` radio buttons:

**Method 1:**
1. Select either one (doesn't matter)
2. Click Continue
3. On next screen, look for "Root Directory" edit option
4. Change it to `safetycaseai`

**Method 2:**
1. Don't select anything
2. Scroll down past the radio buttons
3. Look for "Override" or "Edit" link
4. Click it to reveal text input
5. Type `safetycaseai`

---

## 📊 After Successful Deployment

You'll have access to:

### Vercel Dashboard Features

**Deployments Tab:**
- See all your deployments
- Every git push = new deployment
- Preview URLs for testing

**Analytics Tab:**
- Visitor statistics
- Page views
- Performance metrics

**Logs Tab:**
- Function execution logs
- Error messages
- Debug information

**Settings Tab:**
- Environment variables
- Custom domains
- Build settings

---

## 🔄 Future Updates

Every time you push to GitHub:
1. Vercel automatically deploys
2. Creates a preview URL
3. You can test before promoting to production

To update your live site:
```bash
# Make changes locally
git add .
git commit -m "Update SafetyCase.AI"
git push

# Vercel automatically deploys! ✨
```

---

## 📝 Deployment Checklist

Before you click Deploy:

- ✅ Root Directory: `safetycaseai`
- ✅ Framework: Next.js
- ✅ Environment Variable 1: `ANTHROPIC_API_KEY` = your API key
- ✅ Environment Variable 2: `NEXT_PUBLIC_ADMIN_PASSWORD` = `Muses480!`
- ✅ Build Command: `npm run build`
- ✅ Output Directory: `.next`

---

## 🎯 Quick Reference

**Your Repository:**
https://github.com/TechRecruiter-Guru/awesome-project-mctf66nf

**Branch to Deploy:**
`claude/code-session-setup-011CUvaPTZHjAztWizeDSpUV`

**Root Directory:**
`safetycaseai`

**Environment Variables:**
```
ANTHROPIC_API_KEY=sk-ant-api03-...
NEXT_PUBLIC_ADMIN_PASSWORD=Muses480!
```

**Get Anthropic API Key:**
https://console.anthropic.com/settings/keys

---

## 🎉 You're Ready!

Go to https://vercel.com/new and follow the steps above!

Your SafetyCase.AI app will be live in 2-3 minutes! 🚀
