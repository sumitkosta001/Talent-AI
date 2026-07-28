import React from 'react';
import Link from 'next/link';
import { FileText, Bot, Briefcase, Star } from 'lucide-react';

interface StatCardProps {
  icon: React.ComponentType<any>;
  label: string;
  value: string;
  sub: string;
  color: string;
  href: string;
}

const StatCard = ({ icon: Icon, label, value, sub, color, href }: StatCardProps) => (
  <Link
    href={href}
    className="bg-white rounded-2xl border border-[#E2E8F0] p-5 text-left hover:shadow-md hover:border-[#CBD5E1] transition-all group block"
  >
    <div className={`w-10 h-10 rounded-xl flex items-center justify-center mb-4 ${color}`}>
      <Icon size={18} />
    </div>
    <div className="text-2xl font-bold text-[#0F172A] mb-0.5">{value}</div>
    <div className="text-sm font-medium text-[#0F172A] mb-0.5">{label}</div>
    <div className="text-xs text-[#64748B]">{sub}</div>
  </Link>
);

export default function DashboardStats() {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <StatCard
        icon={FileText}
        label="Resume Uploaded"
        value="1"
        sub="Last updated 3 days ago"
        color="bg-blue-50 text-blue-600"
        href="/candidate/resume/upload"
      />
      <StatCard
        icon={Bot}
        label="ATS Score"
        value="92%"
        sub="Top 5% of candidates"
        color="bg-violet-50 text-violet-600"
        href="/candidate/ats"
      />
      <StatCard
        icon={Briefcase}
        label="Applied Jobs"
        value="48"
        sub="+6 this week"
        color="bg-amber-50 text-amber-600"
        href="/candidate/applications"
      />
      <StatCard
        icon={Star}
        label="Recommended"
        value="24"
        sub="New matches today"
        color="bg-emerald-50 text-emerald-600"
        href="/candidate/jobs"
      />
    </div>
  );
}
