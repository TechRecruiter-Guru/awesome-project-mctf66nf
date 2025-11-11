// SafetyCase.AI - 8 Robot Templates
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

      {/* Features Section */}
      <div className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-5xl mb-4">1️⃣</div>
              <h3 className="font-bold mb-2">Select Template</h3>
              <p className="text-gray-600">
                Choose from 8 industry-specific safety case templates
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
