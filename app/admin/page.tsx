'use client';

import { useEffect, useState } from 'react';
import { Order, OrderStatus } from '@/lib/types';

interface Lead {
  person: string;
  company: string;
  email: string;
  website: string;
  whySelected: string;
  status?: string;
  notes?: string;
  lastContacted?: string;
  nextFollowUp?: string;
  source?: string; // Track which CSV file this lead came from
  campaign?: string; // Track which campaign this lead is in
}

type EmailTemplate =
  | 'moat-first'
  | 'stealth-recruiting'
  | 'source-company'
  | 'linkedin'
  | 'vc-intro'
  | 'funding-announcement'
  | 'job-posting-monitor'
  | 'multi-thread-ceo'
  | 'warm-referral'
  | 'regulatory-trigger'
  | 'acquisition-target';

interface TemplateInfo {
  id: EmailTemplate;
  name: string;
  category: 'positioning' | 'trigger';
  conversionRate: string;
  description: string;
  icon: string;
}

const TEMPLATE_LIBRARY: TemplateInfo[] = [
  // Positioning Templates (5)
  { id: 'moat-first', name: 'Moat-First Email', category: 'positioning', conversionRate: '8-12%', description: 'Lead with recruiting moat advantage', icon: '🏰' },
  { id: 'stealth-recruiting', name: 'Stealth Recruiting', category: 'positioning', conversionRate: '10-15%', description: 'Roadmap protection pitch', icon: '🥷' },
  { id: 'source-company', name: 'Source Company Pitch', category: 'positioning', conversionRate: '12-18%', description: 'Referral partnership model', icon: '🤝' },
  { id: 'linkedin', name: 'LinkedIn Short', category: 'positioning', conversionRate: '5-10%', description: 'Quick InMail format', icon: '💼' },
  { id: 'vc-intro', name: 'VC Introduction', category: 'positioning', conversionRate: '15-20%', description: 'Portfolio company pitch', icon: '📊' },

  // Trigger-Based Templates (6) - HIGH CONVERSION
  { id: 'funding-announcement', name: 'Funding Announcement', category: 'trigger', conversionRate: '20-30%', description: 'Send within 24-48hrs of Series A/B', icon: '💰' },
  { id: 'job-posting-monitor', name: 'Job Posting Monitor', category: 'trigger', conversionRate: '25-35%', description: 'Target 14-30 day old posts', icon: '📝' },
  { id: 'warm-referral', name: 'Warm Referral', category: 'trigger', conversionRate: '40-60%', description: 'HIGHEST CONVERSION - Recent placements', icon: '🌟' },
  { id: 'multi-thread-ceo', name: 'Multi-Thread CEO', category: 'trigger', conversionRate: '15-25%', description: 'Escalate to CEO after CTO no-response', icon: '👔' },
  { id: 'regulatory-trigger', name: 'Regulatory Trigger', category: 'trigger', conversionRate: '15-25%', description: 'EU AI Act updates, compliance deadlines', icon: '⚖️' },
  { id: 'acquisition-target', name: 'Acquisition Target', category: 'trigger', conversionRate: '25-35%', description: 'M&A due diligence urgency', icon: '🎯' },
];

export default function AdminPage() {
  const [authenticated, setAuthenticated] = useState(false);
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(false);
  const [filterStatus, setFilterStatus] = useState<OrderStatus | 'all'>('all');
  const [generatingCode, setGeneratingCode] = useState<string | null>(null);
  const [generatedCode, setGeneratedCode] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'orders' | 'leads' | 'revenue'>('orders');
  const [leads, setLeads] = useState<Lead[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [leadStatusFilter, setLeadStatusFilter] = useState<string>('all');
  const [selectedLeads, setSelectedLeads] = useState<Set<string>>(new Set());
  const [selectedTemplate, setSelectedTemplate] = useState<EmailTemplate>('warm-referral');
  const [previewLead, setPreviewLead] = useState<Lead | null>(null);
  const [bulkAction, setBulkAction] = useState<string>('');
  const [showTemplateLibrary, setShowTemplateLibrary] = useState(true);

  useEffect(() => {
    const auth = sessionStorage.getItem('adminAuthenticated');
    if (auth === 'true') {
      setAuthenticated(true);
      fetchOrders();
      fetchLeads();
    }
  }, []);

  // Auto-select first lead for preview
  useEffect(() => {
    if (filteredLeads.length > 0 && !previewLead) {
      setPreviewLead(filteredLeads[0]);
    }
  }, [leads]);

  const fetchLeads = async () => {
    try {
      const [response1, response2] = await Promise.all([
        fetch('/100 leads safety - Sheet1.csv'),
        fetch('/new_100_leads_safety.csv')
      ]);

      const [csv1, csv2] = await Promise.all([
        response1.text(),
        response2.text()
      ]);

      const parseCSV = (csvText: string, source: string): Lead[] => {
        const lines = csvText.split('\n').filter(line => line.trim());
        const headers = lines[0].split(',');

        return lines.slice(1).map(line => {
          const values = line.match(/(".*?"|[^,]+)(?=\s*,|\s*$)/g) || [];
          const cleanedValues = values.map(v => v.replace(/^"|"$/g, '').trim());

          return {
            person: cleanedValues[0] || '',
            company: cleanedValues[1] || '',
            email: cleanedValues[2] || '',
            website: cleanedValues[3] || '',
            whySelected: cleanedValues[4] || '',
            status: 'Not Contacted',
            notes: '',
            source: source,
            campaign: undefined
          };
        });
      };

      const allLeads = [
        ...parseCSV(csv1, 'Safety Batch 1'),
        ...parseCSV(csv2, 'Safety Batch 2')
      ];
      setLeads(allLeads);
    } catch (error) {
      console.error('Error fetching leads:', error);
    }
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch('/api/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        sessionStorage.setItem('adminAuthenticated', 'true');
        setAuthenticated(true);
        fetchOrders();
        fetchLeads();
      } else {
        setError('Invalid password');
      }
    } catch (err) {
      setError('Authentication failed');
    }
  };

  const fetchOrders = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/admin/get-orders');
      const data = await response.json();

      if (response.ok) {
        setOrders(data.orders);
      }
    } catch (err) {
      console.error('Error fetching orders:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateCode = async (orderId: string) => {
    setGeneratingCode(orderId);
    setGeneratedCode(null);

    try {
      const response = await fetch('/api/admin/activate-order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ orderId }),
      });

      const data = await response.json();

      if (response.ok) {
        setGeneratedCode(data.confirmationCode);
        fetchOrders();
      } else {
        alert(data.message || 'Failed to generate code');
      }
    } catch (err) {
      alert('Error generating confirmation code');
    } finally {
      setGeneratingCode(null);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  const handleLogout = () => {
    sessionStorage.removeItem('adminAuthenticated');
    setAuthenticated(false);
    setPassword('');
  };

  const filteredOrders = filterStatus === 'all'
    ? orders
    : orders.filter(order => order.status === filterStatus);

  const filteredLeads = leads.filter(lead => {
    const matchesSearch =
      lead.person.toLowerCase().includes(searchTerm.toLowerCase()) ||
      lead.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
      lead.email.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesStatus = leadStatusFilter === 'all' || lead.status === leadStatusFilter;

    return matchesSearch && matchesStatus;
  });

  const updateLeadStatus = (email: string, newStatus: string) => {
    setLeads(prev => prev.map(lead =>
      lead.email === email ? {
        ...lead,
        status: newStatus,
        lastContacted: newStatus === 'Contacted' ? new Date().toISOString() : lead.lastContacted
      } : lead
    ));
  };

  const getEmailTemplate = (template: EmailTemplate, lead: Lead): string => {
    const firstName = lead.person.split(' ')[0];

    const templates: Record<EmailTemplate, string> = {
      'moat-first': `Subject: Your competitors can't copy this

Hi ${firstName},

Most Physical AI CTOs think compliance is the hard part.

It's not. **Hiring the team to build the product is.**

You can outsource safety documentation (we do it Instantly for $2K). But finding senior robotics engineers who've actually shipped autonomous systems? That takes a 10-year network.

Which is why we built the only bundle that gives you both:

**SafetyCaseAI Full Stack Bundle ($15K):**
→ Safety case website (Instant delivery, GSN-validated)
→ 12-month recruiting access to our Microsoft/NVIDIA/Intel/Boston Dynamics network
→ No placement fees on first 3 hires (save $60K-$90K)
→ 14-day average time-to-offer (vs. 90-day industry standard)
→ Then: $18K flat fee per hire (not 20-30% like everyone else)

**Here's what makes this unforkable:**

Our compliance tech? Anyone can replicate that in 6 months.

Our recruiting network? We've been placing robotics engineers since 2012. 1,000+ placements = 1,000 referral sources.

**Two ways this works:**
1. You're our client → We solve compliance + talent for $15K
2. You're a source company → Your engineers become our referral sources

Which makes sense for ${lead.company}?

Live Demo: https://safetycaseai-platformv2.vercel.app/demo.html

Best,
John Polhill III
SafetyCaseAI | Physical AI Pros
john@physicalaipros.com`,

      'stealth-recruiting': `Subject: Your hiring reveals your roadmap (fix this)

Hi ${firstName},

When you post "Hiring: Senior Perception Engineer for Humanoid Robots," your competitors learn:
1. You're building humanoids (not AMRs/drones)
2. You're scaling fast (urgency = funding)
3. Exactly which skills you need (they can poach your targets)

**Tesla didn't announce Optimus until the team was in place. You shouldn't either.**

We do Stealth Mode™ Hiring for Physical AI companies:

→ We post anonymously: "Series A Robotics Startup" (not ${lead.company})
→ We describe skills, not projects
→ Candidates see your name ONLY after NDA + mutual interest
→ 90-day poaching shield: Competitors pay 3x fees to hire your placed talent

**$15K Full Stack Bundle:**
→ Safety case website (Instant, GSN-validated)
→ 12-month stealth recruiting support
→ No placement fees on first 3 hires (save $60K-$90K)
→ 14-day average time-to-offer
→ Then: $18K flat fee per hire

Worth 15 minutes to see how stealth recruiting protects ${lead.company}'s moat?

Live Demo: https://safetycaseai-platformv2.vercel.app/demo.html

Best,
John Polhill III
SafetyCaseAI | Physical AI Pros
john@physicalaipros.com`,

      'source-company': `Subject: Referral partnership for ${lead.company} engineers?

Hi ${firstName},

Different ask than most recruiters.

I'm not trying to poach your team. I'm asking if ${lead.company} wants to be a **source company** in our recruiting network.

**The model:**

When your engineers are ready to move (2-3 years from now), they come to us first. We place them. They refer their talented friends. The network compounds.

**What you get:**
→ $5K per placement referral fee
→ Talent intelligence (when competitors are hiring)
→ Priority recruiting access (if YOU need to hire)
→ Free compliance bundle: Safety case website ($2K value)

**What we get:**
Access to your team when they're ready to move (not now, but eventually).

This is how Microsoft, Intel, and 12+ Series A/B robotics companies work with us.

Interested in a 15-minute walkthrough?

Best,
John Polhill III
SafetyCaseAI | Physical AI Pros
john@physicalaipros.com`,

      'linkedin': `Hi ${firstName},

Congrats on ${lead.company} - impressive work!

I've placed 1,000+ robotics engineers at Microsoft, Intel, NVIDIA, Boston Dynamics over 27 years. I keep seeing the same pattern: Founders raise → 6 months on compliance → 6 months hiring → market window closes.

We compress both into 90 days for $15K:

→ Safety case website (Instant delivery)
→ Pre-vetted robotics talent (14-day average hire)
→ No fees on first 3 hires (save $60K-$90K)

Our compliance tech is replicable. Our 10-year recruiting network isn't.

Worth 15 min?

Live demo: https://safetycaseai-platformv2.vercel.app/demo.html

- John Polhill III
SafetyCaseAI | Physical AI Pros
john@physicalaipros.com`,

      'vc-intro': `Subject: Portfolio company intros - SafetyCaseAI

Hi ${firstName},

I'm John Polhill III - placed 1,000+ robotics engineers at Microsoft, Intel, NVIDIA, Boston Dynamics over 27 years.

I built SafetyCaseAI to solve the two bottlenecks killing Physical AI portfolio companies:

1. Compliance: 6-12 months, $500K → We do it Instantly for $2K
2. Talent: 90+ days per hire, $30K fees → We do 14 days, no fees on first 3

**Full Stack Bundle: $15K**
→ Safety case website + 12-month recruiting support
→ Compresses 12 months of non-product work into 90 days
→ Saves $575K vs. traditional path

**Portfolio offer:**
Introduce us to 3+ Physical AI companies, get:
→ 20% discount ($12K instead of $15K)
→ Priority recruiting (24-hour candidate intros)
→ Free compliance audits

Worth 20 min to discuss portfolio fit?

Live Demo: https://safetycaseai-platformv2.vercel.app/demo.html

Best,
John Polhill III
SafetyCaseAI | Physical AI Pros
john@physicalaipros.com`,

      'funding-announcement': `Subject: Series ${lead.company.includes('Series A') ? 'A' : 'B'} runway strategy - compliance + hiring

Hi ${firstName},

Saw the ${lead.company} funding announcement - congrats!

I've worked with 15+ Physical AI companies post-raise, and they all hit the same timeline trap:

**Week 1-8:** Celebrate, plan roadmap, hire first PM
**Week 9-32:** Stuck on compliance docs (investors want safety case for milestones)
**Week 33-56:** Finally start hiring engineers (but best candidates are gone)
**Week 57+:** Scramble to hit Series B milestones with incomplete team

**We compress weeks 9-56 into 90 days:**

→ Safety case website: Instant delivery (not 6 months)
→ Senior robotics engineers: 14-day average hire (not 90+ days)
→ Total cost: $15K + $18K per hire after first 3 (vs. $575K traditional path)

**Why this matters now:**

The companies that hit Series B milestones fastest are the ones who solved compliance + hiring in Q1. The ones who waited 6 months? They're doing bridge rounds.

Worth 20 minutes to see if this accelerates ${lead.company}'s roadmap?

Live Demo: https://safetycaseai-platformv2.vercel.app/demo.html

Best,
John Polhill III
SafetyCaseAI | Physical AI Pros
john@physicalaipros.com

P.S. - Send within 24-48 hours of funding announcement for maximum urgency.`,

      'job-posting-monitor': `Subject: Saw your ${lead.whySelected || 'robotics engineer'} posting - faster way to fill it

Hi ${firstName},

Saw ${lead.company} is hiring (posted recently on LinkedIn).

I'm reaching out because I've placed 1,000+ robotics engineers at Microsoft, Intel, NVIDIA, Boston Dynamics - and I already know 5-7 candidates who fit that profile.

**Here's the problem with public job posts:**

1. **90+ day hiring cycle** (post → screen → interview → offer)
2. **$30K placement fees** (20-30% of first-year salary)
3. **Roadmap exposure** (competitors see you're hiring perception engineers = you're building vision systems)
4. **Poaching risk** (recruiters scrape your post, target same candidates, offer more)

**Our model:**

→ **14-day average hire** (we already have warm candidates)
→ **$18K flat fee** (not 20-30% variable)
→ **Stealth recruiting** (anonymous posts, NDA gateway, zero competitor signals)
→ **90-day poaching shield** (competitors pay 3x to hire your placed talent)

**Bonus:** If you're also stuck on compliance (safety docs for investors/customers), we bundle both:

**$15K Full Stack Bundle:**
→ Safety case website (Instant delivery)
→ 12-month recruiting support
→ No fees on first 3 hires (this role + 2 more)

Worth 15 minutes to see if we can fill this role faster + cheaper than your current pipeline?

Live Demo: https://safetycaseai-platformv2.vercel.app/demo.html

Best,
John Polhill III
SafetyCaseAI | Physical AI Pros
john@physicalaipros.com

P.S. - If this role has been open 30+ days, that's a signal the market is tight. We can intro warm candidates this week (not 90 days from now).`,

      'multi-thread-ceo': `Subject: [CTO NAME] might forward this to you

Hi ${firstName},

I normally reach out to CTOs, but I'm betting they're too busy to prioritize this (even though it could save ${lead.company} $575K and 12 months).

**The bottleneck:**

Most Physical AI founders hit the same pattern:
- Raise Series A → 6 months stuck on compliance → 6 months stuck on hiring → market window closes

**The math:**

Traditional path:
- $500K compliance consultants (6-12 months)
- $90K recruiting fees (3 engineers @ $30K each, 90+ days per hire)
- **Total: $590K, 12-18 months timeline**

Our bundle:
- Safety case website (Instant delivery, $2K standalone)
- 12-month recruiting support (no fees on first 3 hires)
- **Total: $15K, 90-day timeline**

**Why CEOs care (not just CTOs):**

1. **Runway preservation:** $575K savings = 3-4 extra months of runway
2. **Investor optics:** Live compliance website + senior hires = milestone credibility
3. **Competitive velocity:** Ship while competitors are stuck in consultant hell

**Why this works:**

Compliance is commoditized (we automate it with AI). Recruiting is our moat (10-year network at Microsoft/NVIDIA/Intel that competitors can't replicate).

Worth 20 minutes to see if this accelerates ${lead.company}'s Series A roadmap?

Live Demo: https://safetycaseai-platformv2.vercel.app/demo.html

Best,
John Polhill III
SafetyCaseAI | Physical AI Pros
john@physicalaipros.com

P.S. - If your CTO already has compliance + hiring locked down, ignore this. But if they're swamped and these are backburner issues, that's exactly when $15K to compress 12 months into 90 days makes sense.`,

      'warm-referral': `Subject: [REFERRER NAME] suggested I reach out

Hi ${firstName},

[REFERRER NAME] ([REFERRER TITLE] at [REFERRER COMPANY]) suggested I reach out to you.

I placed [REFERRER NAME] at [REFERRER COMPANY] [X] months ago, and they mentioned ${lead.company} might be hitting the same compliance + hiring bottlenecks they faced.

**What [REFERRER NAME] told me:**

"[REFERRER COMPANY] wasted 8 months on safety documentation and another 4 months trying to hire robotics engineers. John's network got us 3 senior hires in 6 weeks, and the compliance bundle saved us $400K in consultant fees."

**For ${lead.company}, this would look like:**

**$15K Full Stack Bundle:**
→ Safety case website (Instant delivery, GSN-validated)
→ 12-month recruiting access (Microsoft/NVIDIA/Intel networks)
→ No placement fees on first 3 hires (save $60K-$90K)
→ 14-day average time-to-offer

**Why warm referrals convert:**

[REFERRER NAME] isn't getting paid to recommend us. They're just tired of watching fellow Physical AI founders waste runway on the same problems they solved.

Worth 15 minutes to see if this accelerates ${lead.company}'s hiring + compliance timeline?

Live Demo: https://safetycaseai-platformv2.vercel.app/demo.html

Best,
John Polhill III
SafetyCaseAI | Physical AI Pros
john@physicalaipros.com

P.S. - [REFERRER NAME] is happy to chat if you want to verify this (I can intro you). But figured I'd reach out directly first.`,

      'regulatory-trigger': `Subject: EU AI Act update - ${lead.company} compliance status?

Hi ${firstName},

The EU AI Act Article 43 (safety documentation for high-risk AI) just got updated with new requirements for autonomous systems.

I'm reaching out because ${lead.company} operates in [REGION], and I've helped 12+ Physical AI companies update their compliance docs to match the new regs.

**What changed (for robotics/autonomous systems):**

1. **Stricter safety case requirements** (Goal Structuring Notation now expected)
2. **AI/ML transparency mandates** (training data, model architecture, fallback mechanisms)
3. **Cyber-physical risk assessments** (not just software, but hardware + environment)
4. **6-month compliance window** (effective [DATE])

**The scramble:**

Companies with old PDF-based safety docs can't update them fast enough. Consultants are quoting $300K+ and 8-12 months.

We automate this: Upload your existing docs → AI extracts safety data → Generates updated GSN-compliant website → Instant delivery.

**$2K Compliance-Only Package:**
→ Safety case website (EU AI Act compliant, ISO 13482/61508)
→ GSN-validated structure (what auditors require)
→ Adaptive updates for 6 months (as regs evolve)

**Or bundle with recruiting ($15K):**
→ Compliance + 12-month recruiting support
→ No fees on first 3 hires

**Why this matters for ${lead.company}:**

EU customers will ask for updated compliance docs in due diligence. If you don't have them ready, deals stall.

Worth 15 minutes to review ${lead.company}'s current compliance status vs. new requirements?

Live Demo: https://safetycaseai-platformv2.vercel.app/demo.html

Best,
John Polhill III
SafetyCaseAI | Physical AI Pros
john@physicalaipros.com

P.S. - If ${lead.company} already has EU AI Act-compliant docs, ignore this. But most companies don't even know Article 43 changed until customers ask for it.`,

      'acquisition-target': `Subject: [ACQUIRER] due diligence - compliance docs ready?

Hi ${firstName},

Saw the news about potential acquisition interest in ${lead.company} or similar companies in your space. Congrats if that's in the works!

I'm reaching out because I've helped 8 Physical AI companies prepare for M&A due diligence, and compliance documentation is ALWAYS on the checklist.

**What acquirers ask for:**

1. **Structured safety case** (not scattered PDFs)
2. **GSN-validated documentation** (Goal Structuring Notation)
3. **Risk assessment matrices** (probabilistic, not qualitative)
4. **AI/ML transparency** (training data, model architecture, validation)
5. **Regulatory compliance proof** (ISO 13482, IEC 61508, industry-specific)

**The problem:**

Acquirers give you 2-4 weeks to produce these docs. If you don't have them ready, the deal stalls or valuation drops.

**We compress this to Instant delivery:**

→ Upload your existing docs (design specs, test logs, FMEA, risk assessments)
→ AI extracts safety-critical data
→ Generates GSN-validated safety case website
→ Instant delivery (not 6-12 months)

**$2K Compliance Package:**
→ Professional safety case website
→ Due diligence-ready format
→ Investor/acquirer-facing (not internal docs)

**Why M&A targets care:**

Every day of due diligence delay = risk of deal falling through. $2K to compress 6 months into Instant delivery = 300x ROI if it saves the acquisition.

Worth 15 minutes to review ${lead.company}'s current compliance documentation vs. M&A checklist requirements?

Live Demo: https://safetycaseai-platformv2.vercel.app/demo.html

Best,
John Polhill III
SafetyCaseAI | Physical AI Pros
john@physicalaipros.com

P.S. - Even if ${lead.company} isn't actively in M&A talks, having this ready shows strategic readiness (which itself increases valuation).`,
    };

    return templates[template];
  };

  const toggleLeadSelection = (email: string) => {
    const newSelected = new Set(selectedLeads);
    if (newSelected.has(email)) {
      newSelected.delete(email);
    } else {
      newSelected.add(email);
    }
    setSelectedLeads(newSelected);
  };

  const toggleSelectAll = () => {
    if (selectedLeads.size === filteredLeads.length) {
      setSelectedLeads(new Set());
    } else {
      setSelectedLeads(new Set(filteredLeads.map(l => l.email)));
    }
  };

  const handleBulkAction = () => {
    if (!bulkAction) return;

    setLeads(prev => prev.map(lead =>
      selectedLeads.has(lead.email) ? { ...lead, status: bulkAction } : lead
    ));
    setSelectedLeads(new Set());
    setBulkAction('');
  };

  const copyEmailToClipboard = (lead: Lead) => {
    const emailContent = getEmailTemplate(selectedTemplate, lead);
    navigator.clipboard.writeText(emailContent);
    alert(`✅ ${TEMPLATE_LIBRARY.find(t => t.id === selectedTemplate)?.name} copied to clipboard!\n\nReady to paste into your email client.`);

    updateLeadStatus(lead.email, 'Contacted');
  };

  const exportToCSV = () => {
    const headers = ['Person', 'Company', 'Email', 'Website', 'Status', 'Why Selected', 'Last Contacted'];
    const rows = filteredLeads.map(lead => [
      lead.person,
      lead.company,
      lead.email,
      lead.website,
      lead.status || 'Not Contacted',
      lead.whySelected,
      lead.lastContacted || ''
    ]);

    const csvContent = [headers, ...rows]
      .map(row => row.map(cell => `"${cell}"`).join(','))
      .join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `leads-export-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
  };

  const getStatusBadge = (status: OrderStatus) => {
    const colors = {
      pending_payment: 'bg-yellow-100 text-yellow-800',
      code_generated: 'bg-blue-100 text-blue-800',
      pdf_uploaded: 'bg-purple-100 text-purple-800',
      completed: 'bg-green-100 text-green-800',
    };

    return (
      <span className={`px-3 py-1 rounded-full text-sm font-semibold ${colors[status]}`}>
        {status.replace('_', ' ').toUpperCase()}
      </span>
    );
  };

  const selectedTemplateInfo = TEMPLATE_LIBRARY.find(t => t.id === selectedTemplate);
  const positioningTemplates = TEMPLATE_LIBRARY.filter(t => t.category === 'positioning');
  const triggerTemplates = TEMPLATE_LIBRARY.filter(t => t.category === 'trigger');

  if (!authenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50">
        <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full border border-gray-200">
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl mx-auto mb-4 flex items-center justify-center">
              <span className="text-3xl">🔐</span>
            </div>
            <h1 className="text-3xl font-bold text-gray-900">Admin Login</h1>
            <p className="text-gray-600 mt-2">SafetyCaseAI CRM Dashboard</p>
          </div>
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label htmlFor="password" className="block text-sm font-semibold text-gray-700 mb-2">
                Password
              </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="Enter admin password"
                required
              />
            </div>

            {error && (
              <div className="bg-red-50 border-l-4 border-red-500 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            <button type="submit" className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all shadow-lg hover:shadow-xl">
              Login to Dashboard
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-purple-50 to-blue-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-700 via-purple-600 to-blue-600 text-white shadow-xl">
        <div className="max-w-[1920px] mx-auto px-6 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold mb-1 flex items-center gap-3">
                <span className="bg-white/20 p-2 rounded-lg">🚀</span>
                SafetyCaseAI Admin Dashboard
              </h1>
              <p className="text-purple-100">Automated Outreach System | {leads.length} Robotics CTOs</p>
            </div>
            <button
              onClick={handleLogout}
              className="bg-white/20 hover:bg-white/30 px-6 py-2 rounded-lg font-semibold transition-all backdrop-blur-sm border border-white/30"
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-10">
        <div className="max-w-[1920px] mx-auto px-6">
          <div className="flex gap-2">
            <button
              onClick={() => setActiveTab('orders')}
              className={`px-8 py-4 font-semibold transition-all relative ${
                activeTab === 'orders'
                  ? 'text-purple-700 border-b-4 border-purple-600 bg-purple-50'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              <span className="flex items-center gap-2">
                📦 Orders
                <span className="bg-purple-600 text-white text-xs px-2 py-1 rounded-full">{orders.length}</span>
              </span>
            </button>
            <button
              onClick={() => setActiveTab('leads')}
              className={`px-8 py-4 font-semibold transition-all relative ${
                activeTab === 'leads'
                  ? 'text-purple-700 border-b-4 border-purple-600 bg-purple-50'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              <span className="flex items-center gap-2">
                👥 Leads CRM
                <span className="bg-blue-600 text-white text-xs px-2 py-1 rounded-full">{leads.length}</span>
              </span>
            </button>
            <button
              onClick={() => setActiveTab('revenue')}
              className={`px-8 py-4 font-semibold transition-all relative ${
                activeTab === 'revenue'
                  ? 'text-purple-700 border-b-4 border-purple-600 bg-purple-50'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              <span className="flex items-center gap-2">
                💰 Revenue Pipeline
                <span className="bg-green-600 text-white text-xs px-2 py-1 rounded-full">
                  ${((leads.filter(l => l.status === 'Qualified' || l.status === 'Follow Up').length) * 2000).toLocaleString()}
                </span>
              </span>
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-[1920px] mx-auto px-6 py-8">
        {generatedCode && activeTab === 'orders' && (
          <div className="bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-400 rounded-2xl p-6 mb-8 shadow-lg">
            <h3 className="text-xl font-bold mb-4 text-green-800 flex items-center gap-2">
              <span className="text-2xl">✅</span>
              Confirmation Code Generated
            </h3>
            <div className="flex items-center gap-4">
              <span className="text-4xl font-mono font-bold text-green-900 bg-white px-6 py-3 rounded-lg border-2 border-green-300">
                {generatedCode}
              </span>
              <button
                onClick={() => copyToClipboard(generatedCode)}
                className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-semibold transition-all shadow-md hover:shadow-lg"
              >
                Copy Code
              </button>
            </div>
            <p className="mt-4 text-green-800 font-medium">
              Send this code to the customer via SafetyCaseAI@physicalAIPros.com
            </p>
          </div>
        )}

        {/* ORDERS TAB */}
        {activeTab === 'orders' && (
          <>
            <div className="bg-white rounded-2xl shadow-lg border border-gray-200 mb-8 overflow-hidden">
              <div className="bg-gradient-to-r from-gray-50 to-purple-50 border-b border-gray-200 p-6">
                <div className="flex justify-between items-center">
                  <h2 className="text-2xl font-bold text-gray-900">Order Management</h2>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setFilterStatus('all')}
                      className={`px-4 py-2 rounded-lg font-semibold transition-all ${filterStatus === 'all' ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-md' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
                    >
                      All ({orders.length})
                    </button>
                    <button
                      onClick={() => setFilterStatus('pending_payment')}
                      className={`px-4 py-2 rounded-lg font-semibold transition-all ${filterStatus === 'pending_payment' ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-md' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
                    >
                      Pending
                    </button>
                    <button
                      onClick={() => setFilterStatus('code_generated')}
                      className={`px-4 py-2 rounded-lg font-semibold transition-all ${filterStatus === 'code_generated' ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-md' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
                    >
                      Active
                    </button>
                    <button
                      onClick={() => setFilterStatus('completed')}
                      className={`px-4 py-2 rounded-lg font-semibold transition-all ${filterStatus === 'completed' ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-md' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
                    >
                      Completed
                    </button>
                  </div>
                </div>
                <button
                  onClick={fetchOrders}
                  disabled={loading}
                  className="mt-4 bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg font-semibold transition-all disabled:opacity-50"
                >
                  {loading ? 'Refreshing...' : '🔄 Refresh Orders'}
                </button>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50 border-b border-gray-200">
                    <tr>
                      <th className="px-6 py-4 text-left text-sm font-bold text-gray-700">Order ID</th>
                      <th className="px-6 py-4 text-left text-sm font-bold text-gray-700">Company</th>
                      <th className="px-6 py-4 text-left text-sm font-bold text-gray-700">Email</th>
                      <th className="px-6 py-4 text-left text-sm font-bold text-gray-700">Template</th>
                      <th className="px-6 py-4 text-left text-sm font-bold text-gray-700">Created</th>
                      <th className="px-6 py-4 text-left text-sm font-bold text-gray-700">Status</th>
                      <th className="px-6 py-4 text-left text-sm font-bold text-gray-700">Code</th>
                      <th className="px-6 py-4 text-left text-sm font-bold text-gray-700">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {filteredOrders.length === 0 ? (
                      <tr>
                        <td colSpan={8} className="px-6 py-12 text-center text-gray-500">
                          <div className="flex flex-col items-center gap-3">
                            <span className="text-5xl opacity-30">📦</span>
                            <p className="text-lg font-medium">No orders found</p>
                          </div>
                        </td>
                      </tr>
                    ) : (
                      filteredOrders.map(order => (
                        <tr key={order.orderId} className="hover:bg-purple-50 transition-colors">
                          <td className="px-6 py-4">
                            <span className="font-mono text-sm bg-gray-100 px-2 py-1 rounded">{order.orderId}</span>
                          </td>
                          <td className="px-6 py-4">
                            <span className="font-semibold text-gray-900">{order.companyName || '—'}</span>
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-600">
                            {order.email || '—'}
                          </td>
                          <td className="px-6 py-4 capitalize text-sm">{order.templateType}</td>
                          <td className="px-6 py-4 text-sm text-gray-600">
                            {new Date(order.createdAt).toLocaleDateString()}
                          </td>
                          <td className="px-6 py-4">{getStatusBadge(order.status)}</td>
                          <td className="px-6 py-4">
                            {order.confirmationCode ? (
                              <span className="font-mono text-sm font-bold bg-green-100 px-2 py-1 rounded text-green-800">
                                {order.confirmationCode}
                              </span>
                            ) : (
                              <span className="text-gray-400">—</span>
                            )}
                          </td>
                          <td className="px-6 py-4">
                            {order.status === 'pending_payment' && (
                              <button
                                onClick={() => handleGenerateCode(order.orderId)}
                                disabled={generatingCode === order.orderId}
                                className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 transition-all shadow-md hover:shadow-lg"
                              >
                                {generatingCode === order.orderId
                                  ? 'Generating...'
                                  : 'Generate Code'}
                              </button>
                            )}
                            {order.confirmationCode && (
                              <button
                                onClick={() => copyToClipboard(order.confirmationCode!)}
                                className="bg-gray-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-gray-700 transition-all shadow-md hover:shadow-lg"
                              >
                                Copy Code
                              </button>
                            )}
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="grid md:grid-cols-3 gap-6">
              <div className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-2xl p-6 border-2 border-yellow-200 shadow-lg">
                <h3 className="font-bold text-lg mb-2 text-yellow-900 flex items-center gap-2">
                  <span className="text-2xl">⏳</span>
                  Pending Payment
                </h3>
                <p className="text-5xl font-bold text-yellow-700">
                  {orders.filter(o => o.status === 'pending_payment').length}
                </p>
              </div>
              <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-6 border-2 border-blue-200 shadow-lg">
                <h3 className="font-bold text-lg mb-2 text-blue-900 flex items-center gap-2">
                  <span className="text-2xl">🔄</span>
                  Active Orders
                </h3>
                <p className="text-5xl font-bold text-blue-700">
                  {orders.filter(o => o.status === 'code_generated' || o.status === 'pdf_uploaded').length}
                </p>
              </div>
              <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-6 border-2 border-green-200 shadow-lg">
                <h3 className="font-bold text-lg mb-2 text-green-900 flex items-center gap-2">
                  <span className="text-2xl">✅</span>
                  Completed
                </h3>
                <p className="text-5xl font-bold text-green-700">
                  {orders.filter(o => o.status === 'completed').length}
                </p>
              </div>
            </div>
          </>
        )}

        {/* LEADS CRM TAB - HUBSPOT STYLE */}
        {activeTab === 'leads' && (
          <>
            {/* Template Library Header */}
            <div className="bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 rounded-2xl p-8 mb-8 text-white shadow-2xl">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h2 className="text-3xl font-bold mb-2 flex items-center gap-3">
                    <span className="bg-white/20 p-2 rounded-lg">📧</span>
                    11 High-Conversion Email Templates
                  </h2>
                  <p className="text-purple-100 text-lg">5 Positioning Templates + 6 Trigger-Based Templates (Often Overlooked!)</p>
                </div>
                <button
                  onClick={() => setShowTemplateLibrary(!showTemplateLibrary)}
                  className="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg font-semibold transition-all backdrop-blur-sm border border-white/30"
                >
                  {showTemplateLibrary ? 'Hide' : 'Show'} Templates
                </button>
              </div>

              {showTemplateLibrary && (
                <div className="grid md:grid-cols-2 gap-6">
                  {/* Positioning Templates */}
                  <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
                    <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                      <span>🎯</span>
                      Positioning Templates (5)
                    </h3>
                    <div className="space-y-3">
                      {positioningTemplates.map(template => (
                        <button
                          key={template.id}
                          onClick={() => setSelectedTemplate(template.id)}
                          className={`w-full text-left p-4 rounded-lg transition-all ${
                            selectedTemplate === template.id
                              ? 'bg-white text-purple-700 shadow-lg'
                              : 'bg-white/20 hover:bg-white/30 text-white'
                          }`}
                        >
                          <div className="flex items-center justify-between mb-1">
                            <span className="font-bold flex items-center gap-2">
                              <span>{template.icon}</span>
                              {template.name}
                            </span>
                            <span className={`px-2 py-1 rounded-full text-xs font-bold ${
                              selectedTemplate === template.id ? 'bg-purple-100 text-purple-700' : 'bg-white/20'
                            }`}>
                              {template.conversionRate}
                            </span>
                          </div>
                          <p className={`text-sm ${selectedTemplate === template.id ? 'text-purple-600' : 'text-purple-100'}`}>
                            {template.description}
                          </p>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Trigger-Based Templates */}
                  <div className="bg-gradient-to-br from-yellow-500/20 to-orange-500/20 backdrop-blur-sm rounded-xl p-6 border-2 border-yellow-400/50">
                    <h3 className="text-xl font-bold mb-2 flex items-center gap-2">
                      <span>⚡</span>
                      Trigger-Based Templates (6) - HIGH CONVERSION
                    </h3>
                    <p className="text-purple-100 text-sm mb-4 font-medium">Often overlooked but 3-6x better conversion!</p>
                    <div className="space-y-3">
                      {triggerTemplates.map(template => (
                        <button
                          key={template.id}
                          onClick={() => setSelectedTemplate(template.id)}
                          className={`w-full text-left p-4 rounded-lg transition-all ${
                            selectedTemplate === template.id
                              ? 'bg-white text-purple-700 shadow-lg'
                              : 'bg-white/20 hover:bg-white/30 text-white'
                          }`}
                        >
                          <div className="flex items-center justify-between mb-1">
                            <span className="font-bold flex items-center gap-2">
                              <span>{template.icon}</span>
                              {template.name}
                            </span>
                            <span className={`px-2 py-1 rounded-full text-xs font-bold ${
                              selectedTemplate === template.id
                                ? 'bg-gradient-to-r from-yellow-400 to-orange-400 text-gray-900'
                                : 'bg-yellow-400/20 text-yellow-100'
                            }`}>
                              {template.conversionRate}
                            </span>
                          </div>
                          <p className={`text-sm ${selectedTemplate === template.id ? 'text-purple-600' : 'text-purple-100'}`}>
                            {template.description}
                          </p>
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Split Panel: Leads List + Email Preview */}
            <div className="grid grid-cols-12 gap-6 mb-8">
              {/* LEFT PANEL - LEADS LIST */}
              <div className="col-span-7 bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
                <div className="bg-gradient-to-r from-gray-50 to-purple-50 border-b border-gray-200 p-6">
                  <h3 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                    <span>👥</span>
                    Lead Database ({filteredLeads.length})
                  </h3>

                  {/* Search and Filters */}
                  <div className="grid grid-cols-12 gap-3 mb-4">
                    <input
                      type="text"
                      placeholder="🔍 Search by name, company, or email..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="col-span-6 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent font-medium"
                    />
                    <select
                      value={leadStatusFilter}
                      onChange={(e) => setLeadStatusFilter(e.target.value)}
                      className="col-span-3 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 font-medium"
                    >
                      <option value="all">All Status</option>
                      <option value="Not Contacted">Not Contacted</option>
                      <option value="Contacted">Contacted</option>
                      <option value="Follow Up">Follow Up</option>
                      <option value="Qualified">Qualified</option>
                      <option value="Closed">Closed</option>
                    </select>
                    <button
                      onClick={exportToCSV}
                      className="col-span-2 px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 font-semibold transition-all shadow-md hover:shadow-lg"
                    >
                      📥 Export
                    </button>
                    <button
                      onClick={() => {setSearchTerm(''); setLeadStatusFilter('all');}}
                      className="col-span-1 px-4 py-3 bg-gray-200 rounded-lg hover:bg-gray-300 font-semibold"
                    >
                      ✕
                    </button>
                  </div>

                  {/* Bulk Actions */}
                  {selectedLeads.size > 0 && (
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex items-center gap-4">
                      <span className="font-bold text-blue-900">{selectedLeads.size} selected</span>
                      <select
                        value={bulkAction}
                        onChange={(e) => setBulkAction(e.target.value)}
                        className="px-4 py-2 border border-blue-300 rounded-lg font-medium"
                      >
                        <option value="">Bulk Action...</option>
                        <option value="Contacted">Mark as Contacted</option>
                        <option value="Follow Up">Mark for Follow Up</option>
                        <option value="Qualified">Mark as Qualified</option>
                        <option value="Closed">Mark as Closed</option>
                      </select>
                      <button
                        onClick={handleBulkAction}
                        disabled={!bulkAction}
                        className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 font-semibold transition-all shadow-md"
                      >
                        Apply
                      </button>
                      <button
                        onClick={() => setSelectedLeads(new Set())}
                        className="px-4 py-2 text-blue-600 hover:text-blue-800 font-semibold"
                      >
                        Clear
                      </button>
                    </div>
                  )}
                </div>

                {/* Leads Table */}
                <div className="overflow-x-auto max-h-[800px]">
                  <table className="w-full">
                    <thead className="bg-gray-50 border-b border-gray-200 sticky top-0">
                      <tr>
                        <th className="px-4 py-3 text-left">
                          <input
                            type="checkbox"
                            checked={selectedLeads.size === filteredLeads.length && filteredLeads.length > 0}
                            onChange={toggleSelectAll}
                            className="w-5 h-5 cursor-pointer"
                          />
                        </th>
                        <th className="px-4 py-3 text-left text-sm font-bold text-gray-700">Contact</th>
                        <th className="px-4 py-3 text-left text-sm font-bold text-gray-700">Status</th>
                        <th className="px-4 py-3 text-left text-sm font-bold text-gray-700">Action</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {filteredLeads.length === 0 ? (
                        <tr>
                          <td colSpan={4} className="px-6 py-12 text-center text-gray-500">
                            <div className="flex flex-col items-center gap-3">
                              <span className="text-5xl opacity-30">🔍</span>
                              <p className="text-lg font-medium">No leads found</p>
                            </div>
                          </td>
                        </tr>
                      ) : (
                        filteredLeads.map((lead, idx) => (
                          <tr
                            key={idx}
                            className={`transition-colors cursor-pointer ${
                              previewLead?.email === lead.email
                                ? 'bg-purple-100 border-l-4 border-purple-600'
                                : selectedLeads.has(lead.email)
                                ? 'bg-blue-50'
                                : 'hover:bg-gray-50'
                            }`}
                            onClick={() => setPreviewLead(lead)}
                          >
                            <td className="px-4 py-3">
                              <input
                                type="checkbox"
                                checked={selectedLeads.has(lead.email)}
                                onChange={(e) => {
                                  e.stopPropagation();
                                  toggleLeadSelection(lead.email);
                                }}
                                className="w-5 h-5 cursor-pointer"
                              />
                            </td>
                            <td className="px-4 py-3">
                              <div>
                                <span className="font-bold text-gray-900 block">{lead.person}</span>
                                <span className="text-sm text-gray-600 block">{lead.company}</span>
                                <a href={`mailto:${lead.email}`} className="text-xs text-purple-600 hover:underline block" onClick={(e) => e.stopPropagation()}>
                                  {lead.email}
                                </a>
                              </div>
                            </td>
                            <td className="px-4 py-3">
                              <select
                                value={lead.status}
                                onChange={(e) => {
                                  e.stopPropagation();
                                  updateLeadStatus(lead.email, e.target.value);
                                }}
                                className="text-xs px-3 py-2 rounded-full border-2 border-gray-300 focus:ring-2 focus:ring-purple-500 font-semibold"
                              >
                                <option value="Not Contacted">🔴 Not Contacted</option>
                                <option value="Contacted">🟡 Contacted</option>
                                <option value="Follow Up">🔵 Follow Up</option>
                                <option value="Qualified">🟢 Qualified</option>
                                <option value="Closed">⚫ Closed</option>
                              </select>
                              {lead.lastContacted && (
                                <div className="text-xs text-gray-500 mt-1">
                                  {new Date(lead.lastContacted).toLocaleDateString()}
                                </div>
                              )}
                            </td>
                            <td className="px-4 py-3">
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  copyEmailToClipboard(lead);
                                }}
                                className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-4 py-2 rounded-lg text-sm font-bold hover:from-purple-700 hover:to-blue-700 shadow-md hover:shadow-lg transition-all"
                              >
                                📋 Copy Email
                              </button>
                            </td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* RIGHT PANEL - EMAIL PREVIEW */}
              <div className="col-span-5 bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden sticky top-6 h-fit max-h-[1000px]">
                <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-6 border-b border-purple-700">
                  <h3 className="text-2xl font-bold mb-2 flex items-center gap-2">
                    <span>📧</span>
                    Email Preview
                  </h3>
                  {selectedTemplateInfo && (
                    <div className="flex items-center gap-2 text-purple-100">
                      <span>{selectedTemplateInfo.icon}</span>
                      <span className="font-semibold">{selectedTemplateInfo.name}</span>
                      <span className="bg-white/20 px-2 py-1 rounded-full text-xs font-bold">
                        {selectedTemplateInfo.conversionRate} conversion
                      </span>
                    </div>
                  )}
                </div>

                {previewLead ? (
                  <div className="p-6">
                    {/* Recipient Info */}
                    <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-4 mb-4 border border-purple-200">
                      <div className="text-sm text-gray-600 mb-1">TO:</div>
                      <div className="font-bold text-lg text-gray-900">{previewLead.person}</div>
                      <div className="text-sm text-gray-600">{previewLead.company}</div>
                      <div className="text-sm text-purple-600 font-mono">{previewLead.email}</div>
                    </div>

                    {/* Email Content */}
                    <div className="bg-gray-50 rounded-lg p-6 border border-gray-200 font-mono text-sm whitespace-pre-wrap max-h-[700px] overflow-y-auto">
                      {getEmailTemplate(selectedTemplate, previewLead)}
                    </div>

                    {/* Copy Button */}
                    <button
                      onClick={() => copyEmailToClipboard(previewLead)}
                      className="w-full mt-4 bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-4 rounded-lg text-lg font-bold hover:from-purple-700 hover:to-blue-700 shadow-lg hover:shadow-xl transition-all flex items-center justify-center gap-2"
                    >
                      <span>📋</span>
                      Copy {selectedTemplateInfo?.name} to Clipboard
                    </button>
                  </div>
                ) : (
                  <div className="p-12 text-center text-gray-400">
                    <span className="text-6xl block mb-4 opacity-30">👈</span>
                    <p className="text-lg font-medium">Click a lead to preview email</p>
                  </div>
                )}
              </div>
            </div>

            {/* Lead Stats */}
            <div className="grid md:grid-cols-5 gap-6">
              <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl p-6 border-2 border-gray-200 shadow-lg">
                <h3 className="font-bold text-lg mb-2 text-gray-900 flex items-center gap-2">
                  <span className="text-2xl">📊</span>
                  Total Leads
                </h3>
                <p className="text-5xl font-bold text-gray-700">{leads.length}</p>
              </div>
              <div className="bg-gradient-to-br from-red-50 to-orange-50 rounded-2xl p-6 border-2 border-red-200 shadow-lg">
                <h3 className="font-bold text-lg mb-2 text-red-900 flex items-center gap-2">
                  <span className="text-2xl">🔴</span>
                  Not Contacted
                </h3>
                <p className="text-5xl font-bold text-red-700">
                  {leads.filter(l => l.status === 'Not Contacted').length}
                </p>
              </div>
              <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-6 border-2 border-blue-200 shadow-lg">
                <h3 className="font-bold text-lg mb-2 text-blue-900 flex items-center gap-2">
                  <span className="text-2xl">🟡</span>
                  Contacted
                </h3>
                <p className="text-5xl font-bold text-blue-700">
                  {leads.filter(l => l.status === 'Contacted').length}
                </p>
              </div>
              <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-6 border-2 border-purple-200 shadow-lg">
                <h3 className="font-bold text-lg mb-2 text-purple-900 flex items-center gap-2">
                  <span className="text-2xl">🟢</span>
                  Qualified
                </h3>
                <p className="text-5xl font-bold text-purple-700">
                  {leads.filter(l => l.status === 'Qualified').length}
                </p>
              </div>
              <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-6 border-2 border-green-200 shadow-lg">
                <h3 className="font-bold text-lg mb-2 text-green-900 flex items-center gap-2">
                  <span className="text-2xl">✅</span>
                  Closed
                </h3>
                <p className="text-5xl font-bold text-green-700">
                  {leads.filter(l => l.status === 'Closed').length}
                </p>
              </div>
            </div>
          </>
        )}

        {/* REVENUE PIPELINE TAB */}
        {activeTab === 'revenue' && (
          <>
            {/* Revenue Overview Cards */}
            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-8 border-2 border-green-300 shadow-lg">
                <h3 className="font-bold text-lg mb-2 text-green-900 flex items-center gap-2">
                  <span className="text-3xl">💰</span>
                  Total Pipeline Value
                </h3>
                <p className="text-5xl font-bold text-green-700 mb-2">
                  ${(leads.length * 2000).toLocaleString()}
                </p>
                <p className="text-sm text-green-600">
                  {leads.length} leads × $2,000 per conversion
                </p>
              </div>

              <div className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-2xl p-8 border-2 border-yellow-300 shadow-lg">
                <h3 className="font-bold text-lg mb-2 text-yellow-900 flex items-center gap-2">
                  <span className="text-3xl">🔥</span>
                  Hot Leads (Qualified + Follow Up)
                </h3>
                <p className="text-5xl font-bold text-yellow-700 mb-2">
                  ${((leads.filter(l => l.status === 'Qualified' || l.status === 'Follow Up').length) * 2000).toLocaleString()}
                </p>
                <p className="text-sm text-yellow-600">
                  {leads.filter(l => l.status === 'Qualified' || l.status === 'Follow Up').length} hot leads × $2,000
                </p>
              </div>

              <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-8 border-2 border-blue-300 shadow-lg">
                <h3 className="font-bold text-lg mb-2 text-blue-900 flex items-center gap-2">
                  <span className="text-3xl">📊</span>
                  Average Deal Size
                </h3>
                <p className="text-5xl font-bold text-blue-700 mb-2">
                  $2,000
                </p>
                <p className="text-sm text-blue-600">
                  Per safety case website
                </p>
              </div>
            </div>

            {/* Campaign Management */}
            <div className="bg-white rounded-2xl shadow-lg border border-gray-200 mb-8 overflow-hidden">
              <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-6">
                <h3 className="text-2xl font-bold mb-2 flex items-center gap-2">
                  <span>📧</span>
                  Campaign Management & Lead Grouping
                </h3>
                <p className="text-purple-100">Organize leads by source and assign email campaigns</p>
              </div>

              <div className="p-6">
                {/* Lead Source Groups */}
                <div className="grid md:grid-cols-2 gap-6">
                  {/* Safety Batch 1 */}
                  <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl p-6 border-2 border-purple-200">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h4 className="text-xl font-bold text-gray-900 mb-1 flex items-center gap-2">
                          <span className="text-2xl">📁</span>
                          Safety Batch 1
                        </h4>
                        <p className="text-sm text-gray-600">
                          {leads.filter(l => l.source === 'Safety Batch 1').length} leads •
                          Potential: ${(leads.filter(l => l.source === 'Safety Batch 1').length * 2000).toLocaleString()}
                        </p>
                      </div>
                      <span className="bg-purple-600 text-white px-3 py-1 rounded-full text-sm font-bold">
                        Batch 1
                      </span>
                    </div>

                    {/* Status Breakdown */}
                    <div className="space-y-2 mb-4">
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-700">Not Contacted:</span>
                        <span className="font-bold text-gray-900">
                          {leads.filter(l => l.source === 'Safety Batch 1' && l.status === 'Not Contacted').length}
                        </span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-700">Contacted:</span>
                        <span className="font-bold text-gray-900">
                          {leads.filter(l => l.source === 'Safety Batch 1' && l.status === 'Contacted').length}
                        </span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-700">Qualified:</span>
                        <span className="font-bold text-green-700">
                          {leads.filter(l => l.source === 'Safety Batch 1' && l.status === 'Qualified').length}
                        </span>
                      </div>
                    </div>

                    {/* Campaign Template Selector */}
                    <div className="bg-white rounded-lg p-4 border border-purple-200">
                      <label className="block text-sm font-bold text-gray-700 mb-2">Assign Campaign:</label>
                      <select className="w-full px-3 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 text-sm">
                        <option value="">Select template...</option>
                        <optgroup label="Positioning Templates">
                          <option value="moat-first">🏰 Moat-First (8-12%)</option>
                          <option value="stealth-recruiting">🥷 Stealth Recruiting (10-15%)</option>
                          <option value="source-company">🤝 Source Company (12-18%)</option>
                          <option value="linkedin">💼 LinkedIn (5-10%)</option>
                          <option value="vc-intro">📊 VC Intro (15-20%)</option>
                        </optgroup>
                        <optgroup label="Trigger-Based Templates">
                          <option value="funding-announcement">💰 Funding Announcement (20-30%)</option>
                          <option value="job-posting-monitor">📝 Job Posting Monitor (25-35%)</option>
                          <option value="warm-referral">🌟 Warm Referral (40-60%)</option>
                          <option value="multi-thread-ceo">👔 Multi-Thread CEO (15-25%)</option>
                          <option value="regulatory-trigger">⚖️ Regulatory Trigger (15-25%)</option>
                          <option value="acquisition-target">🎯 Acquisition Target (25-35%)</option>
                        </optgroup>
                      </select>
                      <button className="w-full mt-3 bg-purple-600 text-white py-2 rounded-lg font-semibold hover:bg-purple-700 transition-colors">
                        Apply to Batch 1
                      </button>
                    </div>
                  </div>

                  {/* Safety Batch 2 */}
                  <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 border-2 border-blue-200">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h4 className="text-xl font-bold text-gray-900 mb-1 flex items-center gap-2">
                          <span className="text-2xl">📁</span>
                          Safety Batch 2
                        </h4>
                        <p className="text-sm text-gray-600">
                          {leads.filter(l => l.source === 'Safety Batch 2').length} leads •
                          Potential: ${(leads.filter(l => l.source === 'Safety Batch 2').length * 2000).toLocaleString()}
                        </p>
                      </div>
                      <span className="bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-bold">
                        Batch 2
                      </span>
                    </div>

                    {/* Status Breakdown */}
                    <div className="space-y-2 mb-4">
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-700">Not Contacted:</span>
                        <span className="font-bold text-gray-900">
                          {leads.filter(l => l.source === 'Safety Batch 2' && l.status === 'Not Contacted').length}
                        </span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-700">Contacted:</span>
                        <span className="font-bold text-gray-900">
                          {leads.filter(l => l.source === 'Safety Batch 2' && l.status === 'Contacted').length}
                        </span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-700">Qualified:</span>
                        <span className="font-bold text-green-700">
                          {leads.filter(l => l.source === 'Safety Batch 2' && l.status === 'Qualified').length}
                        </span>
                      </div>
                    </div>

                    {/* Campaign Template Selector */}
                    <div className="bg-white rounded-lg p-4 border border-blue-200">
                      <label className="block text-sm font-bold text-gray-700 mb-2">Assign Campaign:</label>
                      <select className="w-full px-3 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm">
                        <option value="">Select template...</option>
                        <optgroup label="Positioning Templates">
                          <option value="moat-first">🏰 Moat-First (8-12%)</option>
                          <option value="stealth-recruiting">🥷 Stealth Recruiting (10-15%)</option>
                          <option value="source-company">🤝 Source Company (12-18%)</option>
                          <option value="linkedin">💼 LinkedIn (5-10%)</option>
                          <option value="vc-intro">📊 VC Intro (15-20%)</option>
                        </optgroup>
                        <optgroup label="Trigger-Based Templates">
                          <option value="funding-announcement">💰 Funding Announcement (20-30%)</option>
                          <option value="job-posting-monitor">📝 Job Posting Monitor (25-35%)</option>
                          <option value="warm-referral">🌟 Warm Referral (40-60%)</option>
                          <option value="multi-thread-ceo">👔 Multi-Thread CEO (15-25%)</option>
                          <option value="regulatory-trigger">⚖️ Regulatory Trigger (15-25%)</option>
                          <option value="acquisition-target">🎯 Acquisition Target (25-35%)</option>
                        </optgroup>
                      </select>
                      <button className="w-full mt-3 bg-blue-600 text-white py-2 rounded-lg font-semibold hover:bg-blue-700 transition-colors">
                        Apply to Batch 2
                      </button>
                    </div>
                  </div>
                </div>

                {/* Revenue Projection by Template */}
                <div className="mt-8 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 border-2 border-green-200">
                  <h4 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                    <span className="text-2xl">📈</span>
                    Projected Revenue by Template
                  </h4>
                  <div className="grid md:grid-cols-3 gap-4">
                    <div className="bg-white rounded-lg p-4 border border-green-200">
                      <p className="text-sm text-gray-600 mb-1">If using Positioning Templates (avg 10%)</p>
                      <p className="text-3xl font-bold text-gray-900">
                        ${Math.round(leads.length * 2000 * 0.10).toLocaleString()}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        {Math.round(leads.length * 0.10)} expected conversions
                      </p>
                    </div>
                    <div className="bg-white rounded-lg p-4 border border-green-200">
                      <p className="text-sm text-gray-600 mb-1">If using Trigger Templates (avg 25%)</p>
                      <p className="text-3xl font-bold text-green-700">
                        ${Math.round(leads.length * 2000 * 0.25).toLocaleString()}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        {Math.round(leads.length * 0.25)} expected conversions
                      </p>
                    </div>
                    <div className="bg-white rounded-lg p-4 border border-yellow-200">
                      <p className="text-sm text-gray-600 mb-1">With Warm Referrals (50%)</p>
                      <p className="text-3xl font-bold text-yellow-700">
                        ${Math.round(leads.length * 2000 * 0.50).toLocaleString()}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        {Math.round(leads.length * 0.50)} expected conversions
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Pipeline Stats by Status */}
            <div className="grid md:grid-cols-5 gap-6">
              <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl p-6 border-2 border-gray-200 shadow-lg">
                <h3 className="font-bold text-lg mb-2 text-gray-900 flex items-center gap-2">
                  <span className="text-2xl">📊</span>
                  Total Leads
                </h3>
                <p className="text-5xl font-bold text-gray-700">{leads.length}</p>
                <p className="text-sm text-gray-600 mt-1">${(leads.length * 2000).toLocaleString()} potential</p>
              </div>
              <div className="bg-gradient-to-br from-red-50 to-orange-50 rounded-2xl p-6 border-2 border-red-200 shadow-lg">
                <h3 className="font-bold text-lg mb-2 text-red-900 flex items-center gap-2">
                  <span className="text-2xl">🔴</span>
                  Not Contacted
                </h3>
                <p className="text-5xl font-bold text-red-700">
                  {leads.filter(l => l.status === 'Not Contacted').length}
                </p>
                <p className="text-sm text-red-600 mt-1">${(leads.filter(l => l.status === 'Not Contacted').length * 2000).toLocaleString()} potential</p>
              </div>
              <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-6 border-2 border-blue-200 shadow-lg">
                <h3 className="font-bold text-lg mb-2 text-blue-900 flex items-center gap-2">
                  <span className="text-2xl">🟡</span>
                  Contacted
                </h3>
                <p className="text-5xl font-bold text-blue-700">
                  {leads.filter(l => l.status === 'Contacted').length}
                </p>
                <p className="text-sm text-blue-600 mt-1">${(leads.filter(l => l.status === 'Contacted').length * 2000).toLocaleString()} potential</p>
              </div>
              <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-6 border-2 border-purple-200 shadow-lg">
                <h3 className="font-bold text-lg mb-2 text-purple-900 flex items-center gap-2">
                  <span className="text-2xl">🟢</span>
                  Qualified
                </h3>
                <p className="text-5xl font-bold text-purple-700">
                  {leads.filter(l => l.status === 'Qualified').length}
                </p>
                <p className="text-sm text-purple-600 mt-1">${(leads.filter(l => l.status === 'Qualified').length * 2000).toLocaleString()} potential</p>
              </div>
              <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-6 border-2 border-green-200 shadow-lg">
                <h3 className="font-bold text-lg mb-2 text-green-900 flex items-center gap-2">
                  <span className="text-2xl">✅</span>
                  Closed
                </h3>
                <p className="text-5xl font-bold text-green-700">
                  {leads.filter(l => l.status === 'Closed').length}
                </p>
                <p className="text-sm text-green-600 mt-1">${(leads.filter(l => l.status === 'Closed').length * 2000).toLocaleString()} revenue</p>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
