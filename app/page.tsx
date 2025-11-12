// SafetyCase.AI - 8 Robot Templates
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
            Powered by Anthropic Claude AI
          </div>
          <h1 className="text-5xl font-bold mb-6">
            Professional Safety Case Websites in 48 Hours
          </h1>
          <p className="text-xl mb-8 opacity-90 max-w-3xl mx-auto">
            Purpose-built AI extraction for Physical AI companies. Our proprietary Claude-powered
            system transforms your safety documentation into investor-ready, compliance-certified
            websites—without consultants or weeks of manual work.
          </p>
          <div className="flex justify-center gap-4 mb-6">
            <a href="#templates" className="bg-white text-primary-600 px-8 py-4 rounded-lg font-bold text-lg hover:bg-gray-100 transition-colors">
              View Templates
            </a>
            <a href="/upload" className="bg-primary-700 text-white px-8 py-4 rounded-lg font-bold text-lg hover:bg-primary-800 transition-colors border-2 border-white">
              Already Have Code?
            </a>
          </div>
          <div className="mt-4">
            <a
              href="https://vanguardlab.physicalaipros.com/safetyaiV2.html"
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-white opacity-75 hover:opacity-100 underline transition-opacity"
            >
              Need more information on why safety case documentation matters? →
            </a>
          </div>
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
                <p className="text-sm text-green-700">U.S. Army veteran with 10+ years robotics experience</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="text-4xl">⚡</div>
              <div>
                <p className="font-bold text-green-900">48-Hour Delivery</p>
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
                  <p className="text-gray-600">Claude AI reads your safety docs and extracts all key data automatically. No manual data entry needed.</p>
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
                  <h3 className="font-bold text-lg mb-2">48-Hour Turnaround</h3>
                  <p className="text-gray-600">Upload your PDF, get your website within 2 business days. Rush service available.</p>
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
                <p className="font-bold text-green-600 mb-2">✨ SafetyCase.AI</p>
                <p className="text-4xl font-bold mb-1 text-green-700">$2,000</p>
                <p className="text-green-700 font-semibold">48 hours delivery</p>
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
      <div className="py-20 bg-gradient-to-br from-purple-900 to-indigo-900 text-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <div className="inline-block bg-yellow-400 text-purple-900 px-4 py-2 rounded-full font-bold text-sm mb-4">
              ⭐ EXCLUSIVE BUNDLE FOR FUNDED STARTUPS
            </div>
            <h2 className="text-4xl font-bold mb-4">
              Series B Ready Package: $15,000
            </h2>
            <p className="text-2xl mb-2 opacity-90">
              Safety Documentation + Senior Robotics Recruiting
            </p>
            <p className="text-lg opacity-75 max-w-3xl mx-auto">
              Most Physical AI companies spend 6 months and $75K+ getting safety docs done AND hiring senior robotics talent. We deliver both in 60 days for $15K.
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
                    <p className="font-bold">60-Day Priority Recruiting Engagement</p>
                    <p className="text-sm opacity-90">Dedicated search for 1 senior robotics engineer role ($25,000+ value)</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-2xl">✅</span>
                  <div>
                    <p className="font-bold">Access to Exclusive Physical AI Talent Network</p>
                    <p className="text-sm opacity-90">Engineers from Boston Dynamics, NVIDIA, Tesla, Aurora, Waymo</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-2xl">✅</span>
                  <div>
                    <p className="font-bold">Investor-Ready Compliance Package</p>
                    <p className="text-sm opacity-90">Safety docs formatted for Series B due diligence</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-2xl">✅</span>
                  <div>
                    <p className="font-bold">Strategic Hiring Consultation</p>
                    <p className="text-sm opacity-90">Comp benchmarking, org design, and role scoping</p>
                  </div>
                </li>
              </ul>
            </div>

            {/* Why This Works */}
            <div>
              <div className="bg-green-500 text-white rounded-xl p-8 mb-6">
                <h3 className="text-2xl font-bold mb-4 flex items-center gap-3">
                  <span className="text-3xl">💰</span> Total Value: $27,000+
                </h3>
                <p className="text-5xl font-bold mb-2">You Pay: $15,000</p>
                <p className="text-xl font-semibold">Save $12,000+ (44% savings)</p>
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
          <h2 className="text-3xl font-bold text-center mb-4">Why SafetyCase.AI?</h2>
          <p className="text-center text-gray-600 mb-12 max-w-3xl mx-auto">
            Built by Physical AI safety experts. Powered by Anthropic's Claude AI.
            Purpose-designed for robotics compliance—not generic website builders.
          </p>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="text-4xl mb-4">🧠</div>
              <h3 className="font-bold text-xl mb-2">Proprietary AI Extraction</h3>
              <p className="text-gray-600">
                Our Claude-powered system is specifically trained on Physical AI safety documentation—
                understanding ISO 13482, IEC 61508, and robotics-specific compliance standards that
                generic tools miss.
              </p>
            </div>
            <div className="text-center p-6">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="font-bold text-xl mb-2">48-Hour Turnaround</h3>
              <p className="text-gray-600">
                What takes safety consultants 3-4 weeks ($40-60k), we deliver in 48 hours for $2,000.
                Critical for Series B fundraising timelines and enterprise customer deployments.
              </p>
            </div>
            <div className="text-center p-6">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="font-bold text-xl mb-2">Robot-Specific Templates</h3>
              <p className="text-gray-600">
                8 templates designed by robotics safety engineers covering humanoids, AMRs, cobots, drones,
                inspection robots, construction equipment, medical devices, and forklifts—not one-size-fits-all builders.
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
                We understand Physical AI compliance because we've lived it—not generic web developers.
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
              I built SafetyCase.AI to eliminate this friction—delivering investor-ready compliance docs in 48 hours, the same way I deliver elite talent in 7-14 days. <strong>Military precision. AGI-powered execution.</strong>
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
            {/* Photo Placeholder */}
            <div className="text-center">
              <div className="bg-gray-300 rounded-lg w-full h-96 flex items-center justify-center mb-4">
                <div className="text-center text-gray-600">
                  <div className="text-6xl mb-4">📸</div>
                  <p className="font-semibold">Your Professional Photo Here</p>
                  <p className="text-sm">(Business casual or with robots)</p>
                </div>
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
            Join leading Physical AI companies using SafetyCase.AI for their
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
