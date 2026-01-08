#!/usr/bin/env python3
"""
Initialize the Institutional Memory database
"""
from app import app, db

print("Creating Institutional Memory database tables...")

with app.app_context():
    db.create_all()
    print("✓ Database tables created successfully!")
    print("\nTables created:")
    print("  - Company (multi-tenant customers)")
    print("  - AISystemRecord")
    print("  - RegulatoryContextSnapshot")
    print("  - DisclosureArtifact")
    print("  - HiringDecisionEvent")
    print("  - DecisionRationaleLog")
    print("  - GovernanceApprovalRecord")
    print("  - VendorAssertionRecord")
    print("\nInstitutional Memory API ready!")
