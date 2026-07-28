'use client';

import React from 'react';

interface JobsHeaderProps {
  title?: string;
  subtitle?: string;
  totalJobs?: number;
}

export default function JobsHeader({
  title = 'Explore Jobs',
  subtitle = 'Find your next career step matching your technical skills profile.',
  totalJobs,
}: JobsHeaderProps) {
  return (
    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#E2E8F0] pb-5">
      <div>
        <h1 className="text-xl sm:text-2xl font-bold text-[#0F172A]">{title}</h1>
        <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">{subtitle}</p>
      </div>
      {totalJobs !== undefined && (
        <span className="bg-blue-50 text-blue-700 border border-blue-100 text-xs font-semibold px-3 py-1.5 rounded-xl w-fit">
          {totalJobs} Positions Available
        </span>
      )}
    </div>
  );
}
