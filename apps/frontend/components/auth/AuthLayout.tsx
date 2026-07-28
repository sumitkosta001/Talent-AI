'use client';

import React from 'react';
import { Bot, ShieldCheck, Sparkles, Zap } from 'lucide-react';
import Link from 'next/link';

interface AuthLayoutProps {
  children: React.ReactNode;
  title: string;
  subtitle: string;
}

export default function AuthLayout({ children, title, subtitle }: AuthLayoutProps) {
  return (
    <div className="min-h-screen bg-[#F8FAFC] dark:bg-[#090D16] flex text-[#0F172A] dark:text-[#F8FAFC]">
      <div className="hidden lg:flex lg:w-1/2 bg-[#2563EB] flex-col justify-between p-12 relative overflow-hidden">
        <div
          className="absolute inset-0"
          style={{
            backgroundImage:
              'radial-gradient(circle at center, rgba(255,255,255,0.08) 1px, transparent 1px)',
            backgroundSize: '28px 28px',
          }}
        />
        <div className="relative z-10">
          <Link href="/" className="flex items-center gap-2 mb-16 w-fit">
            <div className="w-9 h-9 bg-white/20 rounded-xl flex items-center justify-center backdrop-blur-xs">
              <Bot size={20} className="text-white animate-pulse" />
            </div>
            <span className="font-bold text-white text-2xl tracking-tight">TalentAI</span>
          </Link>

          <h2 className="text-4xl font-black text-white mb-4 leading-tight">
            Enterprise AI Recruitment &<br />Career Advancement.
          </h2>
          <p className="text-blue-100 text-lg max-w-md leading-relaxed">
            Security-first platform trusted by fortune 500 companies and top tech talent worldwide.
          </p>
        </div>

        <div className="relative z-10 space-y-3">
          {[
            { icon: ShieldCheck, val: '256-bit AES Encryption', label: 'SOC2 Type II Certified' },
            { icon: Sparkles, val: '98% ATS Match Accuracy', label: 'Real-time resume scoring' },
            { icon: Zap, val: '3x Faster Hiring Rate', label: 'Automated candidate workflows' },
          ].map(({ icon: Icon, val, label }, idx) => (
            <div key={idx} className="flex items-center gap-4 bg-white/10 backdrop-blur-md rounded-2xl p-4 border border-white/10">
              <div className="w-10 h-10 rounded-xl bg-white/20 flex items-center justify-center text-white">
                <Icon size={20} />
              </div>
              <div>
                <p className="text-base font-extrabold text-white">{val}</p>
                <p className="text-xs text-blue-100 font-medium">{label}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex-1 flex items-center justify-center p-6 bg-white dark:bg-[#1E293B] lg:bg-[#F8FAFC] dark:lg:bg-[#090D16]">
        <div className="w-full max-w-md">
          <div className="lg:hidden flex items-center gap-2 justify-center mb-8">
            <div className="w-8 h-8 bg-[#2563EB] rounded-lg flex items-center justify-center">
              <Bot size={16} className="text-white" />
            </div>
            <span className="font-bold text-[#0F172A] dark:text-white text-xl">TalentAI</span>
          </div>

          <div className="mb-6">
            <h1 className="text-2xl sm:text-3xl font-black text-[#0F172A] dark:text-white tracking-tight">{title}</h1>
            <p className="text-xs sm:text-sm text-[#64748B] dark:text-slate-400 mt-1">{subtitle}</p>
          </div>

          {children}
        </div>
      </div>
    </div>
  );
}
