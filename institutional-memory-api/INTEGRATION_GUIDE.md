# 🔌 Institutional Memory API - Integration Guide for ATS Vendors

## For: Greenhouse, Lever, Workday, SmartRecruiters, and Custom ATS Systems

---

## 🎯 What This API Does

The Institutional Memory API provides **compliance-as-a-service** for AI-era hiring. When your ATS customers get legally challenged, they need instant proof of what AI they used, what disclosures they made, and why decisions were made.

**Your ATS** handles day-to-day hiring.
**Our API** creates defensible institutional memory.

---

## 💰 Business Model

### For You (ATS Vendor):
- **No upfront costs** - We handle all infrastructure
- **Revenue share** - We split subscription fees 70/30
- **Competitive advantage** - "Built-in compliance protection"
- **Customer retention** - Sticky feature that prevents churn

### Pricing (You charge your customers):
- **Free tier**: 100 decisions/month
- **Starter**: $99/month - 1,000 decisions
- **Pro**: $499/month - 10,000 decisions
- **Enterprise**: Custom pricing

---

## 🚀 Quick Start Integration

### Step 1: Register Your Company

```bash
curl -X POST https://api.institutional-memory.com/api/company/register \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Acme Corp (via Greenhouse)",
    "plan_type": "pro"
  }'
```

**Response**:
```json
{
  "company_id": "comp_a1b2c3d4",
  "api_key": "im_live_xyz123...",
  "note": "Save this API key - it won't be shown again"
}
```

### Step 2: Store API Key Securely

Store this API key in your database for the customer account.

### Step 3: Send Events via Webhooks

Whenever AI is used in hiring, send us an event.

---

## 📡 Integration Points

### Event 1: AI System Usage

When a customer enables AI screening/ranking in your ATS:

```javascript
// In your ATS code
async function enableAIScreening(jobId, aiSettings) {
  // Your normal ATS logic
  await activateAIForJob(jobId, aiSettings);

  // Send to Institutional Memory API
  await fetch('https://api.institutional-memory.com/api/webhook/ai-usage', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': customer.institutionalMemoryApiKey
    },
    body: JSON.stringify({
      ai_system_id: aiSettings.systemId,
      system_name: aiSettings.name,
      vendor_name: aiSettings.vendor,
      system_type: 'screening', // or 'ranking', 'interview_analysis'
      decision_influence: 'assistive', // or 'determinative', 'hybrid'
      intended_use_statement: aiSettings.usageDescription,
      deployment_date: new Date().toISOString()
    })
  });
}
```

### Event 2: Hiring Decision Made

When a recruiter/AI makes a hiring decision:

```javascript
// In your ATS code
async function makeHiringDecision(candidateId, decision, rationale) {
  // Your normal ATS logic
  await updateCandidateStatus(candidateId, decision.status);

  // Send to Institutional Memory API
  await fetch('https://api.institutional-memory.com/api/webhook/hiring-decision', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': customer.institutionalMemoryApiKey
    },
    body: JSON.stringify({
      candidate_id: candidateId,
      role_id: decision.jobId,
      decision_type: decision.status, // 'advance', 'reject', 'score'
      ai_system_id: decision.aiSystemId,
      decision_maker: decision.recruiterId,
      decision_maker_role: 'recruiter',
      rationale: rationale.text,
      rationale_type: rationale.type // 'qualification', 'policy', 'performance'
    })
  });
}
```

---

## 🎯 Complete Example: Greenhouse Integration

```javascript
// greenhouse-integration.js

const INSTITUTIONAL_MEMORY_API = 'https://api.institutional-memory.com/api';

class InstitutionalMemoryIntegration {
  constructor(apiKey) {
    this.apiKey = apiKey;
  }

  async recordAIUsage(job, aiTool) {
    return await fetch(`${INSTITUTIONAL_MEMORY_API}/webhook/ai-usage`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': this.apiKey
      },
      body: JSON.stringify({
        ai_system_id: aiTool.id,
        system_name: aiTool.name,
        vendor_name: aiTool.vendor,
        system_type: aiTool.type,
        decision_influence: aiTool.influence,
        intended_use_statement: aiTool.description
      })
    });
  }

  async recordDecision(candidate, job, decision, recruiter) {
    return await fetch(`${INSTITUTIONAL_MEMORY_API}/webhook/hiring-decision`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': this.apiKey
      },
      body: JSON.stringify({
        candidate_id: candidate.id,
        role_id: job.id,
        decision_type: decision.action,
        ai_system_id: decision.usedAI ? decision.aiSystemId : null,
        decision_maker: recruiter.email,
        rationale: decision.notes
      })
    });
  }

  async generateAuditPack(candidateId) {
    const candidateHash = await this.hashCandidateId(candidateId);

    return await fetch(`${INSTITUTIONAL_MEMORY_API}/audit-pack/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': this.apiKey
      },
      body: JSON.stringify({
        candidate_id_hash: candidateHash
      })
    });
  }

  async hashCandidateId(candidateId) {
    const encoder = new TextEncoder();
    const data = encoder.encode(candidateId);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }
}

// Usage in Greenhouse
const integration = new InstitutionalMemoryIntegration(
  customer.settings.institutionalMemoryApiKey
);

// When AI screening is enabled
await integration.recordAIUsage(job, aiScreeningTool);

// When recruiter makes decision
await integration.recordDecision(candidate, job, decision, recruiter);

// When legal challenge arrives
const auditPack = await integration.generateAuditPack(candidate.id);
```

---

## 📊 What Your Customers Get

### Before Legal Challenge:
- Automatic compliance tracking
- Zero extra work for recruiters
- Peace of mind

### During Legal Challenge:
- **30-second evidence generation**
- Complete audit trail
- Defensible position
- Professional audit report

### Sample Audit Report:

```
================================================================
     INSTITUTIONAL MEMORY AUDIT PACK
     AI-Era Hiring Compliance Evidence Report
================================================================

Company: Acme Corp
Generated: 2024-03-15 14:23:00 UTC
Compliance Status: DEFENSIBLE

EXECUTIVE SUMMARY
-----------------------------------------------------------------
Total AI Systems Used:  1
Total Decisions:        3
Total Disclosures:      3

AI SYSTEMS USED
-----------------------------------------------------------------
System Name:     ResumeRanker Pro
Vendor:          VendorAI Inc
Decision Role:   assistive
Deployed:        2024-01-01

HIRING DECISIONS - CANDIDATE SPECIFIC
-----------------------------------------------------------------
Decision: REJECT
Timestamp: 2024-02-15 10:30:00
Human Involvement: full_review

RATIONALE:
  Type: qualification
  Summary: "Only 2 years Python experience, requirement is 5+ years.
           AI flagged insufficient experience. Recruiter reviewed
           manually and confirmed not qualified."
  By: sarah.recruiter@acme.com

LEGAL DEFENSE POSITION
-----------------------------------------------------------------
✓ AI used in assistive capacity only
✓ Final decision made by human recruiter
✓ Specific, documented rationale exists
✓ No evidence of discrimination
✓ Consistent process applied
================================================================
```

---

## 🔒 Security & Privacy

### API Authentication:
- All requests require `X-API-Key` header
- Keys are unique per customer
- Keys can be rotated instantly

### Data Privacy:
- Candidate IDs are hashed (SHA-256)
- No PII stored (names, emails, addresses)
- GDPR compliant
- SOC 2 Type II certified

### Data Retention:
- **7 years** minimum (matches EEOC requirements)
- Immutable records (append-only)
- Audit logs of all access

---

## 💻 API Reference

### Base URL
```
Production: https://api.institutional-memory.com/api
Sandbox:    https://sandbox.institutional-memory.com/api
```

### Authentication
```
Header: X-API-Key: im_live_your_api_key_here
```

### Endpoints

#### POST /webhook/ai-usage
Register AI system usage

**Request**:
```json
{
  "ai_system_id": "unique-system-id",
  "system_name": "ResumeRanker Pro",
  "vendor_name": "VendorAI Inc",
  "system_type": "screening",
  "decision_influence": "assistive",
  "intended_use_statement": "Ranks candidates by resume match"
}
```

**Response**:
```json
{
  "status": "recorded",
  "ai_system_id": "unique-system-id",
  "message": "AI usage recorded in institutional memory"
}
```

#### POST /webhook/hiring-decision
Record hiring decision

**Request**:
```json
{
  "candidate_id": "cand-12345",
  "role_id": "job-67890",
  "decision_type": "reject",
  "ai_system_id": "unique-system-id",
  "decision_maker": "recruiter@company.com",
  "rationale": "Insufficient experience (2 years vs required 5)"
}
```

**Response**:
```json
{
  "status": "recorded",
  "decision_event_id": "decision_abc123",
  "message": "Hiring decision recorded in institutional memory"
}
```

#### POST /audit-pack/generate
Generate compliance audit pack

**Request**:
```json
{
  "candidate_id_hash": "sha256_hash_of_candidate_id",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```

**Response**: Complete audit evidence (see example above)

---

## 🎓 Testing & Sandbox

### Sandbox Environment
```
URL: https://sandbox.institutional-memory.com/api
Free unlimited testing
No production data
```

### Test API Key
```
X-API-Key: im_test_sandbox_key_12345
```

### Example Test
```bash
curl -X POST https://sandbox.institutional-memory.com/api/webhook/hiring-decision \
  -H "X-API-Key: im_test_sandbox_key_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": "test-candidate-001",
    "decision_type": "reject",
    "rationale": "Test decision for integration testing"
  }'
```

---

## 📞 Support

### Integration Support:
- **Email**: integrations@institutional-memory.com
- **Slack**: Join our ATS Partners channel
- **Docs**: https://docs.institutional-memory.com

### Technical Support:
- **Response time**: < 4 hours
- **Phone**: Available for Enterprise tier
- **Status**: https://status.institutional-memory.com

---

## 🚀 Go-To-Market

### Sales Messaging:

**For Your Sales Team**:
> "Our ATS now includes built-in compliance protection powered by Institutional Memory. When your company gets challenged on AI hiring practices, you'll have instant, complete evidence - not months of discovery and expensive legal bills."

**For Your Customers**:
> "We've partnered with Institutional Memory to give you peace of mind. Every AI-assisted decision is automatically documented with complete audit trails. When (not if) you face a compliance inquiry, you'll have professional evidence ready in 30 seconds."

### ROI Calculation:

**Cost of NOT having this**:
- Average discrimination lawsuit: $50,000 - $200,000
- Discovery costs: $20,000 - $75,000
- Time spent reconstructing evidence: 40-80 hours
- Settlement risk due to missing evidence: High

**Cost of having this**:
- $99-$499/month
- Zero extra work
- Instant evidence
- Strong defense position

---

## 🎊 Ready to Integrate?

1. **Sign up**: https://institutional-memory.com/partners
2. **Get sandbox access**: Test integration risk-free
3. **Review integration guide**: 2-hour implementation
4. **Launch**: Start generating revenue

**Questions?** Contact: partners@institutional-memory.com

---

**Built for**: Greenhouse, Lever, Workday, SmartRecruiters, iCIMS, JazzHR, BambooHR, and custom ATS systems

**Compliance**: GDPR, SOC 2, EEOC, NYC Local Law 144, California AB 2338
