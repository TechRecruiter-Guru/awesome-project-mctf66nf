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
];

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-primary-600 to-primary-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl font-bold mb-6">
            Professional Safety Case Websites
          </h1>
          <p className="text-xl mb-8 opacity-90 max-w-3xl mx-auto">
            Automate your safety case website creation with AI-powered data extraction
            and industry-specific templates. Get a production-ready website in minutes,
            not weeks.
          </p>
          <div className="flex justify-center gap-4">
            <a href="#templates" className="bg-white text-primary-600 px-8 py-4 rounded-lg font-bold text-lg hover:bg-gray-100 transition-colors">
              View Templates
            </a>
            <a href="/upload" className="bg-primary-700 text-white px-8 py-4 rounded-lg font-bold text-lg hover:bg-primary-800 transition-colors border-2 border-white">
              Already Have Code?
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
                Choose from 5 industry-specific safety case templates
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
          <h2 className="text-3xl font-bold text-center mb-12">Why SafetyCase.AI?</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="font-bold text-xl mb-2">Fast & Automated</h3>
              <p className="text-gray-600">
                AI-powered extraction means your safety case website is ready in
                minutes, not days or weeks.
              </p>
            </div>
            <div className="text-center p-6">
              <div className="text-4xl mb-4">💰</div>
              <h3 className="font-bold text-xl mb-2">Fixed Pricing</h3>
              <p className="text-gray-600">
                One-time payment of $2,000. No subscriptions, no hidden fees, no
                ongoing costs.
              </p>
            </div>
            <div className="text-center p-6">
              <div className="text-4xl mb-4">🎨</div>
              <h3 className="font-bold text-xl mb-2">Professional Design</h3>
              <p className="text-gray-600">
                Industry-specific templates designed by safety experts with modern,
                responsive layouts.
              </p>
            </div>
            <div className="text-center p-6">
              <div className="text-4xl mb-4">✏️</div>
              <h3 className="font-bold text-xl mb-2">Fully Editable</h3>
              <p className="text-gray-600">
                Review and edit all extracted data before downloading. Complete
                control over your content.
              </p>
            </div>
            <div className="text-center p-6">
              <div className="text-4xl mb-4">📦</div>
              <h3 className="font-bold text-xl mb-2">Self-Contained</h3>
              <p className="text-gray-600">
                Download a single HTML file with no dependencies. Upload anywhere or
                share directly.
              </p>
            </div>
            <div className="text-center p-6">
              <div className="text-4xl mb-4">🔒</div>
              <h3 className="font-bold text-xl mb-2">No Lock-In</h3>
              <p className="text-gray-600">
                Own your website outright. No hosting required, no vendor lock-in, no
                recurring fees.
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
    </div>
  );
}
