import React from 'react';
import { Star } from 'lucide-react';

const testimonials = [
  {
    quote:
      'TalentAI completely transformed our hiring process. We reduced time-to-hire by 60% and found much better candidates.',
    name: 'Rachel Chen',
    role: 'Head of Talent, Stripe',
    initials: 'RC',
    color: 'bg-blue-500',
  },
  {
    quote:
      'The ATS score feature helped me land interviews at 5 top companies within a week. Absolutely game-changing.',
    name: 'Marcus Williams',
    role: 'Software Engineer',
    initials: 'MW',
    color: 'bg-violet-500',
  },
  {
    quote:
      'As a recruiter, TalentAI saves me hours every day. The AI screening is incredibly accurate and fair.',
    name: 'Sofia Ramirez',
    role: 'Senior Recruiter, Notion',
    initials: 'SR',
    color: 'bg-emerald-500',
  },
];

export default function Testimonials() {
  return (
    <section className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="text-center mb-16">
          <p className="text-sm font-semibold text-[#2563EB] uppercase tracking-wider mb-3">
            Testimonials
          </p>
          <h2 className="text-3xl sm:text-4xl font-bold text-[#0F172A]">Trusted by thousands</h2>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {testimonials.map(({ quote, name, role, initials, color }) => (
            <div
              key={name}
              className="bg-[#F8FAFC] rounded-2xl p-6 border border-[#E2E8F0]"
            >
              <div className="flex gap-1 mb-4">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} size={14} className="fill-[#F59E0B] text-[#F59E0B]" />
                ))}
              </div>
              <p className="text-[#0F172A] text-sm leading-relaxed mb-6">"{quote}"</p>
              <div className="flex items-center gap-3">
                <div
                  className={`w-9 h-9 rounded-full ${color} flex items-center justify-center text-white text-xs font-semibold`}
                >
                  {initials}
                </div>
                <div>
                  <p className="text-sm font-semibold text-[#0F172A]">{name}</p>
                  <p className="text-xs text-[#64748B]">{role}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
