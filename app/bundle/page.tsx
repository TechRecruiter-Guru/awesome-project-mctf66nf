export default function BundlePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-indigo-900 to-blue-900 text-white">
      {/* Hero */}
      <div className="py-20">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-block bg-yellow-400 text-purple-900 px-4 py-2 rounded-full font-bold text-sm mb-6">
            🎯 THE FULL STACK: COMPLIANCE + TALENT
          </div>
          <h1 className="text-6xl font-bold mb-6">
            From Prototype to Funded<br />to Fully Staffed
          </h1>
          <p className="text-2xl mb-8 opacity-90 max-w-4xl mx-auto">
            Most robotics founders spend <strong className="text-yellow-300">$590K and 12+ months</strong> on compliance consultants + recruiting fees.<br />
            We deliver both for <strong className="text-yellow-300">$15K in 90 days</strong>.
          </p>
          <div className="flex justify-center gap-4">
            <a href="#pricing" className="bg-yellow-400 text-purple-900 px-10 py-5 rounded-lg font-bold text-xl hover:bg-yellow-300 transition-all transform hover:scale-105 shadow-2xl">
              See Pricing & What's Included
            </a>
            <a href="/#templates" className="bg-white/10 backdrop-blur-sm text-white px-10 py-5 rounded-lg font-bold text-xl hover:bg-white/20 transition-colors border-2 border-white/30">
              Just Need Compliance ($2K)
            </a>
          </div>
        </div>
      </div>

      {/* The Problem */}
      <div className="py-16 bg-red-900/30 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-center mb-12">💸 The $590K Compliance + Talent Tax</h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border-2 border-red-500/50">
              <h3 className="text-2xl font-bold mb-4 flex items-center gap-3">
                <span className="text-4xl">⚠️</span> Bottleneck #1: Compliance
              </h3>
              <ul className="space-y-3">
                <li className="flex items-start gap-2">
                  <span>❌</span>
                  <span><strong>$500K consultant fees</strong> for a single ISO 13482 safety case</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>❌</span>
                  <span><strong>6-12 month timeline</strong> that burns 30% of runway</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>❌</span>
                  <span><strong>Fragmented regulations:</strong> NHTSA (AVs), FAA (drones), OSHA (cobots), EU AI Act</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>❌</span>
                  <span><strong>"Checkbox compliance"</strong> that fails Series A due diligence</span>
                </li>
              </ul>
            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border-2 border-orange-500/50">
              <h3 className="text-2xl font-bold mb-4 flex items-center gap-3">
                <span className="text-4xl">⚠️</span> Bottleneck #2: Hiring
              </h3>
              <ul className="space-y-3">
                <li className="flex items-start gap-2">
                  <span>❌</span>
                  <span><strong>90+ days to hire</strong> each robotics engineer (if you're lucky)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>❌</span>
                  <span><strong>$30K per placement</strong> in recruiter fees (20-30% of first-year salary)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>❌</span>
                  <span><strong>3-5 engineers needed</strong> for Series A milestones = <strong>$90K+ in recruiting costs</strong></span>
                </li>
                <li className="flex items-start gap-2">
                  <span>❌</span>
                  <span><strong>Wrong hires are expensive:</strong> Robotics talent is specialized—generic tech recruiters miss the mark</span>
                </li>
              </ul>
            </div>
          </div>

          <div className="mt-12 bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/20 text-center">
            <p className="text-3xl font-bold mb-4">Total Traditional Cost: $590,000</p>
            <p className="text-xl opacity-90">Timeline: 12-18 months (if nothing goes wrong)</p>
            <p className="text-lg opacity-75 mt-4">Meanwhile, your competitors are shipping. Market windows are closing. Runway is evaporating.</p>
          </div>
        </div>
      </div>

      {/* The Solution */}
      <div className="py-16 bg-green-900/30 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-center mb-12">⚡ The Full Stack Solution</h2>

          <div className="grid md:grid-cols-2 gap-8 mb-12">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border-2 border-green-500/50">
              <h3 className="text-2xl font-bold mb-4 flex items-center gap-3">
                <span className="text-4xl">📄</span> Compliance Infrastructure
              </h3>
              <p className="mb-6 text-lg opacity-90">Instant GSN-validated safety case website</p>
              <ul className="space-y-3">
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span><strong>Automated extraction:</strong> AI reads your design docs, test logs, FMEA</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span><strong>ISO 13482/61508 compliance:</strong> Not checkbox templates—actual regulatory rigor</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span><strong>GSN validation:</strong> Goal Structuring Notation (what M&A buyers require)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span><strong>Adaptive updates (6 months):</strong> Stays current as regs evolve</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span><strong>Live investor-ready website:</strong> Not PDFs in Dropbox</span>
                </li>
              </ul>
            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border-2 border-blue-500/50">
              <h3 className="text-2xl font-bold mb-4 flex items-center gap-3">
                <span className="text-4xl">👥</span> Talent Infrastructure
              </h3>
              <p className="mb-6 text-lg opacity-90">12-month recruiting support + no placement fees on first 3 hires</p>
              <ul className="space-y-3">
                <li className="flex items-start gap-2">
                  <span>💰</span>
                  <span><strong className="text-yellow-300">No placement fees on first 3 hires:</strong> Save $60K-$90K</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span><strong>14-day average time-to-offer:</strong> vs. 90-day industry standard</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span><strong>Pre-vetted candidates:</strong> Microsoft, NVIDIA, Intel, Boston Dynamics, Tesla, Waymo</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span><strong>Warm pipeline:</strong> 200+ robotics engineers (perception, motion planning, safety, controls)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span><strong>Strategic consultation:</strong> Comp benchmarking, org design, role scoping</span>
                </li>
              </ul>
            </div>
          </div>

          <div className="bg-gradient-to-r from-green-500 to-blue-500 text-white rounded-xl p-10 text-center">
            <h3 className="text-3xl font-bold mb-4">📊 The Math</h3>
            <div className="grid md:grid-cols-3 gap-6 mb-6">
              <div>
                <p className="text-lg mb-2">Traditional Compliance</p>
                <p className="text-4xl font-bold line-through opacity-75">$500K</p>
                <p className="text-sm opacity-90">6-12 months</p>
              </div>
              <div>
                <p className="text-lg mb-2">Traditional Recruiting</p>
                <p className="text-4xl font-bold line-through opacity-75">$90K</p>
                <p className="text-sm opacity-90">9+ months (3 hires @ 90 days each)</p>
              </div>
              <div className="bg-white/20 backdrop-blur-sm rounded-lg p-4">
                <p className="text-lg mb-2 text-yellow-300 font-bold">Full Stack Bundle</p>
                <p className="text-5xl font-bold">$15K</p>
                <p className="text-sm font-semibold">90-day timeline</p>
              </div>
            </div>
            <p className="text-2xl font-bold">💰 Save $575K (97% savings) ⚡ 4x faster execution</p>
          </div>
        </div>
      </div>

      {/* Pricing */}
      <div id="pricing" className="py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-center mb-4">Choose Your Package</h2>
          <p className="text-center text-xl opacity-90 mb-12 max-w-3xl mx-auto">
            All packages include Instant delivery, 30-day money-back guarantee, and veteran-owned business credibility
          </p>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Launchpad */}
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border-2 border-white/20 hover:border-white/40 transition-all">
              <h3 className="text-2xl font-bold mb-2">🚀 Launchpad</h3>
              <p className="text-4xl font-bold mb-4">$2,000</p>
              <p className="text-sm opacity-75 mb-6">One-time payment</p>
              <ul className="space-y-3 mb-8">
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span>1 safety case website (choose from 9 templates)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span>GSN-validated risk models</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span>ISO 13482/61508 compliance</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span>Instant delivery</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span>30-day money-back guarantee</span>
                </li>
              </ul>
              <a href="/#templates" className="block w-full bg-white text-purple-900 px-6 py-4 rounded-lg font-bold text-center hover:bg-gray-100 transition-colors">
                Choose Template →
              </a>
              <p className="text-sm text-center mt-4 opacity-75">Perfect for: Pre-seed investor pitches</p>
            </div>

            {/* Full Stack Bundle - FEATURED */}
            <div className="bg-gradient-to-br from-yellow-400 to-orange-500 text-purple-900 rounded-xl p-8 border-4 border-yellow-300 transform scale-105 shadow-2xl">
              <div className="bg-purple-900 text-yellow-400 px-3 py-1 rounded-full text-xs font-bold inline-block mb-4">
                ⭐ MOST POPULAR
              </div>
              <h3 className="text-2xl font-bold mb-2">🎯 Full Stack Bundle</h3>
              <p className="text-5xl font-bold mb-4">$15,000</p>
              <p className="text-sm opacity-75 mb-6">One-time + 12 months support</p>
              <ul className="space-y-3 mb-8">
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span><strong>Everything in Launchpad, PLUS:</strong></span>
                </li>
                <li className="flex items-start gap-2">
                  <span>💰</span>
                  <span><strong>No placement fees on first 3 hires</strong> (save $60K-$90K)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span>12-month recruiting support</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span>14-day average time-to-offer</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span>Pre-vetted Microsoft/NVIDIA/Intel candidates</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span>6-month adaptive regulatory updates</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span>VC intro network (conditional)*</span>
                </li>
              </ul>
              <a href="mailto:SafetyCaseAI@physicalAIPros.com?subject=Full Stack Bundle Inquiry" className="block w-full bg-purple-900 text-yellow-400 px-6 py-4 rounded-lg font-bold text-center hover:bg-purple-800 transition-colors">
                Contact for Bundle →
              </a>
              <p className="text-sm text-center mt-4 font-semibold">Perfect for: Series A companies scaling teams</p>
            </div>

            {/* Portfolio Shield */}
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border-2 border-white/20 hover:border-white/40 transition-all">
              <h3 className="text-2xl font-bold mb-2">🛡️ Portfolio Shield</h3>
              <p className="text-4xl font-bold mb-4">$25,000</p>
              <p className="text-sm opacity-75 mb-6">Per year</p>
              <ul className="space-y-3 mb-8">
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span>Bulk licensing for entire portfolio (unlimited companies)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span>Standardized compliance across all investments</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span>Portfolio-wide talent sourcing</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span>Quarterly regulatory briefings</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span>White-label option (co-branded)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span>✅</span>
                  <span>Dedicated Slack channel</span>
                </li>
              </ul>
              <a href="mailto:SafetyCaseAI@physicalAIPros.com?subject=Portfolio Shield Inquiry" className="block w-full bg-white text-purple-900 px-6 py-4 rounded-lg font-bold text-center hover:bg-gray-100 transition-colors">
                Contact for Portfolio →
              </a>
              <p className="text-sm text-center mt-4 opacity-75">Perfect for: VCs with 10+ physical AI investments</p>
            </div>
          </div>

          <p className="text-center text-sm opacity-75 mt-8">
            *VC intro network conditional on product-market fit validation. All packages include 30-day money-back guarantee.
          </p>
        </div>
      </div>

      {/* FAQ */}
      <div className="py-16 bg-white/5 backdrop-blur-sm">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-center mb-12">❓ Frequently Asked Questions</h2>

          <div className="space-y-6">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
              <h3 className="text-xl font-bold mb-3">What's the catch with "no placement fees"?</h3>
              <p className="opacity-90">No catch. First 3 hires are included in the $15K bundle. After that, standard 20% placement fees apply (still better than most recruiters' 25-30%).</p>
            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
              <h3 className="text-xl font-bold mb-3">What if we only need compliance, not recruiting?</h3>
              <p className="opacity-90">Compliance-only package is $2K (Launchpad). The bundle is specifically for companies scaling teams post-funding who need both infrastructure layers.</p>
            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
              <h3 className="text-xl font-bold mb-3">How fast can you actually hire robotics engineers?</h3>
              <p className="opacity-90">14-day average time-to-offer. We maintain a warm pipeline of 200+ candidates from Microsoft, NVIDIA, Intel, Boston Dynamics, Tesla, Waymo. When you say "I need a senior perception engineer," we already know 5 people who fit.</p>
            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
              <h3 className="text-xl font-bold mb-3">How does the compliance part work?</h3>
              <p className="opacity-90">You upload your design docs, test logs, FMEA, risk assessments—whatever you have. Our proprietary AI extracts safety-critical data and generates a GSN-validated safety case website Instantly. Not templates—actual regulatory rigor (ISO 13482/61508, FAA/NHTSA/EU AI Act compliant).</p>
            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
              <h3 className="text-xl font-bold mb-3">Who is this NOT for?</h3>
              <p className="opacity-90">Post-Series B companies with dedicated safety + recruiting teams. Early-stage founders with no hardware prototype yet (we need test data to extract). Companies looking for ongoing audit support beyond initial compliance (we offer that separately as Enterprise tier).</p>
            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
              <h3 className="text-xl font-bold mb-3">What's included in "adaptive regulatory updates"?</h3>
              <p className="opacity-90">For 6 months (Full Stack) or 12 months (Portfolio Shield), we monitor EU AI Act, OSHA 3970, NHTSA autonomous vehicle rules, and FAA drone regulations. When standards evolve, we refresh your safety case automatically—no re-audits, no additional fees.</p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="py-16 bg-gradient-to-r from-yellow-400 to-orange-500 text-purple-900">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold mb-4">Ready to Build Your Compliance + Talent Infrastructure?</h2>
          <p className="text-xl mb-8">Join the robotics companies that saved $575K and 12 months by choosing the Full Stack Bundle.</p>
          <div className="flex justify-center gap-4">
            <a href="mailto:SafetyCaseAI@physicalAIPros.com?subject=Full Stack Bundle - Let's Talk" className="bg-purple-900 text-yellow-400 px-10 py-5 rounded-lg font-bold text-xl hover:bg-purple-800 transition-all transform hover:scale-105 shadow-2xl">
              Schedule 15-Minute Consult →
            </a>
            <a href="/#templates" className="bg-white/20 backdrop-blur-sm text-purple-900 px-10 py-5 rounded-lg font-bold text-xl hover:bg-white/30 transition-colors border-2 border-purple-900/30">
              Start with $2K Launchpad
            </a>
          </div>
          <p className="text-sm mt-6 opacity-75">30-day money-back guarantee • Veteran-owned business • 1,000+ placements at Microsoft/Intel/NVIDIA</p>
        </div>
      </div>
    </div>
  );
}
