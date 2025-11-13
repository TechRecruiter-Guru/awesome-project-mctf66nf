# 🚀 Vercel Deployment Guide for SafetyCaseAI

## Quick Deploy Steps

### 1. Go to Vercel
Visit: https://vercel.com/new

### 2. Import Your Repository
- Click "Import Git Repository"
- Select: `TechRecruiter-Guru/awesome-project-mctf66nf`
- Click "Import"

### 3. Configure Project
When Vercel detects your project:

**Root Directory:**
- Set to: `safetycaseai`
- This tells Vercel where the Next.js app is located

**Framework Preset:**
- Should auto-detect: `Next.js`

### 4. Add Environment Variables

Click "Environment Variables" and add these **TWO** variables:

#### Variable 1:
```
Name:  ANTHROPIC_API_KEY
Value: sk-ant-api03-[your-key-from-anthropic-console]
```

#### Variable 2:
```
Name:  NEXT_PUBLIC_ADMIN_PASSWORD
Value: Muses480!
```

**IMPORTANT:** Make sure to paste your actual Anthropic API key!

### 5. Deploy!
- Click "Deploy"
- Wait 2-3 minutes
- Vercel will build and deploy your app

### 6. Get Your Live URL
Once deployed, you'll get a URL like:
```
https://awesome-project-mctf66nf-[random].vercel.app
```

Or if you have a custom domain, you can add it in Vercel settings.

---

## 🎯 After Deployment

### Test Your Live Site

1. **Visit your Vercel URL**
2. **Test the landing page** - Should see all 5 robot templates
3. **Test admin login** - Go to `/admin`, password: `Muses480!`
4. **Create a test order** - Select a template and get an Order ID

### Set Up Custom Domain (Optional)

In Vercel Dashboard:
1. Go to your project
2. Click "Settings" → "Domains"
3. Add: `safetycaseai.com` (or your domain)
4. Follow DNS instructions

---

## 📊 Vercel Dashboard Features

Your Vercel dashboard shows:
- **Deployments**: Every push creates a new deployment
- **Analytics**: See how many people visit
- **Logs**: Debug any issues
- **Environment Variables**: Update API keys anytime

---

## 🔄 Future Updates

When you make changes to your code:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Your changes"
   git push
   ```

2. **Vercel auto-deploys!**
   - Every push triggers a new deployment
   - Takes 2-3 minutes
   - Gets a preview URL you can test

---

## 🐛 Common Deployment Issues

### Build Fails
- Check the build logs in Vercel
- Make sure environment variables are set correctly
- Verify the root directory is `safetycaseai`

### "Cannot find module" errors
- Vercel needs to install dependencies
- Check that `package.json` is in the `safetycaseai` folder

### API Key Issues
- Double-check `ANTHROPIC_API_KEY` is set correctly
- No spaces before/after the key
- Make sure you have Anthropic API credits

---

## 📱 What You'll Get

After deployment, you'll have:

✅ Live website accessible to anyone
✅ HTTPS (secure) by default
✅ Fast global CDN
✅ Automatic deployments on push
✅ Free SSL certificate
✅ Environment variable management
✅ Deployment previews for testing

---

## 💡 Pro Tips

1. **Use Deployment Previews**: Each branch gets its own URL
2. **Check Logs**: If something breaks, check Function Logs in Vercel
3. **Monitor Usage**: Check Analytics to see who's using your app
4. **Environment Variables**: Keep production keys separate from development

---

## 🎉 You're Ready!

Your SafetyCaseAI app will be live and accessible to customers worldwide!

**GitHub Repository:** https://github.com/TechRecruiter-Guru/awesome-project-mctf66nf
**Branch:** claude/code-session-setup-011CUvaPTZHjAztWizeDSpUV
**App Location:** /safetycaseai directory

Need help? The Vercel logs will show you exactly what's happening!
