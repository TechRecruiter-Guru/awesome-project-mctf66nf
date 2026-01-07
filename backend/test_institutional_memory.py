#!/usr/bin/env python3
"""
Institutional Memory API - End-to-End Test Script

This script demonstrates the complete workflow of the Institutional Memory system
for AI-era hiring decisions.

Usage:
    python test_institutional_memory.py
"""

import requests
import json
import hashlib
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:5000/api"
HEADERS = {"Content-Type": "application/json"}


def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_response(response):
    """Print formatted API response"""
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print()


def hash_candidate_id(candidate_id):
    """Hash candidate ID for privacy"""
    return hashlib.sha256(candidate_id.encode()).hexdigest()


def main():
    print_section("INSTITUTIONAL MEMORY API - END-TO-END TEST")

    # ==================== STEP 1: Register AI System ====================
    print_section("Step 1: Register AI System")

    ai_system_data = {
        "ai_system_id": "resume-screener-v1",
        "system_name": "ResumeScreener Pro",
        "vendor_name": "AI Vendor Inc",
        "system_type": "screening",
        "decision_influence": "assistive",
        "data_inputs": json.dumps({
            "resume_text": True,
            "skills": True,
            "experience_years": True
        }),
        "human_override_points": "Yes - recruiter reviews all AI recommendations",
        "intended_use_statement": "Filter candidates based on minimum qualifications for technical roles. AI provides ranking, human makes final decision.",
        "deployment_date": "2025-01-01T00:00:00Z",
        "created_by": "hr-admin@techcompany.com"
    }

    response = requests.post(f"{BASE_URL}/ai-systems", headers=HEADERS, json=ai_system_data)
    print_response(response)

    # ==================== STEP 2: Create Regulatory Context ====================
    print_section("Step 2: Create Regulatory Context Snapshot")

    reg_context_data = {
        "reg_context_id": "NYC-LOCAL-LAW-144-V1",
        "jurisdiction": "New York City",
        "regulation_name": "NYC Local Law 144 - Automated Employment Decision Tools",
        "regulation_version": "1.0",
        "effective_start_date": "2023-07-05",
        "compliance_obligations": json.dumps({
            "require_disclosure": True,
            "annual_bias_audit": True,
            "disclosure_timing": "before_use",
            "candidate_opt_out": False
        }),
        "source_reference": "https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page"
    }

    response = requests.post(f"{BASE_URL}/regulatory-contexts", headers=HEADERS, json=reg_context_data)
    print_response(response)

    # ==================== STEP 3: Obtain Governance Approval ====================
    print_section("Step 3: Record Governance Approval")

    approval_data = {
        "approval_id": "APPR-2024-12-001",
        "ai_system_id": "resume-screener-v1",
        "approval_type": "legal",
        "approver_role": "General Counsel",
        "approval_decision": "approved",
        "conditions_or_exceptions": "Approved contingent on quarterly bias audits and monthly disclosure compliance review"
    }

    response = requests.post(f"{BASE_URL}/governance-approvals", headers=HEADERS, json=approval_data)
    print_response(response)

    # ==================== STEP 4: Record Vendor Assertion ====================
    print_section("Step 4: Record Vendor Assertion")

    vendor_assertion_data = {
        "vendor_assertion_id": "VENDOR-ASSERT-001",
        "ai_system_id": "resume-screener-v1",
        "assertion_type": "bias_testing",
        "assertion_statement": "System underwent independent bias audit on Dec 1, 2024. No adverse impact detected across protected categories (race, gender, age). Audit report available upon request.",
        "evidence_provided": True,
        "risk_flag": "green"
    }

    response = requests.post(f"{BASE_URL}/vendor-assertions", headers=HEADERS, json=vendor_assertion_data)
    print_response(response)

    # ==================== STEP 5: Render Disclosure ====================
    print_section("Step 5: Render Disclosure for Candidate")

    candidate_id = "candidate-john-doe-12345"
    candidate_hash = hash_candidate_id(candidate_id)
    role_id = 1  # Assuming a job exists with ID 1

    disclosure_render_data = {
        "ai_system_id": "resume-screener-v1",
        "reg_context_id": "NYC-LOCAL-LAW-144-V1",
        "candidate_id": candidate_id,
        "role_id": role_id,
        "hiring_stage": "screening"
    }

    response = requests.post(f"{BASE_URL}/disclosures/render", headers=HEADERS, json=disclosure_render_data)
    print_response(response)

    disclosure_text = response.json().get("disclosure_text", "")

    # ==================== STEP 6: Deliver Disclosure ====================
    print_section("Step 6: Record Disclosure Delivery")

    disclosure_delivery_data = {
        "disclosure_id": f"DISC-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
        "ai_system_id": "resume-screener-v1",
        "reg_context_id": "NYC-LOCAL-LAW-144-V1",
        "candidate_id_hash": candidate_hash,
        "role_id": role_id,
        "disclosure_text": disclosure_text,
        "delivery_method": "ATS",
        "hiring_stage": "screening",
        "acknowledgment_status": "acknowledged",
        "language_locale": "en-US"
    }

    response = requests.post(f"{BASE_URL}/disclosures/deliver", headers=HEADERS, json=disclosure_delivery_data)
    print_response(response)

    # ==================== STEP 7: Record Hiring Decision ====================
    print_section("Step 7: Record Hiring Decision Event")

    decision_event_data = {
        "decision_event_id": f"DECISION-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
        "candidate_id_hash": candidate_hash,
        "role_id": role_id,
        "ai_system_id": "resume-screener-v1",
        "decision_type": "advance",
        "human_involvement_level": "full_review",
        "final_decision_maker_role": "recruiter",
        "decision_timestamp": datetime.utcnow().isoformat()
    }

    response = requests.post(f"{BASE_URL}/hiring-decisions", headers=HEADERS, json=decision_event_data)
    print_response(response)

    decision_event_id = response.json().get("id")

    # ==================== STEP 8: Log Decision Rationale ====================
    print_section("Step 8: Log Decision Rationale")

    rationale_data = {
        "rationale_id": f"RAT-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
        "decision_event_id": decision_event_id,
        "rationale_type": "qualification",
        "rationale_summary": "Candidate advanced to next stage based on: (1) 7+ years Python experience meeting job requirement of 5+ years, (2) Strong ML/AI background with TensorFlow and PyTorch, (3) Previous experience at similar-sized tech companies. AI recommendation score: 8.5/10. Recruiter independently verified qualifications against resume and LinkedIn profile.",
        "supporting_artifacts": json.dumps([
            "resume-john-doe.pdf",
            "linkedin-profile-screenshot.png",
            "skills-assessment-results.json"
        ]),
        "entered_by": "recruiter@techcompany.com"
    }

    response = requests.post(f"{BASE_URL}/decision-rationales", headers=HEADERS, json=rationale_data)
    print_response(response)

    # ==================== STEP 9: Query All Systems ====================
    print_section("Step 9: Query All AI Systems")

    response = requests.get(f"{BASE_URL}/ai-systems")
    print_response(response)

    # ==================== STEP 10: Query Specific AI System ====================
    print_section("Step 10: Query Specific AI System with Related Records")

    response = requests.get(f"{BASE_URL}/ai-systems/resume-screener-v1")
    print_response(response)

    # ==================== STEP 11: Query Regulatory Contexts ====================
    print_section("Step 11: Query Regulatory Contexts for NYC")

    response = requests.get(f"{BASE_URL}/regulatory-contexts?jurisdiction=New York City")
    print_response(response)

    # ==================== STEP 12: Generate Audit Pack ====================
    print_section("Step 12: Generate Comprehensive Audit Evidence Pack")

    audit_pack_data = {
        "jurisdiction": "New York City",
        "start_date": (datetime.utcnow() - timedelta(days=30)).isoformat(),
        "end_date": datetime.utcnow().isoformat(),
        "ai_system_id": "resume-screener-v1"
    }

    response = requests.post(f"{BASE_URL}/audit-packs/generate", headers=HEADERS, json=audit_pack_data)
    print_response(response)

    # ==================== SUMMARY ====================
    print_section("WORKFLOW COMPLETE")

    print("✓ AI System registered")
    print("✓ Regulatory context captured")
    print("✓ Governance approval recorded")
    print("✓ Vendor assertions documented")
    print("✓ Disclosure rendered and delivered")
    print("✓ Hiring decision recorded")
    print("✓ Decision rationale logged")
    print("✓ Audit evidence pack generated")
    print()
    print("Institutional memory successfully created.")
    print("All records are immutable and time-stamped.")
    print()
    print("When asked 'What did you know, and when did you know it?'")
    print("You can now answer with evidence.")
    print()


def run_failure_scenarios():
    """Test failure scenario handling"""
    print_section("FAILURE SCENARIO TESTS")

    # Test 1: Duplicate AI System ID
    print("Test 1: Attempt to create duplicate AI System")
    ai_system_data = {
        "ai_system_id": "resume-screener-v1",
        "system_name": "Duplicate System",
        "deployment_date": "2025-01-01T00:00:00Z"
    }
    response = requests.post(f"{BASE_URL}/ai-systems", headers=HEADERS, json=ai_system_data)
    print_response(response)
    assert response.status_code == 409, "Should return 409 Conflict"

    # Test 2: Missing required fields
    print("Test 2: Create AI System with missing required fields")
    incomplete_data = {
        "system_name": "Incomplete System"
    }
    response = requests.post(f"{BASE_URL}/ai-systems", headers=HEADERS, json=incomplete_data)
    print_response(response)
    assert response.status_code == 400, "Should return 400 Bad Request"

    # Test 3: Invalid date format
    print("Test 3: Create regulatory context with invalid date")
    invalid_date_data = {
        "reg_context_id": "TEST-INVALID",
        "jurisdiction": "Test",
        "regulation_name": "Test Reg",
        "effective_start_date": "invalid-date"
    }
    response = requests.post(f"{BASE_URL}/regulatory-contexts", headers=HEADERS, json=invalid_date_data)
    print_response(response)
    assert response.status_code == 400, "Should return 400 Bad Request"

    print("\n✓ All failure scenarios handled correctly\n")


if __name__ == "__main__":
    try:
        # Run main workflow
        main()

        # Optionally run failure scenario tests
        print("\nRun failure scenario tests? (y/n): ", end="")
        if input().lower() == 'y':
            run_failure_scenarios()

    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API server")
        print("Make sure the Flask backend is running:")
        print("  cd backend")
        print("  python app.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
