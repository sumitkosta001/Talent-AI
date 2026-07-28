import React from 'react';
import { Bot, BarChart2, Briefcase, Upload, Shield, Zap } from 'lucide-react';

const stats = [
  { value: '50K+', label: 'Candidates Placed' },
  { value: '2,400+', label: 'Companies Hiring' },
  { value: '98%', label: 'ATS Match Accuracy' },
  { value: '3x', label: 'Faster Hiring' },
];

const features = [
  {
    icon: Bot,
    title: 'AI-Powered Screening',
    desc: 'Our advanced AI analyzes resumes in seconds, matching candidates to roles with unprecedented accuracy.',
    color: 'bg-blue-50 text-blue-600',
  },
  {
    icon: BarChart2,
    title: 'ATS Score Analysis',
    desc: 'Get a detailed breakdown of how your resume performs against Applicant Tracking Systems.',
    color: 'bg-violet-50 text-violet-600',
  },
  {
    icon: Briefcase,
    title: 'Smart Job Matching',
    desc: 'Personalized job recommendations based on your skills, experience, and career goals.',
    color: 'bg-emerald-50 text-emerald-600',
  },
  {
    icon: Upload,
    title: 'One-Click Apply',
    desc: 'Apply to multiple positions with a single click using your optimized resume profile.',
    color: 'bg-orange-50 text-orange-600',
  },
  {
    icon: Shield,
    title: 'Privacy First',
    desc: 'Your data is encrypted and protected. Control who sees your resume and when.',
    color: 'bg-rose-50 text-rose-600',
  },
  {
    icon: Zap,
    title: 'Real-time Insights',
    desc: 'Track application status, get interview prep tips, and receive instant notifications.',
    color: 'bg-amber-50 text-amber-600',
  },
];

export default function Features() {
  return (
    <>
      {/* Stats */}
      <section className="bg-[#F8FAFC] border-y border-[#E2E8F0] py-14">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 grid grid-cols-2 lg:grid-cols-4 gap-8 text-center">
          {stats.map(({ value, label }) => (
            <div key={label}>
              <div className="text-3xl font-bold text-[#2563EB] mb-1">{value}</div>
              <div className="text-sm text-[#64748B]">{label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="text-center mb-16">
            <p className="text-sm font-semibold text-[#2563EB] uppercase tracking-wider mb-3">
              Features
            </p>
            <h2 className="text-3xl sm:text-4xl font-bold text-[#0F172A] mb-4">
              Everything you need to hire better
            </h2>
            <p className="text-[#64748B] max-w-xl mx-auto">
              Built for modern recruiting teams and ambitious candidates who refuse to settle.
            </p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map(({ icon: Icon, title, desc, color }) => (
              <div
                key={title}
                className="p-6 rounded-2xl border border-[#E2E8F0] hover:border-[#CBD5E1] hover:shadow-lg hover:shadow-slate-100 transition-all group"
              >
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center mb-4 ${color}`}>
                  <Icon size={18} />
                </div>
                <h3 className="font-semibold text-[#0F172A] mb-2">{title}</h3>
                <p className="text-sm text-[#64748B] leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
