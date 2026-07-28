import React from 'react';
import Link from 'next/link';
import { ChevronRight, Clock } from 'lucide-react';

const recentActivity = [
  {
    company: 'Stripe',
    role: 'Senior Frontend Engineer',
    status: 'Interview',
    statusColor: 'bg-blue-100 text-blue-700',
    time: '2h ago',
    logo: 'S',
    logoColor: 'bg-violet-500',
  },
  {
    company: 'Vercel',
    role: 'Staff Software Engineer',
    status: 'Applied',
    statusColor: 'bg-amber-100 text-amber-700',
    time: '1d ago',
    logo: 'V',
    logoColor: 'bg-black',
  },
  {
    company: 'Linear',
    role: 'Product Designer',
    status: 'Shortlisted',
    statusColor: 'bg-green-100 text-green-700',
    time: '2d ago',
    logo: 'L',
    logoColor: 'bg-[#5E6AD2]',
  },
  {
    company: 'Notion',
    role: 'Full Stack Engineer',
    status: 'Rejected',
    statusColor: 'bg-red-100 text-red-700',
    time: '3d ago',
    logo: 'N',
    logoColor: 'bg-[#0F172A]',
  },
];

export default function RecentApplications() {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5">
      <div className="flex items-center justify-between mb-5">
        <h2 className="font-semibold text-[#0F172A]">Recent Applications</h2>
        <Link
          href="/candidate/applications"
          className="text-xs text-[#2563EB] hover:underline flex items-center gap-1"
        >
          View all <ChevronRight size={12} />
        </Link>
      </div>
      <div className="space-y-3">
        {recentActivity.map(({ company, role, status, statusColor, time, logo, logoColor }) => (
          <div
            key={company + role}
            className="flex items-center gap-3 p-3 rounded-xl hover:bg-[#F8FAFC] transition-colors"
          >
            <div
              className={`w-9 h-9 rounded-xl ${logoColor} flex items-center justify-center text-white font-bold text-sm flex-shrink-0`}
            >
              {logo}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-[#0F172A] truncate">{role}</p>
              <p className="text-xs text-[#64748B]">{company}</p>
            </div>
            <div className="flex items-center gap-2 flex-shrink-0">
              <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${statusColor}`}>
                {status}
              </span>
              <span className="text-xs text-[#94A3B8] flex items-center gap-1">
                <Clock size={10} />
                {time}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
