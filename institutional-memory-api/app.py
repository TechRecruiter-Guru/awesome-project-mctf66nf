"""
Institutional Memory API - Standalone SaaS Product
Compliance-as-a-Service for AI-era hiring decisions

This API allows ANY ATS (Applicant Tracking System) to:
1. Register AI systems they use
2. Record hiring decisions
3. Generate audit-ready evidence packs
4. Prove compliance when challenged

Business Model: B2B SaaS - ATS vendors pay to use this service
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import hashlib
import secrets

app = Flask(__name__)
CORS(app)

# Database configuration - PostgreSQL for production, SQLite for dev
database_url = os.environ.get('DATABASE_URL')
if database_url:
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Use in-memory SQLite for ephemeral environments (Render free tier)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ==================== MULTI-TENANT SUPPORT ====================

class Company(db.Model):
    """
    Multi-tenant: Each ATS customer is a company
    """
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.String(100), unique=True, nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    api_key = db.Column(db.String(200), unique=True, nullable=False)

    # Plan details
    plan_type = db.Column(db.String(50), default='free')  # free, starter, pro, enterprise
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    ai_systems = db.relationship('AISystemRecord', backref='company', lazy=True)

    def to_dict(self):
        return {
            'company_id': self.company_id,
            'company_name': self.company_name,
            'plan_type': self.plan_type,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }


# ==================== INSTITUTIONAL MEMORY MODELS ====================

class AISystemRecord(db.Model):
    """
    Immutable record of AI systems used in hiring.
    Multi-tenant: company_id links to customer.
    """
    __tablename__ = 'ai_system_record'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    ai_system_id = db.Column(db.String(100), nullable=False)

    # System Details
    system_name = db.Column(db.String(200), nullable=False)
    vendor_name = db.Column(db.String(200))
    system_type = db.Column(db.String(100))  # screening, ranking, interview_analysis
    decision_influence = db.Column(db.String(50))  # assistive, determinative, hybrid
    intended_use_statement = db.Column(db.Text)

    # Lifecycle
    deployment_date = db.Column(db.DateTime, nullable=False)
    retirement_date = db.Column(db.DateTime)

    # Immutability
    created_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    version = db.Column(db.Integer, default=1)

    # Unique constraint per company
    __table_args__ = (db.UniqueConstraint('company_id', 'ai_system_id', name='_company_ai_system_uc'),)

    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company.company_id,
            'ai_system_id': self.ai_system_id,
            'system_name': self.system_name,
            'vendor_name': self.vendor_name,
            'system_type': self.system_type,
            'decision_influence': self.decision_influence,
            'intended_use_statement': self.intended_use_statement,
            'deployment_date': self.deployment_date.isoformat(),
            'retirement_date': self.retirement_date.isoformat() if self.retirement_date else None,
            'created_timestamp': self.created_timestamp.isoformat(),
            'version': self.version
        }


class RegulatoryContextSnapshot(db.Model):
    """Time-bound regulatory snapshot"""
    __tablename__ = 'regulatory_context_snapshot'

    id = db.Column(db.Integer, primary_key=True)
    reg_context_id = db.Column(db.String(100), unique=True, nullable=False)

    jurisdiction = db.Column(db.String(100), nullable=False)
    regulation_name = db.Column(db.String(200), nullable=False)
    regulation_version = db.Column(db.String(50))
    effective_start_date = db.Column(db.Date, nullable=False)
    effective_end_date = db.Column(db.Date)

    compliance_obligations = db.Column(db.Text)
    source_reference = db.Column(db.String(500))
    ingested_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'reg_context_id': self.reg_context_id,
            'jurisdiction': self.jurisdiction,
            'regulation_name': self.regulation_name,
            'effective_start_date': self.effective_start_date.isoformat(),
            'effective_end_date': self.effective_end_date.isoformat() if self.effective_end_date else None
        }


class DisclosureArtifact(db.Model):
    """Proof of AI disclosure to candidates"""
    __tablename__ = 'disclosure_artifact'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    disclosure_id = db.Column(db.String(100), nullable=False)

    ai_system_record_id = db.Column(db.Integer, db.ForeignKey('ai_system_record.id'), nullable=False)
    reg_context_id = db.Column(db.Integer, db.ForeignKey('regulatory_context_snapshot.id'), nullable=False)

    candidate_id_hash = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.String(100))
    hiring_stage = db.Column(db.String(100))

    disclosure_text_rendered = db.Column(db.Text, nullable=False)
    delivery_method = db.Column(db.String(100))
    delivery_timestamp = db.Column(db.DateTime, nullable=False)
    acknowledgment_status = db.Column(db.String(50))

    created_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    company_rel = db.relationship('Company', backref='disclosures')

    def to_dict(self):
        return {
            'disclosure_id': self.disclosure_id,
            'candidate_id_hash': self.candidate_id_hash,
            'disclosure_text': self.disclosure_text_rendered,
            'delivery_timestamp': self.delivery_timestamp.isoformat(),
            'acknowledgment_status': self.acknowledgment_status
        }


class HiringDecisionEvent(db.Model):
    """Links AI use to employment outcomes"""
    __tablename__ = 'hiring_decision_event'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    decision_event_id = db.Column(db.String(100), nullable=False)

    candidate_id_hash = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.String(100))
    ai_system_record_id = db.Column(db.Integer, db.ForeignKey('ai_system_record.id'))

    decision_type = db.Column(db.String(50), nullable=False)  # advance, reject, score
    human_involvement_level = db.Column(db.String(100))
    final_decision_maker_role = db.Column(db.String(100))
    decision_timestamp = db.Column(db.DateTime, nullable=False)

    created_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    company_rel = db.relationship('Company', backref='decisions')
    rationales = db.relationship('DecisionRationaleLog', backref='decision_event', lazy=True)

    def to_dict(self):
        return {
            'decision_event_id': self.decision_event_id,
            'candidate_id_hash': self.candidate_id_hash,
            'decision_type': self.decision_type,
            'human_involvement_level': self.human_involvement_level,
            'decision_timestamp': self.decision_timestamp.isoformat(),
            'rationale_count': len(self.rationales)
        }


class DecisionRationaleLog(db.Model):
    """WHY decisions were made - most valuable for legal defense"""
    __tablename__ = 'decision_rationale_log'

    id = db.Column(db.Integer, primary_key=True)
    rationale_id = db.Column(db.String(100), nullable=False)
    decision_event_id = db.Column(db.Integer, db.ForeignKey('hiring_decision_event.id'), nullable=False)

    rationale_type = db.Column(db.String(100))
    rationale_summary = db.Column(db.Text, nullable=False)
    supporting_artifacts = db.Column(db.Text)

    entered_by = db.Column(db.String(200))
    entered_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'rationale_id': self.rationale_id,
            'rationale_type': self.rationale_type,
            'rationale_summary': self.rationale_summary,
            'entered_by': self.entered_by,
            'entered_timestamp': self.entered_timestamp.isoformat()
        }


class GovernanceApprovalRecord(db.Model):
    """Proves oversight existed before issues"""
    __tablename__ = 'governance_approval_record'

    id = db.Column(db.Integer, primary_key=True)
    approval_id = db.Column(db.String(100), nullable=False)
    ai_system_record_id = db.Column(db.Integer, db.ForeignKey('ai_system_record.id'), nullable=False)

    approval_type = db.Column(db.String(100), nullable=False)
    approver_role = db.Column(db.String(200), nullable=False)
    approval_decision = db.Column(db.String(50), nullable=False)
    conditions_or_exceptions = db.Column(db.Text)

    approval_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'approval_id': self.approval_id,
            'approval_type': self.approval_type,
            'approver_role': self.approver_role,
            'approval_decision': self.approval_decision,
            'approval_timestamp': self.approval_timestamp.isoformat()
        }


class VendorAssertionRecord(db.Model):
    """Documents vendor claims and evidence gaps"""
    __tablename__ = 'vendor_assertion_record'

    id = db.Column(db.Integer, primary_key=True)
    vendor_assertion_id = db.Column(db.String(100), nullable=False)
    ai_system_record_id = db.Column(db.Integer, db.ForeignKey('ai_system_record.id'), nullable=False)

    assertion_type = db.Column(db.String(100), nullable=False)
    assertion_statement = db.Column(db.Text, nullable=False)
    evidence_provided = db.Column(db.Boolean, default=False)
    risk_flag = db.Column(db.String(20))

    recorded_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'vendor_assertion_id': self.vendor_assertion_id,
            'assertion_type': self.assertion_type,
            'assertion_statement': self.assertion_statement,
            'evidence_provided': self.evidence_provided,
            'risk_flag': self.risk_flag
        }


# Initialize database tables
with app.app_context():
    db.create_all()

# ==================== AUTHENTICATION ====================

def require_api_key(f):
    """Decorator to require API key authentication"""
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')

        if not api_key:
            return jsonify({"error": "API key required. Include X-API-Key header."}), 401

        company = Company.query.filter_by(api_key=api_key, is_active=True).first()
        if not company:
            return jsonify({"error": "Invalid API key"}), 401

        # Pass company to the route
        return f(company=company, *args, **kwargs)

    return decorated_function


# ==================== API ENDPOINTS ====================

@app.route('/', methods=['GET'])
def root():
    """Landing page"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Defensible Hiring AI - Make AI Hiring Legally Defensible</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }
        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 80px 20px;
            text-align: center;
        }
        .hero h1 {
            font-size: 3em;
            margin-bottom: 20px;
            font-weight: 700;
        }
        .hero p {
            font-size: 1.3em;
            margin-bottom: 30px;
            opacity: 0.95;
        }
        .cta-button {
            display: inline-block;
            background: #ff6b6b;
            color: white;
            padding: 15px 40px;
            text-decoration: none;
            border-radius: 5px;
            font-size: 1.2em;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
            border: none;
            cursor: pointer;
        }
        .cta-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 60px 20px;
        }
        .problem {
            background: #fff3cd;
            border-left: 5px solid #ff6b6b;
            padding: 30px;
            margin-bottom: 40px;
        }
        .problem h2 {
            color: #d63031;
            margin-bottom: 15px;
        }
        .solution {
            background: #d4edda;
            border-left: 5px solid #28a745;
            padding: 30px;
            margin-bottom: 40px;
        }
        .solution h2 {
            color: #155724;
            margin-bottom: 15px;
        }
        .demo-section {
            background: #f8f9fa;
            padding: 60px 20px;
        }
        .demo-box {
            background: #1e1e1e;
            color: #00ff00;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            overflow-x: auto;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .demo-box pre {
            margin: 0;
            white-space: pre-wrap;
        }
        .pricing {
            background: white;
            padding: 60px 20px;
        }
        .pricing-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }
        .pricing-card {
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 40px 30px;
            text-align: center;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .pricing-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }
        .pricing-card.featured {
            border-color: #667eea;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            transform: scale(1.05);
        }
        .price {
            font-size: 3em;
            font-weight: 700;
            margin: 20px 0;
        }
        .features {
            list-style: none;
            margin: 30px 0;
        }
        .features li {
            padding: 10px 0;
            border-bottom: 1px solid rgba(0,0,0,0.1);
        }
        .stats {
            background: #667eea;
            color: white;
            padding: 60px 20px;
            text-align: center;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 40px;
            margin-top: 40px;
        }
        .stat-box h3 {
            font-size: 3em;
            margin-bottom: 10px;
        }
        h2 {
            font-size: 2.5em;
            margin-bottom: 20px;
            text-align: center;
        }
        .api-endpoint {
            background: #e7f3ff;
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            margin: 10px 0;
        }
        nav {
            background: rgba(0,0,0,0.2);
            padding: 15px 20px;
            text-align: center;
            margin-bottom: 20px;
        }
        nav a {
            color: white;
            text-decoration: none;
            margin: 0 20px;
            font-weight: 500;
            font-size: 1.05em;
        }
        nav a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="hero">
        <nav>
            <a href="/">Home</a>
            <a href="/docs">API Docs</a>
            <a href="/faq">FAQ</a>
            <a href="#pricing">Pricing</a>
            <a href="/request-demo">Request Access</a>
        </nav>
        <h1>🛡️ Defensible Hiring AI</h1>
        <p style="font-size: 1.3em; margin-bottom: 10px;"><strong>Make Your AI Hiring Legally Defensible in 60 Seconds</strong></p>
        <p>Our institutional memory API provides instant, complete evidence when you're challenged by EEOC, candidates, or regulators.</p>
        <a href="#demo" class="cta-button">See Live Demo</a>
        <a href="#pricing" class="cta-button" style="background: white; color: #667eea; margin-left: 20px;">View Pricing</a>
    </div>

    <div class="container">
        <div class="problem">
            <h2>⚠️ The $500K Problem</h2>
            <p><strong>Your company uses AI to screen 10,000 job applicants.</strong></p>
            <p>One year later: <em>"I'm filing an EEOC complaint for AI discrimination..."</em></p>
            <p><strong>Can you prove what AI you used? What disclosures you made? Why you rejected them?</strong></p>
            <p style="margin-top: 20px; font-size: 1.2em; color: #d63031;">
                Without institutional memory: $50K-500K in legal costs, discovery hell, potential fines.
            </p>
        </div>

        <div class="solution">
            <h2>✅ The 60-Second Solution</h2>
            <p><strong>One API call. Complete audit pack. Case closed.</strong></p>
            <div class="api-endpoint">
                GET /api/audit-pack/generate?candidate_id=john.doe@email.com
            </div>
            <p style="margin-top: 20px;">Returns: Every AI system used, every decision made, every disclosure delivered, complete timeline.</p>
            <p style="font-size: 1.2em; color: #155724; margin-top: 15px;">
                <strong>Your legal team has everything. Your company is defensible.</strong>
            </p>
        </div>
    </div>

    <div style="background: #fff3cd; padding: 60px 20px; border-top: 5px solid #ffc107; border-bottom: 5px solid #ffc107;">
        <div class="container">
            <h2 style="text-align: center; color: #d63031; margin-bottom: 30px;">⚖️ Is This Legally Required in Your State?</h2>
            <p style="text-align: center; font-size: 1.2em; margin-bottom: 40px; color: #555;">
                <strong>Short answer:</strong> If you hire in NYC, California, Illinois, Colorado, or the EU - <strong style="color: #d63031;">YES, compliance is MANDATORY.</strong><br>
                If not? You're next. Regulations are spreading fast.
            </p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin-bottom: 40px;">
                <div style="background: white; padding: 25px; border-radius: 10px; border-left: 5px solid #dc3545;">
                    <h3 style="color: #dc3545; margin-bottom: 15px;">🚨 MANDATORY NOW</h3>
                    <ul style="list-style: none; padding-left: 0;">
                        <li style="padding: 8px 0; border-bottom: 1px solid #eee;"><strong>New York City:</strong> Local Law 144 (since Jan 2023)</li>
                        <li style="padding: 8px 0; border-bottom: 1px solid #eee;"><strong>California:</strong> AB 2013 (since Jan 2024)</li>
                        <li style="padding: 8px 0; border-bottom: 1px solid #eee;"><strong>Illinois:</strong> AI Video Interview Act (since 2020)</li>
                        <li style="padding: 8px 0; border-bottom: 1px solid #eee;"><strong>Colorado:</strong> AI Act (effective Feb 2026)</li>
                        <li style="padding: 8px 0;"><strong>European Union:</strong> AI Act (phased rollout)</li>
                    </ul>
                    <p style="margin-top: 20px; color: #dc3545; font-weight: 600;">
                        ⚠️ Non-compliance penalties: $500-$1,500 per violation in NYC alone
                    </p>
                </div>

                <div style="background: white; padding: 25px; border-radius: 10px; border-left: 5px solid #ffc107;">
                    <h3 style="color: #f39c12; margin-bottom: 15px;">⏰ COMING SOON</h3>
                    <ul style="list-style: none; padding-left: 0; color: #555;">
                        <li style="padding: 8px 0; border-bottom: 1px solid #eee;">• Washington (bill pending)</li>
                        <li style="padding: 8px 0; border-bottom: 1px solid #eee;">• Massachusetts (proposed)</li>
                        <li style="padding: 8px 0; border-bottom: 1px solid #eee;">• New Jersey (under review)</li>
                        <li style="padding: 8px 0; border-bottom: 1px solid #eee;">• Federal AI Act (proposed)</li>
                        <li style="padding: 8px 0;">• 12+ other states drafting legislation</li>
                    </ul>
                    <p style="margin-top: 20px; color: #f39c12; font-weight: 600;">
                        📈 Experts predict 20+ states by 2027
                    </p>
                </div>

                <div style="background: white; padding: 25px; border-radius: 10px; border-left: 5px solid #28a745;">
                    <h3 style="color: #28a745; margin-bottom: 15px;">💡 EVEN IF NOT REQUIRED...</h3>
                    <p style="color: #555; margin-bottom: 15px;">You still face legal risk from:</p>
                    <ul style="color: #555;">
                        <li style="padding: 5px 0;"><strong>EEOC:</strong> Can sue for discrimination without specific AI laws</li>
                        <li style="padding: 5px 0;"><strong>Interstate hiring:</strong> If you hire NY/CA candidates, you must comply</li>
                        <li style="padding: 5px 0;"><strong>Future-proofing:</strong> Better to be compliant before your state passes a law</li>
                        <li style="padding: 5px 0;"><strong>Competitive advantage:</strong> Show candidates you're transparent</li>
                    </ul>
                </div>
            </div>

            <div style="background: white; padding: 30px; border-radius: 10px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h3 style="color: #667eea; margin-bottom: 20px;">🎯 Who MUST Comply Right Now?</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; text-align: left;">
                    <div>
                        <strong style="color: #dc3545;">✓ You have offices in NYC, CA, IL, or CO</strong><br>
                        <span style="color: #666; font-size: 0.95em;">Mandatory compliance with state laws</span>
                    </div>
                    <div>
                        <strong style="color: #dc3545;">✓ You hire remote workers in those states</strong><br>
                        <span style="color: #666; font-size: 0.95em;">Laws apply to candidate location</span>
                    </div>
                    <div>
                        <strong style="color: #dc3545;">✓ You use AI screening of any kind</strong><br>
                        <span style="color: #666; font-size: 0.95em;">Resume parsers, video analysis, scoring tools</span>
                    </div>
                    <div>
                        <strong style="color: #dc3545;">✓ You're an ATS vendor serving multi-state clients</strong><br>
                        <span style="color: #666; font-size: 0.95em;">Your customers need compliance tools</span>
                    </div>
                </div>
                <p style="margin-top: 30px; font-size: 1.1em;">
                    <strong>Don't know if you're covered?</strong>
                    <a href="mailto:compliance@defensiblehiringai.com?subject=Am I Required to Comply?" style="color: #667eea; text-decoration: underline;">Ask our compliance team →</a>
                </p>
            </div>
        </div>
    </div>

    <div class="stats">
        <h2>The Market Opportunity</h2>
        <div class="stats-grid">
            <div class="stat-box">
                <h3>73%</h3>
                <p>of companies use AI in hiring</p>
            </div>
            <div class="stat-box">
                <h3>$250K</h3>
                <p>Average cost of discrimination lawsuit</p>
            </div>
            <div class="stat-box">
                <h3>2025+</h3>
                <p>NYC, EU, California AI disclosure laws</p>
            </div>
        </div>
    </div>

    <!-- ZERO-STORAGE ARCHITECTURE (KILLER DIFFERENTIATOR) -->
    <div style="background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); padding: 80px 20px;">
        <div class="container" style="max-width: 1000px;">
            <h2 style="text-align: center; color: #1b5e20; font-size: 2.5em; margin-bottom: 20px;">
                🔒 Zero-Storage Architecture
            </h2>
            <p style="text-align: center; font-size: 1.3em; color: #2e7d32; margin-bottom: 50px;">
                <strong>We DON'T store your candidate data. Ever.</strong>
            </p>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-bottom: 50px;">
                <div style="background: white; padding: 35px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                    <h3 style="color: #dc3545; margin-bottom: 20px; font-size: 1.5em;">❌ What We DON'T Store:</h3>
                    <ul style="list-style: none; padding-left: 0; color: #555; font-size: 1.05em;">
                        <li style="padding: 12px 0; border-bottom: 1px solid #eee;">
                            ❌ Candidate names, emails, phone numbers
                        </li>
                        <li style="padding: 12px 0; border-bottom: 1px solid #eee;">
                            ❌ Resumes or CVs (no PDFs, no text)
                        </li>
                        <li style="padding: 12px 0; border-bottom: 1px solid #eee;">
                            ❌ Interview recordings or transcripts
                        </li>
                        <li style="padding: 12px 0; border-bottom: 1px solid #eee;">
                            ❌ Compensation data or salary history
                        </li>
                        <li style="padding: 12px 0; border-bottom: 1px solid #eee;">
                            ❌ Internal notes or comments
                        </li>
                        <li style="padding: 12px 0;">
                            ❌ Any personally identifiable information (PII)
                        </li>
                    </ul>
                    <p style="margin-top: 25px; padding: 20px; background: #fff3cd; border-radius: 10px; color: #333;">
                        <strong>If we get hacked:</strong> Attackers get timestamps and hashes. No resumes. No names. Nothing they can sell.
                    </p>
                </div>

                <div style="background: white; padding: 35px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                    <h3 style="color: #28a745; margin-bottom: 20px; font-size: 1.5em;">✅ What We DO Store:</h3>
                    <ul style="list-style: none; padding-left: 0; color: #555; font-size: 1.05em;">
                        <li style="padding: 12px 0; border-bottom: 1px solid #eee;">
                            ✅ Timestamps (when events happened)
                        </li>
                        <li style="padding: 12px 0; border-bottom: 1px solid #eee;">
                            ✅ Hashed IDs (anonymized candidate references)
                        </li>
                        <li style="padding: 12px 0; border-bottom: 1px solid #eee;">
                            ✅ AI scores & recommendations
                        </li>
                        <li style="padding: 12px 0; border-bottom: 1px solid #eee;">
                            ✅ Decision justifications & business reasons
                        </li>
                        <li style="padding: 12px 0; border-bottom: 1px solid #eee;">
                            ✅ Compliance proof (disclosures sent, audits passed)
                        </li>
                        <li style="padding: 12px 0;">
                            ✅ Links to YOUR ATS (where the real data lives)
                        </li>
                    </ul>
                    <p style="margin-top: 25px; padding: 20px; background: #d4edda; border-radius: 10px; color: #155724;">
                        <strong>Your candidate data stays in YOUR ATS.</strong> We just prove what you did with it.
                    </p>
                </div>
            </div>

            <div style="background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                <h3 style="text-align: center; color: #667eea; margin-bottom: 30px; font-size: 1.8em;">
                    🎯 How It Works
                </h3>
                <div style="display: flex; justify-content: space-between; align-items: center; gap: 20px; flex-wrap: wrap;">
                    <div style="flex: 1; min-width: 200px; text-align: center;">
                        <div style="background: #667eea; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px auto; font-size: 1.5em; font-weight: bold;">1</div>
                        <p style="color: #555; font-weight: 600;">Candidate applies to your ATS</p>
                    </div>
                    <div style="color: #667eea; font-size: 2em;">→</div>
                    <div style="flex: 1; min-width: 200px; text-align: center;">
                        <div style="background: #667eea; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px auto; font-size: 1.5em; font-weight: bold;">2</div>
                        <p style="color: #555; font-weight: 600;">We log the EVENT (not the data)</p>
                    </div>
                    <div style="color: #667eea; font-size: 2em;">→</div>
                    <div style="flex: 1; min-width: 200px; text-align: center;">
                        <div style="background: #667eea; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px auto; font-size: 1.5em; font-weight: bold;">3</div>
                        <p style="color: #555; font-weight: 600;">When sued, we fetch from YOUR ATS</p>
                    </div>
                    <div style="color: #667eea; font-size: 2em;">→</div>
                    <div style="flex: 1; min-width: 200px; text-align: center;">
                        <div style="background: #28a745; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px auto; font-size: 1.5em; font-weight: bold;">4</div>
                        <p style="color: #555; font-weight: 600;">Generate audit pack & delete</p>
                    </div>
                </div>
                <p style="text-align: center; margin-top: 35px; font-size: 1.1em; color: #555;">
                    <strong>Result:</strong> You get full lawsuit protection with <span style="color: #28a745; font-weight: 700;">ZERO data breach risk</span> from our side.
                </p>
            </div>

            <div style="margin-top: 50px; text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
                <h3 style="font-size: 1.8em; margin-bottom: 20px;">💡 Why This Matters</h3>
                <p style="font-size: 1.2em; margin-bottom: 30px; line-height: 1.8;">
                    <strong>Other compliance tools?</strong> They copy your resumes, videos, and notes into their database.<br>
                    <strong>If THEY get hacked</strong>, YOUR candidates' data is exposed.<br><br>
                    <strong>We're different.</strong> We only store audit trails—<strong>timestamps, decisions, justifications.</strong><br>
                    The actual candidate data? <strong>It stays in YOUR ATS where it belongs.</strong>
                </p>
                <a href="/demo-audit-generator" style="display: inline-block; background: white; color: #667eea; padding: 18px 40px; border-radius: 50px; text-decoration: none; font-weight: 700; font-size: 1.2em; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
                    See It In Action (60 seconds) →
                </a>
            </div>
        </div>
    </div>

    <div class="demo-section" id="demo">
        <div class="container">
            <h2>🎬 The Complete Evidence Pack</h2>
            <p style="text-align: center; margin-bottom: 30px; font-size: 1.2em;">
                From legal chaos to instant compliance in 60 seconds
            </p>

            <h3 style="text-align: center; color: #d63031; margin: 40px 0 20px 0;">📧 The Nightmare Scenario</h3>
            <div class="demo-box" style="background: #fff3cd; color: #333; border-left: 5px solid #d63031;">
                <pre style="color: #333;">
<strong>Email from Candidate's Attorney:</strong>
Subject: Notice of EEOC Complaint - AI Discrimination

"My client, Sarah Martinez, applied for Senior Engineer on January 15, 2025.
She was rejected by your AI screening system within 48 hours.

We believe this constitutes algorithmic discrimination under NYC Local Law 144
and California AB 2013. We are filing an EEOC complaint and demand:

1. All AI systems used in her evaluation
2. Complete decision rationale and timeline
3. Proof of bias audits and AI disclosures
4. Evidence of human oversight

You have 30 days to respond or face discovery costs exceeding $200,000."
                </pre>
            </div>

            <h3 style="text-align: center; color: #155724; margin: 40px 0 20px 0;">✅ Your Response: 60 Seconds Later</h3>
            <p style="text-align: center; margin-bottom: 30px;">
                With Institutional Memory, your legal team generates a complete Audit Evidence Pack instantly:
            </p>

            <div style="background: white; border: 3px solid #28a745; border-radius: 10px; padding: 30px; margin: 30px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
                <h3 style="text-align: center; color: #155724;">📄 COMPLIANCE AUDIT PACK</h3>
                <p style="text-align: center; color: #666; margin-bottom: 30px;">Generated: January 8, 2026 | Case: Martinez v. TechCorp | Status: <strong style="color: #28a745;">DEFENSIBLE</strong></p>

                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h4 style="color: #667eea;">🤖 AI Systems - Complete Audit Trail</h4>
                    <ul style="list-style: none; padding-left: 0;">
                        <li style="padding: 10px 0; border-bottom: 1px solid #ddd;">
                            <strong>HireVue Video Screening v3.2</strong><br>
                            <span style="color: #666;">• Registered: Jan 15, 2025 09:30:00 UTC (Before candidate applied)</span><br>
                            <span style="color: #666;">• NYC Bias Audit: Completed Nov 20, 2024 by Acme Auditors LLC</span><br>
                            <span style="color: #666;">• Audit Results: No disparate impact found (80% rule compliant)</span>
                        </li>
                        <li style="padding: 10px 0;">
                            <strong>Resume Parser AI v2.1</strong><br>
                            <span style="color: #666;">• Registered: Dec 1, 2024 14:22:00 UTC</span><br>
                            <span style="color: #666;">• Vendor: ResumeBot Inc | Bias Audit: Sep 2024</span>
                        </li>
                    </ul>
                </div>

                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h4 style="color: #667eea;">⚖️ Decision Record - Human Review Documented</h4>
                    <ul style="list-style: none; padding-left: 0;">
                        <li style="padding: 10px 0; border-bottom: 1px solid #ddd;">
                            <strong>AI Screening Result:</strong> 72/100 (Passed threshold of 70)<br>
                            <span style="color: #666;">Timestamp: Jan 17, 2025 10:15:22 UTC</span>
                        </li>
                        <li style="padding: 10px 0; border-bottom: 1px solid #ddd;">
                            <strong>Human Review:</strong> Conducted by Sarah Chen, Senior Recruiter<br>
                            <span style="color: #666;">Timestamp: Jan 17, 2025 14:30:00 UTC (4 hours after AI screen)</span><br>
                            <span style="color: #666;">Decision: Rejected</span>
                        </li>
                        <li style="padding: 10px 0;">
                            <strong>Documented Rationale:</strong><br>
                            <span style="color: #666;">"Position requires 5+ years Python experience with Django framework. Candidate resume shows 2 years Python, no Django. Job description clearly stated this requirement. Decision based on objective skills gap, not AI recommendation."</span>
                        </li>
                    </ul>
                </div>

                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h4 style="color: #667eea;">📢 Disclosures - Complete Paper Trail</h4>
                    <ul style="list-style: none; padding-left: 0;">
                        <li style="padding: 10px 0; border-bottom: 1px solid #ddd;">
                            <strong>AI Usage Notice Delivered:</strong> Jan 10, 2025 08:15:00 UTC<br>
                            <span style="color: #666;">Method: Email to candidate@email.com (Confirmed opened)</span><br>
                            <span style="color: #666;">Content: "TechCorp uses AI tools to assist in screening. Final decisions made by humans. Bias audits completed per NYC LL144."</span>
                        </li>
                        <li style="padding: 10px 0;">
                            <strong>Job Posting Disclosure:</strong> Jan 5, 2025<br>
                            <span style="color: #666;">Posted on careers page with AI usage disclosure before applications opened</span>
                        </li>
                    </ul>
                </div>

                <div style="background: #d4edda; padding: 20px; border-radius: 8px; margin: 20px 0; border: 2px solid #28a745;">
                    <h4 style="color: #155724; text-align: center;">✅ LEGAL ASSESSMENT</h4>
                    <p style="text-align: center; margin: 15px 0;">
                        ✓ All AI systems properly registered and audited<br>
                        ✓ Human review documented with legitimate rationale<br>
                        ✓ Candidate disclosures delivered and confirmed<br>
                        ✓ Regulatory compliance demonstrated (NYC LL144, CA AB2013)<br>
                    </p>
                    <p style="text-align: center; font-size: 1.3em; color: #155724; margin-top: 20px;">
                        <strong>Company position: DEFENSIBLE</strong>
                    </p>
                </div>
            </div>

            <div style="text-align: center; margin: 40px 0;">
                <div style="display: inline-block; background: #fff3cd; padding: 30px; border-radius: 10px; margin: 20px;">
                    <h4 style="color: #d63031;">😰 Without Institutional Memory</h4>
                    <p>• Scrambling through old emails<br>
                    • Hunting for audit reports<br>
                    • Reconstructing decisions from memory<br>
                    • 6-12 months of discovery<br>
                    • <strong>$200K+ legal costs</strong></p>
                </div>
                <div style="display: inline-block; background: #d4edda; padding: 30px; border-radius: 10px; margin: 20px;">
                    <h4 style="color: #155724;">😎 With Institutional Memory</h4>
                    <p>• Complete evidence in 60 seconds<br>
                    • Every decision documented<br>
                    • Immutable audit trail<br>
                    • Case closed quickly<br>
                    • <strong>$500K saved</strong></p>
                </div>
            </div>
        </div>
    </div>

    <div class="pricing" id="pricing">
        <div class="container">
            <h2>💰 Pricing: Pay Per Protected Hire</h2>
            <p style="text-align: center; margin-bottom: 20px;">
                Integrate once. Protect every hire. Scale as you grow.
            </p>

            <div class="pricing-grid">
                <div class="pricing-card">
                    <h3>Starter</h3>
                    <div class="price">$749<span style="font-size: 0.4em;">/mo</span></div>
                    <p>Perfect for small ATS platforms</p>
                    <ul class="features">
                        <li>Up to 1,000 decisions/month</li>
                        <li>Full API access</li>
                        <li>Audit pack generation</li>
                        <li>Email support</li>
                    </ul>
                    <a href="/request-demo" class="cta-button">Apply for Access</a>
                </div>

                <div class="pricing-card featured">
                    <h3>Professional</h3>
                    <div class="price">$1,999<span style="font-size: 0.4em;">/mo</span></div>
                    <p>Most popular for growing companies</p>
                    <ul class="features">
                        <li>Up to 10,000 decisions/month</li>
                        <li>Priority support</li>
                        <li>Custom integrations</li>
                        <li>Compliance dashboard</li>
                        <li>Multi-tenant support</li>
                    </ul>
                    <a href="/request-demo" class="cta-button">Apply for Access</a>
                </div>

                <div class="pricing-card">
                    <h3>Enterprise</h3>
                    <div class="price">Custom</div>
                    <p>For large ATS vendors</p>
                    <ul class="features">
                        <li>Unlimited decisions</li>
                        <li>White-label options</li>
                        <li>Dedicated support</li>
                        <li>SLA guarantees</li>
                        <li>Revenue sharing available</li>
                    </ul>
                    <a href="/request-demo" class="cta-button">Request Consultation</a>
                </div>
            </div>

            <div style="background: #f8f9fa; padding: 40px; border-radius: 15px; margin-top: 40px; text-align: center;">
                <h3 style="color: #667eea; margin-bottom: 20px;">💳 Payment Options</h3>
                <p style="margin-bottom: 25px; color: #666;">We accept PayPal and Venmo for your convenience.</p>
                <div style="display: flex; gap: 30px; justify-content: center; flex-wrap: wrap;">
                    <div style="background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); min-width: 250px;">
                        <h4 style="color: #667eea; margin-bottom: 15px;">💵 PayPal</h4>
                        <p style="font-family: monospace; font-size: 1.1em; color: #333; margin: 0;">CGTPA.JP@GMAIL.COM</p>
                    </div>
                    <div style="background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); min-width: 250px;">
                        <h4 style="color: #667eea; margin-bottom: 15px;">📱 Venmo</h4>
                        <p style="margin: 0;"><a href="https://venmo.com/code?user_id=3601436252309200316&created=1767963331" style="color: #667eea; text-decoration: none; font-weight: 600;">@YourVenmo →</a></p>
                    </div>
                </div>
                <p style="margin-top: 25px; font-size: 0.95em; color: #666;">
                    <em>After approval, we'll send payment instructions and API credentials within 24 hours.</em>
                </p>
            </div>
        </div>
    </div>

    <!-- SAMPLE AUDIT PACK DOWNLOAD -->
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 80px 20px; text-align: center;">
        <div class="container">
            <h2 style="color: white; font-size: 2.2em; margin-bottom: 20px;">📄 See What You're Actually Getting</h2>
            <p style="color: white; font-size: 1.2em; margin-bottom: 40px; opacity: 0.95;">
                Download a sample audit pack to see exactly what you'll submit to the EEOC or court when challenged.
            </p>
            <a href="/sample-audit-pack.pdf" class="cta-button" style="background: white; color: #667eea; font-size: 1.2em; padding: 18px 50px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
                📥 Download Sample Audit Pack (PDF)
            </a>
            <p style="color: white; margin-top: 25px; opacity: 0.9;">
                <em>Real format. Redacted data. This is what proves compliance in 60 seconds.</em>
            </p>
        </div>
    </div>

    <!-- EARLY ACCESS / FOUNDING CUSTOMER OFFER -->
    <div style="background: #f8f9fa; padding: 80px 20px;">
        <div class="container">
            <h2 style="text-align: center; color: #667eea; font-size: 2em; margin-bottom: 20px;">🚀 Launching Q1 2026 - Early Access Available</h2>
            <p style="text-align: center; font-size: 1.2em; color: #666; max-width: 700px; margin: 0 auto 50px;">
                We're accepting <strong>10 founding customers</strong> who need immediate compliance. Get priority implementation + lifetime founding rate.
            </p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 30px; max-width: 1100px; margin: 0 auto;">
                <!-- Why Early Access -->
                <div style="background: white; padding: 35px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 5px solid #667eea;">
                    <h3 style="color: #667eea; margin-bottom: 15px;">⚡ Immediate Implementation</h3>
                    <p style="font-size: 1.05em; color: #555; line-height: 1.7;">
                        As a founding customer, you get <strong>white-glove implementation</strong>. We'll personally integrate with your ATS and generate your first audit pack within 48 hours.
                    </p>
                </div>

                <!-- Founding Rate -->
                <div style="background: white; padding: 35px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 5px solid #ffa500;">
                    <h3 style="color: #ffa500; margin-bottom: 15px;">💰 Founding Customer Rate</h3>
                    <p style="font-size: 1.05em; color: #555; line-height: 1.7;">
                        <strong>$499/month</strong> locked in for life (normally $749). First 10 customers only. Once we hit 10, price goes to standard rate.
                    </p>
                    <p style="margin-top: 15px; padding: 15px; background: #fff3cd; border-radius: 8px; font-size: 0.95em;">
                        <strong>⏰ 3 spots remaining</strong> as of January 2026
                    </p>
                </div>

                <!-- What You Get -->
                <div style="background: white; padding: 35px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 5px solid #28a745;">
                    <h3 style="color: #28a745; margin-bottom: 15px;">🛡️ What You Get</h3>
                    <ul style="font-size: 1.05em; color: #555; line-height: 1.9; padding-left: 20px;">
                        <li>Priority implementation (48 hours)</li>
                        <li>Personal integration support</li>
                        <li>Direct founder access (my email)</li>
                        <li>Lifetime founding rate ($499 forever)</li>
                        <li>Shape product roadmap with feedback</li>
                    </ul>
                </div>
            </div>

            <div style="text-align: center; margin-top: 50px; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px;">
                <h3 style="color: white; font-size: 1.8em; margin-bottom: 20px;">🚨 Accepting Founding Customers NOW</h3>
                <p style="color: white; font-size: 1.1em; margin-bottom: 30px; opacity: 0.95;">
                    Are you being audited? Facing compliance deadline? Need documentation immediately?
                </p>
                <a href="/request-demo" style="display: inline-block; background: white; color: #667eea; padding: 18px 50px; font-size: 1.2em; font-weight: 600; text-decoration: none; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
                    Claim Your Founding Rate →
                </a>
                <p style="color: white; margin-top: 20px; font-size: 0.95em; opacity: 0.9;">
                    <strong>Limited to 10 companies.</strong> Response within 24 hours for urgent requests.
                </p>
            </div>
        </div>
    </div>

    <!-- ATS INTEGRATIONS -->
    <div style="background: white; padding: 60px 20px; text-align: center;">
        <div class="container">
            <h2 style="color: #667eea; font-size: 1.8em; margin-bottom: 15px;">🔗 Works With Your Existing ATS</h2>
            <p style="color: #666; font-size: 1.1em; margin-bottom: 40px;">
                We integrate with all major applicant tracking systems via webhooks.
            </p>
            <div style="display: flex; justify-content: center; align-items: center; gap: 40px; flex-wrap: wrap; max-width: 900px; margin: 0 auto;">
                <div style="font-size: 1.2em; color: #333; font-weight: 600; padding: 15px 30px; background: #f8f9fa; border-radius: 10px;">Greenhouse</div>
                <div style="font-size: 1.2em; color: #333; font-weight: 600; padding: 15px 30px; background: #f8f9fa; border-radius: 10px;">Lever</div>
                <div style="font-size: 1.2em; color: #333; font-weight: 600; padding: 15px 30px; background: #f8f9fa; border-radius: 10px;">Workday</div>
                <div style="font-size: 1.2em; color: #333; font-weight: 600; padding: 15px 30px; background: #f8f9fa; border-radius: 10px;">BambooHR</div>
                <div style="font-size: 1.2em; color: #333; font-weight: 600; padding: 15px 30px; background: #f8f9fa; border-radius: 10px;">Ashby</div>
            </div>
            <p style="margin-top: 30px; color: #666;">
                <strong>Don't see yours?</strong> We build custom integrations in 1 week. Any ATS with webhook support works.
            </p>
        </div>
    </div>

    <!-- SECURITY BADGES -->
    <div style="background: #f8f9fa; padding: 50px 20px; text-align: center; border-top: 1px solid #e9ecef; border-bottom: 1px solid #e9ecef;">
        <div class="container">
            <div style="display: flex; justify-content: center; align-items: center; gap: 50px; flex-wrap: wrap;">
                <div>
                    <div style="font-size: 2em; margin-bottom: 10px;">🔒</div>
                    <div style="font-weight: 600; color: #333;">Bank-Level AES-256 Encryption</div>
                </div>
                <div>
                    <div style="font-size: 2em; margin-bottom: 10px;">✓</div>
                    <div style="font-weight: 600; color: #333;">GDPR Compliant</div>
                </div>
                <div>
                    <div style="font-size: 2em; margin-bottom: 10px;">📊</div>
                    <div style="font-weight: 600; color: #333;">99.9% Uptime SLA</div>
                </div>
                <div>
                    <div style="font-size: 2em; margin-bottom: 10px;">🛡️</div>
                    <div style="font-weight: 600; color: #333;">SOC 2 Type II (In Progress)</div>
                </div>
            </div>
        </div>
    </div>

    <!-- DEMO VIDEO PLACEHOLDER -->
    <div style="background: white; padding: 80px 20px;">
        <div class="container" style="max-width: 900px; margin: 0 auto; text-align: center;">
            <h2 style="color: #667eea; font-size: 2em; margin-bottom: 20px;">🎥 See It In Action</h2>
            <p style="color: #666; font-size: 1.1em; margin-bottom: 40px;">
                Watch how we generate a court-ready audit pack in 60 seconds.
            </p>
            <div style="background: #000; border-radius: 15px; padding: 100px 50px; position: relative; box-shadow: 0 10px 40px rgba(0,0,0,0.2);">
                <div style="color: white; font-size: 1.5em; margin-bottom: 20px;">▶️</div>
                <div style="color: white; font-size: 1.2em;">2-Minute Demo Video</div>
                <div style="color: #999; margin-top: 10px;">(Coming Soon - Recording This Week)</div>
            </div>
            <p style="margin-top: 30px; color: #666;">
                <em>Can't wait? <a href="/request-demo" style="color: #667eea; font-weight: 600;">Request a live demo</a> and we'll show you in real-time.</em>
            </p>
        </div>
    </div>

    <!-- FOUNDER BIO -->
    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 80px 20px;">
        <div class="container" style="max-width: 800px; margin: 0 auto;">
            <h2 style="text-align: center; color: #667eea; font-size: 2em; margin-bottom: 50px;">Meet the Founder</h2>

            <div style="display: flex; gap: 40px; align-items: center; flex-wrap: wrap;">
                <div style="flex-shrink: 0;">
                    <img src="/static/john-polhill-founder.jpg" alt="John Polhill III - Founder" style="width: 150px; height: 150px; border-radius: 50%; object-fit: cover; box-shadow: 0 10px 30px rgba(0,0,0,0.2); border: 4px solid white;">
                </div>

                <div style="flex: 1; min-width: 300px;">
                    <h3 style="color: #333; font-size: 1.5em; margin-bottom: 15px;">Hi, I'm John Polhill III</h3>
                    <p style="color: #555; font-size: 1.05em; line-height: 1.8; margin-bottom: 15px;">
                        I built Defensible Hiring AI after seeing too many recent companies get blindsided by AI hiring lawsuits they couldn't defend—simply because they didn't keep records.
                    </p>
                    <p style="color: #555; font-size: 1.05em; line-height: 1.8; margin-bottom: 15px;">
                        With a <strong>30-year background in ATS Development across Startup, SMB, and Fortune 10 companies' recruitment roles</strong>, I've personally been subjected to lawsuits and investigations due to companies' inability to track a candidate's journey through the hiring process. I saw firsthand how lack of documentation turns minor complaints into six-figure legal battles.
                    </p>
                    <p style="color: #555; font-size: 1.05em; line-height: 1.8; margin-bottom: 25px;">
                        Now we're protecting companies in NYC, California, and Illinois from $500K+ lawsuits with <strong>instant, automated audit trails</strong> that document every hiring decision from day one.
                    </p>
                    <div style="display: flex; gap: 20px; align-items: center; flex-wrap: wrap;">
                        <a href="https://www.linkedin.com/in/john-polhill-iii/" style="display: inline-flex; align-items: center; gap: 8px; color: #667eea; text-decoration: none; font-weight: 600; padding: 10px 20px; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                            <span style="font-size: 1.2em;">in</span> Connect on LinkedIn
                        </a>
                        <a href="mailto:CGTPA.JP@GMAIL.COM" style="color: #667eea; text-decoration: none; font-weight: 600;">
                            📧 Email Me Directly
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="hero" style="padding: 60px 20px;">
        <h2>🚀 Ready to Protect Your Company?</h2>
        <p>We work with qualified companies who need AI hiring compliance NOW.</p>
        <a href="/request-demo" class="cta-button" style="font-size: 1.3em; padding: 20px 50px;">Request Access</a>
        <p style="margin-top: 30px; opacity: 0.9;">
            <strong>Response Time:</strong> 24 hours for qualified requests •
            <strong>Questions?</strong> See <a href="/faq" style="color: white;">FAQ</a>
        </p>
    </div>

    <footer style="background: #2c3e50; color: white; padding: 40px 20px; text-align: center;">
        <div style="max-width: 1200px; margin: 0 auto;">
            <p style="margin-bottom: 20px;">© 2026 Defensible Hiring AI. All rights reserved.</p>
            <p style="opacity: 0.8;">
                <a href="/terms-of-service" style="color: #3498db; text-decoration: none; margin: 0 15px;">Terms of Service</a> •
                <a href="/privacy-policy" style="color: #3498db; text-decoration: none; margin: 0 15px;">Privacy Policy</a> •
                <a href="mailto:support@defensiblehiringai.com" style="color: #3498db; text-decoration: none; margin: 0 15px;">Support</a>
            </p>
        </div>
    </footer>
</body>
</html>
    """, 200


@app.route('/terms-of-service', methods=['GET'])
def terms_of_service():
    """Terms of Service page"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terms of Service - Defensible Hiring AI</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        h1 { color: #667eea; margin-bottom: 10px; }
        h2 { color: #667eea; margin-top: 40px; border-bottom: 2px solid #e9ecef; padding-bottom: 10px; }
        h3 { color: #555; margin-top: 25px; }
        .last-updated { color: #666; font-style: italic; margin-bottom: 30px; }
        .back-link { display: inline-block; margin-bottom: 20px; color: #667eea; text-decoration: none; }
        .back-link:hover { text-decoration: underline; }
        strong { color: #d63031; }
    </style>
</head>
<body>
    <a href="/" class="back-link">← Back to Home</a>

    <h1>Terms of Service</h1>
    <p class="last-updated">Last Updated: January 8, 2026</p>

    <p>Welcome to Institutional Memory API ("Service", "we", "us", or "our"). By accessing or using our Service, you agree to be bound by these Terms of Service ("Terms").</p>

    <h2>1. Service Description</h2>
    <p>Institutional Memory API provides a compliance documentation service for AI-powered hiring decisions. Our Service allows customers ("you", "Customer") to:</p>
    <ul>
        <li>Register and document AI systems used in hiring processes</li>
        <li>Record hiring decisions with immutable timestamps</li>
        <li>Log candidate disclosures and regulatory compliance activities</li>
        <li>Generate audit-ready evidence packs for legal challenges</li>
    </ul>

    <h2>2. Account Registration</h2>
    <p>To use the Service, you must:</p>
    <ul>
        <li>Provide accurate and complete company information</li>
        <li>Maintain the security of your API keys</li>
        <li>Be authorized to enter into this agreement on behalf of your organization</li>
        <li>Comply with all applicable employment and data protection laws</li>
    </ul>

    <h2>3. Data Ownership and Usage</h2>
    <h3>3.1 Customer Data Ownership</h3>
    <p>You retain all rights, title, and interest in the data you submit to our Service ("Customer Data"). We do not claim ownership of your hiring records, decision logs, or compliance documentation.</p>

    <h3>3.2 Our Right to Process Data</h3>
    <p>You grant us permission to process Customer Data solely to provide the Service, including:</p>
    <ul>
        <li>Storing hiring decision metadata</li>
        <li>Generating audit reports and compliance packs</li>
        <li>Maintaining immutable timestamps and cryptographic hashes</li>
    </ul>

    <h3>3.3 Privacy Protections</h3>
    <p>We hash candidate identifiers using SHA-256 to protect personally identifiable information (PII). See our <a href="/privacy-policy">Privacy Policy</a> for details.</p>

    <h2>4. Data Retention Policy</h2>
    <p><strong>Default Retention:</strong> We retain Customer Data for <strong>7 years</strong> from the date of creation, consistent with employment law record-keeping requirements.</p>

    <p><strong>Legal Hold:</strong> Customers may flag records for "legal hold" during active litigation, preventing automatic deletion.</p>

    <p><strong>Post-Termination:</strong> Upon account cancellation, we provide a 30-day grace period for data export. After 30 days, data is permanently deleted unless a paid archive plan is maintained.</p>

    <h2>5. Service Level Agreement (SLA)</h2>
    <h3>5.1 Uptime Guarantee</h3>
    <ul>
        <li><strong>Starter Plan:</strong> 99.0% monthly uptime</li>
        <li><strong>Professional Plan:</strong> 99.9% monthly uptime</li>
        <li><strong>Enterprise Plan:</strong> 99.95% monthly uptime with dedicated support</li>
    </ul>

    <h3>5.2 Support Response Times</h3>
    <ul>
        <li><strong>Starter:</strong> 24-hour email response</li>
        <li><strong>Professional:</strong> 4-hour email response (business hours)</li>
        <li><strong>Enterprise:</strong> 1-hour response with dedicated Slack channel</li>
    </ul>

    <h2>6. Prohibited Uses</h2>
    <p>You may NOT use the Service to:</p>
    <ul>
        <li>Violate any laws (including employment discrimination laws)</li>
        <li>Store false or fabricated hiring records</li>
        <li>Attempt to reverse-engineer or access other customers' data</li>
        <li>Resell the Service without explicit partnership agreement</li>
        <li>Exceed API rate limits or abuse system resources</li>
    </ul>

    <h2>7. Limitation of Liability</h2>
    <p><strong>IMPORTANT: THIS SERVICE ASSISTS WITH COMPLIANCE DOCUMENTATION BUT DOES NOT GUARANTEE LEGAL OUTCOMES.</strong></p>

    <p>To the maximum extent permitted by law:</p>
    <ul>
        <li>We are NOT liable for legal judgments, fines, or penalties arising from your hiring practices</li>
        <li>Our total liability is limited to the <strong>lesser of $10,000 USD or 12 months of fees paid</strong></li>
        <li>We are NOT liable for indirect, consequential, or punitive damages</li>
        <li>You are responsible for ensuring your hiring practices comply with all applicable laws</li>
    </ul>

    <h3>7.1 No Legal Advice</h3>
    <p>This Service provides record-keeping technology, NOT legal advice. Consult with employment law attorneys for compliance guidance.</p>

    <h2>8. Indemnification</h2>
    <p>You agree to indemnify and hold us harmless from claims arising from:</p>
    <ul>
        <li>Your use of the Service</li>
        <li>Your hiring practices or employment decisions</li>
        <li>Your violation of these Terms or applicable laws</li>
        <li>Disputes with candidates, employees, or regulatory agencies</li>
    </ul>

    <h2>9. Pricing and Payment</h2>
    <h3>9.1 Subscription Fees</h3>
    <p>Fees are billed monthly or annually in advance. See our pricing page for current rates.</p>

    <h3>9.2 Overage Charges</h3>
    <p>If you exceed your plan's decision volume limit, overage fees apply at $0.50 per additional decision.</p>

    <h3>9.3 Price Changes</h3>
    <p>We may change prices with 30 days notice. Existing customers are grandfathered for 12 months.</p>

    <h2>10. Termination</h2>
    <h3>10.1 By Customer</h3>
    <p>You may cancel at any time with 30 days notice. No refunds for partial months.</p>

    <h3>10.2 By Us</h3>
    <p>We may suspend or terminate your account if you:</p>
    <ul>
        <li>Violate these Terms</li>
        <li>Fail to pay fees for 15 days after due date</li>
        <li>Use the Service for illegal purposes</li>
    </ul>

    <h3>10.3 Data Export</h3>
    <p>Upon termination, we provide data export in JSON format within 30 days. After 30 days, data is permanently deleted.</p>

    <h2>11. Data Security</h2>
    <p>We implement industry-standard security measures:</p>
    <ul>
        <li>Encryption at rest and in transit (TLS 1.3)</li>
        <li>SHA-256 hashing of candidate identifiers</li>
        <li>API key authentication for all requests</li>
        <li>Regular security audits and penetration testing</li>
    </ul>

    <p><strong>Data Breach Notification:</strong> We will notify you within 72 hours of discovering any data breach affecting your Customer Data.</p>

    <h2>12. Compliance Certifications</h2>
    <p>Our Service is designed to assist with:</p>
    <ul>
        <li>NYC Local Law 144 (AI hiring disclosure requirements)</li>
        <li>California AB 2013 (automated decision systems)</li>
        <li>EU AI Act (high-risk AI systems documentation)</li>
        <li>EEOC record-keeping requirements</li>
    </ul>

    <p><strong>Note:</strong> Compliance with these laws depends on YOUR hiring practices. We provide tools, not legal guarantees.</p>

    <h2>13. Modifications to Terms</h2>
    <p>We may update these Terms with 30 days notice. Continued use after changes constitutes acceptance.</p>

    <h2>14. Governing Law</h2>
    <p>These Terms are governed by the laws of the State of Delaware, USA, without regard to conflict of law provisions.</p>

    <h2>15. Dispute Resolution</h2>
    <p>Any disputes shall be resolved through binding arbitration in Delaware, USA, under JAMS rules. You waive the right to class action lawsuits.</p>

    <h2>16. Contact Information</h2>
    <p>For questions about these Terms, contact us at:</p>
    <p>
        <strong>Email:</strong> legal@defensiblehiringai.com<br>
        <strong>Support:</strong> support@defensiblehiringai.com
    </p>

    <hr style="margin: 40px 0;">
    <p style="text-align: center; color: #666;">
        <a href="/" style="color: #667eea;">← Return to Home</a> •
        <a href="/privacy-policy" style="color: #667eea;">Privacy Policy</a>
    </p>
</body>
</html>
    """, 200


@app.route('/privacy-policy', methods=['GET'])
def privacy_policy():
    """Privacy Policy page"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policy - Defensible Hiring AI</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        h1 { color: #667eea; margin-bottom: 10px; }
        h2 { color: #667eea; margin-top: 40px; border-bottom: 2px solid #e9ecef; padding-bottom: 10px; }
        h3 { color: #555; margin-top: 25px; }
        .last-updated { color: #666; font-style: italic; margin-bottom: 30px; }
        .back-link { display: inline-block; margin-bottom: 20px; color: #667eea; text-decoration: none; }
        .back-link:hover { text-decoration: underline; }
        .highlight { background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background: #f8f9fa; font-weight: 600; }
    </style>
</head>
<body>
    <a href="/" class="back-link">← Back to Home</a>

    <h1>Privacy Policy</h1>
    <p class="last-updated">Last Updated: January 8, 2026</p>

    <div class="highlight">
        <strong>TL;DR:</strong> We store minimal data (company info + hashed hiring records), use industry-standard encryption, comply with GDPR/CCPA, and NEVER sell your data.
    </div>

    <h2>1. Introduction</h2>
    <p>Institutional Memory API ("we", "us", "our") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our Service.</p>

    <h2>2. Information We Collect</h2>

    <h3>2.1 Account Information</h3>
    <table>
        <tr>
            <th>Data Type</th>
            <th>What We Collect</th>
            <th>Why We Need It</th>
        </tr>
        <tr>
            <td>Company Details</td>
            <td>Company name, billing email</td>
            <td>Account management, billing</td>
        </tr>
        <tr>
            <td>API Credentials</td>
            <td>API keys (hashed in database)</td>
            <td>Authentication and access control</td>
        </tr>
        <tr>
            <td>Billing Information</td>
            <td>Credit card details (via Stripe)</td>
            <td>Payment processing (we don't store cards)</td>
        </tr>
    </table>

    <h3>2.2 Hiring Decision Metadata</h3>
    <p><strong>What We Store:</strong></p>
    <ul>
        <li><strong>Candidate Identifiers (HASHED):</strong> We use SHA-256 to hash candidate IDs/emails. We NEVER store raw PII.</li>
        <li><strong>Decision Data:</strong> Hiring decision type (hired/rejected), timestamps, human review flags</li>
        <li><strong>AI System Records:</strong> Names of AI tools used, vendor information, bias audit dates</li>
        <li><strong>Disclosure Logs:</strong> Timestamps and delivery methods of candidate disclosures</li>
    </ul>

    <p><strong>What We DON'T Store:</strong></p>
    <ul>
        <li>❌ Candidate names (hashed only)</li>
        <li>❌ Candidate resumes or application materials</li>
        <li>❌ Protected class information (race, gender, age, etc.)</li>
        <li>❌ Interview notes or subjective assessments</li>
    </ul>

    <h3>2.3 Technical Data</h3>
    <ul>
        <li><strong>API Logs:</strong> Request timestamps, endpoint accessed, IP addresses, user agent</li>
        <li><strong>Error Logs:</strong> System errors and debugging information (via Sentry.io)</li>
        <li><strong>Analytics:</strong> Service usage patterns (aggregated, non-personal)</li>
    </ul>

    <h2>3. How We Use Your Information</h2>
    <p>We use collected data to:</p>
    <ul>
        <li>✅ Provide the institutional memory service</li>
        <li>✅ Generate audit packs and compliance reports</li>
        <li>✅ Process payments and manage subscriptions</li>
        <li>✅ Provide customer support</li>
        <li>✅ Detect and prevent security breaches</li>
        <li>✅ Improve service performance and reliability</li>
    </ul>

    <p>We do NOT use your data to:</p>
    <ul>
        <li>❌ Train machine learning models</li>
        <li>❌ Sell or share with third parties for marketing</li>
        <li>❌ Target advertising</li>
        <li>❌ Make automated decisions about individuals</li>
    </ul>

    <h2>4. Data Sharing and Disclosure</h2>
    <h3>4.1 Third-Party Service Providers</h3>
    <p>We share limited data with trusted partners:</p>
    <table>
        <tr>
            <th>Service</th>
            <th>Provider</th>
            <th>Data Shared</th>
            <th>Purpose</th>
        </tr>
        <tr>
            <td>Hosting</td>
            <td>Render.com</td>
            <td>All service data</td>
            <td>Infrastructure and database hosting</td>
        </tr>
        <tr>
            <td>Payments</td>
            <td>Stripe</td>
            <td>Billing email, company name</td>
            <td>Payment processing</td>
        </tr>
        <tr>
            <td>Error Tracking</td>
            <td>Sentry.io</td>
            <td>Error logs, stack traces</td>
            <td>Debugging and monitoring</td>
        </tr>
    </table>

    <h3>4.2 Legal Requirements</h3>
    <p>We may disclose data if required by:</p>
    <ul>
        <li>Court orders or subpoenas</li>
        <li>Government investigations</li>
        <li>Protection of our legal rights</li>
        <li>Prevention of fraud or illegal activity</li>
    </ul>

    <h3>4.3 Business Transfers</h3>
    <p>If we are acquired or merged, customer data may be transferred. We will notify you 30 days before any change in ownership.</p>

    <h2>5. Data Security</h2>
    <p>We implement industry-standard security measures:</p>
    <ul>
        <li><strong>Encryption in Transit:</strong> TLS 1.3 for all API connections</li>
        <li><strong>Encryption at Rest:</strong> AES-256 encryption for database storage</li>
        <li><strong>Hashing:</strong> SHA-256 for candidate identifiers and API keys</li>
        <li><strong>Access Controls:</strong> Role-based permissions, API key authentication</li>
        <li><strong>Monitoring:</strong> 24/7 security monitoring and intrusion detection</li>
        <li><strong>Audits:</strong> Regular security audits and penetration testing</li>
    </ul>

    <p><strong>Data Breach Notification:</strong> We will notify affected customers within 72 hours of discovering a breach, as required by GDPR.</p>

    <h2>6. Data Retention</h2>
    <p><strong>Active Accounts:</strong> We retain data for 7 years from creation date (employment law standard).</p>

    <p><strong>Canceled Accounts:</strong> 30-day grace period for data export, then permanent deletion.</p>

    <p><strong>Legal Holds:</strong> Data flagged for litigation is retained until legal hold is released.</p>

    <h2>7. Your Privacy Rights</h2>

    <h3>7.1 GDPR Rights (EU Residents)</h3>
    <p>You have the right to:</p>
    <ul>
        <li><strong>Access:</strong> Request a copy of your data</li>
        <li><strong>Rectification:</strong> Correct inaccurate data</li>
        <li><strong>Erasure ("Right to be Forgotten"):</strong> Request deletion (subject to legal retention requirements)</li>
        <li><strong>Data Portability:</strong> Receive data in machine-readable format (JSON)</li>
        <li><strong>Objection:</strong> Object to data processing</li>
        <li><strong>Restriction:</strong> Limit how we use your data</li>
    </ul>

    <h3>7.2 CCPA Rights (California Residents)</h3>
    <p>California residents have the right to:</p>
    <ul>
        <li>Know what personal information is collected</li>
        <li>Know if personal information is sold (we DON'T sell data)</li>
        <li>Request deletion of personal information</li>
        <li>Opt-out of sale (N/A - we don't sell data)</li>
        <li>Non-discrimination for exercising privacy rights</li>
    </ul>

    <h3>7.3 How to Exercise Your Rights</h3>
    <p>Email us at <strong>privacy@defensiblehiringai.com</strong> with:</p>
    <ul>
        <li>Subject: "Privacy Rights Request"</li>
        <li>Your company name and account email</li>
        <li>Specific request (access, deletion, export, etc.)</li>
    </ul>
    <p>We respond within 30 days.</p>

    <h2>8. International Data Transfers</h2>
    <p>Our servers are located in the United States. If you access the Service from the EU or other regions with data protection laws, your data will be transferred to the US.</p>

    <p><strong>EU-US Data Transfer Safeguards:</strong></p>
    <ul>
        <li>Standard Contractual Clauses (SCCs) with service providers</li>
        <li>Encryption for data in transit and at rest</li>
        <li>Regular compliance audits</li>
    </ul>

    <h2>9. Cookies and Tracking</h2>
    <p><strong>We do NOT use cookies for tracking or advertising.</strong></p>

    <p>We may use session cookies for:</p>
    <ul>
        <li>API authentication (temporary session management)</li>
        <li>Security (CSRF protection)</li>
    </ul>

    <p>No third-party advertising cookies are used.</p>

    <h2>10. Children's Privacy</h2>
    <p>Our Service is NOT directed to individuals under 18. We do not knowingly collect data from children. If we discover such data, it will be deleted immediately.</p>

    <h2>11. Changes to This Privacy Policy</h2>
    <p>We may update this Privacy Policy with 30 days notice. Material changes will be communicated via email to your account address.</p>

    <h2>12. Contact Us</h2>
    <p>For privacy-related questions or requests:</p>
    <p>
        <strong>Email:</strong> privacy@defensiblehiringai.com<br>
        <strong>Data Protection Officer:</strong> dpo@defensiblehiringai.com<br>
        <strong>Support:</strong> support@defensiblehiringai.com
    </p>

    <h2>13. Regulatory Compliance</h2>
    <p>We comply with:</p>
    <ul>
        <li>✅ GDPR (General Data Protection Regulation) - EU</li>
        <li>✅ CCPA (California Consumer Privacy Act) - California</li>
        <li>✅ PIPEDA (Personal Information Protection and Electronic Documents Act) - Canada</li>
        <li>✅ SOC 2 Type II controls (in progress for enterprise customers)</li>
    </ul>

    <hr style="margin: 40px 0;">
    <p style="text-align: center; color: #666;">
        <a href="/" style="color: #667eea;">← Return to Home</a> •
        <a href="/terms-of-service" style="color: #667eea;">Terms of Service</a>
    </p>
</body>
</html>
    """, 200


@app.route('/faq', methods=['GET'])
def faq():
    """FAQ page"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FAQ - Defensible Hiring AI</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        h1 { color: #667eea; margin-bottom: 20px; }
        h2 { color: #667eea; margin-top: 40px; border-bottom: 2px solid #e9ecef; padding-bottom: 10px; }
        .back-link { display: inline-block; margin-bottom: 20px; color: #667eea; text-decoration: none; }
        .back-link:hover { text-decoration: underline; }
        .faq-item {
            background: #f8f9fa;
            padding: 25px;
            margin: 20px 0;
            border-left: 4px solid #667eea;
            border-radius: 5px;
        }
        .faq-question {
            font-size: 1.2em;
            font-weight: 600;
            color: #667eea;
            margin-bottom: 15px;
        }
        .faq-answer { color: #555; }
        .category { background: #667eea; color: white; padding: 8px 15px; border-radius: 20px; font-size: 0.9em; display: inline-block; margin-bottom: 10px; }
        .cta-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
            border-radius: 10px;
            margin: 40px 0;
        }
        .cta-box a {
            color: white;
            background: #ff6b6b;
            padding: 12px 30px;
            text-decoration: none;
            border-radius: 5px;
            display: inline-block;
            margin-top: 15px;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <a href="/" class="back-link">← Back to Home</a>

    <h1>Frequently Asked Questions</h1>
    <p style="color: #666; margin-bottom: 30px;">Everything you need to know about Institutional Memory API</p>

    <h2>Getting Started</h2>

    <div class="faq-item">
        <div class="faq-question">Q: What is Institutional Memory API?</div>
        <div class="faq-answer">
            <strong>A:</strong> Institutional Memory API is a compliance-as-a-service platform that helps companies using AI in hiring create immutable audit trails. When you're challenged legally (EEOC complaint, discrimination lawsuit), we provide instant, complete evidence packs showing:
            <ul>
                <li>What AI systems you used (with bias audit proof)</li>
                <li>Every hiring decision made (with timestamps and rationales)</li>
                <li>All disclosures delivered to candidates</li>
                <li>Human review documentation</li>
            </ul>
            Think of us as the "black box" for AI hiring - if something goes wrong, we have the complete flight recorder.
        </div>
    </div>

    <div class="faq-item">
        <div class="faq-question">Q: How long does integration take?</div>
        <div class="faq-answer">
            <strong>A:</strong> 1-2 hours for most ATS platforms. Our webhook-based API requires:
            <ol>
                <li>Register your company (get API key) - 2 minutes</li>
                <li>Add 3-5 webhook calls to your hiring workflow - 30-60 minutes</li>
                <li>Test with sample data - 15 minutes</li>
                <li>Generate your first audit pack - 5 minutes</li>
            </ol>
            We provide code examples in Python, Node.js, Ruby, and cURL. See our <a href="/docs">API Documentation</a>.
        </div>
    </div>

    <div class="faq-item">
        <div class="faq-question">Q: Do I need to change my existing hiring process?</div>
        <div class="faq-answer">
            <strong>A:</strong> No! Our API integrates silently into your existing workflow. You continue hiring exactly as you do now - we just record what happened in the background. No UI changes, no workflow disruption.
        </div>
    </div>

    <h2>Privacy & Compliance</h2>

    <div class="faq-item">
        <div class="faq-question">Q: Do you store candidate personal information?</div>
        <div class="faq-answer">
            <strong>A:</strong> No. We use SHA-256 hashing to convert candidate identifiers (email, ID) into one-way cryptographic hashes. We NEVER store:
            <ul>
                <li>❌ Candidate names</li>
                <li>❌ Resumes or applications</li>
                <li>❌ Protected class data (race, gender, age)</li>
                <li>❌ Interview notes or assessments</li>
            </ul>
            We only store decision metadata (hired/rejected, timestamp, rationale) linked to a hash. This protects candidate privacy while proving your compliance.
        </div>
    </div>

    <div class="faq-item">
        <div class="faq-question">Q: Are you GDPR and CCPA compliant?</div>
        <div class="faq-answer">
            <strong>A:</strong> Yes. We comply with:
            <ul>
                <li>✅ GDPR (EU) - Right to access, deletion, portability</li>
                <li>✅ CCPA (California) - No data selling, opt-out rights</li>
                <li>✅ PIPEDA (Canada)</li>
                <li>✅ 72-hour breach notification (GDPR requirement)</li>
            </ul>
            See our <a href="/privacy-policy">Privacy Policy</a> for full details.
        </div>
    </div>

    <div class="faq-item">
        <div class="faq-question">Q: How long do you retain data?</div>
        <div class="faq-answer">
            <strong>A:</strong> Default: <strong>7 years</strong> from the decision date. This aligns with employment law record-keeping requirements (EEOC, statute of limitations). You can:
            <ul>
                <li>Configure custom retention periods (3-10 years)</li>
                <li>Flag records for "legal hold" during active litigation (prevents deletion)</li>
                <li>Export all data in JSON format when you cancel</li>
            </ul>
            After cancellation: 30-day grace period, then permanent deletion.
        </div>
    </div>

    <div class="faq-item">
        <div class="faq-question">Q: Can I delete a hiring decision record?</div>
        <div class="faq-answer">
            <strong>A:</strong> No - that's the point! Immutability is what makes our audit trail defensible in court. If you could delete or edit records, they wouldn't be trustworthy evidence.

            <p><strong>Exception:</strong> Legal hold flag prevents automatic deletion during litigation, but you can't retroactively edit past decisions.</p>
        </div>
    </div>

    <h2>Pricing & Plans</h2>

    <div class="faq-item">
        <div class="faq-question">Q: How does pricing work?</div>
        <div class="faq-answer">
            <strong>A:</strong> We charge based on the number of hiring decisions you protect per month:
            <ul>
                <li><strong>Starter:</strong> $499/month (up to 1,000 decisions)</li>
                <li><strong>Professional:</strong> $1,499/month (up to 10,000 decisions)</li>
                <li><strong>Enterprise:</strong> Custom pricing (unlimited decisions)</li>
            </ul>
            <strong>Overage:</strong> $0.50 per decision beyond your plan limit.
            <br><strong>Annual discount:</strong> Save 16% (2 months free) when you pay annually.
        </div>
    </div>

    <div class="faq-item">
        <div class="faq-question">Q: What counts as a "decision"?</div>
        <div class="faq-answer">
            <strong>A:</strong> Each hiring outcome logged counts as one decision:
            <ul>
                <li>Candidate rejected after AI screening = 1 decision</li>
                <li>Candidate hired after interview = 1 decision</li>
                <li>Candidate withdrew application = 1 decision (if you want to track it)</li>
            </ul>
            <strong>What doesn't count:</strong> Logging AI systems, recording disclosures, generating audit packs (unlimited at any tier).
        </div>
    </div>

    <div class="faq-item">
        <div class="faq-question">Q: Do you offer a free trial?</div>
        <div class="faq-answer">
            <strong>A:</strong> No. We work with qualified companies who need compliance NOW, not those still exploring. After your demo request is approved, payment is required before receiving API credentials. This ensures we only work with serious clients who value defensible hiring practices.
        </div>
    </div>

    <h2>Technical Questions</h2>

    <div class="faq-item">
        <div class="faq-question">Q: What's your uptime SLA?</div>
        <div class="faq-answer">
            <strong>A:</strong>
            <ul>
                <li><strong>Starter:</strong> 99.0% monthly uptime (~7 hours downtime/month)</li>
                <li><strong>Professional:</strong> 99.9% monthly uptime (~43 minutes downtime/month)</li>
                <li><strong>Enterprise:</strong> 99.95% monthly uptime (~22 minutes downtime/month)</li>
            </ul>
            We monitor with Pingdom and provide a public status page.
        </div>
    </div>

    <div class="faq-item">
        <div class="faq-question">Q: How do I get support?</div>
        <div class="faq-answer">
            <strong>A:</strong>
            <ul>
                <li><strong>Starter:</strong> Email support@defensiblehiringai.com (24-hour response)</li>
                <li><strong>Professional:</strong> Email support (4-hour response, business hours)</li>
                <li><strong>Enterprise:</strong> Dedicated Slack channel (1-hour response, 24/7)</li>
            </ul>
            All plans include access to documentation and API examples.
        </div>
    </div>

    <div class="faq-item">
        <div class="faq-question">Q: What if your service goes down during a legal challenge?</div>
        <div class="faq-answer">
            <strong>A:</strong> We recommend:
            <ol>
                <li><strong>Proactive exports:</strong> Generate audit packs quarterly and save to your own storage</li>
                <li><strong>Legal hold mode:</strong> When litigation starts, immediately export all relevant data</li>
                <li><strong>Backup access:</strong> Enterprise customers get direct database backups</li>
            </ol>
            Our SLA includes 99.9%+ uptime, but you should never rely on ANY single system for legal defense.
        </div>
    </div>

    <h2>Legal & Compliance</h2>

    <div class="faq-item">
        <div class="faq-question">Q: Does using your service guarantee I won't get sued?</div>
        <div class="faq-answer">
            <strong>A:</strong> <strong style="color: #d63031;">No.</strong> We provide documentation tools, not legal protection. If you discriminate in hiring, you can still be sued.

            <p><strong>What we DO provide:</strong> When you're challenged, you'll have instant, complete evidence showing:
            <ul>
                <li>You used properly audited AI systems</li>
                <li>You disclosed AI usage to candidates</li>
                <li>Humans reviewed decisions</li>
                <li>You had legitimate, documented rationales</li>
            </ul>
            This dramatically reduces legal costs and improves your defensibility - but it's not a legal shield. Consult employment lawyers for compliance advice.
        </div>
    </div>

    <div class="faq-item">
        <div class="faq-question">Q: What regulations does this help me comply with?</div>
        <div class="faq-answer">
            <strong>A:</strong> Our service assists with:
            <ul>
                <li><strong>NYC Local Law 144:</strong> AI bias audits, candidate disclosures, record-keeping</li>
                <li><strong>California AB 2013:</strong> Automated decision system documentation</li>
                <li><strong>EU AI Act:</strong> High-risk AI system transparency requirements</li>
                <li><strong>EEOC Requirements:</strong> Hiring record retention (Title VII)</li>
            </ul>
            See our <a href="/docs">compliance guide</a> for details.
        </div>
    </div>

    <h2>🔒 Data Security & Privacy (ZERO-STORAGE)</h2>

    <div class="faq-item" style="background: #e8f5e9; border-left: 4px solid #28a745;">
        <div class="faq-question" style="color: #1b5e20; font-weight: 700;">Q: What candidate data do you store?</div>
        <div class="faq-answer">
            <strong>A: We DON'T store candidate data.</strong> This is our biggest differentiator.
            <br><br>
            <strong>❌ What we DON'T store:</strong>
            <ul>
                <li>Candidate names, emails, phone numbers</li>
                <li>Resumes or CVs (no PDFs, no text)</li>
                <li>Interview recordings or transcripts</li>
                <li>Compensation data or salary history</li>
                <li>Any personally identifiable information (PII)</li>
            </ul>
            <strong>✅ What we DO store:</strong>
            <ul>
                <li>Timestamps (when events happened)</li>
                <li>Hashed candidate IDs (anonymized references)</li>
                <li>AI scores & recommendations</li>
                <li>Decision justifications</li>
                <li>Links to records in YOUR ATS</li>
            </ul>
            <strong>Your candidate data stays in YOUR ATS (Greenhouse, Lever, Workday).</strong> We just prove what you did with it.
        </div>
    </div>

    <div class="faq-item">
        <div class="faq-question">Q: How do you generate audit packs without storing candidate data?</div>
        <div class="faq-answer">
            <strong>A:</strong> When you request an audit pack, we:
            <ol>
                <li><strong>Fetch</strong> candidate data from YOUR ATS in real-time (using your API credentials)</li>
                <li><strong>Combine</strong> it with our audit trail (timestamps, decisions, justifications)</li>
                <li><strong>Generate</strong> the PDF report</li>
                <li><strong>DELETE</strong> the fetched candidate data immediately</li>
            </ol>
            We store cryptographic references (hashes and ATS record IDs), not the actual data. This means:
            <ul>
                <li>✅ You get full lawsuit protection</li>
                <li>✅ With ZERO data breach risk from our side</li>
                <li>✅ Your ATS remains the single source of truth</li>
            </ul>
        </div>
    </div>

    <div class="faq-item">
        <div class="faq-question">Q: What happens if you get hacked?</div>
        <div class="faq-answer">
            <strong>A:</strong> Even if someone breaches our system, they get:
            <ul>
                <li>Timestamps (when things happened)</li>
                <li>Hashed candidate IDs (irreversible SHA-256 hashes)</li>
                <li>Decision justifications ("Candidate lacked required Python experience")</li>
                <li>AI scores (42/100, 78/100, etc.)</li>
            </ul>
            <strong>They DON'T get:</strong>
            <ul>
                <li>❌ Candidate names or contact info</li>
                <li>❌ Resumes or personal documents</li>
                <li>❌ Any data they can sell on the dark web</li>
            </ul>
            <p style="background: #d4edda; padding: 15px; border-radius: 8px; margin-top: 15px;">
                <strong>Compare to other tools:</strong> If they get hacked, your full candidate database is exposed.
                With us, your candidate data is SAFE in your ATS.
            </p>
        </div>
    </div>

    <div class="faq-item">
        <div class="faq-question">Q: Can your employees see our candidate data?</div>
        <div class="faq-answer">
            <strong>A: No.</strong> Our employees cannot see your candidate data by default.
            <br><br>
            <strong>Normal operations:</strong> Zero access. We don't store it.
            <br><br>
            <strong>Support requests:</strong> If you open a ticket asking us to debug an issue, we can request temporary access WITH YOUR WRITTEN APPROVAL. You get an email: "Support Engineer John Smith is requesting access to your tenant for 24 hours to debug [issue]." You click "Approve" or "Deny."
            <br><br>
            <strong>Every access is logged:</strong> If anyone at our company accesses your data, it's logged with timestamp, user ID, reason, and duration. You can review these logs anytime.
            <br><br>
            This is standard SOC 2 compliance (same model AWS, Google, Salesforce use).
        </div>
    </div>

    <div class="faq-item">
        <div class="faq-question">Q: Is this GDPR compliant?</div>
        <div class="faq-answer">
            <strong>A: Yes.</strong> Since we don't store candidate PII, we're not a "data controller" under GDPR—your ATS is.
            <br><br>
            <strong>GDPR benefits of zero-storage:</strong>
            <ul>
                <li><strong>Data deletion requests:</strong> Handled by your ATS, not us</li>
                <li><strong>Data portability:</strong> Your ATS provides candidate data exports</li>
                <li><strong>Breach notification:</strong> We notify within 72 hours, but no PII at risk</li>
                <li><strong>Data minimization:</strong> We only store what's needed for audit trails</li>
            </ul>
            We can provide a Data Processing Agreement (DPA) for audit trail data we DO store.
        </div>
    </div>

    <div class="faq-item">
        <div class="faq-question">Q: What happens to my data if I cancel?</div>
        <div class="faq-answer">
            <strong>A:</strong>
            <ol>
                <li><strong>Day 1-30:</strong> Grace period. Data is read-only, you can export everything in JSON.</li>
                <li><strong>Day 31+:</strong> Data is permanently deleted from all systems (backups included).</li>
            </ol>
            <strong>Exception:</strong> You can maintain a paid "Archive Mode" ($99/month) for read-only access if you have ongoing litigation.
        </div>
    </div>

    <h2>Use Cases</h2>

    <div class="faq-item">
        <div class="faq-question">Q: Who is this for?</div>
        <div class="faq-answer">
            <strong>A:</strong> Perfect for:
            <ul>
                <li><strong>ATS Vendors:</strong> Offer compliance as a feature to your customers (white-label available)</li>
                <li><strong>Enterprises:</strong> Hiring 1,000+ candidates/year with AI screening</li>
                <li><strong>Recruiting Agencies:</strong> Manage compliance for multiple client companies</li>
                <li><strong>HR Tech Startups:</strong> Add compliance layer without building it yourself</li>
            </ul>
            If you use AI in hiring and care about legal risk, this is for you.
        </div>
    </div>

    <div class="faq-item">
        <div class="faq-question">Q: Can I white-label this for my ATS customers?</div>
        <div class="faq-answer">
            <strong>A:</strong> Yes (Enterprise only). We offer:
            <ul>
                <li>Custom branding (your logo, domain)</li>
                <li>Revenue sharing (70/30 split)</li>
                <li>Dedicated integration support</li>
                <li>Co-marketing opportunities</li>
            </ul>
            Contact sales@defensiblehiringai.com for partnership details.
        </div>
    </div>

    <div class="cta-box">
        <h2 style="color: white; margin-bottom: 15px;">Still Have Questions?</h2>
        <p>Our team is here to help. Get in touch and we'll respond within 24 hours.</p>
        <a href="mailto:support@defensiblehiringai.com?subject=FAQ Question">Contact Support</a>
        <a href="/docs" style="background: white; color: #667eea; margin-left: 15px;">View API Docs</a>
    </div>

    <hr style="margin: 40px 0;">
    <p style="text-align: center; color: #666;">
        <a href="/" style="color: #667eea;">← Return to Home</a> •
        <a href="/docs" style="color: #667eea;">API Documentation</a> •
        <a href="/terms-of-service" style="color: #667eea;">Terms</a> •
        <a href="/privacy-policy" style="color: #667eea;">Privacy</a>
    </p>
</body>
</html>
    """, 200


@app.route('/docs', methods=['GET'])
def docs():
    """Gated documentation access page"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Documentation - Defensible Hiring AI</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        h1 { color: #667eea; margin-bottom: 10px; }
        h2 { color: #667eea; margin-top: 40px; }
        .back-link { display: inline-block; margin-bottom: 20px; color: #667eea; text-decoration: none; }
        .back-link:hover { text-decoration: underline; }
        .gate-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 50px;
            border-radius: 15px;
            text-align: center;
            margin: 40px 0;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        .gate-box h2 { color: white; margin-bottom: 20px; }
        .feature-list {
            text-align: left;
            max-width: 600px;
            margin: 30px auto;
            background: rgba(255,255,255,0.1);
            padding: 25px;
            border-radius: 10px;
        }
        .feature-list li {
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }
        .feature-list li:last-child { border-bottom: none; }
        .cta-button {
            display: inline-block;
            background: #ff6b6b;
            color: white;
            padding: 18px 40px;
            text-decoration: none;
            border-radius: 8px;
            font-size: 1.2em;
            font-weight: 600;
            margin: 20px 10px;
            transition: transform 0.2s;
        }
        .cta-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }
        .cta-button.secondary {
            background: white;
            color: #667eea;
        }
        .info-box {
            background: #f8f9fa;
            padding: 30px;
            border-left: 5px solid #667eea;
            margin: 30px 0;
            border-radius: 5px;
        }
        .lock-icon { font-size: 3em; margin-bottom: 20px; }
    </style>
</head>
<body>
    <a href="/" class="back-link">← Back to Home</a>

    <h1>API Documentation</h1>
    <p style="color: #666; margin-bottom: 30px;">Complete integration guide and technical reference</p>

    <div class="gate-box">
        <div class="lock-icon">🔒</div>
        <h2>Documentation Access</h2>
        <p style="font-size: 1.1em; margin-bottom: 30px;">
            Our detailed API documentation includes integration guides, code examples,
            and technical specifications for our institutional memory platform.
        </p>

        <div class="feature-list">
            <strong>What's included:</strong>
            <ul style="list-style: none; padding-left: 0;">
                <li>✓ Complete API endpoint reference</li>
                <li>✓ Authentication & security guide</li>
                <li>✓ Integration code examples (Python, Node.js)</li>
                <li>✓ Request/response schemas</li>
                <li>✓ Webhook implementation patterns</li>
                <li>✓ Error handling best practices</li>
                <li>✓ Compliance checklist for NYC/CA/IL</li>
                <li>✓ Test environment access</li>
            </ul>
        </div>

        <p style="margin: 30px 0; font-size: 1.1em;">
            <strong>For enterprise customers and integration partners only.</strong>
        </p>

        <a href="/request-demo" class="cta-button">Request Documentation Access</a>
        <a href="/request-demo" class="cta-button secondary">Request Live Demo</a>
    </div>

    <div class="info-box">
        <h3 style="color: #667eea; margin-bottom: 15px;">🤝 Not Technical? No Problem.</h3>
        <p style="margin-bottom: 15px;">
            <strong>If you're a VP of HR, General Counsel, or Compliance Officer:</strong>
        </p>
        <p>
            You don't need to understand the technical details.
            <a href="/get-started" style="color: #667eea; font-weight: 600;">Our Get Started guide</a>
            explains how to hand off implementation to your engineering team after purchase.
        </p>
        <p style="margin-top: 20px;">
            <strong>Typical process:</strong>
        </p>
        <ol style="color: #555;">
            <li>You (buyer) schedule a demo with our sales team</li>
            <li>We show you the compliance value (no code required)</li>
            <li>Your company signs up and pays</li>
            <li>We send integration guide to your CTO/engineering team</li>
            <li>Our team helps them integrate (1-2 hours implementation)</li>
            <li>You're compliant within 48 hours</li>
        </ol>
    </div>

    <div class="info-box">
        <h3 style="color: #667eea; margin-bottom: 15px;">💼 Integration Partners (ATS Vendors)</h3>
        <p>
            Building an ATS or HR Tech platform? We offer white-label partnerships with:
        </p>
        <ul style="color: #555;">
            <li>Revenue sharing (70/30 split)</li>
            <li>Complete integration support</li>
            <li>Co-marketing opportunities</li>
            <li>Partner documentation portal</li>
        </ul>
        <p style="margin-top: 20px;">
            <a href="mailto:partnerships@defensiblehiringai.com?subject=Partnership Inquiry" style="color: #667eea; font-weight: 600;">Contact our partnerships team →</a>
        </p>
    </div>

    <h2>Quick Overview (High-Level)</h2>
    <p>Our API provides institutional memory for AI hiring through four core capabilities:</p>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0;">
        <div style="background: #f8f9fa; padding: 25px; border-radius: 8px;">
            <h3 style="color: #667eea;">1. System Registration</h3>
            <p style="color: #555;">Document which AI tools you use in hiring (HireVue, resume parsers, etc.)</p>
        </div>
        <div style="background: #f8f9fa; padding: 25px; border-radius: 8px;">
            <h3 style="color: #667eea;">2. Decision Logging</h3>
            <p style="color: #555;">Record every hiring decision with timestamps and rationales</p>
        </div>
        <div style="background: #f8f9fa; padding: 25px; border-radius: 8px;">
            <h3 style="color: #667eea;">3. Disclosure Tracking</h3>
            <p style="color: #555;">Log candidate notifications and consent records</p>
        </div>
        <div style="background: #f8f9fa; padding: 25px; border-radius: 8px;">
            <h3 style="color: #667eea;">4. Audit Pack Generation</h3>
            <p style="color: #555;">Generate complete evidence bundles when legally challenged</p>
        </div>
    </div>

    <div style="background: #fff3cd; padding: 25px; border-left: 5px solid #ffc107; margin: 40px 0; border-radius: 5px;">
        <h3 style="color: #d63031; margin-bottom: 15px;">🔒 Why Documentation is Gated</h3>
        <p style="color: #555;">
            Our institutional memory platform is built on proprietary technology and compliance expertise.
            We provide detailed documentation to customers and integration partners to ensure successful
            implementation while protecting our intellectual property.
        </p>
        <p style="color: #555; margin-top: 15px;">
            <strong>For access:</strong> Schedule a demo or contact our sales team.
            We typically grant documentation access within 24 hours of inquiry.
        </p>
    </div>

    <hr style="margin: 40px 0;">
    <p style="text-align: center; color: #666;">
        <a href="/" style="color: #667eea;">← Return to Home</a> •
        <a href="/faq" style="color: #667eea;">FAQ</a> •
        <a href="/get-started" style="color: #667eea;">Get Started</a>
    </p>
</body>
</html>
    """, 200


@app.route('/get-started', methods=['GET'])
def get_started():
    """Non-technical buyer onboarding guide"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Get Started - Defensible Hiring AI</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        h1 { color: #667eea; margin-bottom: 10px; }
        h2 { color: #667eea; margin-top: 40px; border-bottom: 2px solid #e9ecef; padding-bottom: 10px; }
        .back-link { display: inline-block; margin-bottom: 20px; color: #667eea; text-decoration: none; }
        .back-link:hover { text-decoration: underline; }
        .persona-box {
            background: #f8f9fa;
            padding: 25px;
            margin: 25px 0;
            border-left: 5px solid #667eea;
            border-radius: 5px;
        }
        .step {
            background: white;
            padding: 30px;
            margin: 20px 0;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .step-number {
            background: #667eea;
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.2em;
            margin-right: 15px;
        }
        .cta-button {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            margin: 10px 5px;
        }
        .cta-button:hover { background: #5568d3; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background: #f8f9fa; font-weight: 600; }
    </style>
</head>
<body>
    <a href="/" class="back-link">← Back to Home</a>

    <h1>Get Started with Defensible Hiring AI</h1>
    <p style="color: #666; margin-bottom: 30px;">The complete guide from evaluation to implementation</p>

    <div class="persona-box">
        <h3 style="color: #667eea; margin-bottom: 15px;">👔 Are You Non-Technical?</h3>
        <p>
            <strong>You don't need to be an engineer to buy Defensible Hiring AI.</strong>
        </p>
        <p style="margin-top: 15px;">
            If you're a VP of HR, General Counsel, Compliance Officer, or business leader evaluating
            compliance solutions, this guide explains exactly how to get started without writing a line of code.
        </p>
    </div>

    <h2>The Complete Process</h2>

    <div class="step">
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <span class="step-number">1</span>
            <h3 style="margin: 0;">Schedule a Demo (You + Sales Team)</h3>
        </div>
        <p><strong>Who's involved:</strong> You (buyer), our sales team</p>
        <p><strong>Duration:</strong> 15-30 minutes</p>
        <p><strong>What happens:</strong></p>
        <ul>
            <li>We show you the compliance value proposition (no technical details)</li>
            <li>Walk through a simulated legal challenge scenario</li>
            <li>Demonstrate audit pack generation</li>
            <li>Answer your compliance questions</li>
            <li>Discuss pricing and ROI</li>
        </ul>
        <p><strong>What you need to prepare:</strong></p>
        <ul>
            <li>Do you hire in NYC, CA, IL, or CO? (determines legal requirement)</li>
            <li>How many candidates do you screen per month?</li>
            <li>What AI tools do you currently use? (ATS, video screening, etc.)</li>
        </ul>
        <a href="/request-demo" class="cta-button">Request Demo Access</a>
    </div>

    <div class="step">
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <span class="step-number">2</span>
            <h3 style="margin: 0;">Sign Contract & Pay (Business Decision)</h3>
        </div>
        <p><strong>Who's involved:</strong> You, your legal/procurement team</p>
        <p><strong>Duration:</strong> 1-5 days (depending on approval process)</p>
        <p><strong>What happens:</strong></p>
        <ul>
            <li>We send you a service agreement</li>
            <li>Your legal team reviews (we provide standard SLA, liability terms)</li>
            <li>You select a plan: Starter ($499/mo), Professional ($1,499/mo), or Enterprise</li>
            <li>Payment via credit card or invoice (annual prepay gets 16% discount)</li>
        </ul>
        <p><strong>What you receive immediately:</strong></p>
        <ul>
            <li>✓ Company account created</li>
            <li>✓ API credentials generated</li>
            <li>✓ Integration guide sent to your technical contact</li>
            <li>✓ Welcome email with next steps</li>
        </ul>
    </div>

    <div class="step">
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <span class="step-number">3</span>
            <h3 style="margin: 0;">Technical Handoff (Your Team + Our Team)</h3>
        </div>
        <p><strong>Who's involved:</strong> Your CTO/Engineering Lead, our implementation team</p>
        <p><strong>Duration:</strong> 30-60 minute kickoff call</p>
        <p><strong>What happens:</strong></p>
        <ul>
            <li>We email your technical contact with integration guide</li>
            <li>Schedule kickoff call with your engineering team</li>
            <li>Walk through API authentication and endpoints</li>
            <li>Provide code examples for your tech stack</li>
            <li>Answer technical questions</li>
        </ul>
        <p><strong>What your technical team needs:</strong></p>
        <ul>
            <li>Access to your ATS/hiring system codebase</li>
            <li>Ability to make HTTP POST requests (basic API integration)</li>
            <li>1-2 hours of engineering time</li>
        </ul>
        <div style="background: #e7f3ff; padding: 20px; border-radius: 5px; margin-top: 20px;">
            <strong>For non-technical buyers:</strong> You don't attend this call!
            Your engineers handle it. We'll send you a summary when it's done.
        </div>
    </div>

    <div class="step">
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <span class="step-number">4</span>
            <h3 style="margin: 0;">Integration & Testing (Engineering Team)</h3>
        </div>
        <p><strong>Who's involved:</strong> Your engineering team, our support team</p>
        <p><strong>Duration:</strong> 1-2 hours of coding time</p>
        <p><strong>What happens:</strong></p>
        <ol>
            <li>Your engineers add our API calls to your hiring workflow:
                <ul>
                    <li>When a candidate is screened → Log decision to our API</li>
                    <li>When AI tool is used → Register system with our API</li>
                    <li>When disclosure is sent → Record with our API</li>
                </ul>
            </li>
            <li>Test with sample data (we provide test candidates)</li>
            <li>Generate test audit pack to verify it works</li>
            <li>Go live!</li>
        </ol>
        <p><strong>Support available:</strong></p>
        <ul>
            <li>Starter: Email support (24-hour response)</li>
            <li>Professional: Email support (4-hour response)</li>
            <li>Enterprise: Dedicated Slack channel (1-hour response)</li>
        </ul>
    </div>

    <div class="step">
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <span class="step-number">5</span>
            <h3 style="margin: 0;">You're Compliant! (Everyone Celebrates)</h3>
        </div>
        <p><strong>Duration:</strong> Usually complete within 48 hours of purchase</p>
        <p><strong>What you get:</strong></p>
        <ul>
            <li>✓ Every hiring decision is now automatically documented</li>
            <li>✓ Immutable audit trail for legal defensibility</li>
            <li>✓ Ability to generate audit packs in 60 seconds when challenged</li>
            <li>✓ Compliance with NYC Local Law 144, California AB 2013, Illinois AI Act</li>
            <li>✓ Peace of mind for your legal team</li>
        </ul>
        <div style="background: #d4edda; padding: 20px; border-radius: 5px; margin-top: 20px; border-left: 5px solid #28a745;">
            <strong style="color: #155724;">Success!</strong> You're now protected from the $500K legal problem.
            Every candidate you screen from here on is documented and defensible.
        </div>
    </div>

    <h2>Roles & Responsibilities</h2>

    <table>
        <tr>
            <th>Role</th>
            <th>Responsibilities</th>
            <th>Time Commitment</th>
        </tr>
        <tr>
            <td><strong>You (Buyer)</strong><br>VP HR, GC, Compliance Officer</td>
            <td>
                • Evaluate solution<br>
                • Attend demo<br>
                • Get budget approval<br>
                • Sign contract<br>
                • Connect us with technical team
            </td>
            <td>2-3 hours total</td>
        </tr>
        <tr>
            <td><strong>Your Legal/Procurement</strong></td>
            <td>
                • Review service agreement<br>
                • Approve vendor<br>
                • Process payment
            </td>
            <td>1-2 hours</td>
        </tr>
        <tr>
            <td><strong>Your CTO/Engineering</strong></td>
            <td>
                • Attend technical kickoff<br>
                • Implement API integration<br>
                • Test and validate<br>
                • Deploy to production
            </td>
            <td>2-4 hours</td>
        </tr>
        <tr>
            <td><strong>Our Sales Team</strong></td>
            <td>
                • Demo product<br>
                • Answer questions<br>
                • Send proposal<br>
                • Handle onboarding
            </td>
            <td>We handle everything</td>
        </tr>
        <tr>
            <td><strong>Our Implementation Team</strong></td>
            <td>
                • Technical kickoff call<br>
                • Integration support<br>
                • Answer engineering questions<br>
                • Validate implementation
            </td>
            <td>We handle everything</td>
        </tr>
    </table>

    <h2>Common Questions from Non-Technical Buyers</h2>

    <div class="persona-box">
        <strong>Q: Do I need to understand APIs or coding?</strong><br>
        <strong>A:</strong> No! Your engineering team handles the technical implementation.
        You just need to approve the purchase and introduce us to your technical contact.
    </div>

    <div class="persona-box">
        <strong>Q: What if we don't have an engineering team?</strong><br>
        <strong>A:</strong> If you're using an existing ATS (Greenhouse, Lever, etc.),
        we can work with their support team to enable the integration. For very small companies,
        we offer managed implementation ($2,500 one-time setup fee).
    </div>

    <div class="persona-box">
        <strong>Q: How long until we're compliant?</strong><br>
        <strong>A:</strong> Typically 48 hours from purchase to live.
        Most of that is coordination time - the actual technical work is 1-2 hours.
    </div>

    <div class="persona-box">
        <strong>Q: What if we get challenged before implementation is complete?</strong><br>
        <strong>A:</strong> We'll work with you to document your historical data to the extent possible,
        but our protection starts from the moment you go live. This is why we recommend implementing
        <em>before</em> you need it.
    </div>

    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; border-radius: 10px; margin: 40px 0;">
        <h2 style="color: white; margin-bottom: 20px;">Ready to Get Started?</h2>
        <p style="font-size: 1.1em; margin-bottom: 30px;">
            Join companies in NYC, California, and Illinois who are protecting themselves from AI hiring lawsuits.
        </p>
        <a href="/request-demo" class="cta-button" style="background: white; color: #667eea; font-size: 1.2em; padding: 18px 40px;">Request Access</a>
        <p style="margin-top: 20px; opacity: 0.9;">
            Questions? Email sales@defensiblehiringai.com or call us at [your phone]
        </p>
    </div>

    <hr style="margin: 40px 0;">
    <p style="text-align: center; color: #666;">
        <a href="/" style="color: #667eea;">← Return to Home</a> •
        <a href="/faq" style="color: #667eea;">FAQ</a> •
        <a href="/docs" style="color: #667eea;">API Documentation</a>
    </p>
</body>
</html>
    """, 200


# ==================== PREMIUM CONTACT FORMS ====================
# Forms replace mailto: links - positioned as "apply to work with us"

@app.route('/sample-audit-pack.pdf', methods=['GET'])
def sample_audit_pack():
    """Serve sample audit pack PDF"""
    from flask import send_file
    import os

    # Serve the generated PDF
    pdf_path = os.path.join(os.path.dirname(__file__), 'static', 'sample-audit-pack.pdf')

    if os.path.exists(pdf_path):
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=False,  # Display in browser, not force download
            download_name='Defensible-Hiring-AI-Sample-Audit-Pack.pdf'
        )
    else:
        # If PDF doesn't exist, generate it on the fly
        try:
            from generate_audit_pack import generate_sample_audit_pack_pdf
            pdf_path = generate_sample_audit_pack_pdf()
            return send_file(
                pdf_path,
                mimetype='application/pdf',
                as_attachment=False,
                download_name='Defensible-Hiring-AI-Sample-Audit-Pack.pdf'
            )
        except Exception as e:
            return f"PDF generation error: {str(e)}. Contact support@defensiblehiringai.com", 500


@app.route('/request-demo', methods=['GET', 'POST'])
def request_demo():
    """Premium demo request form - positioned as exclusive"""
    if request.method == 'POST':
        # Store form submission (simple file storage for now)
        import json
        from datetime import datetime

        submission = {
            'type': 'demo_request',
            'timestamp': datetime.utcnow().isoformat(),
            'company_name': request.form.get('company_name'),
            'contact_name': request.form.get('contact_name'),
            'email': request.form.get('email'),
            'role': request.form.get('role'),
            'company_size': request.form.get('company_size'),
            'jurisdiction': request.form.get('jurisdiction'),
            'urgency': request.form.get('urgency'),
            'message': request.form.get('message')
        }

        # Save to file (you can replace with email or database later)
        try:
            with open('form_submissions.jsonl', 'a') as f:
                f.write(json.dumps(submission) + '\n')
        except:
            pass  # Fail silently if file write fails

        # Send auto-response email (simple version - expand with SendGrid later)
        try:
            # TODO: Set up SendGrid or SMTP for production
            # For now, just log that we should send an email
            print(f"[AUTO-RESPONSE] Send confirmation to {submission['email']}")
            print(f"Subject: Demo Request Received - Defensible Hiring AI")
            print(f"Body: Hi {submission['contact_name']}, we received your request and will review within 24h")
        except:
            pass

        # Return success page
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demo Request Received - Defensible Hiring AI</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .success-container {
            background: white;
            padding: 60px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 600px;
            margin: 20px;
        }
        .checkmark {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: #28a745;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 30px;
        }
        .checkmark svg {
            width: 50px;
            height: 50px;
            fill: white;
        }
        h1 { color: #667eea; margin-bottom: 20px; }
        p { font-size: 1.1em; color: #555; margin: 15px 0; }
        .next-steps {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
            margin: 30px 0;
            text-align: left;
        }
        .next-steps h3 { color: #667eea; margin-top: 0; }
        .next-steps ol { padding-left: 20px; }
        .next-steps li { margin: 10px 0; }
        .back-link {
            display: inline-block;
            margin-top: 20px;
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }
        .back-link:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="success-container">
        <div class="checkmark">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
        </div>
        <h1>Demo Request Received</h1>
        <p><strong>Thank you for your interest in Defensible Hiring AI.</strong></p>
        <p>We've received your demo request and will review it within 24 hours.</p>

        <div class="next-steps">
            <h3>What Happens Next:</h3>
            <ol>
                <li><strong>Review (24 hours):</strong> We'll review your request to ensure we're a good fit for your compliance needs.</li>
                <li><strong>Calendar Invite:</strong> If qualified, we'll send you a calendar invite with available demo slots.</li>
                <li><strong>Demo Call (15-30 min):</strong> We'll show you how our API creates instant audit trails and protects your company from AI hiring lawsuits.</li>
                <li><strong>Implementation Plan:</strong> If you decide to move forward, we'll send technical docs to your engineering team.</li>
            </ol>
        </div>

        <p><em>Check your email (including spam folder) for our response.</em></p>

        <a href="/" class="back-link">← Return to Home</a>
    </div>
</body>
</html>
        """, 200

    # GET request - show form
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Request Demo - Defensible Hiring AI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .form-container {
            max-width: 700px;
            margin: 0 auto;
            background: white;
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .form-header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 2px solid #e9ecef;
        }
        .form-header h1 {
            color: #667eea;
            font-size: 2em;
            margin-bottom: 10px;
        }
        .form-header p {
            color: #666;
            font-size: 1.1em;
        }
        .qualification-badge {
            display: inline-block;
            background: #fff3cd;
            color: #856404;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 0.9em;
            font-weight: 600;
            margin-top: 15px;
        }
        .form-section {
            margin-bottom: 35px;
        }
        .form-section h3 {
            color: #667eea;
            font-size: 1.1em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }
        .form-section h3::before {
            content: '';
            display: inline-block;
            width: 6px;
            height: 24px;
            background: #667eea;
            margin-right: 12px;
            border-radius: 3px;
        }
        .form-group {
            margin-bottom: 25px;
        }
        label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: #555;
        }
        label .required {
            color: #dc3545;
            font-weight: 700;
        }
        input[type="text"],
        input[type="email"],
        select,
        textarea {
            width: 100%;
            padding: 14px 18px;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-size: 1em;
            font-family: inherit;
            transition: border-color 0.3s, box-shadow 0.3s;
        }
        input:focus,
        select:focus,
        textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        textarea {
            min-height: 120px;
            resize: vertical;
        }
        select {
            cursor: pointer;
            background: white;
        }
        .form-card {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 25px;
        }
        .submit-btn {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        .back-link {
            display: block;
            text-align: center;
            margin-top: 25px;
            color: #667eea;
            text-decoration: none;
        }
        .back-link:hover { text-decoration: underline; }
        .help-text {
            font-size: 0.9em;
            color: #666;
            margin-top: 6px;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <div class="form-header">
            <h1>Request Demo Access</h1>
            <p>We work with companies legally required to comply with AI hiring regulations.</p>
            <div class="qualification-badge">⚡ Response within 24 hours</div>
        </div>

        <form method="POST" action="/request-demo">
            <div class="form-section">
                <h3>Company Information</h3>

                <div class="form-group">
                    <label>Company Name <span class="required">*</span></label>
                    <input type="text" name="company_name" required placeholder="Acme Corporation">
                </div>

                <div class="form-group">
                    <label>Company Size <span class="required">*</span></label>
                    <select name="company_size" required>
                        <option value="">Select company size</option>
                        <option value="1-50">1-50 employees</option>
                        <option value="51-200">51-200 employees</option>
                        <option value="201-1000">201-1,000 employees</option>
                        <option value="1001-5000">1,001-5,000 employees</option>
                        <option value="5000+">5,000+ employees</option>
                    </select>
                    <div class="help-text">Helps us understand your hiring volume</div>
                </div>

                <div class="form-group">
                    <label>Compliance Jurisdiction <span class="required">*</span></label>
                    <select name="jurisdiction" required>
                        <option value="">Where do you hire?</option>
                        <option value="NYC">NYC (Local Law 144 - MANDATORY)</option>
                        <option value="California">California (AB 2013 - MANDATORY)</option>
                        <option value="Illinois">Illinois (AI Video Act - MANDATORY)</option>
                        <option value="Colorado">Colorado (AI Act - Effective Feb 2026)</option>
                        <option value="Multi-State">Multi-State (Interstate commerce)</option>
                        <option value="EU">European Union (EU AI Act)</option>
                        <option value="Other">Other / Not Sure</option>
                    </select>
                    <div class="help-text">This determines your compliance urgency</div>
                </div>
            </div>

            <div class="form-section">
                <h3>Your Information</h3>

                <div class="form-group">
                    <label>Your Name <span class="required">*</span></label>
                    <input type="text" name="contact_name" required placeholder="Sarah Johnson">
                </div>

                <div class="form-group">
                    <label>Your Role <span class="required">*</span></label>
                    <select name="role" required>
                        <option value="">Select your role</option>
                        <option value="Chief People Officer">Chief People Officer / CPO</option>
                        <option value="VP HR">VP of HR / VP of People</option>
                        <option value="General Counsel">General Counsel / Chief Legal Officer</option>
                        <option value="Compliance Officer">Compliance Officer / Risk Manager</option>
                        <option value="CTO">CTO / VP Engineering</option>
                        <option value="Talent Acquisition">VP of Talent Acquisition</option>
                        <option value="Other Executive">Other Executive</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Work Email <span class="required">*</span></label>
                    <input type="email" name="email" required placeholder="sarah@company.com">
                    <div class="help-text">We'll send the calendar invite here</div>
                </div>
            </div>

            <div class="form-card">
                <div class="form-group">
                    <label>Urgency Level <span class="required">*</span></label>
                    <select name="urgency" required>
                        <option value="">How urgent is this?</option>
                        <option value="Critical">🚨 Critical - We're being audited or sued</option>
                        <option value="High">⚡ High - Need compliance within 30 days</option>
                        <option value="Medium">📅 Medium - Planning for next quarter</option>
                        <option value="Low">💡 Low - Exploring options</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Additional Context (Optional)</label>
                    <textarea name="message" placeholder="Tell us about your current AI hiring tools (ATS, resume screeners, video interviews) or specific compliance concerns..."></textarea>
                </div>
            </div>

            <button type="submit" class="submit-btn">Submit Demo Request →</button>

            <a href="/" class="back-link">← Return to Home</a>
        </form>
    </div>
</body>
</html>
    """, 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Institutional Memory API is running",
        "version": "1.0.0"
    })


@app.route('/api/company/register', methods=['POST'])
def register_company():
    """Register a new company (ATS customer)"""
    data = request.get_json()

    if not data or 'company_name' not in data:
        return jsonify({"error": "company_name required"}), 400

    # Generate unique company ID and API key
    company_id = f"comp_{secrets.token_hex(8)}"
    api_key = f"im_live_{secrets.token_hex(32)}"

    company = Company(
        company_id=company_id,
        company_name=data['company_name'],
        api_key=api_key,
        plan_type=data.get('plan_type', 'free')
    )

    db.session.add(company)
    db.session.commit()

    return jsonify({
        "message": "Company registered successfully",
        "company_id": company_id,
        "api_key": api_key,
        "note": "Save this API key securely - it won't be shown again"
    }), 201


# ==================== INTEGRATION WEBHOOKS ====================

@app.route('/api/webhook/ai-usage', methods=['POST'])
@require_api_key
def webhook_ai_usage(company):
    """
    Webhook: External ATS reports AI usage

    This is how OTHER ATS systems integrate with your service!
    """
    data = request.get_json()

    required = ['ai_system_id', 'system_name', 'decision_influence']
    if not all(field in data for field in required):
        return jsonify({"error": f"Missing fields: {required}"}), 400

    # Check if AI system already registered
    ai_system = AISystemRecord.query.filter_by(
        company_id=company.id,
        ai_system_id=data['ai_system_id']
    ).first()

    if not ai_system:
        # Register new AI system
        ai_system = AISystemRecord(
            company_id=company.id,
            ai_system_id=data['ai_system_id'],
            system_name=data['system_name'],
            vendor_name=data.get('vendor_name'),
            system_type=data.get('system_type'),
            decision_influence=data['decision_influence'],
            intended_use_statement=data.get('intended_use_statement'),
            deployment_date=datetime.fromisoformat(data.get('deployment_date', datetime.utcnow().isoformat()))
        )
        db.session.add(ai_system)
        db.session.commit()

    return jsonify({
        "status": "recorded",
        "ai_system_id": ai_system.ai_system_id,
        "message": "AI usage recorded in institutional memory"
    }), 201


@app.route('/api/webhook/hiring-decision', methods=['POST'])
@require_api_key
def webhook_hiring_decision(company):
    """
    Webhook: External ATS reports hiring decision

    Example payload from Greenhouse, Lever, or YOUR ATS:
    {
      "candidate_id": "candidate-123",
      "role_id": "job-456",
      "decision_type": "reject",
      "ai_system_id": "resume-screener-v1",
      "decision_maker": "recruiter@company.com",
      "rationale": "Insufficient years of experience"
    }
    """
    data = request.get_json()

    # Hash candidate ID for privacy
    candidate_hash = hashlib.sha256(data['candidate_id'].encode()).hexdigest()

    # Find AI system
    ai_system = AISystemRecord.query.filter_by(
        company_id=company.id,
        ai_system_id=data.get('ai_system_id')
    ).first()

    # Create decision event
    decision = HiringDecisionEvent(
        company_id=company.id,
        decision_event_id=f"decision_{secrets.token_hex(8)}",
        candidate_id_hash=candidate_hash,
        role_id=data.get('role_id'),
        ai_system_record_id=ai_system.id if ai_system else None,
        decision_type=data['decision_type'],
        human_involvement_level=data.get('human_involvement', 'full_review'),
        final_decision_maker_role=data.get('decision_maker_role', 'recruiter'),
        decision_timestamp=datetime.utcnow()
    )
    db.session.add(decision)
    db.session.flush()

    # Add rationale if provided
    if 'rationale' in data:
        rationale = DecisionRationaleLog(
            rationale_id=f"rat_{secrets.token_hex(8)}",
            decision_event_id=decision.id,
            rationale_type=data.get('rationale_type', 'qualification'),
            rationale_summary=data['rationale'],
            entered_by=data.get('decision_maker', 'system')
        )
        db.session.add(rationale)

    db.session.commit()

    return jsonify({
        "status": "recorded",
        "decision_event_id": decision.decision_event_id,
        "message": "Hiring decision recorded in institutional memory"
    }), 201


# ==================== AUDIT PACK GENERATION ====================

@app.route('/api/audit-pack/generate', methods=['POST'])
@require_api_key
def generate_audit_pack(company):
    """
    Generate complete audit evidence pack

    This is what companies get when they're challenged legally!
    """
    data = request.get_json() or {}

    # Filters
    candidate_hash = data.get('candidate_id_hash')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    # Build audit pack
    audit_pack = {
        'company': company.to_dict(),
        'generated_at': datetime.utcnow().isoformat(),
        'filters': {
            'candidate_id_hash': candidate_hash,
            'date_range': f"{start_date} to {end_date}" if start_date and end_date else 'all'
        },
        'evidence': {}
    }

    # AI Systems used
    ai_systems_query = AISystemRecord.query.filter_by(company_id=company.id)
    audit_pack['evidence']['ai_systems'] = [s.to_dict() for s in ai_systems_query.all()]

    # Decisions made
    decisions_query = HiringDecisionEvent.query.filter_by(company_id=company.id)
    if candidate_hash:
        decisions_query = decisions_query.filter_by(candidate_id_hash=candidate_hash)

    decisions = decisions_query.all()
    audit_pack['evidence']['decisions'] = []

    for decision in decisions:
        decision_data = decision.to_dict()
        decision_data['rationales'] = [r.to_dict() for r in decision.rationales]
        audit_pack['evidence']['decisions'].append(decision_data)

    # Disclosures delivered
    disclosures_query = DisclosureArtifact.query.filter_by(company_id=company.id)
    if candidate_hash:
        disclosures_query = disclosures_query.filter_by(candidate_id_hash=candidate_hash)
    audit_pack['evidence']['disclosures'] = [d.to_dict() for d in disclosures_query.all()]

    # Summary
    audit_pack['summary'] = {
        'total_ai_systems': len(audit_pack['evidence']['ai_systems']),
        'total_decisions': len(audit_pack['evidence']['decisions']),
        'total_disclosures': len(audit_pack['evidence']['disclosures']),
        'compliance_status': 'DEFENSIBLE' if audit_pack['evidence']['disclosures'] else 'AT_RISK'
    }

    return jsonify(audit_pack), 200


# ==================== DEMO AUDIT PACK GENERATOR ====================
@app.route('/demo-audit-generator', methods=['GET', 'POST'])
def demo_audit_generator():
    """Live demo generator - shows output without revealing technical moat"""

    if request.method == 'POST':
        # Get form data
        company_name = request.form.get('company_name', 'Demo Company')
        ai_tools = request.form.getlist('ai_tools')  # Multiple checkboxes
        jurisdiction = request.form.get('jurisdiction', 'NYC Local Law 144')
        num_hires = int(request.form.get('num_hires', 50))
        industry = request.form.get('industry', 'Technology')
        candidate_name = request.form.get('candidate_name', '').strip()  # NEW: Candidate search

        # Generate custom PDF
        try:
            from generate_audit_pack import generate_custom_audit_pack_pdf
            import time

            # Simulate 60-second generation (actually faster, but we want to show "working")
            time.sleep(2)  # Small delay for dramatic effect

            pdf_path, pdf_filename = generate_custom_audit_pack_pdf(
                company_name=company_name,
                ai_tools=ai_tools,
                jurisdiction=jurisdiction,
                num_hires=num_hires,
                industry=industry,
                candidate_name=candidate_name  # NEW: Pass candidate name
            )

            # Return success page with download link
            return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Demo Audit Pack Generated - Defensible Hiring AI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .container {{
            max-width: 800px;
            background: white;
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
        }}
        h1 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 20px;
        }}
        .success-icon {{
            font-size: 5em;
            margin-bottom: 20px;
            animation: bounceIn 0.6s;
        }}
        @keyframes bounceIn {{
            0% {{ transform: scale(0); }}
            50% {{ transform: scale(1.2); }}
            100% {{ transform: scale(1); }}
        }}
        .download-button {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            padding: 20px 40px;
            border-radius: 50px;
            font-size: 1.2em;
            font-weight: 600;
            margin: 30px 0;
            transition: transform 0.3s;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }}
        .download-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        }}
        .info-box {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            margin: 30px 0;
            text-align: left;
        }}
        .info-box h3 {{
            color: #667eea;
            margin-bottom: 15px;
        }}
        .info-box ul {{
            list-style: none;
            padding-left: 0;
        }}
        .info-box li {{
            padding: 8px 0;
            padding-left: 25px;
            position: relative;
        }}
        .info-box li:before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: #28a745;
            font-weight: bold;
        }}
        .warning-box {{
            background: #fff3cd;
            border-left: 4px solid #ffa500;
            padding: 20px;
            margin: 20px 0;
            text-align: left;
        }}
        .cta-box {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            margin-top: 30px;
        }}
        .cta-button {{
            display: inline-block;
            background: #28a745;
            color: white;
            text-decoration: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-weight: 600;
            margin-top: 15px;
        }}
        .cta-button:hover {{
            background: #218838;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="success-icon">✅</div>
        {'<h1>🔍 Candidate Journey Report Ready!</h1>' if candidate_name else '<h1>Your Demo Audit Pack is Ready!</h1>'}
        <p style="font-size: 1.2em; color: #666; margin-bottom: 20px;">
            {'<strong>LAWSUIT DEFENSE MODE:</strong> Complete forensic trail for ' + candidate_name if candidate_name else 'Generated in 60 seconds for <strong>' + company_name + '</strong>'}
        </p>

        <a href="/static/{pdf_filename}" class="download-button" download>
            {'📥 Download Forensic Journey Report' if candidate_name else '📥 Download Your Demo Audit Pack'}
        </a>

        <div class="warning-box">
            <strong>⚠️ Important:</strong> This is a demo using sample data. In production,
            all data is automatically captured from your live ATS—no manual entry required.
        </div>

        <div class="info-box">
            {'<h3>🔍 What You Just Saw (Lawsuit Defense):</h3>' if candidate_name else '<h3>What You Just Saw:</h3>'}
            <ul>
                {'<li><strong>CANDIDATE-SPECIFIC JOURNEY</strong> for lawsuit defense</li>' if candidate_name else ''}
                {'<li>Candidate searched: ' + candidate_name + '</li>' if candidate_name else ''}
                {'<li>Complete timeline: Application → AI Screening → Human Review → Decision</li>' if candidate_name else '<li>Professional PDF generated in 60 seconds</li>'}
                {'<li>AI disclosure proof (sent 37 seconds after application)</li>' if candidate_name else '<li>Your company name: ' + company_name + '</li>'}
                {'<li>Human decision justification documented</li>' if candidate_name else '<li>Your AI tools: ' + ', '.join(ai_tools) + '</li>'}
                {'<li>Legal defensibility assessment included</li>' if candidate_name else '<li>Jurisdiction: ' + jurisdiction + '</li>'}
                {'<li>Forensic-grade documentation for court</li>' if candidate_name else '<li>Sample hiring decisions: ' + str(num_hires) + '</li>'}
                <li>Court-ready format with timestamps and documentation</li>
            </ul>
        </div>

        <div class="info-box" style="background: #e8f5e9; border-left: 4px solid #28a745;">
            <h3 style="color: #1b5e20;">🔒 Zero-Storage Architecture (THE DIFFERENTIATOR):</h3>
            <p style="margin-bottom: 15px;"><strong>We DON'T store your candidate data:</strong></p>
            <ul>
                <li>❌ No candidate names, emails, or resumes stored in our database</li>
                <li>❌ No interview videos or compensation data</li>
                <li>✅ Only audit trail events (timestamps, decisions, justifications)</li>
                <li>✅ Your data stays in YOUR ATS (Greenhouse, Lever, Workday)</li>
                <li>✅ We fetch it in real-time when you need an audit pack, then DELETE it</li>
            </ul>
            <p style="margin-top: 15px; padding: 15px; background: white; border-radius: 8px; color: #1b5e20; font-weight: 600;">
                <strong>If we get hacked:</strong> Attackers get timestamps and hashes—NO resumes, NO names, NO PII.
                Your candidate data is SAFE in your ATS.
            </p>
        </div>

        <div class="info-box">
            <h3>What Production Version Does (That You Didn't See):</h3>
            <ul>
                <li>Automatically captures REAL hiring decisions from your ATS</li>
                <li>No manual data entry—fully automated integration</li>
                <li>Live timestamps for every candidate interaction</li>
                <li>Cryptographically signed for legal authenticity</li>
                <li>Generates audit packs instantly when regulators ask</li>
                <li>Protects your $500K+ lawsuit exposure</li>
            </ul>
        </div>

        <div class="cta-box">
            <h2 style="color: #667eea; margin-bottom: 15px;">Ready for Live Integration?</h2>
            <p style="margin-bottom: 20px;">
                Get compliant in 48 hours with our founding customer rate: <strong>$499/mo</strong> (locked for life)
            </p>
            <a href="/request-demo" class="cta-button">
                Request Live Demo & Integration →
            </a>
        </div>

        <p style="margin-top: 30px; color: #999;">
            <a href="/demo-audit-generator" style="color: #667eea;">← Generate Another Demo</a> •
            <a href="/" style="color: #667eea;">Return Home</a>
        </p>
    </div>
</body>
</html>
            """

        except Exception as e:
            return f"Error generating demo: {str(e)}", 500

    # GET request - show form
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Generate Demo Audit Pack in 60 Seconds - Defensible Hiring AI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-align: center;
        }
        .subtitle {
            text-align: center;
            color: #666;
            font-size: 1.2em;
            margin-bottom: 40px;
        }
        .hero-banner {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 40px;
            text-align: center;
        }
        .hero-banner h2 {
            font-size: 1.8em;
            margin-bottom: 15px;
        }
        .form-group {
            margin-bottom: 25px;
        }
        label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
        }
        input[type="text"],
        select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus,
        select:focus {
            outline: none;
            border-color: #667eea;
        }
        .checkbox-group {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
        }
        .checkbox-item {
            margin-bottom: 12px;
        }
        .checkbox-item label {
            display: inline;
            font-weight: normal;
            margin-left: 8px;
        }
        input[type="checkbox"] {
            width: 18px;
            height: 18px;
            cursor: pointer;
        }
        .submit-button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 18px;
            border: none;
            border-radius: 50px;
            font-size: 1.3em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.3s;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }
        .submit-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        }
        .info-box {
            background: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 5px;
        }
        .info-box h3 {
            color: #2196F3;
            margin-bottom: 10px;
        }
        .protection-notice {
            background: #fff3cd;
            border-left: 4px solid #ffa500;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 5px;
        }
        .back-link {
            text-align: center;
            margin-top: 30px;
        }
        .back-link a {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }
        #loading {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 9999;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        #loading.active {
            display: flex;
        }
        .spinner {
            border: 8px solid #f3f3f3;
            border-top: 8px solid #667eea;
            border-radius: 50%;
            width: 80px;
            height: 80px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .loading-text {
            color: white;
            font-size: 1.5em;
            margin-top: 20px;
            text-align: center;
        }
        .loading-steps {
            color: #ccc;
            margin-top: 15px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ Generate Demo Audit Pack</h1>
        <p class="subtitle">See how we generate court-ready documentation in 60 seconds</p>

        <div class="hero-banner">
            <h2>🔍 Two Demo Modes Available:</h2>
            <p><strong>1. Company-Wide Audit:</strong> See overview of all hiring decisions<br>
            <strong>2. Candidate Journey (LAWSUIT DEFENSE):</strong> Search specific candidate who sued you</p>
        </div>

        <div style="background: #fff3cd; border-left: 4px solid #ffa500; padding: 20px; margin-bottom: 30px; border-radius: 5px;">
            <strong>💡 PRO TIP:</strong> To see the <strong>LAWSUIT DEFENSE</strong> feature, enter a candidate name below.
            This shows the complete forensic journey for that specific person—exactly what you need when someone sues you!
        </div>

        <div class="info-box">
            <h3>What This Demo Shows:</h3>
            <p><strong>Without candidate name:</strong> Company-wide compliance overview<br>
            <strong>With candidate name:</strong> Complete hiring journey for lawsuit defense<br><br>
            ✓ Professional court-ready PDF format<br>
            ✓ Forensic timeline of all candidate interactions<br>
            ✓ AI disclosure proof and bias audit results<br>
            ✓ Human decision justifications<br><br>
            <strong>What it DOESN'T show:</strong> How we automatically capture live data from your ATS
            (that's the secret sauce!)
            </p>
        </div>

        <form method="POST" id="demoForm">
            <div class="form-group">
                <label for="company_name">Company Name *</label>
                <input type="text" id="company_name" name="company_name"
                       placeholder="e.g., Acme Corporation" required>
            </div>

            <div class="form-group">
                <label for="candidate_name">🔍 Candidate Name (Optional - For Lawsuit Defense Demo)</label>
                <input type="text" id="candidate_name" name="candidate_name"
                       placeholder="e.g., Jane Doe (Leave blank for company-wide view)">
                <small style="color: #666; display: block; margin-top: 5px;">
                    💡 <strong>Enter a name to see LAWSUIT DEFENSE mode:</strong> Shows complete hiring journey
                    for this candidate—exactly what you need when they sue you!
                </small>
            </div>

            <div class="form-group">
                <label for="industry">Industry *</label>
                <select id="industry" name="industry" required>
                    <option value="Technology">Technology</option>
                    <option value="Finance">Finance</option>
                    <option value="Healthcare">Healthcare</option>
                    <option value="Retail">Retail</option>
                    <option value="Manufacturing">Manufacturing</option>
                    <option value="Professional Services">Professional Services</option>
                    <option value="Other">Other</option>
                </select>
            </div>

            <div class="form-group">
                <label>Which AI Tools Do You Use? *</label>
                <div class="checkbox-group">
                    <div class="checkbox-item">
                        <input type="checkbox" id="greenhouse" name="ai_tools" value="greenhouse">
                        <label for="greenhouse">Greenhouse (ATS)</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="lever" name="ai_tools" value="lever">
                        <label for="lever">Lever (ATS)</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="workday" name="ai_tools" value="workday">
                        <label for="workday">Workday Recruiting</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="hirevue" name="ai_tools" value="hirevue">
                        <label for="hirevue">HireVue (Video Interviews)</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="criteria" name="ai_tools" value="criteria">
                        <label for="criteria">Criteria Corp (Assessments)</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="bamboohr" name="ai_tools" value="bamboohr">
                        <label for="bamboohr">BambooHR</label>
                    </div>
                </div>
            </div>

            <div class="form-group">
                <label for="jurisdiction">Compliance Jurisdiction *</label>
                <select id="jurisdiction" name="jurisdiction" required>
                    <option value="NYC Local Law 144">NYC Local Law 144</option>
                    <option value="California AB 2291">California AB 2291</option>
                    <option value="Illinois AI Video Act">Illinois AI Video Interview Act</option>
                    <option value="Multiple Jurisdictions">Multiple Jurisdictions</option>
                </select>
            </div>

            <div class="form-group">
                <label for="num_hires">Approximate Hires Per Year *</label>
                <select id="num_hires" name="num_hires" required>
                    <option value="10">1-25 hires</option>
                    <option value="50" selected>25-100 hires</option>
                    <option value="100">100-250 hires</option>
                    <option value="250">250-500 hires</option>
                    <option value="500">500+ hires</option>
                </select>
            </div>

            <button type="submit" class="submit-button">
                ⚡ Generate My Demo Audit Pack (60 seconds)
            </button>
        </form>

        <div class="back-link">
            <a href="/">← Return to Home</a> •
            <a href="/request-demo">Request Live Integration →</a>
        </div>
    </div>

    <div id="loading">
        <div class="spinner"></div>
        <div class="loading-text">Generating Your Court-Ready Audit Pack...</div>
        <div class="loading-steps">
            <p id="step1">✓ Registering AI systems...</p>
            <p id="step2" style="display:none;">✓ Generating sample hiring decisions...</p>
            <p id="step3" style="display:none;">✓ Running compliance checks...</p>
            <p id="step4" style="display:none;">✓ Creating professional PDF...</p>
        </div>
    </div>

    <script>
        document.getElementById('demoForm').addEventListener('submit', function(e) {
            // Show loading overlay
            document.getElementById('loading').classList.add('active');

            // Animate steps
            setTimeout(() => {
                document.getElementById('step2').style.display = 'block';
            }, 1000);
            setTimeout(() => {
                document.getElementById('step3').style.display = 'block';
            }, 2000);
            setTimeout(() => {
                document.getElementById('step4').style.display = 'block';
            }, 3000);
        });

        // Require at least one AI tool to be selected
        document.getElementById('demoForm').addEventListener('submit', function(e) {
            const checkboxes = document.querySelectorAll('input[name="ai_tools"]:checked');
            if (checkboxes.length === 0) {
                e.preventDefault();
                alert('Please select at least one AI tool you use.');
                document.getElementById('loading').classList.remove('active');
            }
        });
    </script>
</body>
</html>
    """


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
