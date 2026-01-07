#!/usr/bin/env python3
"""
Initialize the database and create all tables
"""
from app import app, db

print("Creating database tables...")

with app.app_context():
    db.create_all()
    print("✓ Database tables created successfully!")
    print("\nTables created:")
    print("  - Candidate")
    print("  - Job")
    print("  - Application")
    print("  - Publication")
    print("  - SavedSearch")
    print("  - EmailCampaign")
    print("  - Interview")
    print("  - Offer")
    print("  - AISystemRecord")
    print("  - RegulatoryContextSnapshot")
    print("  - DisclosureArtifact")
    print("  - HiringDecisionEvent")
    print("  - DecisionRationaleLog")
    print("  - GovernanceApprovalRecord")
    print("  - VendorAssertionRecord")
    print("\nDatabase ready!")
