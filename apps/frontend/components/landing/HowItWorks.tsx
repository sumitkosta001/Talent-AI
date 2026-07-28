import React from 'react';

const steps = [
  {
    step: '01',
    title: 'Create Your Profile',
    desc: 'Sign up as a candidate or recruiter and set up your profile in minutes.',
  },
  {
    step: '02',
    title: 'Upload Your Resume',
    desc: 'Upload your resume and let our AI analyze it for strengths and improvements.',
  },
  {
    step: '03',
    title: 'Get Matched',
    desc: 'Our AI matches you with the best opportunities based on your unique profile.',
  },
  {
    step: '04',
    title: 'Land Your Dream Job',
    desc: 'Apply with confidence, track progress, and get hired faster than ever before.',
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="py-24 bg-[#F8FAFC]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="text-center mb-16">
          <p className="text-sm font-semibold text-[#2563EB] uppercase tracking-wider mb-3">
            How it works
          </p>
          <h2 className="text-3xl sm:text-4xl font-bold text-[#0F172A]">
            From resume to offer in 4 steps
          </h2>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {steps.map(({ step, title, desc }) => (
            <div key={step} className="relative">
              <div className="text-5xl font-bold text-[#E2E8F0] mb-4">{step}</div>
              <h3 className="font-semibold text-[#0F172A] mb-2 text-lg">{title}</h3>
              <p className="text-sm text-[#64748B] leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
