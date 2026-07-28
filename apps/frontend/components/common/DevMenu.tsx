'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { DEV_MODE } from '@/lib/config';
import { Terminal, X, ChevronUp, Link as LinkIcon } from 'lucide-react';

export default function DevMenu() {
  const [open, setOpen] = useState(false);

  if (!DEV_MODE) return null;

  const routes = [
    { label: 'Landing Page', href: '/' },
    { label: 'Login', href: '/login' },
    { label: 'Register', href: '/register' },
    { label: 'Forgot Password', href: '/forgot-password' },
    { label: 'Candidate Dashboard', href: '/candidate' },
    { label: 'Resume Overview', href: '/candidate/resume' },
    { label: 'Resume Upload', href: '/candidate/resume/upload' },
    { label: 'Resume Analysis', href: '/candidate/resume/analysis' },
    { label: 'ATS Score', href: '/candidate/ats' },
    { label: 'My Applications', href: '/candidate/applications' },
    { label: 'Recruiter Dashboard', href: '/recruiter' },
    { label: 'Recruiter Analytics', href: '/recruiter/analytics' },
    { label: 'Recruiter Company', href: '/recruiter/company' },
    { label: 'Recruiter Jobs', href: '/recruiter/jobs' },
    { label: 'Admin Dashboard', href: '/admin' },
  ];

  return (
    <div className="fixed bottom-6 right-6 z-[9999] font-sans">
      {open ? (
        <div className="bg-[#0F172A] text-white border border-slate-800 rounded-2xl p-4 w-72 shadow-2xl animate-in slide-in-from-bottom duration-200">
          <div className="flex items-center justify-between border-b border-slate-800 pb-2 mb-3">
            <div className="flex items-center gap-2 text-[#2563EB]">
              <Terminal size={16} />
              <span className="font-bold text-sm">DEV NAV CONSOLE</span>
            </div>
            <button
              onClick={() => setOpen(false)}
              className="p-1 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white cursor-pointer"
            >
              <X size={16} />
            </button>
          </div>
          <div className="max-h-80 overflow-y-auto space-y-1.5 scrollbar-thin scrollbar-thumb-slate-800 pr-1">
            {routes.map(({ label, href }) => (
              <Link
                key={href}
                href={href}
                onClick={() => setOpen(false)}
                className="flex items-center gap-2 w-full text-left text-xs text-slate-300 hover:text-white hover:bg-slate-800 px-2.5 py-1.5 rounded-lg transition-colors"
              >
                <LinkIcon size={12} className="text-slate-500" />
                {label}
              </Link>
            ))}
          </div>
        </div>
      ) : (
        <button
          onClick={() => setOpen(true)}
          className="flex items-center gap-2 bg-[#0F172A] hover:bg-[#1E293B] text-white border border-slate-800 rounded-full px-4 py-2.5 shadow-xl transition-all hover:scale-105 cursor-pointer text-xs font-semibold"
        >
          <Terminal size={14} className="text-[#2563EB]" />
          Dev Menu
          <ChevronUp size={12} className="text-slate-400" />
        </button>
      )}
    </div>
  );
}
