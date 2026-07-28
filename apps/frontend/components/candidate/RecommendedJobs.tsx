import React from 'react';
import Link from 'next/link';
import { ChevronRight } from 'lucide-react';

const recommendedJobs = [
  {
    company: 'Figma',
    role: 'React Engineer',
    salary: '$160K–$200K',
    match: 96,
    location: 'Remote',
    logo: 'F',
    logoColor: 'bg-red-500',
  },
  {
    company: 'GitHub',
    role: 'Frontend Architect',
    salary: '$170K–$210K',
    match: 91,
    location: 'San Francisco',
    logo: 'G',
    logoColor: 'bg-[#24292F]',
  },
  {
    company: 'Supabase',
    role: 'Full Stack Developer',
    salary: '$140K–$180K',
    match: 88,
    location: 'Remote',
    logo: 'S',
    logoColor: 'bg-emerald-600',
  },
];

export default function RecommendedJobs() {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5">
      <div className="flex items-center justify-between mb-5">
        <h2 className="font-semibold text-[#0F172A]">Top Matches</h2>
        <Link
          href="/candidate/jobs"
          className="text-xs text-[#2563EB] hover:underline flex items-center gap-1"
        >
          See all <ChevronRight size={12} />
        </Link>
      </div>
      <div className="space-y-3">
        {recommendedJobs.map(({ company, role, salary, match, location, logo, logoColor }) => (
          <Link
            key={company}
            href={`/candidate/jobs/${company.toLowerCase()}`}
            className="block w-full text-left p-3 rounded-xl border border-[#E2E8F0] hover:border-[#CBD5E1] hover:shadow-sm transition-all"
          >
            <div className="flex items-center gap-2.5 mb-2">
              <div
                className={`w-8 h-8 rounded-lg ${logoColor} flex items-center justify-center text-white font-bold text-xs`}
              >
                {logo}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-[#0F172A] truncate">{role}</p>
                <p className="text-xs text-[#64748B]">{company}</p>
              </div>
              <div className="text-xs font-semibold text-[#22C55E] bg-green-50 px-1.5 py-0.5 rounded-full">
                {match}%
              </div>
            </div>
            <div className="flex items-center justify-between text-xs text-[#64748B]">
              <span>{salary}</span>
              <span>{location}</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
