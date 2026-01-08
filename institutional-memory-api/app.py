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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///institutional_memory.db'

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
