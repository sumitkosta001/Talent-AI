'use client';

import React from 'react';
import Link from 'next/link';
import { Job } from '@/types/job';

interface CompactJobCardProps {
  job: Job;
  isActive?: boolean;
  isDashboardLink?: boolean;
}

export default function CompactJobCard({
  job,
  isActive = false,
  isDashboardLink = false,
}: CompactJobCardProps) {
  const detailLink = isDashboardLink 
    ? `/candidate/jobs/${job.id}` 
    : `/jobs/${job.id}`;

  return (
    <Link
      href={detailLink}
      className={`block p-4 rounded-2xl border transition-all text-left ${
        isActive
          ? 'bg-blue-50/50 border-[#2563EB] shadow-sm'
          : 'bg-white border-[#E2E8F0] hover:border-[#CBD5E1]'
      }`}
    >
      <div className="flex gap-3">
        <div className={`w-10 h-10 rounded-xl ${job.logoColor} flex items-center justify-center text-white font-bold text-base flex-shrink-0`}>
          {job.logo}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex justify-between items-start gap-1">
            <h4 className="text-xs sm:text-sm font-semibold text-[#0F172A] line-clamp-1">
              {job.role}
            </h4>
            <span className="text-[10px] font-bold text-green-600 flex-shrink-0">
              {job.match}%
            </span>
          </div>
          <p className="text-[11px] text-[#64748B] mt-0.5">{job.company}</p>
          <div className="flex items-center gap-2 mt-2 text-[10px] text-[#64748B]">
            <span>{job.location}</span>
            <span>·</span>
            <span>{job.salary}</span>
          </div>
        </div>
      </div>
    </Link>
  );
}
