#!/usr/bin/env python3
"""
DEMO: What Happens When a Company Gets Legally Challenged

This demonstrates:
1. How an ATS integrates with Institutional Memory API
2. Normal hiring operations (AI screening, decisions made)
3. A legal challenge arrives (candidate sues or regulator inquires)
4. Company generates audit pack - FULL EVIDENCE immediately available

This is what you SELL to ATS companies!
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5001/api"
HEADERS = {"Content-Type": "application/json"}

def print_section(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def main():
    print_section("INSTITUTIONAL MEMORY API - LEGAL CHALLENGE DEMO")
    print("Scenario: TechCorp uses an ATS with AI screening.")
    print("One year later, a rejected candidate sues for discrimination.")
    print("Watch how Institutional Memory provides instant, complete evidence.\n")

    # ==================== STEP 1: COMPANY SIGNS UP ====================
    print_section("STEP 1: TechCorp Signs Up for Institutional Memory Service")

    signup_data = {
        "company_name": "TechCorp Inc",
        "plan_type": "pro"
    }

    response = requests.post(f"{BASE_URL}/company/register", headers=HEADERS, json=signup_data)
    signup_result = response.json()

    print(f"✓ Company registered: {signup_result['company_id']}")
    print(f"✓ API Key issued: {signup_result['api_key'][:20]}...")
    print(f"\nTechCorp now integrates this API key into their ATS...")

    API_KEY = signup_result['api_key']
    AUTH_HEADERS = {
        **HEADERS,
        "X-API-Key": API_KEY
    }

    # ==================== STEP 2: NORMAL HIRING OPERATIONS ====================
    print_section("STEP 2: Normal Hiring Operations (January - March 2024)")

    print("TechCorp posts a Senior Python Developer position...")
    print("They use AI screening tool: 'ResumeRanker Pro' by VendorAI")
    print()

    # Register AI usage
    ai_usage_data = {
        "ai_system_id": "resume-ranker-v2",
        "system_name": "ResumeRanker Pro",
        "vendor_name": "VendorAI Inc",
        "system_type": "screening",
        "decision_influence": "assistive",
        "intended_use_statement": "Ranks candidates based on resume match to job requirements. Final decision made by human recruiter.",
        "deployment_date": "2024-01-01T00:00:00Z"
    }

    response = requests.post(f"{BASE_URL}/webhook/ai-usage", headers=AUTH_HEADERS, json=ai_usage_data)
    print(f"✓ AI system registered in institutional memory")
    print(f"  System: {ai_usage_data['system_name']}")
    print(f"  Influence: {ai_usage_data['decision_influence']}")
    print()

    # Simulate 3 hiring decisions
    candidates = [
        {
            "name": "Jane Smith",
            "candidate_id": "cand-001",
            "role_id": "job-python-sr-001",
            "decision_type": "advance",
            "ai_system_id": "resume-ranker-v2",
            "decision_maker": "sarah.recruiter@techcorp.com",
            "rationale": "Strong Python experience (8 years), ML background, great culture fit. AI scored 9/10, recruiter independently verified and agreed."
        },
        {
            "name": "John Davis",
            "candidate_id": "cand-002",
            "role_id": "job-python-sr-001",
            "decision_type": "reject",
            "ai_system_id": "resume-ranker-v2",
            "decision_maker": "sarah.recruiter@techcorp.com",
            "rationale": "Only 2 years Python experience, requirement is 5+ years. AI flagged insufficient experience. Recruiter reviewed manually and confirmed not qualified."
        },
        {
            "name": "Maria Garcia",
            "candidate_id": "cand-003",
            "role_id": "job-python-sr-001",
            "decision_type": "advance",
            "ai_system_id": "resume-ranker-v2",
            "decision_maker": "sarah.recruiter@techcorp.com",
            "rationale": "7 years Python, Django expert, strong references. AI scored 8.5/10, recruiter validated experience."
        }
    ]

    print("Processing candidates...")
    for candidate in candidates:
        response = requests.post(f"{BASE_URL}/webhook/hiring-decision", headers=AUTH_HEADERS, json=candidate)
        result = response.json()
        print(f"✓ {candidate['name']}: {candidate['decision_type'].upper()}")
        print(f"  Decision ID: {result['decision_event_id']}")
        print(f"  Rationale: {candidate['rationale'][:60]}...")
        print()

    print("Hiring continues normally for months...")
    print("Jane Smith gets hired. John Davis receives rejection email.")
    print("Maria Garcia declines offer, accepts position elsewhere.")
    print()

    # ==================== STEP 3: LEGAL CHALLENGE ====================
    print_section("STEP 3: One Year Later - Legal Challenge Arrives!")

    print("📧 Email to TechCorp General Counsel:")
    print("-" * 80)
    print("From: John Davis <jdavis@email.com>")
    print("Subject: Discrimination Complaint - AI Hiring")
    print()
    print("I applied for Senior Python Developer in March 2024 and was rejected.")
    print("I believe your AI screening system discriminated against me based on")
    print("my age and ethnicity. I am filing a complaint with the EEOC.")
    print()
    print("I request all records showing:")
    print("1. What AI system you used")
    print("2. How it influenced your decision")
    print("3. What human review occurred")
    print("4. Why I was rejected")
    print("-" * 80)
    print()

    print("😰 Without Institutional Memory, TechCorp would scramble to:")
    print("  ❌ Find emails from a year ago")
    print("  ❌ Remember which AI tool was used")
    print("  ❌ Reconstruct who made the decision")
    print("  ❌ Prove human involvement")
    print("  ❌ Show the actual rationale")
    print()

    print("✅ With Institutional Memory API:")
    print("  → General Counsel logs into dashboard")
    print("  → Clicks 'Generate Audit Pack'")
    print("  → 30 seconds later: Complete evidence ready")
    print()

    # ==================== STEP 4: GENERATE AUDIT PACK ====================
    print_section("STEP 4: Generating Audit Evidence Pack")

    import hashlib
    candidate_hash = hashlib.sha256("cand-002".encode()).hexdigest()

    audit_request = {
        "candidate_id_hash": candidate_hash,
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    }

    print(f"Generating audit pack for candidate: {candidate_hash[:16]}...")
    print()

    response = requests.post(f"{BASE_URL}/audit-pack/generate", headers=AUTH_HEADERS, json=audit_request)
    audit_pack = response.json()

    # ==================== STEP 5: AUDIT REPORT ====================
    print_section("STEP 5: AUDIT REPORT - What TechCorp's Lawyer Receives")

    print("="*80)
    print("            INSTITUTIONAL MEMORY AUDIT PACK")
    print("         AI-Era Hiring Compliance Evidence Report")
    print("="*80)
    print()
    print(f"Generated: {audit_pack['generated_at']}")
    print(f"Company: {audit_pack['company']['company_name']}")
    print(f"Compliance Status: {audit_pack['summary']['compliance_status']}")
    print()
    print("-"*80)
    print("EXECUTIVE SUMMARY")
    print("-"*80)
    print()
    print(f"Total AI Systems Used:  {audit_pack['summary']['total_ai_systems']}")
    print(f"Total Decisions:        {audit_pack['summary']['total_decisions']}")
    print(f"Total Disclosures:      {audit_pack['summary']['total_disclosures']}")
    print()
    print("-"*80)
    print("AI SYSTEMS USED IN HIRING PROCESS")
    print("-"*80)
    print()

    for ai_system in audit_pack['evidence']['ai_systems']:
        print(f"System Name:     {ai_system['system_name']}")
        print(f"Vendor:          {ai_system['vendor_name']}")
        print(f"System Type:     {ai_system['system_type']}")
        print(f"Decision Role:   {ai_system['decision_influence']}")
        print(f"Deployed:        {ai_system['deployment_date']}")
        print()
        print("Intended Use Statement:")
        print(f"  {ai_system['intended_use_statement']}")
        print()

    print("-"*80)
    print("HIRING DECISIONS - CANDIDATE SPECIFIC")
    print("-"*80)
    print()

    for decision in audit_pack['evidence']['decisions']:
        print(f"Decision ID:          {decision['decision_event_id']}")
        print(f"Candidate (hashed):  {decision['candidate_id_hash'][:32]}...")
        print(f"Decision Type:       {decision['decision_type'].upper()}")
        print(f"Human Involvement:   {decision['human_involvement_level']}")
        print(f"Decision Timestamp:  {decision['decision_timestamp']}")
        print()

        if decision['rationale_count'] > 0:
            print("DECISION RATIONALE (Why this decision was made):")
            for rationale in decision['rationales']:
                print(f"  Type:    {rationale['rationale_type']}")
                print(f"  Summary: {rationale['rationale_summary']}")
                print(f"  By:      {rationale['entered_by']}")
                print(f"  When:    {rationale['entered_timestamp']}")
                print()

    print("-"*80)
    print("LEGAL DEFENSE POSITION")
    print("-"*80)
    print()
    print("Based on this evidence, TechCorp can demonstrate:")
    print()
    print("✓ AI was used in 'ASSISTIVE' capacity only")
    print("✓ Final decision made by human recruiter")
    print("✓ Specific, documented rationale exists")
    print("✓ Rejection based on objective qualification gap:")
    print("  → Candidate had 2 years experience")
    print("  → Position required 5+ years")
    print("  → Both AI and human recruiter independently confirmed")
    print()
    print("✓ No evidence of discrimination based on protected class")
    print("✓ Consistent process applied to all candidates")
    print("✓ Complete institutional memory preserved")
    print()
    print("="*80)
    print("           END OF AUDIT REPORT")
    print("="*80)
    print()

    # ==================== STEP 6: OUTCOME ====================
    print_section("STEP 6: Legal Outcome")

    print("TechCorp's General Counsel sends audit pack to company lawyer.")
    print()
    print("Lawyer's response:")
    print("-" * 80)
    print("This is exactly what we needed. The evidence clearly shows:")
    print()
    print("1. AI was used appropriately (assistive role, not determinative)")
    print("2. Human made the final decision after independent review")
    print("3. Rejection was based on legitimate, documented qualification gap")
    print("4. Same process applied consistently to all candidates")
    print("5. Complete audit trail exists")
    print()
    print("We can defend this position confidently. I'll draft a response")
    print("to the EEOC showing this evidence.")
    print("-" * 80)
    print()

    print("💼 Without Institutional Memory:")
    print("  - Months of discovery")
    print("  - $50,000+ in legal fees")
    print("  - Risk of settlement due to lack of evidence")
    print("  - Reputational damage")
    print()

    print("✅ With Institutional Memory:")
    print("  - 30 seconds to generate complete evidence")
    print("  - Strong defense position immediately")
    print("  - Documented compliance")
    print("  - Confidence to fight or settle based on facts, not fear")
    print()

    # ==================== FINAL MESSAGE ====================
    print_section("THIS IS WHAT YOU SELL")

    print("🎯 Product: Institutional Memory API")
    print("💰 Revenue Model: B2B SaaS")
    print()
    print("Pricing Tiers:")
    print("  - Free:       1 company, 100 decisions/month")
    print("  - Starter:    $99/month  - 1,000 decisions/month")
    print("  - Pro:        $499/month - 10,000 decisions/month")
    print("  - Enterprise: Custom     - Unlimited + white-label")
    print()
    print("Who Pays:")
    print("  - ATS vendors (Greenhouse, Lever, etc.) - integrate your API")
    print("  - Enterprises with in-house ATS")
    print("  - HR tech companies adding compliance")
    print("  - Staffing agencies")
    print()
    print("Value Proposition:")
    print("  'When you get sued, you'll wish you had this.")
    print("   Don't wait until it's too late.'")
    print()
    print("="*80)
    print()


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to Institutional Memory API")
        print("Make sure the API is running:")
        print("  cd institutional-memory-api")
        print("  python app.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
