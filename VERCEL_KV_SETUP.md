# Vercel KV Setup Guide for SafetyCase.AI

This guide will help you set up Vercel KV storage to persist orders and confirmation codes across serverless function invocations.

## What Changed?

The app has been upgraded from `/tmp` file storage to **Vercel KV** (Redis-based key-value store). This fixes the issue where:
- ❌ Orders disappeared after creation
- ❌ Admin dashboard showed zero orders
- ❌ Confirmation codes weren't persisting

## Setup Steps

### Step 1: Create Vercel KV Database

1. Go to your Vercel Dashboard: https://vercel.com/dashboard
2. Click on the **"Storage"** tab in the top navigation
3. Click **"Create Database"**
4. Select **"KV"** (Key-Value Store)
5. Choose a name like: `safetycaseai-kv` or `production-kv`
6. Select your region (choose closest to your users for best performance)
7. Click **"Create"**

### Step 2: Connect KV to Your Project

1. After creating the database, you'll see the database dashboard
2. Click on the **"Connect Project"** button
3. Select your SafetyCase.AI project from the dropdown
4. Choose environment(s):
   - ✅ **Production** (required)
   - ✅ **Preview** (recommended for testing)
   - ⚠️ **Development** (optional - only if you want KV in local dev)
5. Click **"Connect"**

**Vercel will automatically add these environment variables to your project:**
- `KV_URL`
- `KV_REST_API_URL`
- `KV_REST_API_TOKEN`
- `KV_REST_API_READ_ONLY_TOKEN`

### Step 3: Redeploy Your Application

After connecting the KV database, you need to trigger a new deployment:

1. Go to your project → **Deployments** tab
2. Click on the latest deployment
3. Click the **"⋯"** menu → **"Redeploy"**
4. **IMPORTANT:** Uncheck "Use existing Build Cache"
5. Click **"Redeploy"**

OR push a new commit to trigger automatic deployment.

### Step 4: Verify It's Working

1. **Go to your app:** https://safetycaseai-platformv2.vercel.app/
2. **Create a test order:**
   - Click "Humanoid Robots"
   - Enter Company Name: "Test Company"
   - Enter Email: your email
   - Click "Continue to Payment"
   - Note your Order ID (e.g., `20250109-1234-123`)

3. **Check Admin Dashboard:**
   - Go to: https://safetycaseai-platformv2.vercel.app/admin
   - Password: `Muses480!`
   - You should see your order with company name and email
   - Click **"Generate Code"** → You'll get `UNLOCK-001`

4. **Test the full flow:**
   - Go to: https://safetycaseai-platformv2.vercel.app/upload
   - Enter the confirmation code
   - Upload a test PDF
   - Verify data extraction works

## Pricing

Vercel KV pricing:
- **Free tier:** 256 MB storage, 3,000 commands/day
- **Pro tier:** 512 MB storage, 10,000 commands/day (included in Vercel Pro)
- **Enterprise:** Custom limits

For SafetyCase.AI with low volume:
- **Free tier should be sufficient** for testing and initial launch
- Each order creates ~2-3 KV operations
- You can handle hundreds of orders per day on free tier

## Troubleshooting

### Orders still not showing up?

**Check environment variables:**
1. Go to Project → Settings → Environment Variables
2. Verify these variables exist:
   - `KV_REST_API_URL`
   - `KV_REST_API_TOKEN`
   - `KV_URL`
3. If missing, reconnect the KV database (Step 2)

**Check deployment logs:**
1. Go to Deployments → Click latest deployment
2. Scroll to "Function Logs" section
3. Look for errors mentioning "KV" or "Redis"

### Build failing?

**Clear build cache:**
1. Go to latest deployment
2. Click "⋯" → "Redeploy"
3. **Uncheck** "Use existing Build Cache"
4. Click "Redeploy"

### KV connection errors in production?

**Verify KV is connected to production:**
1. Storage tab → Your KV database
2. Click "Settings"
3. Under "Connected Projects", verify your project shows "Production" environment

## Manual Testing (Optional)

Want to verify KV is working? Use Vercel CLI:

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Test KV connection
vercel env pull .env.local

# Run locally with KV
npm run dev
```

Now local development will use your Vercel KV database.

## What Data Is Stored in KV?

### Orders (Key: `orders`)
```json
{
  "20250109-1234-123": {
    "orderId": "20250109-1234-123",
    "templateType": "humanoid",
    "email": "user@company.com",
    "companyName": "Test Company",
    "createdAt": "2025-01-09T12:34:56.789Z",
    "status": "pending_payment",
    "confirmationCode": null,
    "pdfUploaded": false,
    "htmlGenerated": false
  }
}
```

### Confirmation Codes (Key: `confirmationCodes`)
```json
{
  "UNLOCK-001": {
    "code": "UNLOCK-001",
    "orderId": "20250109-1234-123",
    "generatedAt": "2025-01-09T12:35:00.000Z",
    "used": false,
    "usedAt": null
  }
}
```

## Need Help?

If you run into issues:
1. Check Vercel deployment logs
2. Verify KV database is connected to your project
3. Ensure environment variables are set
4. Try redeploying with cache cleared

Your SafetyCase.AI app is now using persistent storage! 🎉
