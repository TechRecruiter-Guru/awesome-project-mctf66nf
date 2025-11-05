"""
Sample data for AI/ML Applicant Tracking System
Run this to populate the database with realistic candidates and jobs
"""

import requests
import json

API_URL = "http://localhost:5000"

# Sample Candidates
candidates = [
    {
        "first_name": "Yann",
        "last_name": "LeCun",
        "email": "yann.lecun@example.edu",
        "primary_expertise": "Computer Vision",
        "google_scholar_url": "https://scholar.google.com/citations?user=WLN3QrAAAAAJ",
        "h_index": 150,
        "citation_count": 300000,
        "years_experience": 35,
        "location": "New York, NY",
        "github_url": "https://github.com/ylecun",
        "status": "new"
    },
    {
        "first_name": "Fei-Fei",
        "last_name": "Li",
        "email": "feifei@example.edu",
        "primary_expertise": "Computer Vision",
        "google_scholar_url": "https://scholar.google.com/citations?user=rDfyQnIAAAAJ",
        "h_index": 120,
        "citation_count": 180000,
        "years_experience": 20,
        "location": "Stanford, CA",
        "status": "reviewing"
    },
    {
        "first_name": "Yoshua",
        "last_name": "Bengio",
        "email": "yoshua.bengio@example.ca",
        "primary_expertise": "Deep Learning",
        "google_scholar_url": "https://scholar.google.com/citations?user=kukA0LcAAAAJ",
        "h_index": 175,
        "citation_count": 400000,
        "years_experience": 30,
        "location": "Montreal, Canada",
        "status": "new"
    },
    {
        "first_name": "Andrew",
        "last_name": "Ng",
        "email": "andrew.ng@example.edu",
        "primary_expertise": "Machine Learning",
        "google_scholar_url": "https://scholar.google.com/citations?user=mG4imMEAAAAJ",
        "h_index": 140,
        "citation_count": 250000,
        "years_experience": 25,
        "location": "Palo Alto, CA",
        "github_url": "https://github.com/andrewng",
        "status": "interviewing"
    },
    {
        "first_name": "Emily",
        "last_name": "Chen",
        "email": "emily.chen@example.edu",
        "primary_expertise": "Natural Language Processing",
        "google_scholar_url": "https://scholar.google.com/citations?user=example",
        "h_index": 45,
        "citation_count": 12000,
        "years_experience": 8,
        "location": "Seattle, WA",
        "github_url": "https://github.com/emilychen",
        "linkedin_url": "https://linkedin.com/in/emilychen",
        "status": "new"
    },
    {
        "first_name": "Marcus",
        "last_name": "Rodriguez",
        "email": "marcus.r@example.edu",
        "primary_expertise": "Reinforcement Learning",
        "google_scholar_url": "https://scholar.google.com/citations?user=example2",
        "arxiv_author_id": "marcus-rodriguez",
        "h_index": 35,
        "citation_count": 8500,
        "years_experience": 6,
        "location": "Austin, TX",
        "github_url": "https://github.com/marcusr",
        "status": "reviewing"
    }
]

# Sample Jobs (some confidential)
jobs = [
    {
        "title": "Senior Research Scientist - Computer Vision",
        "company": "Meta AI Research",
        "location": "Menlo Park, CA",
        "job_type": "full-time",
        "description": "Lead research in computer vision and multimodal learning. Work on cutting-edge problems in visual understanding.",
        "requirements": "PhD in Computer Science or related field, 5+ years of research experience, strong publication record at top-tier venues (CVPR, ICCV, ECCV, NeurIPS)",
        "required_expertise": "Computer Vision",
        "education_required": "PhD",
        "research_focus": "Multimodal Learning and Visual Understanding",
        "salary_min": 250000,
        "salary_max": 450000,
        "confidential": False
    },
    {
        "title": "AI Research Scientist",
        "company": "Stealth AI Startup",
        "location": "San Francisco, CA",
        "job_type": "full-time",
        "description": "Join a well-funded stealth startup working on breakthrough AI technology. Competitive comp + equity.",
        "requirements": "PhD in CS/ML, publications at NeurIPS/ICML/ICLR, experience with large language models",
        "required_expertise": "Deep Learning",
        "education_required": "PhD",
        "research_focus": "Large Language Models",
        "salary_min": 300000,
        "salary_max": 500000,
        "confidential": True  # Stealth mode!
    },
    {
        "title": "ML Research Lead - NLP",
        "company": "Leading Tech Company",
        "location": "Remote",
        "job_type": "full-time",
        "description": "Lead NLP research team. Build state-of-the-art language models. Company name revealed after mutual interest.",
        "requirements": "PhD preferred, 10+ years experience, proven track record of shipping ML products",
        "required_expertise": "Natural Language Processing",
        "education_required": "PhD",
        "research_focus": "Language Models and Generation",
        "salary_min": 280000,
        "salary_max": 480000,
        "confidential": True  # Stealth mode!
    },
    {
        "title": "Research Scientist - Reinforcement Learning",
        "company": "DeepMind",
        "location": "London, UK",
        "job_type": "full-time",
        "description": "Push the boundaries of RL research. Work on AGI-related problems with world-class team.",
        "requirements": "PhD in CS/ML/related field, strong RL background, publications at top venues",
        "required_expertise": "Reinforcement Learning",
        "education_required": "PhD",
        "research_focus": "Multi-agent RL and Game Playing",
        "salary_min": 180000,
        "salary_max": 320000,
        "confidential": False
    },
    {
        "title": "Principal ML Engineer",
        "company": "Confidential - Series C Startup",
        "location": "New York, NY",
        "job_type": "full-time",
        "description": "Join as founding ML team member. $150M+ in funding. Revolutionary product in stealth mode.",
        "requirements": "MS/PhD, 5+ years ML experience, proven ability to ship production ML systems",
        "required_expertise": "MLOps",
        "education_required": "Masters",
        "research_focus": "Production ML Systems",
        "salary_min": 220000,
        "salary_max": 380000,
        "confidential": True  # Stealth mode!
    },
    {
        "title": "AI Research Scientist - Multimodal",
        "company": "OpenAI",
        "location": "San Francisco, CA",
        "job_type": "full-time",
        "description": "Work on next generation multimodal models combining vision, language, and other modalities.",
        "requirements": "PhD, strong publication record, experience with large-scale models",
        "required_expertise": "Deep Learning",
        "education_required": "PhD",
        "research_focus": "Multimodal AI",
        "salary_min": 300000,
        "salary_max": 500000,
        "confidential": False
    }
]

# Sample Publications
publications = [
    {
        "candidate_id": 1,  # Yann LeCun
        "title": "Gradient-Based Learning Applied to Document Recognition",
        "authors": "Y. LeCun, L. Bottou, Y. Bengio, P. Haffner",
        "venue": "Proceedings of the IEEE",
        "year": 1998,
        "citation_count": 45000,
        "research_area": "Computer Vision"
    },
    {
        "candidate_id": 2,  # Fei-Fei Li
        "title": "ImageNet: A Large-Scale Hierarchical Image Database",
        "authors": "J. Deng, W. Dong, R. Socher, L.-J. Li, K. Li, L. Fei-Fei",
        "venue": "CVPR 2009",
        "year": 2009,
        "citation_count": 75000,
        "research_area": "Computer Vision"
    },
    {
        "candidate_id": 3,  # Yoshua Bengio
        "title": "Learning Long-Term Dependencies with Gradient Descent is Difficult",
        "authors": "Y. Bengio, P. Simard, P. Frasconi",
        "venue": "IEEE Transactions on Neural Networks",
        "year": 1994,
        "citation_count": 15000,
        "research_area": "Deep Learning"
    },
    {
        "candidate_id": 5,  # Emily Chen
        "title": "Attention-Based Neural Machine Translation",
        "authors": "E. Chen, M. Rodriguez",
        "venue": "ACL 2020",
        "year": 2020,
        "arxiv_id": "2004.12345",
        "citation_count": 2500,
        "research_area": "Natural Language Processing"
    }
]

def populate_database():
    print("🚀 Populating AI/ML ATS with sample data...\n")

    # Add candidates
    print("👥 Adding candidates...")
    candidate_ids = []
    for candidate in candidates:
        try:
            response = requests.post(f"{API_URL}/api/candidates", json=candidate)
            if response.status_code == 201:
                data = response.json()
                candidate_ids.append(data['id'])
                print(f"  ✅ Added: {candidate['first_name']} {candidate['last_name']} (ID: {data['id']})")
            else:
                print(f"  ❌ Failed to add {candidate['first_name']} {candidate['last_name']}: {response.text}")
        except Exception as e:
            print(f"  ❌ Error adding {candidate['first_name']} {candidate['last_name']}: {str(e)}")

    print(f"\n📊 Added {len(candidate_ids)} candidates\n")

    # Add jobs
    print("💼 Adding jobs...")
    job_ids = []
    for job in jobs:
        try:
            response = requests.post(f"{API_URL}/api/jobs", json=job)
            if response.status_code == 201:
                data = response.json()
                job_ids.append(data['id'])
                confidential_tag = "🔒 CONFIDENTIAL" if job['confidential'] else "🌐 PUBLIC"
                print(f"  ✅ Added: {job['title']} at {job['company']} (ID: {data['id']}) {confidential_tag}")
            else:
                print(f"  ❌ Failed to add {job['title']}: {response.text}")
        except Exception as e:
            print(f"  ❌ Error adding {job['title']}: {str(e)}")

    print(f"\n📊 Added {len(job_ids)} jobs\n")

    # Add publications
    print("📄 Adding publications...")
    pub_count = 0
    for pub in publications:
        try:
            response = requests.post(f"{API_URL}/api/publications", json=pub)
            if response.status_code == 201:
                pub_count += 1
                print(f"  ✅ Added: {pub['title']}")
            else:
                print(f"  ❌ Failed to add publication: {response.text}")
        except Exception as e:
            print(f"  ❌ Error adding publication: {str(e)}")

    print(f"\n📊 Added {pub_count} publications\n")

    # Get stats
    try:
        response = requests.get(f"{API_URL}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print("📈 Final Statistics:")
            print(f"  • Total Candidates: {stats['total_candidates']}")
            print(f"  • Total Jobs: {stats['total_jobs']}")
            print(f"  • Total Applications: {stats['total_applications']}")
            print(f"  • Top Expertise Areas: {stats['top_expertise_areas']}")
    except Exception as e:
        print(f"❌ Error fetching stats: {str(e)}")

    print("\n✅ Sample data population complete!\n")
    print("🔒 Note: Some jobs are in STEALTH MODE - company names are hidden until interest is shown!")
    print("\n💡 To test stealth mode:")
    print(f"   View jobs: curl {API_URL}/api/jobs")
    print(f"   Reveal company: curl -X POST {API_URL}/api/jobs/2/reveal")

if __name__ == "__main__":
    populate_database()
