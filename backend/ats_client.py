"""
ATS API Client - HTTP client for the PhysicalAIPros ATS backend.
Used by the agent platform (sourcer_agent, screening_pipeline) to
create leads, push screening results, and trigger bias alerts.
"""

import os
import hmac
import hashlib
import json
import requests
from datetime import datetime


class ATSClient:
    """Client for communicating with the ATS backend API"""

    def __init__(self, base_url=None, webhook_secret=None):
        self.base_url = (base_url or os.environ.get('ATS_API_URL', 'http://localhost:5000')).rstrip('/')
        self.webhook_secret = webhook_secret or os.environ.get('AGENT_WEBHOOK_SECRET', '')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'AgentPlatform/1.0'
        })

    def _sign_payload(self, payload_bytes):
        """Generate HMAC-SHA256 signature for webhook payloads"""
        if not self.webhook_secret:
            return None
        sig = hmac.new(self.webhook_secret.encode(), payload_bytes, hashlib.sha256).hexdigest()
        return f'sha256={sig}'

    def _webhook_post(self, endpoint, data):
        """POST to a webhook endpoint with HMAC signature"""
        payload = json.dumps(data).encode()
        headers = {}
        signature = self._sign_payload(payload)
        if signature:
            headers['X-Webhook-Signature'] = signature
        response = self.session.post(
            f'{self.base_url}{endpoint}',
            data=payload,
            headers=headers,
            timeout=15
        )
        response.raise_for_status()
        return response.json()

    # ==================== LEAD / CANDIDATE CREATION ====================

    def create_lead(self, candidate_data):
        """Create a new candidate (lead) in the ATS from sourcing results"""
        response = self.session.post(
            f'{self.base_url}/api/candidates',
            json=candidate_data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    def export_candidates(self, candidates):
        """Bulk export candidates from search results into the ATS"""
        response = self.session.post(
            f'{self.base_url}/api/export-candidates',
            json={'candidates': candidates},
            timeout=15
        )
        response.raise_for_status()
        return response.json()

    def get_candidates(self, status=None):
        """Fetch candidates from ATS, optionally filtered by status"""
        params = {}
        if status:
            params['status'] = status
        response = self.session.get(
            f'{self.base_url}/api/candidates',
            params=params,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    # ==================== APPLICATION MANAGEMENT ====================

    def get_applications(self, status=None):
        """Fetch applications, optionally filtered by status"""
        params = {}
        if status:
            params['status'] = status
        response = self.session.get(
            f'{self.base_url}/api/applications',
            params=params,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    def create_application(self, candidate_id, job_id, **kwargs):
        """Create a new application linking candidate to job"""
        data = {
            'candidate_id': candidate_id,
            'job_id': job_id,
            **kwargs
        }
        response = self.session.post(
            f'{self.base_url}/api/applications',
            json=data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    def update_application(self, application_id, **kwargs):
        """Update application status, scores, notes, etc."""
        response = self.session.put(
            f'{self.base_url}/api/applications/{application_id}',
            json=kwargs,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    # ==================== WEBHOOK ENDPOINTS ====================

    def send_agent_results(self, agent_name, action, entity_type=None,
                           entity_id=None, score=None, input_summary='',
                           output_summary='', duration_ms=None, status='success'):
        """Send agent results to ATS via webhook (logged to audit trail)"""
        data = {
            'agent_name': agent_name,
            'action': action,
            'entity_type': entity_type,
            'entity_id': entity_id,
            'score': score,
            'input_summary': input_summary,
            'output_summary': output_summary,
            'duration_ms': duration_ms,
            'status': status,
            'timestamp': datetime.utcnow().isoformat()
        }
        return self._webhook_post('/webhooks/agent-results', data)

    def send_bias_alert(self, alert_type, description, severity='medium',
                        source_agent='', candidate_id=None, job_id=None,
                        recommendation=None):
        """Send a bias alert to ATS via webhook"""
        data = {
            'alert_type': alert_type,
            'description': description,
            'severity': severity,
            'source_agent': source_agent,
            'candidate_id': candidate_id,
            'job_id': job_id,
            'recommendation': recommendation,
            'timestamp': datetime.utcnow().isoformat()
        }
        return self._webhook_post('/webhooks/bias-alert', data)

    # ==================== READ ENDPOINTS ====================

    def get_bias_alerts(self, status=None, severity=None):
        """Fetch bias alerts from ATS"""
        params = {}
        if status:
            params['status'] = status
        if severity:
            params['severity'] = severity
        response = self.session.get(
            f'{self.base_url}/api/bias-alerts',
            params=params,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    def get_audit_log(self, agent_name=None, action=None, limit=50):
        """Fetch agent audit log from ATS"""
        params = {'limit': limit}
        if agent_name:
            params['agent_name'] = agent_name
        if action:
            params['action'] = action
        response = self.session.get(
            f'{self.base_url}/api/audit-log',
            params=params,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    def get_agent_config(self):
        """Fetch agent platform config and status from ATS"""
        response = self.session.get(
            f'{self.base_url}/api/agent-config',
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    def get_jobs(self, status='open'):
        """Fetch open jobs from ATS"""
        response = self.session.get(
            f'{self.base_url}/api/jobs',
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    def health_check(self):
        """Check ATS API health"""
        try:
            response = self.session.get(f'{self.base_url}/api/health', timeout=5)
            return response.status_code == 200
        except Exception:
            return False
