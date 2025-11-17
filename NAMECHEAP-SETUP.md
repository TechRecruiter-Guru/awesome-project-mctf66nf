# Namecheap Shared Hosting Setup for SafetyCaseAI Form

This guide shows you how to set up the Strategy Call form to send emails using **PHP mail()** on Namecheap shared hosting — **no external dependencies required!**

---

## 🎯 Overview

Your Next.js app runs on **Vercel** (free tier), but the form handler runs on **Namecheap shared hosting** using native PHP `mail()` function.

**Why this approach?**
- ✅ No external services needed (Resend, SendGrid, etc.)
- ✅ No API keys to manage
- ✅ Built-in PHP mail() on all Namecheap plans
- ✅ Free - no additional costs
- ✅ Simple setup in 5 minutes

---

## 📋 Step-by-Step Setup

### **Step 1: Upload PHP File to Namecheap**

1. **Log in to Namecheap cPanel**:
   - Go to: https://www.namecheap.com → Your Account → Hosting List
   - Click "Manage" on your hosting plan
   - Click "cPanel" button

2. **Open File Manager**:
   - In cPanel, find "File Manager" under "Files" section
   - Click "File Manager"

3. **Navigate to public_html**:
   - Click on `public_html` folder (this is your website root)

4. **Upload the PHP File**:
   - Click "Upload" button at top
   - Select the file: `public/schedule-handler.php` from this project
   - Wait for upload to complete
   - Go back to File Manager

5. **Set Permissions**:
   - Right-click on `schedule-handler.php`
   - Click "Change Permissions"
   - Set to **644** (Owner: Read+Write, Group: Read, World: Read)
   - Click "Change Permissions" button

6. **Verify Upload**:
   - Visit: `https://yourdomain.com/schedule-handler.php` in browser
   - You should see: `{"success":false,"message":"Method not allowed"}`
   - This is **CORRECT** — it means the file is working (it only accepts POST requests)

---

### **Step 2: Configure Vercel Environment Variable**

1. **Go to Vercel Dashboard**:
   - Visit: https://vercel.com
   - Select your SafetyCaseAI project

2. **Add Environment Variable**:
   - Go to: Settings → Environment Variables
   - Click "Add New"
   - **Name**: `NEXT_PUBLIC_FORM_ENDPOINT`
   - **Value**: `https://yourdomain.com/schedule-handler.php`
   - Select: Production, Preview, Development
   - Click "Save"

3. **Redeploy**:
   - Go to "Deployments" tab
   - Click "..." on latest deployment
   - Click "Redeploy"
   - Wait for deployment to complete

---

### **Step 3: Test the Form**

1. **Visit Your Website**:
   - Go to: `https://your-vercel-app.vercel.app/schedule`

2. **Fill Out the Form**:
   - Enter test data (use your own email for testing)
   - Click "Schedule My Strategy Call"

3. **Check Email**:
   - Email should arrive at: **jp@physicalaipros.com**
   - Subject: "🚀 New Strategy Call: [Company Name]"
   - Should have HTML formatting with purple/blue gradient

4. **Troubleshooting** (if email doesn't arrive):
   - Check spam folder
   - Wait 5-10 minutes (shared hosting can be slow)
   - Check logs (see Troubleshooting section below)

---

## 🔧 Advanced Configuration

### **Custom "From" Email Address**

By default, emails are sent from: `noreply@yourdomain.com`

To use a custom email address:

1. **Create Email Account in cPanel**:
   - cPanel → Email Accounts
   - Create: `noreply@yourdomain.com` or `info@yourdomain.com`

2. **Edit PHP File** (optional):
   - In File Manager, right-click `schedule-handler.php`
   - Click "Edit"
   - Find line ~185: `'From: SafetyCaseAI <noreply@' . $_SERVER['HTTP_HOST'] . '>'`
   - Change to: `'From: SafetyCaseAI <your-custom@yourdomain.com>'`
   - Click "Save Changes"

---

### **CORS Configuration** (Security)

By default, the PHP file accepts requests from ANY domain (`Access-Control-Allow-Origin: *`).

**To restrict to only your Vercel domain:**

1. **Edit PHP File**:
   - Open `schedule-handler.php` in File Manager
   - Find line ~24: `header('Access-Control-Allow-Origin: *');`
   - Change to: `header('Access-Control-Allow-Origin: https://your-app.vercel.app');`
   - Click "Save Changes"

---

## 🐛 Troubleshooting

### **Emails Not Arriving?**

**1. Check PHP mail() is enabled:**
```
Create a test file: test-mail.php
```
```php
<?php
$to = 'your-email@example.com';
$subject = 'Test Email';
$message = 'This is a test email from Namecheap.';
$headers = 'From: test@yourdomain.com';

if (mail($to, $subject, $message, $headers)) {
    echo 'Email sent successfully!';
} else {
    echo 'Email failed to send.';
}
?>
```
- Upload to `public_html/test-mail.php`
- Visit: `https://yourdomain.com/test-mail.php`
- If it says "Email sent successfully" but you don't get the email:
  - Check spam folder
  - Contact Namecheap support — they may need to enable mail()

**2. Check Form Submission Logs:**
- In File Manager, check if file exists: `public_html/form-submissions.log`
- Right-click → View
- This shows all form submissions and whether emails were sent
- Format: `2025-01-15 10:30:45 - Company Name (email@example.com) - Mail sent: YES`

**3. Check PHP Error Logs:**
- In File Manager, check if file exists: `public_html/php-errors.log`
- Right-click → View
- Shows any PHP errors that occurred

**4. Common Issues:**

| Issue | Solution |
|-------|----------|
| CORS error in browser console | Add your Vercel domain to CORS header (see above) |
| "Method not allowed" | Correct! File only accepts POST requests |
| Email in spam | Common with shared hosting. Ask Namecheap to configure SPF/DKIM |
| No response from form | Check Vercel env variable is set correctly |

---

### **SPF and DKIM Records** (Reduce Spam Issues)

Emails from shared hosting often land in spam. Fix this:

1. **Log in to Namecheap Dashboard**
2. **Go to Domain List → Manage**
3. **Click "Advanced DNS"**
4. **Add SPF Record**:
   - Type: `TXT`
   - Host: `@`
   - Value: `v=spf1 include:_spf.hosting.namecheap.com ~all`
   - TTL: Automatic

5. **Enable DKIM in cPanel**:
   - cPanel → Email Deliverability
   - Click "Manage" next to your domain
   - Click "Install DKIM" if not already enabled

6. **Wait 24-48 hours** for DNS propagation

---

## 📊 File Structure

```
awesome-project-mctf66nf/
├── public/
│   └── schedule-handler.php      ← Upload this to Namecheap
├── app/
│   └── schedule/
│       └── page.tsx               ← Form (runs on Vercel)
└── NAMECHEAP-SETUP.md             ← This file
```

**On Namecheap:**
```
public_html/
├── schedule-handler.php           ← Your PHP email handler
├── form-submissions.log           ← Submission logs (auto-created)
├── php-errors.log                 ← Error logs (auto-created)
└── test-mail.php                  ← Optional test file
```

---

## ✅ Verification Checklist

- [ ] Uploaded `schedule-handler.php` to Namecheap public_html
- [ ] File permissions set to 644
- [ ] Visited PHP file URL and see "Method not allowed" message
- [ ] Added `NEXT_PUBLIC_FORM_ENDPOINT` to Vercel environment variables
- [ ] Redeployed Vercel app
- [ ] Tested form submission
- [ ] Received email at jp@physicalaipros.com
- [ ] (Optional) Configured custom "From" email address
- [ ] (Optional) Restricted CORS to only your Vercel domain
- [ ] (Optional) Set up SPF/DKIM records

---

## 🆘 Need Help?

1. **Check Logs**:
   - `form-submissions.log` — Shows all submissions
   - `php-errors.log` — Shows PHP errors

2. **Test Email Directly**:
   - Use the test-mail.php script above

3. **Contact Namecheap Support**:
   - If mail() doesn't work, Namecheap support can enable it
   - Usually enabled by default, but some plans may have it disabled

4. **Verify Environment Variable**:
   - In Vercel, check that `NEXT_PUBLIC_FORM_ENDPOINT` is set correctly
   - Make sure it starts with `https://` not `http://`

---

## 🚀 You're Done!

Your form now sends emails using Namecheap's PHP mail() function — no external dependencies, no API keys, no monthly costs!

**Next Steps:**
- Monitor `form-submissions.log` to track leads
- Set up SPF/DKIM to improve email deliverability
- Consider setting up forwarding rules in cPanel to send copies to multiple emails
