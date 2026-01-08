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
    <title>Institutional Memory API - AI Hiring Compliance Defense</title>
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
            <a href="mailto:sales@defensiblehiringai.com">Contact Sales</a>
        </nav>
        <h1>🛡️ Institutional Memory API</h1>
        <p>When your AI hiring gets challenged, have complete evidence ready in seconds</p>
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

    <div class="demo-section" id="demo">
        <div class="container">
            <h2>🎬 What Your Customers Get: The Complete Evidence Pack</h2>
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
                    <div class="price">$499<span style="font-size: 0.4em;">/mo</span></div>
                    <p>Perfect for small ATS platforms</p>
                    <ul class="features">
                        <li>Up to 1,000 decisions/month</li>
                        <li>Full API access</li>
                        <li>Audit pack generation</li>
                        <li>Email support</li>
                    </ul>
                    <a href="mailto:sales@defensiblehiringai.com?subject=Starter Plan Inquiry" class="cta-button">Get Started</a>
                </div>

                <div class="pricing-card featured">
                    <h3>Professional</h3>
                    <div class="price">$1,499<span style="font-size: 0.4em;">/mo</span></div>
                    <p>Most popular for growing companies</p>
                    <ul class="features">
                        <li>Up to 10,000 decisions/month</li>
                        <li>Priority support</li>
                        <li>Custom integrations</li>
                        <li>Compliance dashboard</li>
                        <li>Multi-tenant support</li>
                    </ul>
                    <a href="mailto:sales@defensiblehiringai.com?subject=Professional Plan Inquiry" class="cta-button">Start Free Trial</a>
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
                    <a href="mailto:sales@defensiblehiringai.com?subject=Enterprise Plan Inquiry" class="cta-button">Contact Sales</a>
                </div>
            </div>
        </div>
    </div>

    <div class="hero" style="padding: 60px 20px;">
        <h2>🚀 Ready to Protect Your Customers?</h2>
        <p>Integrate Institutional Memory in 1 hour. Protect every hire from day one.</p>
        <a href="mailto:sales@defensiblehiringai.com?subject=API Integration Request" class="cta-button" style="font-size: 1.3em; padding: 20px 50px;">Schedule Integration Call</a>
        <p style="margin-top: 30px; opacity: 0.9;">
            <strong>API Documentation:</strong> <a href="/api/health" style="color: white;">/api/health</a> •
            Questions? sales@defensiblehiringai.com
        </p>
    </div>

    <footer style="background: #2c3e50; color: white; padding: 40px 20px; text-align: center;">
        <div style="max-width: 1200px; margin: 0 auto;">
            <p style="margin-bottom: 20px;">© 2026 Institutional Memory API. All rights reserved.</p>
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
    <title>Terms of Service - Institutional Memory API</title>
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
    <title>Privacy Policy - Institutional Memory API</title>
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
    <title>FAQ - Institutional Memory API</title>
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
            <strong>A:</strong> Yes! 14-day free trial, no credit card required. You get full access to all features to test integration and generate sample audit packs.
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
    """API Documentation page"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Documentation - Institutional Memory API</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        h1 { color: #667eea; margin-bottom: 10px; }
        h2 { color: #667eea; margin-top: 50px; border-bottom: 2px solid #e9ecef; padding-bottom: 10px; }
        h3 { color: #555; margin-top: 30px; }
        .back-link { display: inline-block; margin-bottom: 20px; color: #667eea; text-decoration: none; }
        .back-link:hover { text-decoration: underline; }
        .endpoint {
            background: #f8f9fa;
            padding: 25px;
            margin: 25px 0;
            border-left: 5px solid #667eea;
            border-radius: 5px;
        }
        .method {
            background: #28a745;
            color: white;
            padding: 5px 12px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 0.9em;
            display: inline-block;
            margin-right: 10px;
        }
        .method.post { background: #007bff; }
        .method.get { background: #28a745; }
        .method.delete { background: #dc3545; }
        .path {
            font-family: 'Courier New', monospace;
            background: #e9ecef;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 1.1em;
        }
        .code-block {
            background: #1e1e1e;
            color: #00ff00;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
        }
        .code-block pre {
            margin: 0;
            white-space: pre-wrap;
        }
        .param-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        .param-table th,
        .param-table td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        .param-table th {
            background: #f8f9fa;
            font-weight: 600;
        }
        .required {
            color: #dc3545;
            font-weight: 600;
        }
        .optional {
            color: #6c757d;
            font-style: italic;
        }
        .auth-box {
            background: #fff3cd;
            border-left: 5px solid #ffc107;
            padding: 20px;
            margin: 25px 0;
        }
        .quickstart {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin: 30px 0;
        }
        .quickstart h3 { color: white; }
    </style>
</head>
<body>
    <a href="/" class="back-link">← Back to Home</a>

    <h1>API Documentation</h1>
    <p style="color: #666; margin-bottom: 10px;">Complete reference for Institutional Memory API</p>
    <p style="color: #666; margin-bottom: 30px;">Version 1.0 • Last Updated: January 8, 2026</p>

    <div class="quickstart">
        <h3>Quick Start (5 minutes)</h3>
        <ol>
            <li><strong>Register your company:</strong> POST to /api/company/register → Get your API key</li>
            <li><strong>Record an AI system:</strong> POST to /api/webhook/ai-system</li>
            <li><strong>Log a hiring decision:</strong> POST to /api/webhook/hiring-decision</li>
            <li><strong>Generate audit pack:</strong> GET /api/audit-pack/generate</li>
        </ol>
        <p>That's it! You now have institutional memory protection.</p>
    </div>

    <h2>Authentication</h2>

    <div class="auth-box">
        <strong>All API requests require authentication via API key.</strong>
        <br><br>
        <strong>Header:</strong> <code>X-API-Key: your_api_key_here</code>
        <br><br>
        Get your API key by registering your company (see endpoint below).
    </div>

    <div class="code-block">
        <pre>
# Example authenticated request
curl -X POST https://defensiblehiringai.com/api/webhook/ai-system \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: im_live_your_api_key_here" \\
  -d '{"system_name": "HireVue", "vendor": "HireVue Inc"}'
        </pre>
    </div>

    <h2>Base URL</h2>
    <p><strong>Production:</strong> <code>https://defensiblehiringai.com/api</code></p>
    <p><strong>All responses:</strong> JSON format</p>

    <h2>Endpoints</h2>

    <!-- Company Registration -->
    <div class="endpoint">
        <span class="method post">POST</span>
        <span class="path">/api/company/register</span>
        <p style="margin-top: 15px;"><strong>Description:</strong> Register your company and receive an API key. This is your first step.</p>

        <h4>Request Body:</h4>
        <table class="param-table">
            <tr>
                <th>Parameter</th>
                <th>Type</th>
                <th>Required</th>
                <th>Description</th>
            </tr>
            <tr>
                <td>company_name</td>
                <td>string</td>
                <td><span class="required">Required</span></td>
                <td>Your company name</td>
            </tr>
            <tr>
                <td>plan_type</td>
                <td>string</td>
                <td><span class="optional">Optional</span></td>
                <td>"free", "starter", "pro", "enterprise" (default: "free")</td>
            </tr>
        </table>

        <h4>Example Request:</h4>
        <div class="code-block">
            <pre>
POST /api/company/register
Content-Type: application/json

{
  "company_name": "TechCorp Inc",
  "plan_type": "pro"
}
            </pre>
        </div>

        <h4>Example Response:</h4>
        <div class="code-block">
            <pre>
{
  "message": "Company registered successfully",
  "company_id": "comp_a1b2c3d4e5f6",
  "api_key": "im_live_x7y8z9w1v2u3t4s5r6q7p8o9",
  "plan_type": "pro"
}

⚠️ SAVE YOUR API KEY - You'll need it for all subsequent requests!
            </pre>
        </div>
    </div>

    <!-- Record AI System -->
    <div class="endpoint">
        <span class="method post">POST</span>
        <span class="path">/api/webhook/ai-system</span>
        <p style="margin-top: 15px;"><strong>Description:</strong> Register an AI system you use in hiring. Do this once per AI tool.</p>

        <h4>Authentication:</h4>
        <p><span class="required">Required:</span> X-API-Key header</p>

        <h4>Request Body:</h4>
        <table class="param-table">
            <tr>
                <th>Parameter</th>
                <th>Type</th>
                <th>Required</th>
                <th>Description</th>
            </tr>
            <tr>
                <td>system_name</td>
                <td>string</td>
                <td><span class="required">Required</span></td>
                <td>Name of AI system (e.g., "HireVue Video Screening")</td>
            </tr>
            <tr>
                <td>vendor</td>
                <td>string</td>
                <td><span class="required">Required</span></td>
                <td>Vendor/provider name</td>
            </tr>
            <tr>
                <td>decision_type</td>
                <td>string</td>
                <td><span class="optional">Optional</span></td>
                <td>"screening", "ranking", "recommendation"</td>
            </tr>
            <tr>
                <td>bias_audit_date</td>
                <td>string</td>
                <td><span class="optional">Optional</span></td>
                <td>ISO date of last bias audit (YYYY-MM-DD)</td>
            </tr>
        </table>

        <h4>Example Request:</h4>
        <div class="code-block">
            <pre>
POST /api/webhook/ai-system
X-API-Key: im_live_your_key_here
Content-Type: application/json

{
  "system_name": "HireVue Video Screening v3.2",
  "vendor": "HireVue Inc",
  "decision_type": "screening",
  "bias_audit_date": "2024-11-20"
}
            </pre>
        </div>

        <h4>Example Response:</h4>
        <div class="code-block">
            <pre>
{
  "message": "AI system recorded",
  "ai_system_id": "ai_sys_f9g8h7i6j5",
  "recorded_timestamp": "2026-01-08T10:30:00Z"
}
            </pre>
        </div>
    </div>

    <!-- Record Hiring Decision -->
    <div class="endpoint">
        <span class="method post">POST</span>
        <span class="path">/api/webhook/hiring-decision</span>
        <p style="margin-top: 15px;"><strong>Description:</strong> Log a hiring decision for a candidate. Call this for every hire/reject.</p>

        <h4>Authentication:</h4>
        <p><span class="required">Required:</span> X-API-Key header</p>

        <h4>Request Body:</h4>
        <table class="param-table">
            <tr>
                <th>Parameter</th>
                <th>Type</th>
                <th>Required</th>
                <th>Description</th>
            </tr>
            <tr>
                <td>candidate_id</td>
                <td>string</td>
                <td><span class="required">Required</span></td>
                <td>Candidate email or ID (will be SHA-256 hashed)</td>
            </tr>
            <tr>
                <td>decision_type</td>
                <td>string</td>
                <td><span class="required">Required</span></td>
                <td>"hired", "rejected", "withdrew", "pending"</td>
            </tr>
            <tr>
                <td>human_involvement</td>
                <td>string</td>
                <td><span class="optional">Optional</span></td>
                <td>"full_review", "partial_review", "ai_only"</td>
            </tr>
            <tr>
                <td>rationale</td>
                <td>string</td>
                <td><span class="optional">Optional</span></td>
                <td>Why this decision was made (critical for legal defense!)</td>
            </tr>
        </table>

        <h4>Example Request:</h4>
        <div class="code-block">
            <pre>
POST /api/webhook/hiring-decision
X-API-Key: im_live_your_key_here
Content-Type: application/json

{
  "candidate_id": "john.doe@email.com",
  "decision_type": "rejected",
  "human_involvement": "full_review",
  "rationale": "Required 5 years Python experience, candidate has 2 years"
}
            </pre>
        </div>

        <h4>Example Response:</h4>
        <div class="code-block">
            <pre>
{
  "message": "Decision logged successfully",
  "decision_id": "decision_k9l8m7n6o5",
  "candidate_hash": "5e884898da28047151d0e56f8dc6292773603d0d...",
  "timestamp": "2026-01-08T14:22:00Z"
}

Note: Candidate ID is hashed for privacy. Original not stored.
            </pre>
        </div>
    </div>

    <!-- Generate Audit Pack -->
    <div class="endpoint">
        <span class="method post">POST</span>
        <span class="path">/api/audit-pack/generate</span>
        <p style="margin-top: 15px;"><strong>Description:</strong> Generate complete compliance audit pack. Use this when legally challenged.</p>

        <h4>Authentication:</h4>
        <p><span class="required">Required:</span> X-API-Key header</p>

        <h4>Request Body:</h4>
        <table class="param-table">
            <tr>
                <th>Parameter</th>
                <th>Type</th>
                <th>Required</th>
                <th>Description</th>
            </tr>
            <tr>
                <td>candidate_id</td>
                <td>string</td>
                <td><span class="optional">Optional</span></td>
                <td>Filter for specific candidate (email/ID)</td>
            </tr>
            <tr>
                <td>start_date</td>
                <td>string</td>
                <td><span class="optional">Optional</span></td>
                <td>Filter from date (ISO format)</td>
            </tr>
            <tr>
                <td>end_date</td>
                <td>string</td>
                <td><span class="optional">Optional</span></td>
                <td>Filter to date (ISO format)</td>
            </tr>
        </table>

        <h4>Example Request:</h4>
        <div class="code-block">
            <pre>
POST /api/audit-pack/generate
X-API-Key: im_live_your_key_here
Content-Type: application/json

{
  "candidate_id": "sarah.martinez@email.com"
}
            </pre>
        </div>

        <h4>Example Response:</h4>
        <div class="code-block">
            <pre>
{
  "company": {
    "company_id": "comp_a1b2c3d4",
    "company_name": "TechCorp Inc"
  },
  "evidence": {
    "ai_systems": [
      {
        "system_name": "HireVue Video Screening v3.2",
        "vendor": "HireVue Inc",
        "registered_timestamp": "2025-01-15T09:30:00Z",
        "bias_audit_date": "2024-11-20",
        "audit_result": "No disparate impact found"
      }
    ],
    "decisions": [
      {
        "decision_type": "rejected",
        "timestamp": "2025-01-20T14:22:00Z",
        "human_review": "full_review",
        "reviewer": "Sarah Chen, Senior Recruiter",
        "rationale": "Required 5yr Python, candidate has 2yr"
      }
    ],
    "disclosures": [
      {
        "disclosure_type": "ai_usage_notice",
        "delivered_at": "2025-01-10T08:15:00Z",
        "method": "email",
        "confirmed": true
      }
    ]
  },
  "summary": {
    "total_ai_systems": 1,
    "total_decisions": 1,
    "total_disclosures": 1,
    "compliance_status": "DEFENSIBLE"
  }
}
            </pre>
        </div>
    </div>

    <h2>Error Codes</h2>
    <table class="param-table">
        <tr>
            <th>Status Code</th>
            <th>Meaning</th>
            <th>Common Causes</th>
        </tr>
        <tr>
            <td>200</td>
            <td>Success</td>
            <td>Request completed successfully</td>
        </tr>
        <tr>
            <td>400</td>
            <td>Bad Request</td>
            <td>Missing required parameters, invalid format</td>
        </tr>
        <tr>
            <td>401</td>
            <td>Unauthorized</td>
            <td>Missing or invalid API key</td>
        </tr>
        <tr>
            <td>403</td>
            <td>Forbidden</td>
            <td>API key valid but lacks permission</td>
        </tr>
        <tr>
            <td>429</td>
            <td>Too Many Requests</td>
            <td>Rate limit exceeded (1000 req/hour)</td>
        </tr>
        <tr>
            <td>500</td>
            <td>Server Error</td>
            <td>Internal error (contact support)</td>
        </tr>
    </table>

    <h2>Code Examples</h2>

    <h3>Python</h3>
    <div class="code-block">
        <pre>
import requests

API_KEY = "im_live_your_api_key_here"
BASE_URL = "https://defensiblehiringai.com/api"
HEADERS = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

# Record AI system
response = requests.post(
    f"{BASE_URL}/webhook/ai-system",
    headers=HEADERS,
    json={
        "system_name": "HireVue Video",
        "vendor": "HireVue Inc"
    }
)
print(response.json())

# Log hiring decision
response = requests.post(
    f"{BASE_URL}/webhook/hiring-decision",
    headers=HEADERS,
    json={
        "candidate_id": "candidate@email.com",
        "decision_type": "rejected",
        "human_involvement": "full_review",
        "rationale": "Skills mismatch"
    }
)
print(response.json())
        </pre>
    </div>

    <h3>Node.js</h3>
    <div class="code-block">
        <pre>
const axios = require('axios');

const API_KEY = 'im_live_your_api_key_here';
const BASE_URL = 'https://defensiblehiringai.com/api';
const headers = {
  'Content-Type': 'application/json',
  'X-API-Key': API_KEY
};

// Record AI system
async function recordAISystem() {
  const response = await axios.post(
    `${BASE_URL}/webhook/ai-system`,
    {
      system_name: 'HireVue Video',
      vendor: 'HireVue Inc'
    },
    { headers }
  );
  console.log(response.data);
}

// Log hiring decision
async function logDecision() {
  const response = await axios.post(
    `${BASE_URL}/webhook/hiring-decision`,
    {
      candidate_id: 'candidate@email.com',
      decision_type: 'rejected',
      human_involvement: 'full_review',
      rationale: 'Skills mismatch'
    },
    { headers }
  );
  console.log(response.data);
}
        </pre>
    </div>

    <h2>Rate Limits</h2>
    <ul>
        <li><strong>Default:</strong> 1000 requests per hour per API key</li>
        <li><strong>Burst:</strong> 100 requests per minute</li>
        <li><strong>Enterprise:</strong> Custom limits available</li>
    </ul>
    <p>When rate limited, you'll receive a 429 error. Retry after 60 seconds.</p>

    <h2>Webhook Integration</h2>
    <p>Our API uses a <strong>webhook pattern</strong>. Your ATS calls our webhooks when events happen:</p>
    <ul>
        <li>New AI tool configured → POST /webhook/ai-system</li>
        <li>Candidate screened → POST /webhook/hiring-decision</li>
        <li>Disclosure sent to candidate → POST /webhook/disclosure</li>
        <li>Legal challenge arrives → POST /audit-pack/generate</li>
    </ul>

    <h2>Support</h2>
    <p><strong>Questions?</strong> Contact us at <a href="mailto:support@defensiblehiringai.com">support@defensiblehiringai.com</a></p>
    <p><strong>Bugs?</strong> Report at <a href="mailto:bugs@defensiblehiringai.com">bugs@defensiblehiringai.com</a></p>
    <p><strong>Feature Requests?</strong> Email <a href="mailto:product@defensiblehiringai.com">product@defensiblehiringai.com</a></p>

    <hr style="margin: 40px 0;">
    <p style="text-align: center; color: #666;">
        <a href="/" style="color: #667eea;">← Return to Home</a> •
        <a href="/faq" style="color: #667eea;">FAQ</a> •
        <a href="/terms-of-service" style="color: #667eea;">Terms</a> •
        <a href="/privacy-policy" style="color: #667eea;">Privacy</a>
    </p>
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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
