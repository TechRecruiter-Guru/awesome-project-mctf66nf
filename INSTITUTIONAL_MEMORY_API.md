# Institutional Memory API Documentation

## AI-Era Hiring Decisions: Minimum Defensible Product (MDP)

This API implements **institutional memory for AI-era hiring decisions** - creating time-bound, immutable records that prove what your organization knew, disclosed, and decided at the moment hiring actions occurred.

---

## Core Principle

This system does NOT store "current truth."
It stores **time-bound truth**:

> What the organization knew, believed, disclosed, and approved — at the moment a hiring decision occurred.

That is what regulators, courts, and counsel evaluate.

---

## Architecture Overview

### Structural Rules (Defensibility by Design)

1. **Immutability**: Records are append-only. Corrections create new versions. Nothing is silently overwritten.
2. **Time-Bound Truth**: Every object references regulation version, system state, and disclosure language at that time.
3. **Separation of Memory**: Operational systems ≠ memory system. HR can act; memory records what happened.

### What This Model Intentionally Does NOT Do

- Does not judge fairness
- Does not score bias automatically
- Does not give legal advice
- Does not optimize hiring outcomes

**That restraint increases credibility.**

---

## Data Models

### 1. AI System Record
**Purpose**: Proves where and how AI touched hiring.

**Endpoint**: `/api/ai-systems`

**Model Fields**:
```json
{
  "ai_system_id": "unique-identifier",
  "system_name": "ResumeScreener Pro",
  "vendor_name": "AI Vendor Inc",
  "system_type": "screening | ranking | interview_analysis | assessment",
  "decision_influence": "assistive | determinative | hybrid",
  "data_inputs": "resume text, assessment scores",
  "human_override_points": "Yes - recruiter can override",
  "intended_use_statement": "Filter candidates based on minimum qualifications",
  "deployment_date": "2025-01-01T00:00:00Z",
  "retirement_date": null,
  "created_by": "recruiter@company.com",
  "version": 1
}
```

---

### 2. Regulatory Context Snapshot
**Purpose**: Captures which laws applied at that time.

**Endpoint**: `/api/regulatory-contexts`

**Model Fields**:
```json
{
  "reg_context_id": "NYC-LOCAL-LAW-144-V1",
  "jurisdiction": "New York City",
  "regulation_name": "NYC Local Law 144",
  "regulation_version": "1.0",
  "effective_start_date": "2023-07-05",
  "effective_end_date": null,
  "compliance_obligations": "{\"require_disclosure\": true, \"annual_audit\": true}",
  "source_reference": "https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page"
}
```

**Defensibility Value**: Freezes legal reality in time. Protects against retroactive enforcement narratives.

---

### 3. Disclosure Artifact
**Purpose**: Proves what was disclosed, to whom, when, and why.

**Endpoint**: `/api/disclosures`

**Model Fields**:
```json
{
  "disclosure_id": "DISC-2025-0001",
  "ai_system_id": "resume-screener-v1",
  "reg_context_id": "NYC-LOCAL-LAW-144-V1",
  "candidate_id_hash": "sha256-hash-of-candidate-id",
  "role_id": 123,
  "hiring_stage": "screening",
  "disclosure_text_rendered": "Full verbatim disclosure text shown to candidate",
  "delivery_method": "ATS | email | portal",
  "delivery_timestamp": "2025-01-07T10:00:00Z",
  "acknowledgment_status": "acknowledged | pending | not_required",
  "language_locale": "en-US"
}
```

**Defensibility Value**: Preserves historical disclosure language. Prevents "current template overwrite" risk.

---

### 4. Hiring Decision Event
**Purpose**: Anchors AI use to a real employment outcome.

**Endpoint**: `/api/hiring-decisions`

**Model Fields**:
```json
{
  "decision_event_id": "DECISION-2025-0001",
  "candidate_id_hash": "sha256-hash",
  "role_id": 123,
  "ai_system_id": "resume-screener-v1",
  "decision_type": "advance | reject | score",
  "human_involvement_level": "full_review | override | approved_ai_recommendation",
  "final_decision_maker_role": "recruiter | hiring_manager | system",
  "decision_timestamp": "2025-01-07T10:30:00Z"
}
```

**Defensibility Value**: Links AI influence to human accountability. Prevents over-attribution to automation.

---

### 5. Decision Rationale Log
**Purpose**: Captures WHY decisions were made — not just what happened.

**Endpoint**: `/api/decision-rationales`

**Model Fields**:
```json
{
  "rationale_id": "RAT-2025-0001",
  "decision_event_id": 1,
  "rationale_type": "policy | performance | qualification | override",
  "rationale_summary": "Candidate advanced due to strong technical qualifications and relevant experience",
  "supporting_artifacts": "[\"resume-id-123\", \"assessment-id-456\"]",
  "entered_by": "recruiter@company.com",
  "entered_timestamp": "2025-01-07T10:35:00Z"
}
```

**Defensibility Value**: Demonstrates human judgment. Defuses "algorithm made the decision" claims. **Most overlooked and most valuable.**

---

### 6. Governance Approval Record
**Purpose**: Proves oversight existed before issues arose.

**Endpoint**: `/api/governance-approvals`

**Model Fields**:
```json
{
  "approval_id": "APPR-2025-0001",
  "ai_system_id": "resume-screener-v1",
  "approval_type": "legal | HR | security | ethics",
  "approver_role": "General Counsel | CHRO | CISO",
  "approval_decision": "approved | conditional | denied",
  "conditions_or_exceptions": "Approved with requirement for quarterly bias audits",
  "approval_timestamp": "2024-12-15T14:00:00Z"
}
```

**Defensibility Value**: Shows proactive governance. Establishes institutional control. Protects executives individually.

---

### 7. Vendor Assertion Record
**Purpose**: Documents what vendors claimed — and what they didn't.

**Endpoint**: `/api/vendor-assertions`

**Model Fields**:
```json
{
  "vendor_assertion_id": "VENDOR-ASSERT-001",
  "ai_system_id": "resume-screener-v1",
  "assertion_type": "bias_testing | data_sourcing | accuracy",
  "assertion_statement": "System tested for adverse impact across protected categories",
  "evidence_provided": true,
  "risk_flag": "green | amber | red",
  "recorded_timestamp": "2024-12-01T00:00:00Z"
}
```

**Defensibility Value**: Shifts liability boundaries. Shows reasonable reliance. Documents known gaps explicitly.

---

## API Endpoints

### AI System Registry

#### Create AI System
```http
POST /api/ai-systems
Content-Type: application/json

{
  "ai_system_id": "resume-screener-v1",
  "system_name": "ResumeScreener Pro",
  "vendor_name": "AI Vendor Inc",
  "system_type": "screening",
  "decision_influence": "assistive",
  "intended_use_statement": "Filter candidates based on minimum qualifications",
  "deployment_date": "2025-01-01T00:00:00Z",
  "created_by": "hr@company.com"
}
```

#### Get All AI Systems
```http
GET /api/ai-systems
```

#### Get Specific AI System
```http
GET /api/ai-systems/{ai_system_id}
```

#### Retire AI System
```http
POST /api/ai-systems/{system_id}/retire
```

---

### Regulatory Context Snapshot

#### Create Regulatory Context
```http
POST /api/regulatory-contexts
Content-Type: application/json

{
  "reg_context_id": "NYC-LOCAL-LAW-144-V1",
  "jurisdiction": "New York City",
  "regulation_name": "NYC Local Law 144",
  "regulation_version": "1.0",
  "effective_start_date": "2023-07-05",
  "compliance_obligations": "{\"require_disclosure\": true}"
}
```

#### Get Regulatory Contexts
```http
GET /api/regulatory-contexts?jurisdiction=New York City&date=2025-01-07
```

---

### Disclosure Memory

#### Render Disclosure
```http
POST /api/disclosures/render
Content-Type: application/json

{
  "ai_system_id": "resume-screener-v1",
  "reg_context_id": "NYC-LOCAL-LAW-144-V1",
  "candidate_id": "candidate-123",
  "role_id": 1,
  "hiring_stage": "screening"
}
```

#### Deliver Disclosure
```http
POST /api/disclosures/deliver
Content-Type: application/json

{
  "disclosure_id": "DISC-2025-0001",
  "ai_system_id": "resume-screener-v1",
  "reg_context_id": "NYC-LOCAL-LAW-144-V1",
  "candidate_id_hash": "sha256-hash",
  "role_id": 1,
  "disclosure_text": "Full disclosure text...",
  "delivery_method": "ATS",
  "hiring_stage": "screening"
}
```

---

### Hiring Decision Event

#### Record Hiring Decision
```http
POST /api/hiring-decisions
Content-Type: application/json

{
  "decision_event_id": "DECISION-2025-0001",
  "candidate_id_hash": "sha256-hash",
  "role_id": 1,
  "ai_system_id": "resume-screener-v1",
  "decision_type": "advance",
  "human_involvement_level": "full_review",
  "final_decision_maker_role": "recruiter"
}
```

---

### Decision Rationale Log

#### Log Decision Rationale
```http
POST /api/decision-rationales
Content-Type: application/json

{
  "rationale_id": "RAT-2025-0001",
  "decision_event_id": 1,
  "rationale_type": "qualification",
  "rationale_summary": "Candidate has 5+ years experience in required technologies",
  "entered_by": "recruiter@company.com"
}
```

---

### Governance & Approval

#### Record Governance Approval
```http
POST /api/governance-approvals
Content-Type: application/json

{
  "approval_id": "APPR-2025-0001",
  "ai_system_id": "resume-screener-v1",
  "approval_type": "legal",
  "approver_role": "General Counsel",
  "approval_decision": "approved",
  "conditions_or_exceptions": "Require quarterly bias audits"
}
```

---

### Vendor Assertion Record

#### Record Vendor Assertion
```http
POST /api/vendor-assertions
Content-Type: application/json

{
  "vendor_assertion_id": "VENDOR-ASSERT-001",
  "ai_system_id": "resume-screener-v1",
  "assertion_type": "bias_testing",
  "assertion_statement": "System tested for adverse impact",
  "evidence_provided": true,
  "risk_flag": "green"
}
```

---

### Audit Evidence Export

#### Generate Audit Pack
```http
POST /api/audit-packs/generate
Content-Type: application/json

{
  "jurisdiction": "New York City",
  "start_date": "2025-01-01T00:00:00Z",
  "end_date": "2025-12-31T23:59:59Z",
  "ai_system_id": "resume-screener-v1",
  "role_id": 1
}
```

**Response**: Comprehensive evidence bundle containing:
- AI systems registry
- Regulatory contexts
- Disclosure history
- Decision logs
- Governance approvals
- Vendor assertions

---

## Event Flow: End-to-End Example

### Scenario: Candidate Screening with AI

```
1. ATS emits ai_usage_detected event
   ↓
2. System resolves AI System ID from registry
   → GET /api/ai-systems/resume-screener-v1
   ↓
3. System resolves Regulatory Context by location
   → GET /api/regulatory-contexts?jurisdiction=New York City&date=2025-01-07
   ↓
4. Disclosure rendered and delivered
   → POST /api/disclosures/render
   → POST /api/disclosures/deliver
   ↓
5. AI-assisted screening occurs
   ↓
6. Hiring Decision Event recorded
   → POST /api/hiring-decisions
   ↓
7. Decision Rationale Log appended
   → POST /api/decision-rationales
   ↓
8. Memory preserved, immutable

No reconstruction. No guesswork.
```

---

## Failure Modes (Designed For)

| Failure | Memory Response |
|---------|----------------|
| Vendor refuses transparency | `VendorAssertionRecord` flags gap |
| Law changes mid-hiring | Snapshot preserves original rule |
| Recruiter bypasses AI | Rationale log documents override |
| System decommissioned | Retirement event frozen |
| Regulator asks "why" | Intent + rationale already logged |

**This is defensive engineering.**

---

## Strategic Reality Check

This API layer does one thing extremely well:

> **It creates an authoritative, time-locked memory of AI-era hiring decisions that can be defended years later.**

That is not a feature.
That is infrastructure-grade differentiation.

---

## Why This Wins

Most vendors sell compliance claims.
**This sells provable institutional memory.**

When asked:

> "What did you know, and when did you know it?"

Your customer can answer — calmly, credibly, and with evidence.

---

## Implementation Notes

### Database
- SQLite (development)
- PostgreSQL recommended for production
- All models use SQLAlchemy ORM

### Security Considerations
- Candidate IDs are hashed (SHA-256) for privacy
- API authentication not implemented (add JWT/OAuth in production)
- Rate limiting recommended for production
- Audit logs for all write operations

### Immutability Enforcement
- All models use `created_timestamp` (auto-set)
- No UPDATE endpoints provided (append-only)
- Version tracking on AI System Records
- Database constraints prevent modifications

---

## Testing

See `backend/test_institutional_memory.py` for end-to-end workflow examples.

Run:
```bash
cd backend
python test_institutional_memory.py
```

---

## License

MIT License - See LICENSE file for details

---

## Support

For questions about institutional memory API implementation:
- GitHub Issues: [Create an issue](https://github.com/yourusername/awesome-project/issues)
- Email: contact@yourcompany.com

---

Built for defensible AI-era hiring decisions.
