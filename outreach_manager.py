#!/usr/bin/env python3
"""
Outreach Manager - Track and manage contributor outreach campaigns
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os

class OutreachManager:
    def __init__(self, db_path="outreach.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize the SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Platforms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS platforms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                url TEXT,
                audience_size TEXT,
                category TEXT,
                notes TEXT
            )
        ''')

        # Posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform_id INTEGER,
                status TEXT DEFAULT 'draft',
                content TEXT,
                title TEXT,
                scheduled_date TEXT,
                posted_date TEXT,
                post_url TEXT,
                views INTEGER DEFAULT 0,
                upvotes INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                notes TEXT,
                FOREIGN KEY (platform_id) REFERENCES platforms (id)
            )
        ''')

        # Analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER,
                date TEXT,
                views INTEGER DEFAULT 0,
                clicks INTEGER DEFAULT 0,
                stars INTEGER DEFAULT 0,
                FOREIGN KEY (post_id) REFERENCES posts (id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_platform(self, name: str, url: str, audience_size: str, category: str, notes: str = ""):
        """Add a new platform to track"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO platforms (name, url, audience_size, category, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, url, audience_size, category, notes))
            conn.commit()
            print(f"✅ Added platform: {name}")
        except sqlite3.IntegrityError:
            print(f"⚠️  Platform {name} already exists")
        finally:
            conn.close()

    def add_post(self, platform_name: str, title: str, content: str,
                 status: str = "draft", scheduled_date: str = None):
        """Add a post to track"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get platform ID
        cursor.execute('SELECT id FROM platforms WHERE name = ?', (platform_name,))
        result = cursor.fetchone()

        if not result:
            print(f"❌ Platform {platform_name} not found. Add it first.")
            conn.close()
            return

        platform_id = result[0]

        cursor.execute('''
            INSERT INTO posts (platform_id, title, content, status, scheduled_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (platform_id, title, content, status, scheduled_date))

        conn.commit()
        conn.close()
        print(f"✅ Added post for {platform_name}: {title}")

    def update_post_status(self, post_id: int, status: str, post_url: str = None):
        """Update post status (draft, scheduled, posted, failed)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if status == "posted":
            posted_date = datetime.now().isoformat()
            cursor.execute('''
                UPDATE posts
                SET status = ?, posted_date = ?, post_url = ?
                WHERE id = ?
            ''', (status, posted_date, post_url, post_id))
        else:
            cursor.execute('''
                UPDATE posts SET status = ? WHERE id = ?
            ''', (status, post_id))

        conn.commit()
        conn.close()
        print(f"✅ Updated post {post_id} status to: {status}")

    def update_analytics(self, post_id: int, views: int = 0, upvotes: int = 0, comments: int = 0):
        """Update post analytics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE posts
            SET views = ?, upvotes = ?, comments = ?
            WHERE id = ?
        ''', (views, upvotes, comments, post_id))

        # Also log to analytics table
        cursor.execute('''
            INSERT INTO analytics (post_id, date, views, clicks)
            VALUES (?, ?, ?, ?)
        ''', (post_id, datetime.now().isoformat(), views, upvotes))

        conn.commit()
        conn.close()
        print(f"✅ Updated analytics for post {post_id}")

    def get_status_summary(self) -> Dict:
        """Get summary of all posts by status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT status, COUNT(*)
            FROM posts
            GROUP BY status
        ''')

        summary = dict(cursor.fetchall())
        conn.close()
        return summary

    def get_platforms_summary(self) -> List[Dict]:
        """Get summary of posts by platform"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                p.name,
                p.audience_size,
                COUNT(po.id) as total_posts,
                SUM(CASE WHEN po.status = 'posted' THEN 1 ELSE 0 END) as posted,
                SUM(po.views) as total_views,
                SUM(po.upvotes) as total_upvotes,
                SUM(po.comments) as total_comments
            FROM platforms p
            LEFT JOIN posts po ON p.id = po.platform_id
            GROUP BY p.id
            ORDER BY total_views DESC
        ''')

        columns = ['name', 'audience_size', 'total_posts', 'posted', 'views', 'upvotes', 'comments']
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

        conn.close()
        return results

    def get_pending_posts(self) -> List[Dict]:
        """Get all posts that need to be posted"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                po.id,
                p.name as platform,
                po.title,
                po.status,
                po.scheduled_date
            FROM posts po
            JOIN platforms p ON po.platform_id = p.id
            WHERE po.status IN ('draft', 'scheduled')
            ORDER BY po.scheduled_date
        ''')

        columns = ['id', 'platform', 'title', 'status', 'scheduled_date']
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

        conn.close()
        return results

    def get_post_content(self, post_id: int) -> Optional[Dict]:
        """Get full post content by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                po.id,
                p.name as platform,
                p.url as platform_url,
                po.title,
                po.content,
                po.status,
                po.post_url
            FROM posts po
            JOIN platforms p ON po.platform_id = p.id
            WHERE po.id = ?
        ''', (post_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            columns = ['id', 'platform', 'platform_url', 'title', 'content', 'status', 'post_url']
            return dict(zip(columns, row))
        return None

    def generate_report(self) -> str:
        """Generate a text report of outreach progress"""
        report = []
        report.append("=" * 60)
        report.append("📊 OUTREACH CAMPAIGN REPORT")
        report.append("=" * 60)
        report.append("")

        # Status summary
        status_summary = self.get_status_summary()
        report.append("📈 Status Summary:")
        for status, count in status_summary.items():
            report.append(f"   {status.upper()}: {count}")
        report.append("")

        # Platform summary
        platforms = self.get_platforms_summary()
        report.append("🌐 Platform Performance:")
        report.append(f"{'Platform':<25} {'Posts':<8} {'Views':<10} {'Upvotes':<10} {'Comments':<10}")
        report.append("-" * 70)
        for p in platforms:
            report.append(
                f"{p['name']:<25} "
                f"{p['posted'] or 0}/{p['total_posts'] or 0:<7} "
                f"{p['views'] or 0:<10} "
                f"{p['upvotes'] or 0:<10} "
                f"{p['comments'] or 0:<10}"
            )
        report.append("")

        # Pending posts
        pending = self.get_pending_posts()
        if pending:
            report.append("⏰ Pending Posts:")
            for post in pending:
                report.append(f"   [{post['id']}] {post['platform']}: {post['title']} ({post['status']})")

        report.append("")
        report.append("=" * 60)

        return "\n".join(report)


def init_platforms(manager: OutreachManager):
    """Initialize all target platforms"""
    platforms = [
        # Reddit
        ("r/opensource", "https://www.reddit.com/r/opensource/", "349k", "reddit", "General open source community"),
        ("r/MachineLearning", "https://www.reddit.com/r/MachineLearning/", "2.9M", "reddit", "Post on Saturdays - Project Showcase"),
        ("r/cscareerquestions", "https://www.reddit.com/r/cscareerquestions/", "1.5M", "reddit", "Career-focused audience"),
        ("r/recruitinghell", "https://www.reddit.com/r/recruitinghell/", "293k", "reddit", "Frustrated with ATS angle"),
        ("r/Python", "https://www.reddit.com/r/Python/", "1.4M", "reddit", "Python developers"),
        ("r/reactjs", "https://www.reddit.com/r/reactjs/", "508k", "reddit", "React developers"),

        # Dev Communities
        ("Dev.to", "https://dev.to/", "1M+", "dev", "Developer blogging platform"),
        ("Hacker News", "https://news.ycombinator.com/", "5M+", "dev", "Tech news and Show HN"),
        ("Hashnode", "https://hashnode.com/", "500k+", "dev", "Developer blogging"),
        ("Indie Hackers", "https://www.indiehackers.com/", "100k+", "dev", "Indie makers community"),

        # Social
        ("LinkedIn Personal", "https://linkedin.com/", "900M", "social", "Personal profile post"),
        ("LinkedIn ML Group", "https://linkedin.com/", "500k+", "social", "Machine Learning & AI group"),
        ("Twitter/X", "https://twitter.com/", "500M+", "social", "Use #BuildInPublic #OpenSource"),

        # Discord
        ("Reactiflux Discord", "https://www.reactiflux.com/", "200k+", "discord", "#showcase channel"),
        ("Python Discord", "https://pythondiscord.com/", "430k+", "discord", "#showcase channel"),
        ("MLOps Community", "https://mlops.community/", "50k+", "discord", "Slack - #projects"),

        # Other
        ("Product Hunt", "https://www.producthunt.com/", "10M+", "launch", "Tuesday-Thursday best"),
        ("GitHub Topics", "https://github.com/", "100M+", "github", "Add topics to repo"),
    ]

    for platform in platforms:
        manager.add_platform(*platform)


def init_content(manager: OutreachManager):
    """Initialize post content for each platform"""

    # Short content for Twitter/LinkedIn
    short_content = """🚀 Just launched an open-source AI/ML Applicant Tracking System!

Unlike traditional ATS, it tracks what actually matters for AI/ML recruiting:
🎓 Google Scholar profiles
📊 H-index & citations
📄 arXiv publications
🔒 Stealth mode for confidential roles

Built with React + Flask. First contributors welcome!

Live demo: https://awesome-project-mctf66nf-techrecruiter-gurus-projects.vercel.app/
Repo: https://github.com/TechRecruiter-Guru/awesome-project-mctf66nf

#OpenSource #MachineLearning #TechRecruiting"""

    # Medium content for Reddit/Forums
    medium_content = """**Show HN: AI/ML ATS that tracks research credentials traditional platforms miss**

Hey everyone! 👋

I built an open-source Applicant Tracking System specifically for recruiting AI/ML talent.

**The Problem:**
Traditional ATS platforms (Greenhouse, Lever, etc.) completely miss the most important signals when recruiting AI/ML researchers:
- Research publications (arXiv, Google Scholar)
- Academic impact (H-index, citations)
- Conference contributions (NeurIPS, ICML, CVPR)
- Research focus areas

**The Solution:**
An ATS that puts research credentials first, with features like:
- 🎓 Google Scholar / arXiv / ORCID integration fields
- 📊 H-index and citation tracking
- 📚 Publication management
- 🔒 Stealth mode for confidential job postings (hide company names)
- 🧠 AI/ML specialization tracking (CV, NLP, RL, etc.)

**Tech Stack:**
- Frontend: React 18
- Backend: Flask + SQLAlchemy
- Database: SQLite (easily swappable)
- Deployment: Vercel + Render

**Live Demo:** https://awesome-project-mctf66nf-techrecruiter-gurus-projects.vercel.app/

**Looking for contributors to help with:**
- Google Scholar API integration
- arXiv API integration
- Advanced search/filtering
- Analytics dashboard
- Mobile responsiveness improvements

**Repo:** https://github.com/TechRecruiter-Guru/awesome-project-mctf66nf

All contributions welcome - from bug fixes to new features! Check out CONTRIBUTING.md to get started.

Would love feedback from recruiters and ML engineers!"""

    # Add posts for each platform
    posts = [
        ("Twitter/X", "AI/ML ATS Launch", short_content, "draft", "2025-11-06"),
        ("LinkedIn Personal", "Launching Open Source AI/ML ATS", short_content, "draft", "2025-11-06"),
        ("Hacker News", "Show HN: AI/ML ATS for research credential tracking", medium_content, "draft", "2025-11-06"),
        ("r/opensource", "Open-source ATS for AI/ML recruiting", medium_content, "draft", "2025-11-06"),
        ("r/MachineLearning", "[P] AI/ML ATS with research credential tracking", medium_content, "draft", "2025-11-09"),  # Saturday
        ("r/Python", "Built an ATS with Flask + React", medium_content, "draft", "2025-11-07"),
        ("r/reactjs", "React app for AI/ML recruiting", medium_content, "draft", "2025-11-07"),
        ("Dev.to", "Building an AI/ML-First ATS", medium_content, "draft", "2025-11-06"),
        ("Product Hunt", "AI/ML Applicant Tracking System", short_content, "draft", "2025-11-12"),  # Tuesday
    ]

    for platform, title, content, status, date in posts:
        manager.add_post(platform, title, content, status, date)


def main():
    """Main CLI interface"""
    import sys

    manager = OutreachManager()

    if len(sys.argv) < 2:
        print("Outreach Manager - Manage your contributor outreach campaign")
        print()
        print("Commands:")
        print("  init              - Initialize platforms and content")
        print("  report            - Generate full report")
        print("  pending           - Show pending posts")
        print("  get <id>          - Get post content by ID")
        print("  mark-posted <id> <url> - Mark post as posted")
        print("  update-stats <id> <views> <upvotes> <comments> - Update post stats")
        print()
        print("Examples:")
        print("  python outreach_manager.py init")
        print("  python outreach_manager.py report")
        print("  python outreach_manager.py get 1")
        print("  python outreach_manager.py mark-posted 1 https://reddit.com/...")
        print("  python outreach_manager.py update-stats 1 150 25 10")
        return

    command = sys.argv[1]

    if command == "init":
        print("Initializing platforms and content...")
        init_platforms(manager)
        init_content(manager)
        print("✅ Initialization complete!")
        print("\nRun 'python outreach_manager.py report' to see the status")

    elif command == "report":
        print(manager.generate_report())

    elif command == "pending":
        pending = manager.get_pending_posts()
        print("\n⏰ Pending Posts:\n")
        for post in pending:
            print(f"[{post['id']}] {post['platform']}")
            print(f"    Title: {post['title']}")
            print(f"    Status: {post['status']}")
            print(f"    Scheduled: {post['scheduled_date']}")
            print()
        print(f"Total: {len(pending)} posts pending")

    elif command == "get":
        if len(sys.argv) < 3:
            print("Usage: python outreach_manager.py get <post_id>")
            return

        post_id = int(sys.argv[2])
        post = manager.get_post_content(post_id)

        if post:
            print("\n" + "=" * 60)
            print(f"📝 Post #{post['id']}: {post['platform']}")
            print("=" * 60)
            print(f"\nTitle: {post['title']}")
            print(f"Status: {post['status']}")
            print(f"Platform URL: {post['platform_url']}")
            if post['post_url']:
                print(f"Post URL: {post['post_url']}")
            print(f"\n--- CONTENT (Copy below) ---\n")
            print(post['content'])
            print(f"\n--- END CONTENT ---\n")
        else:
            print(f"❌ Post {post_id} not found")

    elif command == "mark-posted":
        if len(sys.argv) < 4:
            print("Usage: python outreach_manager.py mark-posted <post_id> <url>")
            return

        post_id = int(sys.argv[2])
        url = sys.argv[3]
        manager.update_post_status(post_id, "posted", url)

    elif command == "update-stats":
        if len(sys.argv) < 6:
            print("Usage: python outreach_manager.py update-stats <post_id> <views> <upvotes> <comments>")
            return

        post_id = int(sys.argv[2])
        views = int(sys.argv[3])
        upvotes = int(sys.argv[4])
        comments = int(sys.argv[5])
        manager.update_analytics(post_id, views, upvotes, comments)

    else:
        print(f"❌ Unknown command: {command}")


if __name__ == "__main__":
    main()
