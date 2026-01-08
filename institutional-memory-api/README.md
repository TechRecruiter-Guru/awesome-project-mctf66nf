# 🏛️ Institutional Memory API

## Compliance-as-a-Service for AI-Era Hiring Decisions

**When companies get sued, they'll wish they had this. Don't let them wait until it's too late.**

---

## 🎯 The Problem

Companies using AI in hiring face a **ticking time bomb**:

1. **AI bias lawsuits are exploding** - NYC Local Law 144, California AB 2338, EU AI Act
2. **When challenged, companies can't prove compliance** - No records of what AI was used, what disclosures were made, or why decisions happened
3. **Discovery is expensive** - $50K-$200K to reconstruct what happened 6-12 months ago
4. **Settlements happen due to fear** - Not guilt, but inability to prove innocence

---

## 💡 The Solution

**Institutional Memory API** creates time-bound, immutable records of:
- What AI systems were used
- What disclosures were delivered
- What hiring decisions were made
- **WHY decisions were made** (the rationale)

When a company gets challenged → **30-second evidence generation** instead of months of discovery.

---

## 💰 Business Model

### **Two Products, Two Revenue Streams**

#### Product 1: Your ATS (Applicant Tracking System)
- You already have this
- Sell to companies directly
- Monthly subscription or usage-based

#### Product 2: Institutional Memory API (This Product)
- **Standalone SaaS API**
- **B2B SaaS** - ATS vendors integrate and resell
- **Revenue share model** - 70/30 split with ATS partners

---

## 🎲 Revenue Model

### Who Pays:
1. **ATS vendors** (Greenhouse, Lever, etc.) - Integrate your API
2. **Enterprises** with in-house ATS systems
3. **HR tech companies** adding compliance features
4. **Staffing agencies** managing high-volume hiring

### Pricing Tiers:
```
Free:       100 decisions/month    $0
Starter:  1,000 decisions/month    $99/month
Pro:     10,000 decisions/month    $499/month
Enterprise: Unlimited              Custom
```

### Revenue Share (for ATS partners):
- **You get**: 30% of all subscription revenue
- **We get**: 70% (covers infrastructure, support, compliance updates)
- **They pay us**: Via Stripe, we send you monthly payout

---

## 🏗️ Architecture

```
┌───────────────────────────────────┐
│   Any ATS System                  │
│   (Greenhouse, Lever, YOUR ATS)   │
│                                   │
│   - Posts jobs                    │
│   - Screens candidates            │
│   - Uses AI tools                 │
│   - Makes hiring decisions        │
└────────────┬──────────────────────┘
             │ Webhooks
             │ POST events
             ▼
┌───────────────────────────────────┐
│  INSTITUTIONAL MEMORY API         │
│  (This Product - Standalone SaaS) │
│                                   │
│  - Multi-tenant                   │
│  - Records AI usage               │
│  - Captures disclosures           │
│  - Logs decision rationales       │
│  - Generates audit packs          │
└────────────┬──────────────────────┘
             │ When challenged
             ▼
┌───────────────────────────────────┐
│   AUDIT EVIDENCE PACK             │
│   Complete legal defense          │
└───────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd institutional-memory-api
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python init_db.py
```

### 3. Start API Server
```bash
python app.py
```

Server runs on: `http://localhost:5001`

### 4. Run Demo
```bash
python demo_legal_challenge.py
```

This demonstrates:
- How an ATS integrates
- What happens during legal challenge
- What the audit report looks like

---

## 📡 API Integration

### Register Company (Customer Signs Up)
```bash
curl -X POST http://localhost:5001/api/company/register \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Acme Corp",
    "plan_type": "pro"
  }'
```

**Response**:
```json
{
  "company_id": "comp_a1b2c3d4",
  "api_key": "im_live_xyz123...",
  "note": "Save this API key securely"
}
```

### Record AI Usage (When ATS enables AI)
```bash
curl -X POST http://localhost:5001/api/webhook/ai-usage \
  -H "X-API-Key: im_live_xyz123..." \
  -H "Content-Type: application/json" \
  -d '{
    "ai_system_id": "resume-ranker-v1",
    "system_name": "ResumeRanker Pro",
    "vendor_name": "VendorAI",
    "system_type": "screening",
    "decision_influence": "assistive"
  }'
```

### Record Hiring Decision
```bash
curl -X POST http://localhost:5001/api/webhook/hiring-decision \
  -H "X-API-Key: im_live_xyz123..." \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": "cand-001",
    "role_id": "job-001",
    "decision_type": "reject",
    "ai_system_id": "resume-ranker-v1",
    "decision_maker": "recruiter@company.com",
    "rationale": "Insufficient experience (2 years vs required 5)"
  }'
```

### Generate Audit Pack (When Challenged)
```bash
curl -X POST http://localhost:5001/api/audit-pack/generate \
  -H "X-API-Key: im_live_xyz123..." \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id_hash": "sha256_of_candidate_id",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31"
  }'
```

---

## 🎯 What Makes This Different

### vs. Compliance Checklists:
- ❌ They give you a list of "should dos"
- ✅ We create **provable evidence** of what you did

### vs. Legal Tech:
- ❌ They help after you're sued
- ✅ We **prevent lawsuits** by creating defensibility upfront

### vs. HR Audit Tools:
- ❌ They audit once per year
- ✅ We record **every decision in real-time**

### vs. Internal Documentation:
- ❌ Scattered emails, lost notes, "I think we did this"
- ✅ **Immutable, timestamped, complete evidence**

---

## 📊 Demo Output Example

When you run `python demo_legal_challenge.py`, you see:

```
================================================================================
  STEP 4: Generating Audit Evidence Pack
================================================================================

Generating audit pack for candidate: abc123def456...

================================================================================
  STEP 5: AUDIT REPORT - What TechCorp's Lawyer Receives
================================================================================

================================================================================
            INSTITUTIONAL MEMORY AUDIT PACK
         AI-Era Hiring Compliance Evidence Report
================================================================================

Generated: 2024-03-15T14:23:00Z
Company: TechCorp Inc
Compliance Status: DEFENSIBLE

--------------------------------------------------------------------------------
EXECUTIVE SUMMARY
--------------------------------------------------------------------------------

Total AI Systems Used:  1
Total Decisions:        3
Total Disclosures:      0 (configure disclosure tracking)

--------------------------------------------------------------------------------
AI SYSTEMS USED IN HIRING PROCESS
--------------------------------------------------------------------------------

System Name:     ResumeRanker Pro
Vendor:          VendorAI Inc
System Type:     screening
Decision Role:   assistive
Deployed:        2024-01-01T00:00:00Z

Intended Use Statement:
  Ranks candidates based on resume match to job requirements.
  Final decision made by human recruiter.

--------------------------------------------------------------------------------
HIRING DECISIONS - CANDIDATE SPECIFIC
--------------------------------------------------------------------------------

Decision ID:          decision_abc123
Candidate (hashed):  sha256_hash...
Decision Type:       REJECT
Human Involvement:   full_review
Decision Timestamp:  2024-02-15T10:30:00Z

DECISION RATIONALE (Why this decision was made):
  Type:    qualification
  Summary: Only 2 years Python experience, requirement is 5+ years.
           AI flagged insufficient experience. Recruiter reviewed
           manually and confirmed not qualified.
  By:      sarah.recruiter@techcorp.com
  When:    2024-02-15T10:35:00Z

--------------------------------------------------------------------------------
LEGAL DEFENSE POSITION
--------------------------------------------------------------------------------

Based on this evidence, TechCorp can demonstrate:

✓ AI was used in 'ASSISTIVE' capacity only
✓ Final decision made by human recruiter
✓ Specific, documented rationale exists
✓ Rejection based on objective qualification gap
✓ No evidence of discrimination based on protected class
✓ Consistent process applied to all candidates
✓ Complete institutional memory preserved

================================================================================
           END OF AUDIT REPORT
================================================================================
```

---

## 🔐 Security & Compliance

### Data Privacy:
- ✅ Candidate IDs hashed (SHA-256)
- ✅ No PII stored (names, emails, addresses)
- ✅ GDPR compliant
- ✅ SOC 2 Type II (in progress)

### Data Retention:
- ✅ 7 years minimum (EEOC requirement)
- ✅ Immutable records (append-only)
- ✅ Audit logs of all access

### Security:
- ✅ API key authentication
- ✅ Rate limiting
- ✅ TLS/HTTPS encryption
- ✅ Database encryption at rest

---

## 📚 Documentation

- **Integration Guide**: `INTEGRATION_GUIDE.md` - For ATS vendors
- **API Reference**: See `/api/health` endpoint for Swagger docs
- **Demo Script**: `demo_legal_challenge.py` - Sales demo

---

## 🚀 Deployment

### Option 1: Render.com (Free Tier)
```bash
# Uses existing render.yaml in root directory
# Connects to existing PostgreSQL database
```

### Option 2: Heroku
```bash
heroku create institutional-memory-api
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

### Option 3: AWS/GCP
- Deploy as Docker container
- Use managed PostgreSQL (RDS/Cloud SQL)
- Set DATABASE_URL environment variable

---

## 💼 Sales Pitch

### For ATS Vendors:
> "Partner with us to add compliance protection to your ATS. We handle all the infrastructure, you get 30% revenue share and a competitive advantage. Your customers get peace of mind, and you get a sticky feature that prevents churn."

### For Enterprises:
> "When you get sued for AI hiring discrimination, discovery costs $50K-$200K and takes months. With Institutional Memory, you generate complete evidence in 30 seconds. It's $499/month - pays for itself the first time you're challenged."

### For HR Tech Companies:
> "Don't build this yourself. Integrate our API in 2 hours and start generating compliance revenue tomorrow. We handle updates when regulations change (they will), you focus on your core product."

---

## 📈 Market Size

### TAM (Total Addressable Market):
- 15,000 ATS vendors globally
- $2.3B HR tech market
- 70% using AI in hiring (growing)

### Target Customers:
- **Tier 1**: Large ATS vendors (Greenhouse, Lever, Workday) - $10K-$50K/month
- **Tier 2**: Mid-market ATS ($1K-$10K/month)
- **Tier 3**: Small/custom ATS ($99-$499/month)

### Growth Strategy:
1. **Phase 1**: Direct to 10 enterprise customers ($499/month each)
2. **Phase 2**: Partner with 3-5 mid-market ATS vendors
3. **Phase 3**: Self-serve for small ATS/enterprises
4. **Phase 4**: White-label for large vendors

---

## 🎊 Project Structure

```
institutional-memory-api/
├── app.py                    # Main Flask API (multi-tenant)
├── requirements.txt          # Python dependencies
├── init_db.py               # Database initialization
├── demo_legal_challenge.py  # Sales demo script
├── INTEGRATION_GUIDE.md     # For ATS vendors
├── README.md                # This file
└── render.yaml              # Deployment config (in root)
```

---

## 🤝 Contributing

This is a commercial product. For partnership inquiries:
- **Email**: partnerships@institutional-memory.com
- **Website**: https://institutional-memory.com

---

## 📞 Support

- **Integration Support**: integrations@institutional-memory.com
- **Technical Docs**: https://docs.institutional-memory.com
- **Status Page**: https://status.institutional-memory.com

---

## 🏆 Competitive Advantages

1. **First Mover** - No one else does this (yet)
2. **Network Effects** - More ATS integrations = more valuable
3. **Regulatory Moat** - We track regulation changes, customers don't have to
4. **Technical Moat** - Time-bound truth is hard to retrofit
5. **Customer Lock-in** - Can't switch once you have 7 years of data

---

## 🎯 Next Steps

1. **Run the demo**: `python demo_legal_challenge.py`
2. **Review integration guide**: `INTEGRATION_GUIDE.md`
3. **Deploy to production**: See Deployment section
4. **Get first customer**: Start with your own ATS!

---

**Built with**: Flask, PostgreSQL, Python 3.11
**License**: Commercial - Contact for licensing
**Version**: 1.0.0

---

> "When you get sued, you'll wish you had this. Don't wait until it's too late."

**Start building defensible institutional memory today.**
