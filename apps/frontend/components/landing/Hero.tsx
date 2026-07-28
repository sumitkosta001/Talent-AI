import React from 'react';
import Link from 'next/link';
import { Zap, ArrowRight, ChevronRight } from 'lucide-react';

export default function Hero() {
  return (
    <section className="relative overflow-hidden bg-white pt-20 pb-28">
      {/* Background gradients */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_50%_at_50%_-10%,rgba(37,99,235,0.08),transparent)]" />
      <div
        className="absolute inset-0"
        style={{
          backgroundImage:
            'radial-gradient(circle at center, rgba(37,99,235,0.06) 1px, transparent 1px)',
          backgroundSize: '32px 32px',
        }}
      />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 text-center">
        <div className="inline-flex items-center gap-2 bg-blue-50 border border-blue-100 text-[#2563EB] text-xs font-semibold px-3 py-1.5 rounded-full mb-6">
          <Zap size={12} />
          <span>AI-Powered Recruitment Platform</span>
        </div>

        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-[#0F172A] leading-tight mb-6 max-w-4xl mx-auto">
          Hire Smarter with{' '}
          <span className="text-[#2563EB]">AI-Powered</span>{' '}
          Talent Intelligence
        </h1>

        <p className="text-lg text-[#64748B] mb-10 max-w-2xl mx-auto leading-relaxed">
          TalentAI connects the right candidates with the right companies using advanced AI screening, ATS optimization, and intelligent matching — making hiring 3x faster.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
          <Link
            href="/register"
            className="flex items-center gap-2 bg-[#2563EB] text-white px-6 py-3 rounded-xl font-semibold hover:bg-[#1D4ED8] transition-all shadow-lg shadow-blue-200 hover:shadow-blue-300"
          >
            Get Started Free
            <ArrowRight size={16} />
          </Link>
          <Link
            href="/login"
            className="flex items-center gap-2 text-[#0F172A] px-6 py-3 rounded-xl font-semibold border border-[#E2E8F0] hover:border-[#CBD5E1] hover:bg-[#F8FAFC] transition-all"
          >
            View Demo
            <ChevronRight size={16} />
          </Link>
        </div>

        {/* Dashboard preview */}
        <div className="relative max-w-5xl mx-auto">
          <div className="bg-[#F8FAFC] border border-[#E2E8F0] rounded-2xl p-6 shadow-2xl shadow-slate-200/80">
            <div className="flex items-center gap-1.5 mb-4">
              <div className="w-3 h-3 rounded-full bg-[#EF4444]" />
              <div className="w-3 h-3 rounded-full bg-[#F59E0B]" />
              <div className="w-3 h-3 rounded-full bg-[#22C55E]" />
            </div>
            <div className="grid grid-cols-4 gap-3">
              {[
                { label: 'Applications', val: '48', icon: '📋', color: 'bg-blue-50' },
                { label: 'ATS Score', val: '92%', icon: '🎯', color: 'bg-violet-50' },
                { label: 'Shortlisted', val: '12', icon: '⭐', color: 'bg-amber-50' },
                { label: 'Interviews', val: '5', icon: '📅', color: 'bg-emerald-50' },
              ].map((s) => (
                <div key={s.label} className={`${s.color} rounded-xl p-3`}>
                  <div className="text-xl mb-1">{s.icon}</div>
                  <div className="text-xl font-bold text-[#0F172A]">{s.val}</div>
                  <div className="text-xs text-[#64748B]">{s.label}</div>
                </div>
              ))}
            </div>
            <div className="mt-3 h-24 bg-white rounded-xl border border-[#E2E8F0] flex items-end px-4 py-3 gap-2">
              {[40, 65, 50, 80, 75, 90, 85].map((h, i) => (
                <div key={i} className="flex-1 bg-[#2563EB] rounded-t opacity-80" style={{ height: `${h}%` }} />
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
