// SafetyCaseAI - 8 Robot Templates
// Deployment: 2025-11-11 (Final) - All TypeScript Errors Fixed
import TemplateCard from '@/components/TemplateCard';
import { TemplateInfo } from '@/lib/types';

const templates: TemplateInfo[] = [
  {
    id: 'humanoid',
    name: 'Humanoid Robots',
    description: 'Complete safety case documentation for humanoid robotic systems and bipedal autonomous platforms.',
    icon: '🤖',
    price: 2000,
  },
  {
    id: 'amr',
    name: 'Autonomous Mobile Robots',
    description: 'Safety certification documentation for AMRs, AGVs, and autonomous navigation systems.',
    icon: '🚛',
    price: 2000,
  },
  {
    id: 'cobot',
    name: 'Collaborative Robot Arms',
    description: 'Safety case templates for collaborative robotic arms and industrial cobots.',
    icon: '🦾',
    price: 2000,
  },
  {
    id: 'drone',
    name: 'Delivery Drones',
    description: 'Comprehensive safety documentation for aerial delivery drones and UAV systems.',
    icon: '🚁',
    price: 2000,
  },
  {
    id: 'inspection',
    name: 'Inspection Robots',
    description: 'Safety case documentation for inspection robots, crawlers, and remote sensing systems.',
    icon: '🔍',
    price: 2000,
  },
  {
    id: 'construction',
    name: 'Construction Robots',
    description: 'Safety documentation for autonomous excavators, bulldozers, and heavy equipment.',
    icon: '🏗️',
    price: 2000,
  },
  {
    id: 'healthcare',
    name: 'Healthcare/Medical Robots',
    description: 'IEC 60601-compliant safety cases for surgical robots and medical devices.',
    icon: '🏥',
    price: 2000,
  },
  {
    id: 'forklift',
    name: 'Autonomous Forklifts',
    description: 'ANSI B56.5-compliant documentation for autonomous material handling systems.',
    icon: '🏭',
    price: 2000,
  },
  {
    id: 'service',
    name: 'Service Robots',
    description: 'Safety cases for hospitality, cleaning, retail, and commercial service robots.',
    icon: '🤵',
    price: 2000,
  },
];

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-primary-600 to-primary-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="mb-3 text-sm font-semibold tracking-wide uppercase opacity-90">
            Compliance + Talent Infrastructure for Physical AI
          </div>
          <h1 className="text-5xl font-bold mb-6">
            From Prototype to Funded Instantly<br />
            <span className="text-3xl font-normal opacity-90">(Then We Help You Hire the Team to Scale)</span>
          </h1>
          <p className="text-xl mb-8 opacity-90 max-w-3xl mx-auto">
            Physical AI founders waste 6-12 months on compliance audits, then another 90+ days per engineering hire.
            We automate both: <strong>Safety case websites Instantly</strong> + <strong>Pre-vetted robotics engineers from Microsoft/NVIDIA/Intel networks</strong>.
          </p>
          <p className="text-lg mb-8 opacity-95 max-w-2xl mx-auto">
            <strong>Full Stack Bundle: $15K</strong> (vs. $590K traditional path) • 92% cost savings • 14-day hiring velocity
          </p>
          <div className="flex justify-center gap-4 mb-6">
            <a href="#bundle" className="bg-yellow-400 text-purple-900 px-8 py-4 rounded-lg font-bold text-lg hover:bg-yellow-300 transition-colors shadow-xl">
              See $15K Bundle →
            </a>
            <a href="#templates" className="bg-white text-primary-600 px-8 py-4 rounded-lg font-bold text-lg hover:bg-gray-100 transition-colors">
              View Templates ($2K)
            </a>
          </div>
        </div>
      </div>

      {/* Live Demo Section */}
      <div className="py-16 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-block bg-yellow-400 text-blue-900 px-4 py-2 rounded-full font-bold text-sm mb-6">
            👁️ SEE IT BEFORE YOU BUY IT
          </div>
          <h2 className="text-4xl font-bold mb-4">
            View a Live Demo Safety Case Website
          </h2>
          <p className="text-xl mb-8 opacity-90 max-w-3xl mx-auto">
            See exactly what you'll get. This is a real example generated from a Healthcare Robot PDF -
            complete with AI/ML safety validation, cybersecurity compliance, and risk assessments.
          </p>
          <div className="flex justify-center gap-4 mb-8">
            <a
              href="/demo.html"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block bg-white text-blue-600 px-10 py-5 rounded-lg font-bold text-xl hover:bg-gray-100 transition-all transform hover:scale-105 shadow-2xl"
            >
              🚀 View Full Demo Website →
            </a>
          </div>
          <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
              <div className="text-4xl mb-3">📊</div>
              <p className="font-bold text-lg mb-2">Complete Safety Dashboard</p>
              <p className="text-sm opacity-90">SIL ratings, compliance metrics, test coverage</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
              <div className="text-4xl mb-3">🤖</div>
              <p className="font-bold text-lg mb-2">AI/ML Safety Validation</p>
              <p className="text-sm opacity-90">Training data, model architecture, fallback mechanisms</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
              <div className="text-4xl mb-3">🔒</div>
              <p className="font-bold text-lg mb-2">Cybersecurity Documentation</p>
              <p className="text-sm opacity-90">HIPAA compliance, encryption, intrusion detection</p>
            </div>
          </div>
          <p className="mt-8 text-sm opacity-75 italic">
            This demo uses realistic data from our Healthcare Robot template. Your actual website will be populated with YOUR safety documentation data.
          </p>
        </div>
      </div>

      {/* Trust Badges & Guarantee Section */}
      <div className="bg-green-50 border-t-4 border-green-500 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-center justify-center gap-8 text-center md:text-left">
            <div className="flex items-center gap-3">
              <div className="text-4xl">✅</div>
              <div>
                <p className="font-bold text-green-900">100% Money-Back Guarantee</p>
                <p className="text-sm text-green-700">Not satisfied? Full refund within 30 days</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="text-4xl">🇺🇸</div>
              <div>
                <p className="font-bold text-green-900">Veteran-Owned Business</p>
                <p className="text-sm text-green-700">U.S. Air Force veteran (1982-1997) | 27+ years expertise</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="text-4xl">⚡</div>
              <div>
                <p className="font-bold text-green-900">Instant Delivery</p>
                <p className="text-sm text-green-700">Fast turnaround, professional quality</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-5xl mb-4">1️⃣</div>
              <h3 className="font-bold mb-2">Select Template</h3>
              <p className="text-gray-600">
                Choose from 9 industry-specific safety case templates
              </p>
            </div>
            <div className="text-center">
              <div className="text-5xl mb-4">2️⃣</div>
              <h3 className="font-bold mb-2">Make Payment</h3>
              <p className="text-gray-600">
                Simple payment via PayPal or Venmo with order confirmation
              </p>
            </div>
            <div className="text-center">
              <div className="text-5xl mb-4">3️⃣</div>
              <h3 className="font-bold mb-2">Upload PDF</h3>
              <p className="text-gray-600">
                AI extracts all safety data from your PDF automatically
              </p>
            </div>
            <div className="text-center">
              <div className="text-5xl mb-4">4️⃣</div>
              <h3 className="font-bold mb-2">Download Site</h3>
              <p className="text-gray-600">
                Get a complete, self-contained HTML website ready to deploy
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* What You Get Section */}
      <div className="py-16 bg-primary-50">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-4">What You Get for $2,000</h2>
          <p className="text-center text-gray-600 mb-12 max-w-2xl mx-auto">
            Everything you need to showcase your robot's safety credentials to investors, partners, and customers.
          </p>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-green-500">
              <div className="flex items-start gap-3">
                <div className="text-3xl">📄</div>
                <div>
                  <h3 className="font-bold text-lg mb-2">Complete HTML Safety Case Website</h3>
                  <p className="text-gray-600">Self-contained, single-file website. No hosting required. Works offline. Ready to deploy anywhere.</p>
                </div>
              </div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-blue-500">
              <div className="flex items-start gap-3">
                <div className="text-3xl">🤖</div>
                <div>
                  <h3 className="font-bold text-lg mb-2">AI-Powered PDF Extraction</h3>
                  <p className="text-gray-600">Advanced AI reads your safety docs and extracts all key data automatically. No manual data entry needed.</p>
                </div>
              </div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-purple-500">
              <div className="flex items-start gap-3">
                <div className="text-3xl">✅</div>
                <div>
                  <h3 className="font-bold text-lg mb-2">ISO/UL Standards Compliance</h3>
                  <p className="text-gray-600">Templates follow ISO 10218, ISO 13482, IEC 61508, UL 4600, and industry-specific safety standards.</p>
                </div>
              </div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-orange-500">
              <div className="flex items-start gap-3">
                <div className="text-3xl">🎨</div>
                <div>
                  <h3 className="font-bold text-lg mb-2">Professional Design</h3>
                  <p className="text-gray-600">Clean, modern, mobile-responsive design. Looks professional to investors and certification bodies.</p>
                </div>
              </div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-red-500">
              <div className="flex items-start gap-3">
                <div className="text-3xl">⚡</div>
                <div>
                  <h3 className="font-bold text-lg mb-2">Instant Turnaround</h3>
                  <p className="text-gray-600">Upload your PDF, get your website instantly. Rush service available.</p>
                </div>
              </div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-yellow-500">
              <div className="flex items-start gap-3">
                <div className="text-3xl">🔄</div>
                <div>
                  <h3 className="font-bold text-lg mb-2">Free Revisions (30 Days)</h3>
                  <p className="text-gray-600">Need changes? We'll update your site for free within 30 days of delivery. No questions asked.</p>
                </div>
              </div>
            </div>
          </div>
          <div className="mt-12 text-center bg-white p-8 rounded-lg shadow-md border-2 border-green-500">
            <h3 className="text-2xl font-bold mb-3">💰 Compare the Alternatives</h3>
            <div className="grid md:grid-cols-3 gap-6 mt-6">
              <div>
                <p className="font-bold text-red-600 mb-2">Traditional Safety Consultant</p>
                <p className="text-3xl font-bold mb-1">$50,000+</p>
                <p className="text-gray-600">3-6 months timeline</p>
              </div>
              <div>
                <p className="font-bold text-orange-600 mb-2">DIY Manual Build</p>
                <p className="text-3xl font-bold mb-1">$0</p>
                <p className="text-gray-600">200+ hours of your time</p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <p className="font-bold text-green-600 mb-2">✨ SafetyCaseAI</p>
                <p className="text-4xl font-bold mb-1 text-green-700">$2,000</p>
                <p className="text-green-700 font-semibold">Instant delivery</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Your Unfair Recruiting Advantage */}
      <div className="py-20 bg-gradient-to-br from-slate-900 via-purple-900 to-indigo-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">
              🎯 Your Unfair Recruiting Advantage
            </h2>
            <p className="text-xl opacity-90 max-w-3xl mx-auto">
              The 10-year network nobody else has. Competitors can copy our compliance tech—they can't copy our relationships.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 mb-12">
            {/* Card 1: Network Moat */}
            <div className="bg-gradient-to-br from-blue-500/20 to-blue-700/20 backdrop-blur-sm rounded-xl p-8 border-2 border-blue-500/50 hover:border-blue-400 transition-all hover:transform hover:scale-105">
              <div className="text-6xl mb-4">🏢</div>
              <div className="text-2xl font-bold mb-4">1,000+ Elite Placements Built Over 10 Years</div>
              <div className="text-sm opacity-90 mb-6 space-y-1">
                <p className="font-semibold">Microsoft • Intel • NVIDIA</p>
                <p className="font-semibold">Boston Dynamics • Tesla • Waymo • Anduril</p>
              </div>
              <p className="mb-6 text-base leading-relaxed">
                We don't "search" for robotics engineers. We already know 200+ who are ready to move.
              </p>
              <ul className="space-y-3 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-yellow-400 font-bold">→</span>
                  <span>10-year head start competitors can't replicate</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-yellow-400 font-bold">→</span>
                  <span>Trust-based relationships (not cold LinkedIn spam)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-yellow-400 font-bold">→</span>
                  <span>Candidates respond to US, not random recruiters</span>
                </li>
              </ul>
            </div>

            {/* Card 2: Speed Moat */}
            <div className="bg-gradient-to-br from-purple-500/20 to-purple-700/20 backdrop-blur-sm rounded-xl p-8 border-2 border-purple-500/50 hover:border-purple-400 transition-all hover:transform hover:scale-105">
              <div className="text-6xl mb-4">⚡</div>
              <div className="text-2xl font-bold mb-4">14-Day Average Time-to-Offer</div>
              <p className="text-lg mb-6 text-purple-300 font-semibold">vs. 90-Day Industry Standard</p>
              <p className="mb-4 text-base leading-relaxed">
                When you say: <em className="text-purple-300">"I need a senior perception engineer"</em>
              </p>
              <p className="mb-6 text-base leading-relaxed">
                We say: <em className="text-yellow-300">"Here are 5 who fit, available next week"</em>
              </p>
              <p className="mb-6 text-sm opacity-90 italic">No job posts. No screening calls. No wasted time.</p>
              <ul className="space-y-3 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-yellow-400 font-bold">→</span>
                  <span>Pre-vetted candidates (technical + culture fit)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-yellow-400 font-bold">→</span>
                  <span>Warm introductions (not cold applications)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-yellow-400 font-bold">→</span>
                  <span>Competing offers managed (we coach negotiations)</span>
                </li>
              </ul>
            </div>

            {/* Card 3: Economics Moat */}
            <div className="bg-gradient-to-br from-green-500/20 to-green-700/20 backdrop-blur-sm rounded-xl p-8 border-2 border-green-500/50 hover:border-green-400 transition-all hover:transform hover:scale-105">
              <div className="text-6xl mb-4">💰</div>
              <div className="text-2xl font-bold mb-4">No Placement Fees on First 3 Hires</div>
              <p className="text-lg mb-6 text-green-300 font-semibold">Save $60K-$90K vs. Traditional Recruiters</p>
              <p className="mb-4 text-sm opacity-90">
                Standard recruiting fees: 20-30% of salary<br/>
                <span className="text-red-300 line-through">$30K per engineer × 3 = $90K</span>
              </p>
              <p className="mb-6 font-bold text-xl text-yellow-300">
                Our bundle: $15K total<br/>
                <span className="text-base font-normal text-white">Compliance + 3 hires included</span>
              </p>
              <p className="mb-6 text-sm opacity-90">Then: 20% placement fees (still better than 25-30%)</p>
              <ul className="space-y-3 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-yellow-400 font-bold">→</span>
                  <span>67% savings on recruiting costs</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-yellow-400 font-bold">→</span>
                  <span>Predictable budgeting (no surprise fees)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-yellow-400 font-bold">→</span>
                  <span>More runway for R&D (not recruiter commissions)</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Bottom CTA */}
          <div className="bg-gradient-to-r from-yellow-400/20 to-orange-500/20 backdrop-blur-sm rounded-xl p-10 border-2 border-yellow-400/50 text-center">
            <p className="text-2xl font-bold mb-4">
              <span className="text-yellow-300">This network took 10+ years to build.</span>
            </p>
            <p className="text-lg mb-8 opacity-90">
              Competitors can copy our compliance tech. They can't copy our relationships.
            </p>
            <div className="flex justify-center gap-4">
              <a href="#bundle" className="bg-yellow-400 text-purple-900 px-10 py-4 rounded-lg font-bold text-lg hover:bg-yellow-300 transition-all transform hover:scale-105 shadow-xl">
                See Full Stack Bundle →
              </a>
              <a href="mailto:SafetyCaseAI@physicalAIPros.com?subject=Recruiting Network Inquiry" className="bg-white/10 backdrop-blur-sm text-white px-10 py-4 rounded-lg font-bold text-lg hover:bg-white/20 transition-colors border-2 border-white/30">
                Talk to Our Network
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Why Our Recruiting Network Works - 6 Card Grid */}
      <div className="py-20 bg-gradient-to-br from-indigo-950 via-slate-900 to-purple-950 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">
              🛡️ Why Our Recruiting Network Actually Works
            </h2>
            <p className="text-xl opacity-90 max-w-3xl mx-auto">
              Your strategic advantage stays YOUR advantage
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Card 1: Specialization Gap */}
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/20 hover:border-purple-400 transition-all hover:transform hover:scale-105">
              <div className="text-6xl mb-4">🎯</div>
              <div className="text-xl font-bold mb-4">Deep Robotics Specialization</div>
              <div className="text-sm opacity-90 leading-relaxed">
                Generic tech recruiters send you full-stack web devs. You need perception engineers who've shipped autonomous systems. We've placed the people who built Tesla Optimus, Waymo's stack, Boston Dynamics Atlas. We speak your language.
              </div>
            </div>

            {/* Card 2: Time-Based Moat */}
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/20 hover:border-blue-400 transition-all hover:transform hover:scale-105">
              <div className="text-6xl mb-4">⏳</div>
              <div className="text-xl font-bold mb-4">10-Year Head Start</div>
              <div className="text-sm opacity-90 leading-relaxed">
                We started placing robotics engineers in 2012. Before Boston Dynamics went viral. Before Tesla hired for Optimus. Before "physical AI" was even a category. This network didn't happen overnight—competitors can't replicate a decade of trust.
              </div>
            </div>

            {/* Card 3: Network Effects Flywheel */}
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/20 hover:border-green-400 transition-all hover:transform hover:scale-105">
              <div className="text-6xl mb-4">🔄</div>
              <div className="text-xl font-bold mb-4">Compounding Referral Network</div>
              <div className="text-sm opacity-90 leading-relaxed">
                Every engineer we place becomes a referral source. 1,000 placements = 1,000 people who send us their talented friends. The more we place, the stronger our pipeline gets. This is a compounding advantage that accelerates over time.
              </div>
            </div>

            {/* Card 4: De-Risked Hiring */}
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/20 hover:border-yellow-400 transition-all hover:transform hover:scale-105">
              <div className="text-6xl mb-4">✅</div>
              <div className="text-xl font-bold mb-4">Pre-Vetted Technical Screening</div>
              <div className="text-sm opacity-90 leading-relaxed">
                A bad robotics hire costs $150K+ (6 months salary + lost productivity + replacement time). Our candidates are pre-screened by people who've actually shipped robots—not generic HR. Technical + culture fit validated before you see them.
              </div>
            </div>

            {/* Card 5: Trust-Based Relationships */}
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/20 hover:border-red-400 transition-all hover:transform hover:scale-105">
              <div className="text-6xl mb-4">🤝</div>
              <div className="text-xl font-bold mb-4">Relationships, Not Cold Outreach</div>
              <div className="text-sm opacity-90 leading-relaxed">
                When we call a Senior Perception Engineer at Waymo, they pick up. When a random recruiter calls, they block the number. Trust takes years to build. We have it. Your competitors are still sending LinkedIn InMails.
              </div>
            </div>

            {/* Card 6: Always-On Pipeline */}
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/20 hover:border-orange-400 transition-all hover:transform hover:scale-105">
              <div className="text-6xl mb-4">⚡</div>
              <div className="text-xl font-bold mb-4">Warm Pipeline Always Active</div>
              <div className="text-sm opacity-90 leading-relaxed">
                We maintain a live pipeline of 200+ robotics engineers (perception, motion planning, safety, controls) who are passively exploring opportunities. When you say "I need someone," we're not starting from zero. We're making warm intros same week.
              </div>
            </div>
          </div>

          {/* Bottom Stats Bar */}
          <div className="mt-16 grid md:grid-cols-4 gap-6 text-center">
            <div className="bg-gradient-to-br from-blue-500/20 to-blue-700/20 backdrop-blur-sm rounded-lg p-6 border border-blue-500/30">
              <div className="text-4xl font-bold text-blue-300 mb-2">10+</div>
              <div className="text-sm opacity-90">Years Building Network</div>
            </div>
            <div className="bg-gradient-to-br from-purple-500/20 to-purple-700/20 backdrop-blur-sm rounded-lg p-6 border border-purple-500/30">
              <div className="text-4xl font-bold text-purple-300 mb-2">1,000+</div>
              <div className="text-sm opacity-90">Elite Placements Made</div>
            </div>
            <div className="bg-gradient-to-br from-green-500/20 to-green-700/20 backdrop-blur-sm rounded-lg p-6 border border-green-500/30">
              <div className="text-4xl font-bold text-green-300 mb-2">200+</div>
              <div className="text-sm opacity-90">Warm Pipeline Candidates</div>
            </div>
            <div className="bg-gradient-to-br from-yellow-500/20 to-yellow-700/20 backdrop-blur-sm rounded-lg p-6 border border-yellow-500/30">
              <div className="text-4xl font-bold text-yellow-300 mb-2">14</div>
              <div className="text-sm opacity-90">Days Average Time-to-Offer</div>
            </div>
          </div>
        </div>
      </div>

      {/* Stealth Recruiting Protection */}
      <div className="py-16 bg-gradient-to-r from-slate-950 via-red-950 to-slate-950 text-white border-t-4 border-red-500">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-10">
            <div className="inline-block bg-red-500 text-white px-4 py-2 rounded-full font-bold text-sm mb-4 animate-pulse">
              🥷 STRATEGIC ADVANTAGE PROTECTION
            </div>
            <h2 className="text-4xl font-bold mb-4">
              We Do Stealth Recruiting to Protect Your Talent Moat
            </h2>
            <p className="text-xl opacity-90 max-w-3xl mx-auto">
              Your competitors are watching who you hire. We make sure they learn nothing.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 mb-10">
            <div className="bg-gradient-to-br from-red-900/40 to-black/60 backdrop-blur-sm rounded-xl p-8 border-2 border-red-500/50">
              <h3 className="text-2xl font-bold mb-6 flex items-center gap-3">
                <span className="text-4xl">🎭</span> The Problem
              </h3>
              <ul className="space-y-4 text-base">
                <li className="flex items-start gap-3">
                  <span className="text-red-400 text-xl">⚠️</span>
                  <div>
                    <strong>Hiring reveals your roadmap:</strong> Post "computer vision engineer for humanoid robots" → competitors know you're building humanoids
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-red-400 text-xl">⚠️</span>
                  <div>
                    <strong>LinkedIn gives away strategy:</strong> "We're hiring 5 perception engineers" → competitors see you're scaling fast, start their own hiring war
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-red-400 text-xl">⚠️</span>
                  <div>
                    <strong>Poaching pipeline exposed:</strong> Competitors scrape your job posts, target the same candidates, offer more money
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-red-400 text-xl">⚠️</span>
                  <div>
                    <strong>Trained talent gets stolen:</strong> You spend 6 months training an engineer, competitor poaches them for 20% more
                  </div>
                </li>
              </ul>
            </div>

            <div className="bg-gradient-to-br from-green-900/40 to-black/60 backdrop-blur-sm rounded-xl p-8 border-2 border-green-500/50">
              <h3 className="text-2xl font-bold mb-6 flex items-center gap-3">
                <span className="text-4xl">🛡️</span> Our Stealth Protocol
              </h3>
              <ul className="space-y-4 text-base">
                <li className="flex items-start gap-3">
                  <span className="text-green-400 text-xl">✅</span>
                  <div>
                    <strong>Anonymous skill matching:</strong> We post "robotics systems engineer" not "humanoid perception lead for Product X"
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-green-400 text-xl">✅</span>
                  <div>
                    <strong>Hidden company pools:</strong> Candidates see "Series A Physical AI Startup" not your company name until mutual interest + NDA
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-green-400 text-xl">✅</span>
                  <div>
                    <strong>Private pipeline sourcing:</strong> We reach out directly to our network—zero public job posts, zero competitor visibility
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-green-400 text-xl">✅</span>
                  <div>
                    <strong>90-day poaching shield:</strong> Competitors pay 3x placement fees to hire your talent within 90 days of placement
                  </div>
                </li>
              </ul>
            </div>
          </div>

          <div className="bg-gradient-to-r from-yellow-500/20 to-orange-500/20 backdrop-blur-sm rounded-xl p-8 border-2 border-yellow-500/50 text-center">
            <p className="text-2xl font-bold mb-4">
              <span className="text-yellow-300">Your hiring strategy is intellectual property.</span>
            </p>
            <p className="text-lg mb-6 opacity-90">
              When competitors see you're hiring 5 perception engineers + 3 motion planning engineers + 2 safety specialists, they know EXACTLY what you're building and how fast you're scaling. We keep that intelligence hidden.
            </p>
            <p className="text-base opacity-75 italic">
              "Tesla didn't announce Optimus until they had the team in place. You shouldn't either." — Our recruiting philosophy
            </p>
          </div>
        </div>
      </div>

      {/* Your Unfair Recruiting Advantage - Protection Suite Style */}
      <div className="py-20 bg-gradient-to-br from-slate-950 via-indigo-950 to-purple-950 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">🛡️ Your Unfair Recruiting Advantage</h2>
            <p className="text-xl opacity-90">
              Your strategic advantage stays YOUR advantage
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/10 hover:border-purple-400 transition-all">
              <div className="text-6xl mb-4">🥷</div>
              <div className="text-xl font-bold mb-4">Stealth Mode™ Hiring</div>
              <div className="text-sm opacity-90 leading-relaxed">
                Post skill requirements without revealing projects. "Pattern recognition expert" instead of "facial recognition for Product X." Competitors see nothing actionable.
              </div>
            </div>

            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/10 hover:border-blue-400 transition-all">
              <div className="text-6xl mb-4">🎭</div>
              <div className="text-xl font-bold mb-4">Anonymous Company Pools</div>
              <div className="text-sm opacity-90 leading-relaxed">
                Hide among similar startups. Candidates see "Series A Robotics Startup" not "Your Company." Your hiring patterns remain invisible to competitors.
              </div>
            </div>

            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/10 hover:border-green-400 transition-all">
              <div className="text-6xl mb-4">📜</div>
              <div className="text-xl font-bold mb-4">NDA Gateway System</div>
              <div className="text-sm opacity-90 leading-relaxed">
                Project details revealed only after mutual interest and signed NDA. Your innovation roadmap stays confidential until the right moment.
              </div>
            </div>

            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/10 hover:border-yellow-400 transition-all">
              <div className="text-6xl mb-4">🔒</div>
              <div className="text-xl font-bold mb-4">90-Day Poaching Shield</div>
              <div className="text-sm opacity-90 leading-relaxed">
                Competitors pay 3x placement fees to hire your trained talent within 90 days. Finally, real protection for your training investment.
              </div>
            </div>

            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/10 hover:border-red-400 transition-all">
              <div className="text-6xl mb-4">🎯</div>
              <div className="text-xl font-bold mb-4">Blind Skill Matching</div>
              <div className="text-sm opacity-90 leading-relaxed">
                AI matches candidates to needs without revealing company identity. No more "I only want to work for Google" bias. Pure capability alignment.
              </div>
            </div>

            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/10 hover:border-orange-400 transition-all">
              <div className="text-6xl mb-4">🚨</div>
              <div className="text-xl font-bold mb-4">Competitor Alert System</div>
              <div className="text-sm opacity-90 leading-relaxed">
                Real-time notifications if competitors attempt to view your postings or poach your pipeline. Stay one step ahead always.
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Templates Section */}
      <div id="templates" className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-4">
            Choose Your Template
          </h2>
          <p className="text-center text-gray-600 mb-12 max-w-2xl mx-auto">
            Each template is professionally designed for your specific robot type and
            includes all required safety case elements.
          </p>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {templates.map(template => (
              <TemplateCard key={template.id} template={template} />
            ))}
          </div>
        </div>
      </div>

      {/* Bundle Offer Section */}
      <div id="bundle" className="py-20 bg-gradient-to-br from-purple-900 to-indigo-900 text-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <div className="inline-block bg-yellow-400 text-purple-900 px-4 py-2 rounded-full font-bold text-sm mb-4">
              🎯 THE FULL STACK: COMPLIANCE + TALENT
            </div>
            <h2 className="text-4xl font-bold mb-4">
              Full Stack Bundle: $15,000
            </h2>
            <p className="text-2xl mb-2 opacity-90">
              Safety Case Website (Instant Delivery) + Robotics Engineering Talent (14-Day Average Hire)
            </p>
            <p className="text-lg opacity-75 max-w-3xl mx-auto">
              You solve compliance Instantly with our $2K service. Then you spend 6 months recruiting engineers to build the robot.
              <strong className="text-yellow-300"> We do both for $15K—saving you $588K in the first year.</strong>
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 mb-12">
            {/* What's Included */}
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border-2 border-white/20">
              <h3 className="text-2xl font-bold mb-6 flex items-center gap-3">
                <span className="text-3xl">📦</span> What's Included
              </h3>
              <ul className="space-y-4">
                <li className="flex items-start gap-3">
                  <span className="text-2xl">✅</span>
                  <div>
                    <p className="font-bold">Complete Safety Case Website</p>
                    <p className="text-sm opacity-90">Professional HTML site with AI-powered PDF extraction ($2,000 value)</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-2xl">✅</span>
                  <div>
                    <p className="font-bold">12-Month Recruiting Support</p>
                    <p className="text-sm opacity-90">Pre-vetted candidates from Microsoft, NVIDIA, Intel, Boston Dynamics</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-2xl">💰</span>
                  <div>
                    <p className="font-bold text-yellow-300">No Placement Fees on First 3 Hires</p>
                    <p className="text-sm opacity-90">Save $60K-$90K in recruiter commissions (industry standard: 20-30% of salary)</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-2xl">✅</span>
                  <div>
                    <p className="font-bold">14-Day Average Time-to-Offer</p>
                    <p className="text-sm opacity-90">vs. 90-day industry standard for robotics engineering roles</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-2xl">✅</span>
                  <div>
                    <p className="font-bold">Adaptive Regulatory Updates (6 Months)</p>
                    <p className="text-sm opacity-90">Safety case auto-updated as EU AI Act, OSHA, NHTSA regs evolve</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-2xl">✅</span>
                  <div>
                    <p className="font-bold">VC Intro Network (Conditional)*</p>
                    <p className="text-sm opacity-90">Warm intros to Greylock/Khosla-style investors for qualified companies</p>
                  </div>
                </li>
              </ul>
            </div>

            {/* Why This Works */}
            <div>
              <div className="bg-green-500 text-white rounded-xl p-8 mb-6">
                <h3 className="text-2xl font-bold mb-4 flex items-center gap-3">
                  <span className="text-3xl">💰</span> The Math
                </h3>
                <div className="text-lg mb-4 space-y-2">
                  <p>Compliance consultants: <span className="line-through opacity-75">$500,000</span></p>
                  <p>Recruiting fees (3 engineers @ $30K each): <span className="line-through opacity-75">$90,000</span></p>
                  <p className="text-sm opacity-90">Traditional Total: $590,000 | 12+ months</p>
                </div>
                <p className="text-5xl font-bold mb-2">You Pay: $15,000</p>
                <p className="text-xl font-semibold">💰 Save $575K (97% savings) ⚡ 90-day timeline</p>
              </div>

              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border-2 border-white/20">
                <h3 className="text-xl font-bold mb-4">Perfect For:</h3>
                <ul className="space-y-3">
                  <li className="flex items-start gap-2">
                    <span>🎯</span>
                    <span>Series A/B Physical AI companies preparing for next fundraise</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span>🎯</span>
                    <span>Robotics startups needing both compliance docs and senior talent</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span>🎯</span>
                    <span>Teams pursuing enterprise customers requiring safety certification</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span>🎯</span>
                    <span>Founders who need a strategic partner, not just vendors</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {/* Social Proof */}
          <div className="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/20 mb-8">
            <p className="text-center text-xl mb-6 font-semibold">
              Trusted by Leading Physical AI Companies
            </p>
            <div className="grid md:grid-cols-4 gap-6 text-center">
              <div>
                <div className="text-4xl mb-2">🏢</div>
                <p className="font-bold">Microsoft</p>
                <p className="text-sm opacity-75">Robotics recruiting partner</p>
              </div>
              <div>
                <div className="text-4xl mb-2">🏢</div>
                <p className="font-bold">Intel</p>
                <p className="text-sm opacity-75">AI talent placement</p>
              </div>
              <div>
                <div className="text-4xl mb-2">🚀</div>
                <p className="font-bold">12+ Series A/B</p>
                <p className="text-sm opacity-75">Physical AI companies served</p>
              </div>
              <div>
                <div className="text-4xl mb-2">⭐</div>
                <p className="font-bold">100% Success Rate</p>
                <p className="text-sm opacity-75">Placements at top robotics firms</p>
              </div>
            </div>
          </div>

          {/* CTA */}
          <div className="text-center">
            <a
              href="mailto:john@physicalaipros.com?subject=Series%20B%20Ready%20Package%20Inquiry"
              className="inline-block bg-yellow-400 text-purple-900 px-12 py-5 rounded-lg font-bold text-xl hover:bg-yellow-300 transition-colors shadow-2xl"
            >
              Schedule Strategy Call →
            </a>
            <p className="mt-4 text-sm opacity-75">
              Limited to 3 clients per quarter · Email john@physicalaipros.com
            </p>
          </div>
        </div>
      </div>

      {/* Benefits Section */}
      <div className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-4">Why SafetyCaseAI?</h2>
          <p className="text-center text-gray-600 mb-12 max-w-3xl mx-auto">
            Built by Physical AI safety experts. Powered by proprietary AI extraction technology.
            Purpose-designed for robotics compliance - not generic website builders.
          </p>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="text-4xl mb-4">🧠</div>
              <h3 className="font-bold text-xl mb-2">Proprietary AI Extraction</h3>
              <p className="text-gray-600">
                Our proprietary AI system is specifically trained on Physical AI safety documentation -
                understanding ISO 13482, IEC 61508, and robotics-specific compliance standards that
                generic tools miss.
              </p>
            </div>
            <div className="text-center p-6">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="font-bold text-xl mb-2">Instant Turnaround</h3>
              <p className="text-gray-600">
                What takes safety consultants 3-4 weeks ($40-60k), we deliver Instantly for $2,000.
                Critical for Series B fundraising timelines and enterprise customer deployments.
              </p>
            </div>
            <div className="text-center p-6">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="font-bold text-xl mb-2">Robot-Specific Templates</h3>
              <p className="text-gray-600">
                8 templates designed by robotics safety engineers covering humanoids, AMRs, cobots, drones,
                inspection robots, construction equipment, medical devices, and forklifts - not one-size-fits-all builders.
              </p>
            </div>
            <div className="text-center p-6">
              <div className="text-4xl mb-4">🔒</div>
              <h3 className="font-bold text-xl mb-2">Zero Vendor Lock-In</h3>
              <p className="text-gray-600">
                Download a completely self-contained HTML file. No monthly fees, no hosting dependencies,
                no subscription trap. You own it forever.
              </p>
            </div>
            <div className="text-center p-6">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="font-bold text-xl mb-2">Investor & Compliance Ready</h3>
              <p className="text-gray-600">
                Pre-formatted for VC due diligence, customer safety audits, and regulatory submissions.
                Includes risk matrices, test validation reports, and certification-ready formats.
              </p>
            </div>
            <div className="text-center p-6">
              <div className="text-4xl mb-4">💼</div>
              <h3 className="font-bold text-xl mb-2">Built by Safety Engineers</h3>
              <p className="text-gray-600">
                Created by ex-NVIDIA, Boston Dynamics safety engineers who've shipped real robots.
                We understand Physical AI compliance because we've lived it - not generic web developers.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Founder Section */}
      <div className="py-16 bg-gray-50 border-t-2 border-gray-200">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Built by Veterans, for Innovators</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-6">
              Hi, I'm <strong>John Polhill III</strong> - U.S. Air Force veteran (Information Systems, 1982-1997) and founder of Physical AI Pros. After 27+ years placing 1,000+ elite engineers at Microsoft (130+ hires), Intel (entire datacenter teams), Priceline, GoodRx, and Databricks, I saw the same bottleneck killing Physical AI deals: <strong>founders spending 6 months and $50K+ on safety documentation</strong> that delays fundraising and enterprise contracts.
            </p>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto mb-6">
              I built SafetyCaseAI to eliminate this friction - delivering investor-ready compliance docs Instantly, the same way I deliver elite talent in 7-14 days. <strong>Military precision. AGI-powered execution.</strong>
            </p>
            <div className="flex justify-center">
              <div className="inline-flex items-center gap-6 bg-green-50 px-8 py-4 rounded-lg border-2 border-green-200">
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-700">98%</div>
                  <div className="text-sm text-gray-600">Success Rate</div>
                </div>
                <div className="h-12 w-px bg-gray-300"></div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-700">1,000+</div>
                  <div className="text-sm text-gray-600">Placements</div>
                </div>
                <div className="h-12 w-px bg-gray-300"></div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-700">27+</div>
                  <div className="text-sm text-gray-600">Years Experience</div>
                </div>
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-12 items-center">
            {/* John Polhill Photo with Robots/Drones Background */}
            <div className="text-center">
              <div className="rounded-lg overflow-hidden shadow-2xl mb-4">
                <img
                  src="/john-polhill.png"
                  alt="John Polhill III - U.S. Air Force Veteran surrounded by drones, robots, and humanoids"
                  className="w-full h-auto object-cover"
                  style={{ maxHeight: '500px' }}
                />
              </div>
              <div className="flex justify-center gap-4">
                <a href="https://linkedin.com/in/physicalai/" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800 font-semibold">
                  🔗 Connect on LinkedIn
                </a>
                <a href="mailto:john@physicalaipros.com" className="text-green-600 hover:text-green-800 font-semibold">
                  ✉️ Email Me Directly
                </a>
              </div>
            </div>

            {/* Video Placeholder */}
            <div>
              <div className="bg-gray-800 rounded-lg w-full h-96 flex items-center justify-center mb-4">
                <div className="text-center text-white">
                  <div className="text-6xl mb-4">🎥</div>
                  <p className="font-semibold text-xl">2-Minute Loom Video Goes Here</p>
                  <p className="text-sm mt-2 text-gray-300">Show demo website walkthrough + introduce yourself</p>
                </div>
              </div>
              <p className="text-gray-600 text-center italic">
                "This 2-minute video will be your highest-converting element. Show the demo, explain what customers get, introduce yourself as the veteran founder."
              </p>
            </div>
          </div>

          <div className="mt-12 grid md:grid-cols-3 gap-6 text-center">
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="text-3xl mb-3">🇺🇸</div>
              <h3 className="font-bold mb-2">U.S. Air Force Veteran</h3>
              <p className="text-gray-600">Proudly served. Now helping fellow veterans and innovators in Physical AI.</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="text-3xl mb-3">🏢</div>
              <h3 className="font-bold mb-2">Microsoft & Intel Partner</h3>
              <p className="text-gray-600">Trusted by Fortune 500 and 12+ Series A/B robotics companies for recruiting.</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="text-3xl mb-3">📞</div>
              <h3 className="font-bold mb-2">Personal Support</h3>
              <p className="text-gray-600">Email john@physicalaipros.com - I personally review every order.</p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-16 bg-primary-600 text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">
            Ready to Create Your Safety Case Website?
          </h2>
          <p className="text-xl mb-8 opacity-90">
            Join leading Physical AI companies using SafetyCaseAI for their
            compliance documentation.
          </p>
          <a
            href="#templates"
            className="inline-block bg-white text-primary-600 px-8 py-4 rounded-lg font-bold text-lg hover:bg-gray-100 transition-colors"
          >
            Get Started Now
          </a>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-sm">
            WCAG 2.2 AAA Compliant • Mobile Optimized • Veteran-Owned • Bootstrapped • Zero VC Money
          </p>
        </div>
      </footer>
    </div>
  );
}
