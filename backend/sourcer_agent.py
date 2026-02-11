"""
Sourcer Agent - Searches GitHub for candidates matching open job requisitions
and creates leads in the ATS via the ats_client.

Usage:
    python sourcer_agent.py                    # Source for all open jobs
    python sourcer_agent.py --job-id 3         # Source for a specific job
    python sourcer_agent.py --dry-run          # Preview without creating leads
"""

import os
import re
import time
import argparse
import requests
from datetime import datetime
from ats_client import ATSClient


AGENT_NAME = 'sourcer_agent'


def extract_search_keywords(job):
    """Extract search keywords from a job posting"""
    keywords = []

    title = job.get('title', '')
    if title:
        # Clean up common job title noise
        clean_title = re.sub(r'(Senior|Junior|Lead|Staff|Principal|Sr\.|Jr\.)\s*', '', title)
        keywords.extend(clean_title.split())

    # Parse required skills (stored as JSON string or comma-separated)
    required_skills = job.get('required_skills', '')
    if required_skills:
        try:
            import json
            skills = json.loads(required_skills)
            if isinstance(skills, list):
                keywords.extend(skills)
        except (json.JSONDecodeError, TypeError):
            keywords.extend([s.strip() for s in required_skills.split(',') if s.strip()])

    # Add expertise area
    expertise = job.get('required_expertise', '')
    if expertise:
        keywords.extend(expertise.split())

    # Add research focus
    research = job.get('research_focus', '')
    if research:
        keywords.extend(research.split())

    # Deduplicate and limit
    seen = set()
    unique = []
    for kw in keywords:
        kw_lower = kw.lower().strip()
        if kw_lower and len(kw_lower) > 2 and kw_lower not in seen:
            seen.add(kw_lower)
            unique.append(kw)
    return unique[:8]


def search_github_users(keywords, max_results=10):
    """Search GitHub for users matching keywords"""
    search_query = ' '.join(keywords[:5])
    url = f'https://api.github.com/search/users?q={search_query}&per_page={max_results}'

    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'PAIP-SourcerAgent/1.0'
    }
    github_token = os.environ.get('GITHUB_TOKEN')
    if github_token:
        headers['Authorization'] = f'token {github_token}'

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        print(f'  GitHub API error: {response.status_code}')
        return []

    data = response.json()
    users = data.get('items', [])

    # Enrich with profile details
    enriched = []
    for user in users[:max_results]:
        detail = _get_github_user_detail(user.get('url'), headers)
        if detail:
            languages = _get_user_languages(user.get('login'), headers)
            enriched.append({
                'username': detail.get('login'),
                'name': detail.get('name') or detail.get('login'),
                'profile_url': detail.get('html_url'),
                'avatar': detail.get('avatar_url'),
                'email': detail.get('email'),
                'bio': detail.get('bio'),
                'location': detail.get('location'),
                'company': detail.get('company'),
                'followers': detail.get('followers', 0),
                'following': detail.get('following', 0),
                'public_repos': detail.get('public_repos', 0),
                'languages': languages,
                'score': user.get('score'),
                'source': 'GitHub'
            })
        else:
            enriched.append({
                'username': user.get('login'),
                'name': user.get('login'),
                'profile_url': user.get('html_url'),
                'avatar': user.get('avatar_url'),
                'email': None,
                'bio': None,
                'location': None,
                'company': None,
                'followers': 0,
                'public_repos': 0,
                'languages': [],
                'score': user.get('score'),
                'source': 'GitHub'
            })
    return enriched


def _get_github_user_detail(user_url, headers):
    """Fetch detailed GitHub user profile"""
    try:
        response = requests.get(user_url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f'  Error fetching user detail: {e}')
    return None


def _get_user_languages(username, headers):
    """Fetch top languages from a user's repos"""
    try:
        url = f'https://api.github.com/users/{username}/repos?sort=updated&per_page=10'
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            repos = response.json()
            lang_counts = {}
            for repo in repos:
                lang = repo.get('language')
                if lang:
                    lang_counts[lang] = lang_counts.get(lang, 0) + 1
            sorted_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)
            return [l[0] for l in sorted_langs[:5]]
    except Exception:
        pass
    return []


def run_sourcer(ats, job_id=None, dry_run=False, max_per_job=10):
    """Run the sourcer agent for open jobs"""
    start_time = time.time()

    print(f'[{AGENT_NAME}] Starting sourcer run at {datetime.utcnow().isoformat()}')

    # Check ATS health
    if not ats.health_check():
        print(f'[{AGENT_NAME}] ERROR: ATS API is not reachable at {ats.base_url}')
        return

    # Get open jobs
    jobs_data = ats.get_jobs()
    all_jobs = jobs_data.get('jobs', [])
    if job_id:
        all_jobs = [j for j in all_jobs if j.get('id') == job_id]

    open_jobs = [j for j in all_jobs if j.get('status') == 'open']
    print(f'[{AGENT_NAME}] Found {len(open_jobs)} open job(s) to source for')

    total_leads_created = 0

    for job in open_jobs:
        job_title = job.get('title', 'Unknown')
        print(f'\n[{AGENT_NAME}] Sourcing for: {job_title} (ID: {job["id"]})')

        keywords = extract_search_keywords(job)
        if not keywords:
            print(f'  Skipping - no searchable keywords extracted')
            continue
        print(f'  Search keywords: {", ".join(keywords)}')

        # Search GitHub
        candidates = search_github_users(keywords, max_results=max_per_job)
        print(f'  Found {len(candidates)} GitHub candidates')

        if dry_run:
            for c in candidates:
                print(f'    [DRY RUN] Would create lead: {c["name"]} (@{c["username"]})')
            continue

        # Export candidates to ATS as leads
        if candidates:
            try:
                result = ats.export_candidates(candidates)
                created = result.get('created', 0)
                skipped = result.get('skipped', 0)
                total_leads_created += created
                print(f'  Exported: {created} created, {skipped} skipped (duplicates)')

                # Log to audit trail
                ats.send_agent_results(
                    agent_name=AGENT_NAME,
                    action='source',
                    entity_type='job',
                    entity_id=job['id'],
                    input_summary=f'Sourced for "{job_title}" with keywords: {", ".join(keywords)}',
                    output_summary=f'Found {len(candidates)} candidates, exported {created} new leads',
                    duration_ms=int((time.time() - start_time) * 1000)
                )
            except Exception as e:
                print(f'  ERROR exporting candidates: {e}')
                ats.send_agent_results(
                    agent_name=AGENT_NAME,
                    action='source',
                    entity_type='job',
                    entity_id=job['id'],
                    input_summary=f'Sourced for "{job_title}"',
                    output_summary=f'Error: {str(e)}',
                    status='error'
                )

    elapsed = time.time() - start_time
    print(f'\n[{AGENT_NAME}] Sourcer run complete in {elapsed:.1f}s — {total_leads_created} total leads created')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sourcer Agent - finds candidates for open jobs')
    parser.add_argument('--job-id', type=int, help='Source for a specific job ID')
    parser.add_argument('--dry-run', action='store_true', help='Preview without creating leads')
    parser.add_argument('--max-per-job', type=int, default=10, help='Max candidates per job')
    parser.add_argument('--ats-url', type=str, help='ATS API URL (default: from env or localhost:5000)')
    args = parser.parse_args()

    ats = ATSClient(base_url=args.ats_url)
    run_sourcer(ats, job_id=args.job_id, dry_run=args.dry_run, max_per_job=args.max_per_job)
