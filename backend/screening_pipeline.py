"""
Screening Pipeline - Scores candidates and moves qualified ones to "Pending Review"
for human decision. Sends results to ATS via webhooks and checks for bias.

Usage:
    python screening_pipeline.py                       # Screen all new candidates
    python screening_pipeline.py --candidate-id 5      # Screen a specific candidate
    python screening_pipeline.py --threshold 60        # Custom score threshold
    python screening_pipeline.py --dry-run             # Preview without updating ATS
"""

import time
import argparse
from datetime import datetime
from ats_client import ATSClient


AGENT_NAME = 'screening_pipeline'

# Score weights
WEIGHTS = {
    'technical': 0.40,
    'research': 0.30,
    'culture_fit': 0.30
}


def score_technical(candidate):
    """Score a candidate's technical strength (0-100)"""
    score = 0

    # GitHub repos (max 30 points)
    repos = candidate.get('github_repos', 0)
    if repos >= 50:
        score += 30
    elif repos >= 20:
        score += 20
    elif repos >= 5:
        score += 10

    # GitHub followers as social proof (max 20 points)
    followers = candidate.get('github_followers', 0)
    if followers >= 100:
        score += 20
    elif followers >= 30:
        score += 15
    elif followers >= 5:
        score += 5

    # Skills breadth (max 25 points)
    skills = candidate.get('skills', '')
    if skills:
        skill_count = len([s for s in skills.split(',') if s.strip()])
        if skill_count >= 5:
            score += 25
        elif skill_count >= 3:
            score += 15
        elif skill_count >= 1:
            score += 8

    # Has GitHub profile (10 points)
    if candidate.get('github_url'):
        score += 10

    # Has portfolio/scholar URL (15 points)
    if candidate.get('portfolio_url') or candidate.get('google_scholar_url'):
        score += 15

    return min(100, score)


def score_research(candidate):
    """Score a candidate's research profile (0-100)"""
    score = 0

    # h-index (max 40 points)
    h_index = candidate.get('h_index', 0) or candidate.get('s2_h_index', 0)
    if h_index >= 20:
        score += 40
    elif h_index >= 10:
        score += 30
    elif h_index >= 5:
        score += 20
    elif h_index > 0:
        score += 10

    # Citations (max 30 points)
    citations = candidate.get('citation_count', 0) or candidate.get('s2_citation_count', 0)
    if citations >= 1000:
        score += 30
    elif citations >= 500:
        score += 20
    elif citations >= 100:
        score += 15
    elif citations > 0:
        score += 5

    # Paper count (max 20 points)
    papers = candidate.get('s2_paper_count', 0)
    if papers >= 20:
        score += 20
    elif papers >= 10:
        score += 15
    elif papers >= 3:
        score += 10
    elif papers > 0:
        score += 5

    # Has academic profile (10 points)
    if candidate.get('semantic_scholar_id') or candidate.get('arxiv_author_id'):
        score += 10

    return min(100, score)


def score_culture_fit(candidate):
    """Score culture fit based on available signals (0-100)"""
    score = 50  # Neutral baseline — no bias toward or against

    # Has bio (shows effort in self-presentation)
    if candidate.get('bio'):
        score += 15

    # Active in community (following/followers ratio)
    followers = candidate.get('github_followers', 0)
    following = candidate.get('following', 0) if 'following' in candidate else 0
    if followers > 0 and following > 0:
        score += 10

    # Has location (transparency)
    if candidate.get('location'):
        score += 10

    # Has company (currently employed)
    if candidate.get('company'):
        score += 10

    # Expertise alignment
    expertise = candidate.get('primary_expertise', '')
    ai_ml_keywords = ['machine learning', 'ai', 'deep learning', 'robotics', 'nlp',
                       'computer vision', 'autonomous', 'neural', 'data science']
    if any(kw in expertise.lower() for kw in ai_ml_keywords):
        score += 5

    return min(100, score)


def check_for_bias(candidate, scores):
    """Check for potential bias in scoring and return alerts if detected"""
    alerts = []

    # Flag if culture fit is disproportionately low vs technical
    if scores['culture_fit'] < 30 and scores['technical'] > 70:
        alerts.append({
            'alert_type': 'culture_fit_disparity',
            'severity': 'medium',
            'description': (
                f"Culture fit score ({scores['culture_fit']}) is significantly lower than "
                f"technical score ({scores['technical']}) for {candidate.get('full_name', 'candidate')}. "
                f"Review to ensure scoring is based on objective criteria."
            ),
            'recommendation': 'Verify culture fit scoring uses only job-relevant signals.'
        })

    # Flag if candidate has very few data points
    data_points = sum([
        1 if candidate.get('github_url') else 0,
        1 if candidate.get('bio') else 0,
        1 if candidate.get('skills') else 0,
        1 if candidate.get('location') else 0,
        1 if candidate.get('portfolio_url') or candidate.get('google_scholar_url') else 0,
    ])
    if data_points <= 1 and scores['overall'] < 50:
        alerts.append({
            'alert_type': 'insufficient_data',
            'severity': 'low',
            'description': (
                f"Candidate {candidate.get('full_name', 'unknown')} has very few data points "
                f"({data_points}/5) and received a low score ({scores['overall']}). "
                f"Low data availability may unfairly disadvantage this candidate."
            ),
            'recommendation': 'Consider requesting additional information before rejecting.'
        })

    return alerts


def screen_candidate(candidate, ats, dry_run=False):
    """Score a single candidate and return results"""
    name = candidate.get('full_name', f"{candidate.get('first_name', '')} {candidate.get('last_name', '')}")

    technical = score_technical(candidate)
    research = score_research(candidate)
    culture_fit = score_culture_fit(candidate)

    overall = int(
        technical * WEIGHTS['technical'] +
        research * WEIGHTS['research'] +
        culture_fit * WEIGHTS['culture_fit']
    )

    scores = {
        'technical': technical,
        'research': research,
        'culture_fit': culture_fit,
        'overall': overall
    }

    # Check for bias
    bias_alerts = check_for_bias(candidate, scores)

    if not dry_run:
        for alert in bias_alerts:
            try:
                ats.send_bias_alert(
                    alert_type=alert['alert_type'],
                    description=alert['description'],
                    severity=alert['severity'],
                    source_agent=AGENT_NAME,
                    candidate_id=candidate.get('id'),
                    recommendation=alert['recommendation']
                )
            except Exception as e:
                print(f'    WARN: Failed to send bias alert: {e}')

    return {
        'candidate_id': candidate.get('id'),
        'candidate_name': name,
        'scores': scores,
        'bias_alerts': bias_alerts
    }


def run_screening(ats, candidate_id=None, threshold=60, dry_run=False):
    """Run the screening pipeline on new candidates"""
    start_time = time.time()

    print(f'[{AGENT_NAME}] Starting screening run at {datetime.utcnow().isoformat()}')
    print(f'[{AGENT_NAME}] Threshold: {threshold} | Dry run: {dry_run}')

    # Check ATS health
    if not ats.health_check():
        print(f'[{AGENT_NAME}] ERROR: ATS API is not reachable at {ats.base_url}')
        return

    # Get candidates to screen
    candidates_data = ats.get_candidates(status='new')
    all_candidates = candidates_data.get('candidates', [])

    if candidate_id:
        all_candidates = [c for c in all_candidates if c.get('id') == candidate_id]

    print(f'[{AGENT_NAME}] Found {len(all_candidates)} candidate(s) to screen')

    results_summary = {'screened': 0, 'advanced': 0, 'below_threshold': 0, 'bias_alerts': 0}

    for candidate in all_candidates:
        name = candidate.get('full_name', 'Unknown')
        cid = candidate.get('id')
        print(f'\n  Screening: {name} (ID: {cid})')

        result = screen_candidate(candidate, ats, dry_run=dry_run)
        scores = result['scores']
        results_summary['screened'] += 1
        results_summary['bias_alerts'] += len(result['bias_alerts'])

        print(f'    Technical: {scores["technical"]} | Research: {scores["research"]} | '
              f'Culture: {scores["culture_fit"]} | Overall: {scores["overall"]}')

        if result['bias_alerts']:
            for alert in result['bias_alerts']:
                print(f'    BIAS ALERT [{alert["severity"]}]: {alert["alert_type"]}')

        if dry_run:
            action = 'ADVANCE to review' if scores['overall'] >= threshold else 'SKIP (below threshold)'
            print(f'    [DRY RUN] Would: {action}')
            continue

        # Get applications for this candidate
        try:
            apps_data = ats.get_applications()
            candidate_apps = [a for a in apps_data.get('applications', [])
                              if a.get('candidate_id') == cid]
        except Exception:
            candidate_apps = []

        if scores['overall'] >= threshold:
            results_summary['advanced'] += 1

            # Update applications to 'reviewing' status with scores
            if candidate_apps:
                for app in candidate_apps:
                    if app.get('status') in ('applied', 'screening'):
                        try:
                            ats.update_application(
                                app['id'],
                                status='reviewing',
                                stage='agent_screened',
                                technical_score=scores['technical'],
                                research_score=scores['research'],
                                culture_fit_score=scores['culture_fit'],
                                overall_score=scores['overall'],
                                notes=f'Auto-screened by {AGENT_NAME} at {datetime.utcnow().isoformat()} — moved to Pending Review'
                            )
                            print(f'    Application {app["id"]} → REVIEWING (Pending Human Review)')
                        except Exception as e:
                            print(f'    ERROR updating application {app["id"]}: {e}')

            # Send results to ATS webhook
            try:
                ats.send_agent_results(
                    agent_name=AGENT_NAME,
                    action='score',
                    entity_type='candidate',
                    entity_id=cid,
                    score=scores['overall'],
                    input_summary=f'Screened candidate {name}',
                    output_summary=f'Score {scores["overall"]}/100 — Advanced to Pending Review',
                    duration_ms=int((time.time() - start_time) * 1000)
                )
            except Exception as e:
                print(f'    WARN: Failed to log agent results: {e}')

            print(f'    RESULT: Advanced to Pending Review (score {scores["overall"]} >= {threshold})')
        else:
            results_summary['below_threshold'] += 1

            # Log low-score result
            try:
                ats.send_agent_results(
                    agent_name=AGENT_NAME,
                    action='score',
                    entity_type='candidate',
                    entity_id=cid,
                    score=scores['overall'],
                    input_summary=f'Screened candidate {name}',
                    output_summary=f'Score {scores["overall"]}/100 — Below threshold ({threshold})',
                    duration_ms=int((time.time() - start_time) * 1000)
                )
            except Exception as e:
                print(f'    WARN: Failed to log agent results: {e}')

            print(f'    RESULT: Below threshold (score {scores["overall"]} < {threshold})')

    elapsed = time.time() - start_time
    print(f'\n[{AGENT_NAME}] Screening complete in {elapsed:.1f}s')
    print(f'  Screened: {results_summary["screened"]}')
    print(f'  Advanced to Review: {results_summary["advanced"]}')
    print(f'  Below Threshold: {results_summary["below_threshold"]}')
    print(f'  Bias Alerts: {results_summary["bias_alerts"]}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Screening Pipeline - scores and routes candidates')
    parser.add_argument('--candidate-id', type=int, help='Screen a specific candidate ID')
    parser.add_argument('--threshold', type=int, default=60, help='Minimum overall score to advance (default: 60)')
    parser.add_argument('--dry-run', action='store_true', help='Preview without updating ATS')
    parser.add_argument('--ats-url', type=str, help='ATS API URL (default: from env or localhost:5000)')
    args = parser.parse_args()

    ats = ATSClient(base_url=args.ats_url)
    run_screening(ats, candidate_id=args.candidate_id, threshold=args.threshold, dry_run=args.dry_run)
