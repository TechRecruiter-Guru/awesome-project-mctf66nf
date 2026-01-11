# Sample Audit Pack - Defensible Hiring AI
## NYC Local Law 144 Compliance Documentation

**Generated:** January 9, 2026 at 14:32 UTC
**Company:** Acme Corporation (REDACTED)
**Request ID:** audit-pack-20260109-1432
**Audit Period:** January 1, 2025 - December 31, 2025

---

## ⚖️ EXECUTIVE SUMMARY

This audit pack provides complete documentation of AI hiring system usage and decision-making processes for Acme Corporation during the audit period specified above.

All records are **immutable, timestamped, and cryptographically signed** to ensure authenticity and prevent tampering.

**Compliance Status:** ✅ COMPLIANT with NYC Local Law 144

---

## 📊 AI SYSTEMS REGISTERED

| AI System ID | System Name | Vendor | Type | Deployment Date | Decision Influence |
|--------------|-------------|--------|------|-----------------|-------------------|
| ai-sys-001 | Resume Screening AI | Greenhouse | Resume Screening | 2024-03-15 | HIGH - Auto-rejects candidates below threshold |
| ai-sys-002 | Video Interview Analyzer | HireVue | Video Analysis | 2024-06-01 | MEDIUM - Provides recommendation scores |
| ai-sys-003 | Skill Assessment Engine | Criteria Corp | Assessment Scoring | 2023-11-20 | HIGH - Gates advancement to interview stage |

**Bias Audit Status:**
- ai-sys-001: Last audited 2025-10-15 (Pass - No disparate impact detected)
- ai-sys-002: Last audited 2025-09-22 (Pass - Within acceptable variance)
- ai-sys-003: Last audited 2025-11-30 (Pass - Compliant with EEOC guidelines)

**Public Disclosure:** ✅ Posted at acmecorp.com/ai-hiring-disclosure

---

## 📋 HIRING DECISIONS LOG (Sample - 5 of 1,247 records)

### Decision #1
**Timestamp:** 2025-03-15 09:23:41 UTC
**Candidate ID:** hash-a1b2c3d4 (SHA-256 hashed for privacy)
**Role:** Software Engineer - Backend
**Decision:** REJECTED
**AI Systems Used:** ai-sys-001 (Resume Screening AI)
**Human Decision Maker:** hiring-manager-42 (John D., Engineering Manager)
**Disclosure Sent:** ✅ 2025-03-10 14:22:01 UTC (email confirmation logged)

**AI Recommendation:** REJECT (Score: 42/100 - Below 60 threshold)
**Human Override:** NO
**Final Decision:** REJECTED - Resume did not meet minimum qualifications

**Evidence Trail:**
- Resume submitted: 2025-03-10 14:22:00 UTC
- AI processing completed: 2025-03-10 14:22:05 UTC
- Disclosure email sent: 2025-03-10 14:22:01 UTC
- Human review: 2025-03-15 09:23:30 UTC
- Final decision logged: 2025-03-15 09:23:41 UTC

---

### Decision #2
**Timestamp:** 2025-04-22 16:45:12 UTC
**Candidate ID:** hash-e5f6g7h8
**Role:** Product Manager
**Decision:** ADVANCED TO INTERVIEW
**AI Systems Used:** ai-sys-002 (Video Interview Analyzer)
**Human Decision Maker:** hiring-manager-18 (Sarah K., Product Director)
**Disclosure Sent:** ✅ 2025-04-18 10:15:33 UTC

**AI Recommendation:** ADVANCE (Score: 78/100 - Confidence, Communication positive)
**Human Override:** NO
**Final Decision:** ADVANCED - Strong video interview performance

---

### Decision #3
**Timestamp:** 2025-07-08 11:12:05 UTC
**Candidate ID:** hash-i9j0k1l2
**Role:** Data Analyst
**Decision:** HIRED
**AI Systems Used:** ai-sys-001, ai-sys-003
**Human Decision Maker:** hiring-manager-09 (Michael R., Analytics Lead)
**Disclosure Sent:** ✅ 2025-06-30 08:44:19 UTC

**AI Recommendation:** HIRE (Resume: 89/100, Skills Test: 92/100)
**Human Override:** NO
**Final Decision:** HIRED - Excellent technical fit

---

### Decision #4 (Human Override Example)
**Timestamp:** 2025-09-14 13:28:47 UTC
**Candidate ID:** hash-m3n4o5p6
**Role:** UX Designer
**Decision:** ADVANCED TO INTERVIEW
**AI Systems Used:** ai-sys-001 (Resume Screening AI)
**Human Decision Maker:** hiring-manager-27 (Lisa T., Design Manager)
**Disclosure Sent:** ✅ 2025-09-10 09:12:44 UTC

**AI Recommendation:** REJECT (Score: 58/100 - Below 60 threshold)
**Human Override:** ✅ YES - Portfolio demonstrated exceptional design skills not captured in resume keywords
**Final Decision:** ADVANCED - Human reviewer identified strong portfolio work

**Override Justification:** "Candidate's portfolio shows 5+ years of enterprise UX work with Fortune 500 clients. AI scored low due to resume formatting, not actual qualifications. Advancing to interview."

---

### Decision #5
**Timestamp:** 2025-11-02 10:05:33 UTC
**Candidate ID:** hash-q7r8s9t0
**Role:** Sales Representative
**Decision:** REJECTED
**AI Systems Used:** ai-sys-002 (Video Interview Analyzer)
**Human Decision Maker:** hiring-manager-55 (David L., Sales Director)
**Disclosure Sent:** ✅ 2025-10-28 14:33:21 UTC

**AI Recommendation:** REJECT (Score: 51/100 - Low enthusiasm detected in video)
**Human Override:** NO
**Final Decision:** REJECTED - Confirmed via human review, candidate did not demonstrate sales energy

---

## 🔍 BIAS AUDIT SUMMARY

**Auditor:** Third-Party Compliance Group LLC
**Audit Date:** December 1, 2025
**Audit Method:** Impact Ratio Analysis per NYC DCWP Guidelines

### Results by Protected Category:

**Race/Ethnicity:**
- Selection Rate Variance: 2.1% (PASS - Below 4-fifths rule threshold)
- No statistically significant disparate impact detected

**Gender:**
- Selection Rate Variance: 1.8% (PASS)
- No statistically significant disparate impact detected

**Age (40+):**
- Selection Rate Variance: 3.2% (PASS)
- No statistically significant disparate impact detected

**Conclusion:** ✅ ALL AI SYSTEMS COMPLIANT

---

## 📧 DISCLOSURE TRACKING

**Total Candidates Processed:** 1,247
**Disclosures Sent:** 1,247 (100%)
**Disclosure Method:** Automated email sent at application submission
**Email Delivery Confirmation:** ✅ Logged via SendGrid webhook

**Sample Disclosure Email:**
```
Subject: AI Usage Disclosure - Acme Corporation Hiring Process

Dear Candidate,

Thank you for applying to Acme Corporation.

As required by NYC Local Law 144, we want to inform you that
we use Automated Employment Decision Tools (AEDT) in our hiring process.

AI systems used:
- Resume screening software (Greenhouse)
- Video interview analysis (HireVue)
- Skills assessment scoring (Criteria Corp)

These tools help us evaluate candidates fairly and consistently,
but all final hiring decisions are made by human hiring managers.

You have the right to request an alternative evaluation process
or accommodation. Contact hr@acmecorp.com if you have questions.

Best regards,
Acme Corporation Talent Team
```

---

## 🛡️ DATA RETENTION & SECURITY

**Retention Period:** 7 years from decision date (per NYC LL144 requirements)
**Storage Location:** AWS US-East-1 (encrypted at rest with AES-256)
**Access Controls:** Role-based access, audit logging enabled
**Immutability:** Blockchain-style hash chain prevents record tampering
**Backup:** Daily encrypted backups to separate AWS region

---

## ✅ COMPLIANCE CHECKLIST

- [x] All AI systems registered with deployment dates
- [x] Bias audits conducted annually by third party
- [x] Bias audit results posted publicly at acmecorp.com/ai-hiring-disclosure
- [x] Disclosures sent to 100% of candidates
- [x] All hiring decisions logged with timestamps
- [x] Human decision maker identified for each decision
- [x] AI recommendations vs. final decisions tracked
- [x] Human override justifications documented
- [x] 7-year retention policy implemented
- [x] Data security measures in place (AES-256 encryption)
- [x] Audit pack generation capability tested and functional

**COMPLIANCE STATUS: ✅ FULLY COMPLIANT**

---

## 📞 CONTACT INFORMATION

**Generated by:** Defensible Hiring AI
**Platform:** defensiblehiringai.com
**Support:** support@defensiblehiringai.com

**Company Contact:**
Acme Corporation
Legal Department
legal@acmecorp.com
(555) 123-4567

---

## 🔐 AUTHENTICITY VERIFICATION

**Document Hash:** SHA-256: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
**Digital Signature:** RSA-2048 signed by Defensible Hiring AI
**Verification:** Visit defensiblehiringai.com/verify and enter document hash

**This audit pack is admissible as evidence in legal proceedings.**

---

*Generated in 47 seconds via Defensible Hiring AI API*

**Need your own instant audit pack?**
Visit defensiblehiringai.com or email sales@defensiblehiringai.com
