'use client';

import { Button } from '@/components/ui/button';
import { ArrowRight, CheckCircle, Zap, Shield, Users, TrendingUp, Clock, Brain } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white shadow-sm z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="text-2xl font-bold text-blue-600">⚖️ DClaw Patent</div>
          <div className="hidden md:flex gap-6">
            <a href="#features" className="text-gray-600 hover:text-blue-600">Features</a>
            <a href="#pricing" className="text-gray-600 hover:text-blue-600">Pricing</a>
            <a href="#about" className="text-gray-600 hover:text-blue-600">About</a>
          </div>
          <Button>Get Started</Button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 leading-tight mb-6">
              AI-Powered Patent Management for Modern IP Teams
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              DClaw Patent combines AI claim drafting, legal automation, and intelligent docketing to help you manage patents 10x faster than traditional tools.
            </p>
            <div className="flex gap-4 mb-8">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
                Start Free Trial <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
              <Button size="lg" variant="outline">
                Watch Demo
              </Button>
            </div>
            <div className="flex gap-8 text-sm">
              <div>
                <div className="text-2xl font-bold text-blue-600">60+</div>
                <div className="text-gray-600">API Endpoints</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-blue-600">50+</div>
                <div className="text-gray-600">Test Cases</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-blue-600">8</div>
                <div className="text-gray-600">Data Models</div>
              </div>
            </div>
          </div>
          <div className="bg-gradient-to-br from-blue-100 to-purple-100 rounded-2xl p-8 h-96 flex items-center justify-center">
            <div className="text-center">
              <Brain className="w-24 h-24 text-blue-600 mx-auto mb-4" />
              <p className="text-gray-600">Powered by Claude AI</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Overview */}
      <section id="features" className="bg-white py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16">All the Features You Need</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { icon: Brain, title: 'AI Claim Drafting', desc: 'Generate claims in 2 minutes, not 2 days' },
              { icon: Clock, title: 'Smart Docketing', desc: 'Auto-calculate deadlines by jurisdiction' },
              { icon: Zap, title: 'Legal Automation', desc: 'Auto-parse office actions & create dockets' },
              { icon: Shield, title: 'FTO Analysis', desc: 'Freedom-to-operate risk assessment' },
              { icon: TrendingUp, title: 'Patent Intelligence', desc: 'Competitive patent monitoring' },
              { icon: Users, title: 'Real-Time Collab', desc: 'Comments, mentions, and threading' },
            ].map((feature, i) => (
              <div key={i} className="p-6 border rounded-lg hover:shadow-lg transition">
                <feature.icon className="w-10 h-10 text-blue-600 mb-4" />
                <h3 className="font-bold text-lg mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Patent Portfolio Management */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-blue-50 to-purple-50">
        <div className="max-w-7xl mx-auto grid md:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="text-4xl font-bold mb-6">Manage Your Patent Portfolio</h2>
            <p className="text-lg text-gray-600 mb-6">
              Track patents across multiple jurisdictions (US, EP, JP, CN, IN) with intelligent search and filtering.
            </p>
            <ul className="space-y-4">
              {[
                'Search by title, abstract, or claims',
                'Filter by status (draft, filed, issued)',
                'Track by jurisdiction and tech class',
                'View filing & publication dates',
                'Monitor patent lifecycle',
                'Export bulk reports',
              ].map((item, i) => (
                <li key={i} className="flex gap-3">
                  <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-1" />
                  <span className="text-gray-700">{item}</span>
                </li>
              ))}
            </ul>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-8 border-2 border-blue-100">
            <div className="space-y-4">
              <div className="h-3 bg-gray-200 rounded w-3/4"></div>
              <div className="h-3 bg-gray-200 rounded w-full"></div>
              <div className="h-3 bg-gray-200 rounded w-5/6"></div>
              <div className="mt-6 space-y-3">
                <div className="flex justify-between items-center p-3 bg-blue-50 rounded">
                  <div className="h-2 bg-blue-200 rounded w-1/3"></div>
                  <div className="h-2 bg-green-200 rounded w-1/4"></div>
                </div>
                <div className="flex justify-between items-center p-3 bg-yellow-50 rounded">
                  <div className="h-2 bg-yellow-200 rounded w-1/3"></div>
                  <div className="h-2 bg-orange-200 rounded w-1/4"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* AI Claim Drafting */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div className="bg-gradient-to-br from-purple-100 to-pink-100 rounded-xl shadow-lg p-8 h-96 flex items-center justify-center">
            <div className="text-center">
              <Zap className="w-20 h-20 text-purple-600 mx-auto mb-4" />
              <p className="text-gray-700 font-semibold">AI-Generated Claims in 2 Minutes</p>
            </div>
          </div>
          <div>
            <h2 className="text-4xl font-bold mb-6">AI Claim Drafting</h2>
            <p className="text-lg text-gray-600 mb-6">
              Upload your invention disclosure and let Claude AI generate multiple claim variants with independent and dependent claims.
            </p>
            <ul className="space-y-4 mb-8">
              {[
                'Generate 3 claim variants automatically',
                'Get abstract generation in seconds',
                'Quality scoring on 5 dimensions',
                'Edit and iterate on drafts',
                'Version history and comparison',
                'No hallucinations (claim-disclosure matching)',
              ].map((item, i) => (
                <li key={i} className="flex gap-3">
                  <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-1" />
                  <span className="text-gray-700">{item}</span>
                </li>
              ))}
            </ul>
            <p className="text-sm text-gray-600 italic">
              ⚡ Average time: 30 seconds to 2 minutes per invention disclosure
            </p>
          </div>
        </div>
      </section>

      {/* Smart Docketing */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-green-50 to-emerald-50">
        <div className="max-w-7xl mx-auto grid md:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="text-4xl font-bold mb-6">Smart Docket Management</h2>
            <p className="text-lg text-gray-600 mb-6">
              Never miss a deadline again. DClaw automatically calculates jurisdiction-specific deadlines and sends reminders 30, 14, and 7 days before due dates.
            </p>
            <ul className="space-y-4 mb-8">
              {[
                'Jurisdiction-specific calculations (US, EP, JP, CN, IN)',
                'Color-coded urgency (red overdue, yellow <14 days, blue <30)',
                'Mark complete with checkboxes',
                'Export to CSV or iCal for calendar apps',
                'Overdue alerts with email notifications',
                'Bulk docket operations',
              ].map((item, i) => (
                <li key={i} className="flex gap-3">
                  <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-1" />
                  <span className="text-gray-700">{item}</span>
                </li>
              ))}
            </ul>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-8 space-y-4">
            <div className="flex justify-between items-center p-3 bg-red-50 border-l-4 border-red-500 rounded">
              <span className="font-semibold text-gray-800">Office Action Due</span>
              <span className="text-red-600 font-bold">3 days overdue</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-yellow-50 border-l-4 border-yellow-500 rounded">
              <span className="font-semibold text-gray-800">Maintenance Fee</span>
              <span className="text-yellow-600 font-bold">12 days remaining</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-blue-50 border-l-4 border-blue-500 rounded">
              <span className="font-semibold text-gray-800">Response Deadline</span>
              <span className="text-blue-600 font-bold">28 days remaining</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-green-50 border-l-4 border-green-500 rounded">
              <span className="font-semibold text-gray-800">Publication</span>
              <span className="text-green-600 font-bold">✓ Completed</span>
            </div>
          </div>
        </div>
      </section>

      {/* Legal Automation */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div className="bg-gradient-to-br from-orange-100 to-red-100 rounded-xl shadow-lg p-8 h-96 flex items-center justify-center">
            <div className="text-center">
              <Shield className="w-20 h-20 text-orange-600 mx-auto mb-4" />
              <p className="text-gray-700 font-semibold">Automatic Office Action Parsing</p>
            </div>
          </div>
          <div>
            <h2 className="text-4xl font-bold mb-6">Legal Automation</h2>
            <p className="text-lg text-gray-600 mb-6">
              Upload USPTO/EPO office actions and DClaw automatically extracts deadlines, rejections, and requirements. Dockets are created automatically.
            </p>
            <ul className="space-y-4 mb-8">
              {[
                'Parse office actions (PDF or text)',
                'Extract deadlines and classify action types',
                'Identify claim rejections and requirements',
                'Auto-create dockets from parsed data',
                'Maintenance fee schedules (US: 3.5, 7.5, 11.5yr)',
                'EP annual fees (years 3-20)',
              ].map((item, i) => (
                <li key={i} className="flex gap-3">
                  <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-1" />
                  <span className="text-gray-700">{item}</span>
                </li>
              ))}
            </ul>
            <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
              <p className="text-sm text-gray-700">
                <strong>Webhook Support:</strong> Integrate with USPTO/EPO APIs to automatically receive and process office actions
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Competitive Intelligence */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-indigo-50 to-blue-50">
        <div className="max-w-7xl mx-auto grid md:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="text-4xl font-bold mb-6">Competitive Patent Watch</h2>
            <p className="text-lg text-gray-600 mb-6">
              Monitor competitor patent filings in real-time. Get alerted when key competitors file patents in your tech areas.
            </p>
            <ul className="space-y-4 mb-8">
              {[
                'Create watchlists of competitor assignees',
                'Track patent filings by technology class',
                'Real-time alerts on new filings',
                'Relevance scoring (AI-powered)',
                'Patent landscape visualization',
                'Identify white-space opportunities',
              ].map((item, i) => (
                <li key={i} className="flex gap-3">
                  <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-1" />
                  <span className="text-gray-700">{item}</span>
                </li>
              ))}
            </ul>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-8">
            <div className="space-y-4">
              <div className="text-center mb-6">
                <TrendingUp className="w-12 h-12 text-blue-600 mx-auto mb-2" />
                <h4 className="font-bold text-gray-800">Competitor Filing Trend</h4>
              </div>
              <div className="space-y-2">
                {['Apple Inc', 'Google LLC', 'Microsoft Corp', 'Samsung Electronics', 'IBM'].map((company, i) => (
                  <div key={i} className="flex justify-between items-center">
                    <span className="text-sm text-gray-700">{company}</span>
                    <div className="bg-blue-100 rounded-full px-3 py-1 text-xs font-bold text-blue-600">
                      {12 + (i * 5)} filings
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Collaboration */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div className="bg-gradient-to-br from-teal-100 to-cyan-100 rounded-xl shadow-lg p-8 h-96 flex items-center justify-center">
            <div className="text-center">
              <Users className="w-20 h-20 text-teal-600 mx-auto mb-4" />
              <p className="text-gray-700 font-semibold">Real-Time Collaboration</p>
            </div>
          </div>
          <div>
            <h2 className="text-4xl font-bold mb-6">Real-Time Collaboration</h2>
            <p className="text-lg text-gray-600 mb-6">
              Work together with your team on patents. Comment on claims, mention colleagues with @mentions, and build threaded conversations.
            </p>
            <ul className="space-y-4 mb-8">
              {[
                'Patent-specific comment threads',
                '@mention teammates for instant notifications',
                'Reply directly to comments',
                'Mark conversations as resolved',
                'View full comment history',
                'Real-time updates across team',
              ].map((item, i) => (
                <li key={i} className="flex gap-3">
                  <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-1" />
                  <span className="text-gray-700">{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16">Simple, Transparent Pricing</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {/* Free Tier */}
            <div className="bg-white rounded-xl shadow-lg p-8 border-2 border-gray-200 hover:border-blue-400 transition">
              <h3 className="text-2xl font-bold mb-4">Free</h3>
              <p className="text-gray-600 mb-6">Perfect for getting started</p>
              <div className="text-3xl font-bold mb-6">$0<span className="text-sm text-gray-600">/month</span></div>
              <ul className="space-y-3 mb-8">
                <li className="flex gap-2">
                  <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
                  <span className="text-sm">5 patents</span>
                </li>
                <li className="flex gap-2">
                  <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
                  <span className="text-sm">Basic docketing</span>
                </li>
                <li className="flex gap-2">
                  <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
                  <span className="text-sm">3 watchlists</span>
                </li>
                <li className="flex gap-2">
                  <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
                  <span className="text-sm">Community support</span>
                </li>
              </ul>
              <Button variant="outline" className="w-full">Get Started Free</Button>
            </div>

            {/* Pro Tier */}
            <div className="bg-blue-600 text-white rounded-xl shadow-lg p-8 transform scale-105 border-2 border-blue-600">
              <div className="bg-blue-500 text-white px-3 py-1 rounded-full inline-block text-sm font-bold mb-4">
                MOST POPULAR
              </div>
              <h3 className="text-2xl font-bold mb-4">Pro</h3>
              <p className="text-blue-100 mb-6">For growing teams</p>
              <div className="text-4xl font-bold mb-6">$99<span className="text-sm text-blue-100">/month</span></div>
              <ul className="space-y-3 mb-8">
                <li className="flex gap-2">
                  <CheckCircle className="w-5 h-5 text-green-300 flex-shrink-0" />
                  <span className="text-sm">Unlimited patents</span>
                </li>
                <li className="flex gap-2">
                  <CheckCircle className="w-5 h-5 text-green-300 flex-shrink-0" />
                  <span className="text-sm">AI claim drafting</span>
                </li>
                <li className="flex gap-2">
                  <CheckCircle className="w-5 h-5 text-green-300 flex-shrink-0" />
                  <span className="text-sm">Unlimited watchlists</span>
                </li>
                <li className="flex gap-2">
                  <CheckCircle className="w-5 h-5 text-green-300 flex-shrink-0" />
                  <span className="text-sm">Legal automation</span>
                </li>
                <li className="flex gap-2">
                  <CheckCircle className="w-5 h-5 text-green-300 flex-shrink-0" />
                  <span className="text-sm">Priority support</span>
                </li>
              </ul>
              <Button className="w-full bg-white text-blue-600 hover:bg-gray-100">Start Pro Trial</Button>
            </div>

            {/* Enterprise Tier */}
            <div className="bg-white rounded-xl shadow-lg p-8 border-2 border-gray-200 hover:border-blue-400 transition">
              <h3 className="text-2xl font-bold mb-4">Enterprise</h3>
              <p className="text-gray-600 mb-6">For large organizations</p>
              <div className="text-3xl font-bold mb-6">Custom<span className="text-sm text-gray-600">/month</span></div>
              <ul className="space-y-3 mb-8">
                <li className="flex gap-2">
                  <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
                  <span className="text-sm">Everything in Pro</span>
                </li>
                <li className="flex gap-2">
                  <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
                  <span className="text-sm">API access</span>
                </li>
                <li className="flex gap-2">
                  <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
                  <span className="text-sm">SSO & advanced security</span>
                </li>
                <li className="flex gap-2">
                  <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
                  <span className="text-sm">Dedicated support</span>
                </li>
                <li className="flex gap-2">
                  <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
                  <span className="text-sm">Custom integrations</span>
                </li>
              </ul>
              <Button variant="outline" className="w-full">Contact Sales</Button>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Start Managing Patents Like a Fortune 500 Company
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Get started in minutes. No credit card required. Free tier includes up to 5 patents.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-white text-blue-600 hover:bg-gray-100">
              Start Free Trial
            </Button>
            <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-blue-600">
              Schedule Demo
            </Button>
          </div>
          <p className="text-sm text-blue-100 mt-6">
            ✓ Free for up to 5 patents  ✓ No credit card required  ✓ Cancel anytime
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto grid md:grid-cols-4 gap-8 mb-8">
          <div>
            <h4 className="text-white font-bold mb-4">Product</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="hover:text-white">Features</a></li>
              <li><a href="#" className="hover:text-white">Pricing</a></li>
              <li><a href="#" className="hover:text-white">Security</a></li>
              <li><a href="#" className="hover:text-white">Roadmap</a></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-bold mb-4">Company</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="hover:text-white">About</a></li>
              <li><a href="#" className="hover:text-white">Blog</a></li>
              <li><a href="#" className="hover:text-white">Careers</a></li>
              <li><a href="#" className="hover:text-white">Contact</a></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-bold mb-4">Resources</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="hover:text-white">Documentation</a></li>
              <li><a href="#" className="hover:text-white">API Reference</a></li>
              <li><a href="#" className="hover:text-white">GitHub</a></li>
              <li><a href="#" className="hover:text-white">Support</a></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-bold mb-4">Legal</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="hover:text-white">Privacy</a></li>
              <li><a href="#" className="hover:text-white">Terms</a></li>
              <li><a href="#" className="hover:text-white">Security</a></li>
              <li><a href="#" className="hover:text-white">Status</a></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-800 pt-8 text-center text-sm">
          <p>© 2026 DClaw Patent. All rights reserved. Powered by Claude AI.</p>
          <p className="mt-2">Owner: Udai Kiran (udai.kiran@oneconvergence.com)</p>
        </div>
      </footer>
    </div>
  );
}
