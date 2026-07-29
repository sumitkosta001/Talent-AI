'use client';

import React from 'react';
import Link from 'next/link';
import { Plus, Users, Building, BarChart2 } from 'lucide-react';

export default function QuickActions() {
  const actions = [
    { label: 'Post New Job', href: '/recruiter/jobs/create', icon: Plus, color: 'bg-blue-600 text-white hover:bg-blue-700' },
    { label: 'Manage Candidates', href: '/recruiter/applicants', icon: Users, color: 'bg-white border border-[#E2E8F0] text-slate-700 hover:bg-[#F8FAFC]' },
    { label: 'Company Profile', href: '/recruiter/company', icon: Building, color: 'bg-white border border-[#E2E8F0] text-slate-700 hover:bg-[#F8FAFC]' },
    { label: 'Hiring Reports', href: '/recruiter/analytics', icon: BarChart2, color: 'bg-white border border-[#E2E8F0] text-slate-700 hover:bg-[#F8FAFC]' },
  ];

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
      <h3 className="font-bold text-[#0F172A] text-sm">Quick Actions</h3>
      <div className="grid grid-cols-2 gap-3">
        {actions.map(({ label, href, icon: Icon, color }) => (
          <Link
            key={label}
            href={href}
            className={`
              flex flex-col items-center justify-center p-4 rounded-xl text-center gap-2 transition-all text-xs font-semibold cursor-pointer
              ${color}
            `}
          >
            <Icon size={18} />
            <span>{label}</span>
          </Link>
        ))}
      </div>
    </div>
  );
}
