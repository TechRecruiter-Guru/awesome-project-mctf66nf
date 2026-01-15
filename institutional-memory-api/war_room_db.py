"""
War Room Database - Multi-User Backend
Stores leads, activities, and contributor stats
"""

import sqlite3
import json
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'war_room.db')

def init_db():
    """Initialize the War Room database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Leads table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT NOT NULL,
            stage TEXT NOT NULL,
            value INTEGER NOT NULL,
            added_by TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Activities table (tracks daily actions)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_type TEXT NOT NULL,
            username TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date TEXT NOT NULL
        )
    ''')

    # Contributors table (cached stats for performance)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contributors (
            username TEXT PRIMARY KEY,
            linkedin_sent INTEGER DEFAULT 0,
            emails_sent INTEGER DEFAULT 0,
            demos_booked INTEGER DEFAULT 0,
            deals_closed INTEGER DEFAULT 0,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def get_all_leads():
    """Get all leads"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM leads ORDER BY created_at DESC')
    leads = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return leads

def add_lead(name, company, stage, value, added_by):
    """Add a new lead"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO leads (name, company, stage, value, added_by)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, company, stage, value, added_by))

    lead_id = cursor.lastrowid

    # Update contributor stats if this is a closed deal
    if stage == 'Cash':
        increment_contributor_stat(added_by, 'deals_closed')

    conn.commit()
    conn.close()

    return lead_id

def update_lead_stage(lead_id, new_stage):
    """Update lead stage"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get the lead first to check who added it
    cursor.execute('SELECT added_by, stage FROM leads WHERE id = ?', (lead_id,))
    result = cursor.fetchone()

    if result:
        added_by, old_stage = result

        cursor.execute('''
            UPDATE leads SET stage = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (new_stage, lead_id))

        # Update contributor stats if moving to Cash
        if new_stage == 'Cash' and old_stage != 'Cash':
            increment_contributor_stat(added_by, 'deals_closed')

        conn.commit()

    conn.close()

def delete_lead(lead_id):
    """Delete a lead"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM leads WHERE id = ?', (lead_id,))

    conn.commit()
    conn.close()

def log_activity(activity_type, username):
    """Log an activity (linkedin, email, demo)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    today = datetime.now().strftime('%Y-%m-%d')

    cursor.execute('''
        INSERT INTO activities (activity_type, username, date)
        VALUES (?, ?, ?)
    ''', (activity_type, username, today))

    # Update contributor stats
    stat_map = {
        'linkedin': 'linkedin_sent',
        'email': 'emails_sent',
        'demo': 'demos_booked'
    }

    if activity_type in stat_map:
        increment_contributor_stat(username, stat_map[activity_type])

    conn.commit()
    conn.close()

def get_today_stats():
    """Get today's total stats"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    today = datetime.now().strftime('%Y-%m-%d')

    stats = {
        'linkedin': 0,
        'email': 0,
        'demo': 0,
        'deals': 0
    }

    # Get activity counts for today
    cursor.execute('''
        SELECT activity_type, COUNT(*) as count
        FROM activities
        WHERE date = ?
        GROUP BY activity_type
    ''', (today,))

    for row in cursor.fetchall():
        activity_type, count = row
        if activity_type in stats:
            stats[activity_type] = count

    # Get deals closed today
    cursor.execute('''
        SELECT COUNT(*) FROM leads
        WHERE stage = 'Cash' AND DATE(created_at) = ?
    ''', (today,))

    stats['deals'] = cursor.fetchone()[0]

    conn.close()
    return stats

def increment_contributor_stat(username, stat_field):
    """Increment a contributor stat"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if contributor exists
    cursor.execute('SELECT username FROM contributors WHERE username = ?', (username,))

    if cursor.fetchone():
        # Update existing
        cursor.execute(f'''
            UPDATE contributors
            SET {stat_field} = {stat_field} + 1, last_active = CURRENT_TIMESTAMP
            WHERE username = ?
        ''', (username,))
    else:
        # Create new contributor
        cursor.execute(f'''
            INSERT INTO contributors (username, {stat_field})
            VALUES (?, 1)
        ''', (username,))

    conn.commit()
    conn.close()

def get_contributors():
    """Get all contributors with their stats"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM contributors
        ORDER BY deals_closed DESC, demos_booked DESC, linkedin_sent DESC
    ''')

    contributors = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return contributors

def get_revenue_stats():
    """Get total revenue from closed deals"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT SUM(value) as total_revenue, COUNT(*) as deal_count
        FROM leads
        WHERE stage = 'Cash'
    ''')

    result = cursor.fetchone()
    total_revenue = result[0] if result[0] else 0
    deal_count = result[1] if result[1] else 0

    conn.close()

    return {
        'total_revenue': total_revenue,
        'deal_count': deal_count,
        'deals_needed': max(0, 6 - deal_count)
    }

# Initialize database on import
init_db()
