import React from 'react';
import Link from 'next/link';
import { Check } from 'lucide-react';

const pricingPlans = [
  {
    name: 'Candidate',
    price: 'Free',
    period: '',
    desc: 'Perfect for job seekers',
    features: [
      'Resume upload & analysis',
      'ATS score checker',
      'Up to 10 job applications/month',
      'Basic job recommendations',
      'Email notifications',
    ],
    cta: 'Get Started Free',
    highlight: false,
  },
  {
    name: 'Pro',
    price: '$19',
    period: '/month',
    desc: 'For serious job seekers',
    features: [
      'Everything in Free',
      'Unlimited applications',
      'Priority AI screening',
      'Resume optimization tips',
      'Interview preparation',
      'Advanced analytics',
    ],
    cta: 'Start Pro Trial',
    highlight: true,
  },
  {
    name: 'Recruiter',
    price: '$79',
    period: '/month',
    desc: 'For hiring teams',
    features: [
      'Unlimited job postings',
      'AI candidate screening',
      'Team collaboration',
      'Advanced analytics',
      'ATS integration',
      'Dedicated support',
    ],
    cta: 'Start Hiring',
    highlight: false,
  },
];

export default function Pricing() {
  return (
    <section id="pricing" className="py-24 bg-[#F8FAFC]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="text-center mb-16">
          <p className="text-sm font-semibold text-[#2563EB] uppercase tracking-wider mb-3">
            Pricing
          </p>
          <h2 className="text-3xl sm:text-4xl font-bold text-[#0F172A]">
            Simple, transparent pricing
          </h2>
        </div>

        <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          {pricingPlans.map(({ name, price, period, desc, features, cta, highlight }) => (
            <div
              key={name}
              className={`rounded-2xl p-6 border ${
                highlight
                  ? 'bg-[#2563EB] border-[#2563EB] text-white shadow-xl shadow-blue-200'
                  : 'bg-white border-[#E2E8F0]'
              }`}
            >
              <h3 className={`font-semibold mb-1 ${highlight ? 'text-white' : 'text-[#0F172A]'}`}>
                {name}
              </h3>
              <p className={`text-xs mb-4 ${highlight ? 'text-blue-100' : 'text-[#64748B]'}`}>
                {desc}
              </p>
              <div className="flex items-baseline gap-1 mb-6">
                <span className={`text-4xl font-bold ${highlight ? 'text-white' : 'text-[#0F172A]'}`}>
                  {price}
                </span>
                {period && (
                  <span className={`text-sm ${highlight ? 'text-blue-200' : 'text-[#64748B]'}`}>
                    {period}
                  </span>
                )}
              </div>
              <Link
                href="/register"
                className={`block text-center w-full py-2.5 rounded-xl text-sm font-semibold mb-6 transition-colors ${
                  highlight
                    ? 'bg-white text-[#2563EB] hover:bg-blue-50'
                    : 'bg-[#2563EB] text-white hover:bg-[#1D4ED8]'
                }`}
              >
                {cta}
              </Link>
              <ul className="space-y-2.5">
                {features.map((f) => (
                  <li
                    key={f}
                    className={`flex items-center gap-2 text-sm ${
                      highlight ? 'text-blue-100' : 'text-[#64748B]'
                    }`}
                  >
                    <Check size={14} className={highlight ? 'text-blue-200' : 'text-[#22C55E]'} />
                    {f}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
