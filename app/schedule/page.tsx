'use client';

import { useState } from 'react';

interface FormData {
  // Contact Information
  fullName: string;
  email: string;
  phone: string;
  companyName: string;
  companyWebsite: string;
  role: string;

  // Recruiting Needs
  hiringRoles: string[];
  numberOfHires: string;
  hiringUrgency: string;

  // Compliance Needs
  complianceStatus: string;
  regulatoryFrameworks: string[];

  // Business Context
  fundingStage: string;
  currentChallenges: string[];
  timeline: string;

  // Additional Info
  additionalNotes: string;
}

const HIRING_ROLES = [
  { id: 'robotics-engineer', label: 'Robotics Engineer', icon: '🤖' },
  { id: 'perception-engineer', label: 'Perception Engineer', icon: '👁️' },
  { id: 'controls-engineer', label: 'Controls Engineer', icon: '🎮' },
  { id: 'ml-engineer', label: 'ML/AI Engineer', icon: '🧠' },
  { id: 'systems-engineer', label: 'Systems Engineer', icon: '⚙️' },
  { id: 'embedded-engineer', label: 'Embedded Engineer', icon: '💾' },
  { id: 'hardware-engineer', label: 'Hardware Engineer', icon: '🔧' },
  { id: 'cto', label: 'CTO / VP Engineering', icon: '👔' },
];

const CHALLENGES = [
  { id: 'slow-hiring', label: '90+ day hiring cycles', icon: '⏰' },
  { id: 'expensive-fees', label: 'High placement fees (20-30%)', icon: '💸' },
  { id: 'compliance-stuck', label: 'Stuck on safety documentation', icon: '📋' },
  { id: 'roadmap-exposure', label: 'Hiring reveals our roadmap', icon: '🔍' },
  { id: 'candidate-quality', label: "Can't find senior talent", icon: '🎯' },
  { id: 'investor-pressure', label: 'Investor milestones at risk', icon: '📊' },
];

const REGULATORY_FRAMEWORKS = [
  { id: 'iso-13482', label: 'ISO 13482 (Service Robots)' },
  { id: 'iec-61508', label: 'IEC 61508 (Functional Safety)' },
  { id: 'ul-3300', label: 'UL 3300 (Autonomous Products)' },
  { id: 'eu-ai-act', label: 'EU AI Act' },
  { id: 'fda', label: 'FDA (Medical Devices)' },
  { id: 'iso-26262', label: 'ISO 26262 (Automotive)' },
];

export default function SchedulePage() {
  const [formData, setFormData] = useState<FormData>({
    fullName: '',
    email: '',
    phone: '',
    companyName: '',
    companyWebsite: '',
    role: '',
    hiringRoles: [],
    numberOfHires: '',
    hiringUrgency: '',
    complianceStatus: '',
    regulatoryFrameworks: [],
    fundingStage: '',
    currentChallenges: [],
    timeline: '',
    additionalNotes: '',
  });

  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');

  const toggleArrayField = (field: keyof FormData, value: string) => {
    const currentArray = formData[field] as string[];
    if (currentArray.includes(value)) {
      setFormData({ ...formData, [field]: currentArray.filter(v => v !== value) });
    } else {
      setFormData({ ...formData, [field]: [...currentArray, value] });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');

    try {
      // Use PHP endpoint if configured, otherwise use Next.js API
      const endpoint = process.env.NEXT_PUBLIC_FORM_ENDPOINT || '/api/schedule';

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        setSubmitted(true);
      } else {
        setError(data.message || 'Failed to submit form. Please try again.');
      }
    } catch (err) {
      setError('Network error. Please try again or email jp@physicalaipros.com directly.');
    } finally {
      setSubmitting(false);
    }
  };

  if (submitted) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50 px-4">
        <div className="max-w-2xl w-full bg-white rounded-3xl shadow-2xl p-12 text-center border border-gray-200">
          <div className="w-24 h-24 bg-gradient-to-br from-green-500 to-emerald-500 rounded-full mx-auto mb-6 flex items-center justify-center">
            <span className="text-5xl">✅</span>
          </div>
          <h1 className="text-4xl font-bold mb-4 text-gray-900">Strategy Call Requested!</h1>
          <p className="text-xl text-gray-700 mb-6">
            Thanks for reaching out, <strong>{formData.fullName}</strong>!
          </p>
          <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl p-6 mb-6 border border-purple-200">
            <p className="text-lg text-gray-800 mb-2">
              <strong>John Polhill III</strong> will personally review your information and reach out within <strong>24 hours</strong>.
            </p>
            <p className="text-gray-700">
              We'll send a calendar invite to: <strong className="text-purple-700">{formData.email}</strong>
            </p>
          </div>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="/"
              className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-8 py-4 rounded-lg font-bold text-lg hover:from-purple-700 hover:to-blue-700 transition-all shadow-lg hover:shadow-xl"
            >
              Back to Home
            </a>
            <a
              href="mailto:jp@physicalaipros.com"
              className="bg-white border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-lg font-bold text-lg hover:bg-gray-50 transition-all shadow-md"
            >
              Email Directly
            </a>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50 py-12 px-4">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <a href="/" className="inline-block mb-6 text-purple-600 hover:text-purple-800 font-semibold transition-colors">
            ← Back to SafetyCaseAI
          </a>
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-purple-700 to-blue-600 bg-clip-text text-transparent">
            Schedule Your Strategy Call
          </h1>
          <p className="text-xl text-gray-700 max-w-3xl mx-auto">
            Let's discuss how SafetyCaseAI can compress your compliance + hiring timeline from <strong>12 months to 90 days</strong> and save <strong>$575K+</strong> in the process.
          </p>
          <div className="flex items-center justify-center gap-6 mt-6 text-gray-600">
            <span className="flex items-center gap-2">
              <span className="text-2xl">⏱️</span>
              <span className="font-semibold">30-minute call</span>
            </span>
            <span className="flex items-center gap-2">
              <span className="text-2xl">📞</span>
              <span className="font-semibold">No pitch, just insights</span>
            </span>
            <span className="flex items-center gap-2">
              <span className="text-2xl">🎯</span>
              <span className="font-semibold">Custom roadmap</span>
            </span>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="bg-white rounded-3xl shadow-2xl p-8 sm:p-12 border border-gray-200">
          {/* Contact Information */}
          <div className="mb-10">
            <h2 className="text-2xl font-bold mb-6 text-gray-900 flex items-center gap-3">
              <span className="bg-gradient-to-br from-purple-500 to-blue-500 text-white w-10 h-10 rounded-lg flex items-center justify-center text-lg font-bold">1</span>
              Contact Information
            </h2>
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">Full Name *</label>
                <input
                  type="text"
                  required
                  value={formData.fullName}
                  onChange={e => setFormData({ ...formData, fullName: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                  placeholder="John Smith"
                />
              </div>
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">Work Email *</label>
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={e => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                  placeholder="john@company.com"
                />
              </div>
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">Phone Number *</label>
                <input
                  type="tel"
                  required
                  value={formData.phone}
                  onChange={e => setFormData({ ...formData, phone: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                  placeholder="+1 (555) 123-4567"
                />
              </div>
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">Your Role *</label>
                <input
                  type="text"
                  required
                  value={formData.role}
                  onChange={e => setFormData({ ...formData, role: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                  placeholder="CTO, CEO, VP Engineering, etc."
                />
              </div>
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">Company Name *</label>
                <input
                  type="text"
                  required
                  value={formData.companyName}
                  onChange={e => setFormData({ ...formData, companyName: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                  placeholder="Acme Robotics"
                />
              </div>
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">Company Website</label>
                <input
                  type="url"
                  value={formData.companyWebsite}
                  onChange={e => setFormData({ ...formData, companyWebsite: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                  placeholder="https://acmerobotics.com"
                />
              </div>
            </div>
          </div>

          {/* Recruiting Needs */}
          <div className="mb-10 pb-10 border-b border-gray-200">
            <h2 className="text-2xl font-bold mb-6 text-gray-900 flex items-center gap-3">
              <span className="bg-gradient-to-br from-purple-500 to-blue-500 text-white w-10 h-10 rounded-lg flex items-center justify-center text-lg font-bold">2</span>
              Recruiting Needs
            </h2>

            <div className="mb-6">
              <label className="block text-sm font-bold text-gray-700 mb-3">Which roles are you hiring for? (Select all that apply)</label>
              <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-3">
                {HIRING_ROLES.map(role => (
                  <button
                    key={role.id}
                    type="button"
                    onClick={() => toggleArrayField('hiringRoles', role.id)}
                    className={`p-4 rounded-xl border-2 transition-all text-left ${
                      formData.hiringRoles.includes(role.id)
                        ? 'border-purple-500 bg-purple-50 shadow-md'
                        : 'border-gray-300 hover:border-purple-300 hover:bg-gray-50'
                    }`}
                  >
                    <span className="text-2xl block mb-1">{role.icon}</span>
                    <span className="text-sm font-semibold text-gray-900">{role.label}</span>
                  </button>
                ))}
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">How many hires in next 12 months? *</label>
                <select
                  required
                  value={formData.numberOfHires}
                  onChange={e => setFormData({ ...formData, numberOfHires: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all bg-white"
                >
                  <option value="">Select number...</option>
                  <option value="1-3">1-3 hires</option>
                  <option value="4-6">4-6 hires</option>
                  <option value="7-10">7-10 hires</option>
                  <option value="10+">10+ hires</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">How urgent is your first hire? *</label>
                <select
                  required
                  value={formData.hiringUrgency}
                  onChange={e => setFormData({ ...formData, hiringUrgency: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all bg-white"
                >
                  <option value="">Select timeline...</option>
                  <option value="immediate">Immediate (hiring now)</option>
                  <option value="30-days">Within 30 days</option>
                  <option value="60-days">Within 60 days</option>
                  <option value="90-days">Within 90 days</option>
                  <option value="planning">Just planning ahead</option>
                </select>
              </div>
            </div>
          </div>

          {/* Compliance Needs */}
          <div className="mb-10 pb-10 border-b border-gray-200">
            <h2 className="text-2xl font-bold mb-6 text-gray-900 flex items-center gap-3">
              <span className="bg-gradient-to-br from-purple-500 to-blue-500 text-white w-10 h-10 rounded-lg flex items-center justify-center text-lg font-bold">3</span>
              Compliance Needs
            </h2>

            <div className="mb-6">
              <label className="block text-sm font-bold text-gray-700 mb-2">Current compliance documentation status? *</label>
              <select
                required
                value={formData.complianceStatus}
                onChange={e => setFormData({ ...formData, complianceStatus: e.target.value })}
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all bg-white"
              >
                <option value="">Select status...</option>
                <option value="no-docs">No documentation yet (starting from scratch)</option>
                <option value="internal-docs">Have internal docs but not structured for regulators</option>
                <option value="consultant">Working with consultant (slow/expensive)</option>
                <option value="compliant">Already compliant (need updates/maintenance)</option>
                <option value="not-needed">Don't need compliance docs yet</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">Which regulatory frameworks apply? (Select all)</label>
              <div className="grid sm:grid-cols-2 gap-3">
                {REGULATORY_FRAMEWORKS.map(framework => (
                  <label
                    key={framework.id}
                    className={`flex items-center p-4 rounded-lg border-2 cursor-pointer transition-all ${
                      formData.regulatoryFrameworks.includes(framework.id)
                        ? 'border-purple-500 bg-purple-50'
                        : 'border-gray-300 hover:border-purple-300 hover:bg-gray-50'
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={formData.regulatoryFrameworks.includes(framework.id)}
                      onChange={() => toggleArrayField('regulatoryFrameworks', framework.id)}
                      className="w-5 h-5 text-purple-600 rounded focus:ring-purple-500 mr-3"
                    />
                    <span className="text-sm font-semibold text-gray-900">{framework.label}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>

          {/* Current Challenges */}
          <div className="mb-10 pb-10 border-b border-gray-200">
            <h2 className="text-2xl font-bold mb-6 text-gray-900 flex items-center gap-3">
              <span className="bg-gradient-to-br from-purple-500 to-blue-500 text-white w-10 h-10 rounded-lg flex items-center justify-center text-lg font-bold">4</span>
              Current Challenges
            </h2>

            <label className="block text-sm font-bold text-gray-700 mb-3">What's blocking your team? (Select all that apply)</label>
            <div className="grid sm:grid-cols-2 gap-3">
              {CHALLENGES.map(challenge => (
                <button
                  key={challenge.id}
                  type="button"
                  onClick={() => toggleArrayField('currentChallenges', challenge.id)}
                  className={`p-4 rounded-xl border-2 transition-all text-left flex items-center gap-3 ${
                    formData.currentChallenges.includes(challenge.id)
                      ? 'border-red-500 bg-red-50 shadow-md'
                      : 'border-gray-300 hover:border-red-300 hover:bg-gray-50'
                  }`}
                >
                  <span className="text-2xl">{challenge.icon}</span>
                  <span className="text-sm font-semibold text-gray-900">{challenge.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Business Context */}
          <div className="mb-10 pb-10 border-b border-gray-200">
            <h2 className="text-2xl font-bold mb-6 text-gray-900 flex items-center gap-3">
              <span className="bg-gradient-to-br from-purple-500 to-blue-500 text-white w-10 h-10 rounded-lg flex items-center justify-center text-lg font-bold">5</span>
              Business Context
            </h2>

            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">Funding Stage *</label>
                <select
                  required
                  value={formData.fundingStage}
                  onChange={e => setFormData({ ...formData, fundingStage: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all bg-white"
                >
                  <option value="">Select stage...</option>
                  <option value="pre-seed">Pre-seed / Bootstrapped</option>
                  <option value="seed">Seed</option>
                  <option value="series-a">Series A</option>
                  <option value="series-b">Series B</option>
                  <option value="series-c+">Series C+</option>
                  <option value="established">Established / Profitable</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">Ideal timeline to start? *</label>
                <select
                  required
                  value={formData.timeline}
                  onChange={e => setFormData({ ...formData, timeline: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all bg-white"
                >
                  <option value="">Select timeline...</option>
                  <option value="this-week">This week</option>
                  <option value="this-month">This month</option>
                  <option value="next-month">Next month</option>
                  <option value="this-quarter">This quarter</option>
                  <option value="exploring">Just exploring options</option>
                </select>
              </div>
            </div>
          </div>

          {/* Additional Notes */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold mb-6 text-gray-900 flex items-center gap-3">
              <span className="bg-gradient-to-br from-purple-500 to-blue-500 text-white w-10 h-10 rounded-lg flex items-center justify-center text-lg font-bold">6</span>
              Additional Information
            </h2>
            <label className="block text-sm font-bold text-gray-700 mb-2">Anything else we should know?</label>
            <textarea
              value={formData.additionalNotes}
              onChange={e => setFormData({ ...formData, additionalNotes: e.target.value })}
              rows={4}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all resize-none"
              placeholder="E.g., specific compliance deadlines, investor requirements, unique hiring challenges..."
            />
          </div>

          {error && (
            <div className="mb-6 bg-red-50 border-2 border-red-300 rounded-lg p-4">
              <p className="text-red-700 font-semibold">{error}</p>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={submitting}
            className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white px-8 py-5 rounded-xl text-xl font-bold hover:from-purple-700 hover:to-blue-700 transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {submitting ? (
              <span className="flex items-center justify-center gap-3">
                <svg className="animate-spin h-6 w-6" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Submitting...
              </span>
            ) : (
              <span>Schedule My Strategy Call 🚀</span>
            )}
          </button>

          <p className="text-center text-sm text-gray-600 mt-4">
            By submitting, you agree to be contacted by SafetyCaseAI. We respect your privacy and won't spam you.
          </p>
        </form>

        {/* Trust Indicators */}
        <div className="mt-12 text-center">
          <div className="flex flex-wrap justify-center items-center gap-8 text-gray-600">
            <div className="flex items-center gap-2">
              <span className="text-2xl">✅</span>
              <span className="font-semibold">No sales pitch</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-2xl">🔒</span>
              <span className="font-semibold">Your info is confidential</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-2xl">⚡</span>
              <span className="font-semibold">24-hour response</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
