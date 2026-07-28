import React from 'react';
import Link from 'next/link';
import { Upload, Bot, Briefcase, FileText, ChevronRight } from 'lucide-react';

const actions = [
  {
    icon: Upload,
    label: 'Upload Resume',
    sub: 'Add or update your resume',
    href: '/candidate/resume/upload',
    color: 'bg-blue-50 text-blue-600',
  },
  {
    icon: Bot,
    label: 'Check ATS Score',
    sub: 'See how you rank',
    href: '/candidate/ats',
    color: 'bg-violet-50 text-violet-600',
  },
  {
    icon: Briefcase,
    label: 'Browse Jobs',
    sub: '340+ open positions',
    href: '/candidate/jobs',
    color: 'bg-amber-50 text-amber-600',
  },
  {
    icon: FileText,
    label: 'View Analysis',
    sub: 'Resume insights',
    href: '/candidate/resume/analysis',
    color: 'bg-emerald-50 text-emerald-600',
  },
];

export default function QuickActions() {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5">
      <h2 className="font-semibold text-[#0F172A] mb-4">Quick Actions</h2>
      <div className="space-y-2">
        {actions.map(({ icon: Icon, label, sub, href, color }) => (
          <Link
            key={label}
            href={href}
            className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-[#F8FAFC] transition-colors group"
          >
            <div className={`w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0 ${color}`}>
              <Icon size={16} />
            </div>
            <div className="text-left flex-1">
              <p className="text-sm font-medium text-[#0F172A]">{label}</p>
              <p className="text-xs text-[#64748B]">{sub}</p>
            </div>
            <ChevronRight size={14} className="text-[#94A3B8] group-hover:text-[#64748B]" />
          </Link>
        ))}
      </div>
    </div>
  );
}
