# SafetyCase AI CRM Setup Guide

## Overview

This CRM system is built into your SafetyCase admin area with **zero npm dependencies** for email functionality. It uses native Node.js SMTP to send emails via NameCheap.

## Features

✅ **Lead Management** - Import and manage 197 curated robotics leads
✅ **Pipeline View** - Kanban-style pipeline (New → Contacted → Qualified → Nurturing → Customer → Lost)
✅ **Activity Tracking** - Log emails, calls, meetings, demos, and notes
✅ **Email Integration** - Send emails directly from the CRM using NameCheap SMTP
✅ **Email Templates** - Pre-built templates (Welcome, Follow-up, Demo Scheduled)
✅ **Lead Search & Filter** - Search by name, company, email; filter by status
✅ **Stats Dashboard** - Track conversion rates and lead metrics
✅ **Zero Dependencies** - Native Node.js SMTP (no nodemailer or external packages)

---

## Environment Variables

Create a `.env.local` file in the root directory with the following variables:

```bash
# NameCheap Private Email SMTP Configuration
SMTP_HOST=mail.privateemail.com
SMTP_PORT=465
SMTP_SECURE=true
SMTP_USER=jp@physicalaipros.com
SMTP_PASS=your_namecheap_email_password_here

# Admin Password (already configured)
NEXT_PUBLIC_ADMIN_PASSWORD=Muses480!

# Vercel KV (for data storage - already configured)
KV_REST_API_URL=your_kv_url
KV_REST_API_TOKEN=your_kv_token
```

### NameCheap Email SMTP Settings

For **NameCheap Private Email**, use these settings:

- **SMTP Host**: `mail.privateemail.com`
- **SMTP Port**: `465` (SSL) or `587` (TLS)
- **SMTP Secure**: `true` for SSL
- **Username**: Your full email address (`jp@physicalaipros.com`)
- **Password**: Your NameCheap email password

**How to get your NameCheap email password:**
1. Log into your NameCheap account
2. Go to Private Email section
3. Use your existing email password, or reset it if needed
4. Copy the password to your `.env.local` file

---

## Quick Start

### 1. Access the CRM

1. Log into the admin dashboard: `/admin`
2. Click the **"📊 CRM (197 Leads)"** button in the header
3. You'll see the CRM dashboard at `/admin/crm`

### 2. Import Your 197 Leads

On the CRM dashboard:
1. Click **"Import 197 Leads"** button
2. The system will import leads from:
   - `public/100 leads safety - Sheet1.csv`
   - `public/new_100_leads_safety.csv`
3. Duplicates (based on email) will be automatically skipped
4. View the import results and see your leads populate

### 3. Manage Leads

**List View:**
- Search leads by name, company, or email
- Filter by status (New, Contacted, Qualified, etc.)
- Click on any lead to view details
- Change lead status directly from the dropdown

**Pipeline View:**
- Switch to Kanban-style pipeline view
- See leads organized by stage
- Quick overview of pipeline health

### 4. Send Emails

From any lead detail page:
1. Click **"📧 Send Email"**
2. Choose a template or write a custom email:
   - **Welcome Email** - Initial outreach
   - **Follow-up Email** - Follow up on previous contact
   - **Custom Email** - Write your own
3. Templates automatically populate with lead details (name, company)
4. Click **"Send Email"** to send via NameCheap SMTP
5. Email activity is automatically logged

### 5. Log Activities

Track all interactions with leads:
- **Email** - Sent emails
- **Call** - Phone calls
- **Meeting** - In-person or virtual meetings
- **Demo** - Product demonstrations
- **Note** - General notes

Each activity can include:
- Subject
- Notes
- Outcome
- Follow-up date

---

## File Structure

```
app/
├── admin/
│   ├── crm/
│   │   ├── page.tsx                    # CRM Dashboard
│   │   └── leads/
│   │       └── [id]/
│   │           └── page.tsx            # Lead Detail Page
│   └── page.tsx                        # Admin Dashboard (with CRM link)
├── api/
│   └── crm/
│       ├── leads/route.ts              # Lead CRUD API
│       ├── activities/route.ts         # Activity CRUD API
│       ├── import/route.ts             # CSV Import API
│       └── send-email/route.ts         # Email Sending API

lib/
├── types.ts                            # TypeScript interfaces
├── leadManager.ts                      # Lead/Activity data management
├── csvParser.ts                        # CSV parsing (zero dependencies)
└── emailer.ts                          # Native Node.js SMTP mailer

public/
├── 100 leads safety - Sheet1.csv       # 100 leads
└── new_100_leads_safety.csv            # 96 leads
```

---

## API Endpoints

### Leads
- `GET /api/crm/leads` - Fetch all leads (with optional filters)
- `GET /api/crm/leads?stats=true` - Fetch CRM statistics
- `POST /api/crm/leads` - Create a new lead
- `PUT /api/crm/leads` - Update an existing lead
- `DELETE /api/crm/leads?id={leadId}` - Delete a lead

### Activities
- `GET /api/crm/activities` - Fetch all activities
- `GET /api/crm/activities?leadId={leadId}` - Fetch activities for a lead
- `POST /api/crm/activities` - Create a new activity
- `PUT /api/crm/activities` - Update an activity
- `DELETE /api/crm/activities?id={activityId}` - Delete an activity

### Import
- `GET /api/crm/import` - Get available CSV files
- `POST /api/crm/import` - Import leads from CSV files

### Email
- `GET /api/crm/send-email` - Get available email templates
- `POST /api/crm/send-email` - Send email to a lead

---

## Email Templates

### Welcome Email
```
Subject: Welcome to SafetyCase AI - {name}

Hi {name},

Thank you for your interest in SafetyCase AI!

We noticed you work at {company}, and we'd love to show you how our
AI-powered robot safety documentation platform can help streamline
your compliance process.

Would you be available for a quick 15-minute demo this week?

Best regards,
The SafetyCase AI Team
jp@physicalaipros.com
```

### Follow-up Email
```
Subject: Following up - SafetyCase AI Demo

Hi {name},

I wanted to follow up on my previous email about SafetyCase AI.

We're helping companies like {company} automate their robot safety
documentation and compliance workflows.

Are you available for a brief call to discuss how we can help?

Best regards,
The SafetyCase AI Team
jp@physicalaipros.com
```

You can customize these templates in `/lib/emailer.ts` (search for `getEmailTemplates()`).

---

## Lead CSV Format

Your CSV files should have the following columns:

| Column | Description |
|--------|-------------|
| Person | Contact name (e.g., "Alexandre Resende") |
| Company | Company name (e.g., "RobCo") |
| Email | Contact email (e.g., "alexandre@robco.de") |
| Website | Company website (e.g., "https://robco.de") |
| Why Selected | Reason for selection (e.g., "CTO of Series B cobot...") |

---

## Troubleshooting

### Email Not Sending

1. **Check environment variables**:
   ```bash
   # Verify .env.local has correct values
   SMTP_HOST=mail.privateemail.com
   SMTP_PORT=465
   SMTP_USER=jp@physicalaipros.com
   SMTP_PASS=your_password
   ```

2. **Verify NameCheap email is active**:
   - Log into NameCheap
   - Ensure Private Email subscription is active
   - Test sending an email from NameCheap webmail

3. **Check SMTP port**:
   - Port 465 = SSL (recommended)
   - Port 587 = TLS (alternative)
   - Some networks block these ports

4. **View error logs**:
   - Check the browser console (F12)
   - Check Vercel deployment logs
   - Look for SMTP error messages

### Leads Not Importing

1. **Verify CSV files exist**:
   ```bash
   ls public/*.csv
   ```

2. **Check CSV format**:
   - Files must have header row
   - Required columns: Person, Company, Email
   - UTF-8 encoding

3. **Check Vercel KV**:
   - Ensure Vercel KV is set up
   - Check KV_REST_API_URL and KV_REST_API_TOKEN in environment variables

---

## Alternative: PHP Email Sender

If you prefer to use **PHPMailer** as mentioned, here's a simple PHP script you can use:

**Create `send_email.php` in your project root:**

```php
<?php
// Simple PHPMailer alternative using native PHP mail()
// Or download PHPMailer from: https://github.com/PHPMailer/PHPMailer

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

$data = json_decode(file_get_contents('php://input'), true);

$to = $data['to'] ?? '';
$subject = $data['subject'] ?? '';
$message = $data['message'] ?? '';
$from = 'jp@physicalaipros.com';

if (!$to || !$subject || !$message) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing required fields']);
    exit;
}

$headers = [
    'From: ' . $from,
    'Reply-To: ' . $from,
    'X-Mailer: PHP/' . phpversion(),
    'Content-Type: text/plain; charset=UTF-8'
];

$success = mail($to, $subject, $message, implode("\r\n", $headers));

if ($success) {
    echo json_encode(['success' => true]);
} else {
    http_response_code(500);
    echo json_encode(['error' => 'Failed to send email']);
}
?>
```

Then update the email API to call this PHP script instead.

---

## Next Steps

1. **Set up environment variables** (`.env.local` with NameCheap SMTP credentials)
2. **Import your 197 leads** using the CRM dashboard
3. **Start reaching out** using email templates
4. **Track activities** for each lead interaction
5. **Move leads through pipeline** as they progress
6. **Monitor conversion rates** on the stats dashboard

---

## Support

For issues or questions:
- Check Vercel deployment logs
- Review browser console errors (F12)
- Ensure all environment variables are set
- Verify NameCheap email account is active

---

**Built with zero npm dependencies for email** ✅
**Native Node.js TLS/Net SMTP** 🚀
**NameCheap Private Email Ready** 📧
