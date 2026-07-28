'use client';

import React from 'react';
import Link from 'next/link';
import { Job } from '@/types/job';
import BookmarkButton from './BookmarkButton';
import ApplyButton from './ApplyButton';

interface FeaturedJobCardProps {
  job: Job;
  isDashboardLink?: boolean;
}

export default function FeaturedJobCard({ job, isDashboardLink = false }: FeaturedJobCardProps) {
  const detailLink = isDashboardLink 
    ? `/candidate/jobs/${job.id}` 
    : `/jobs/${job.id}`;

  return (
    <div className="bg-gradient-to-r from-blue-600 to-blue-800 rounded-3xl p-6 text-white relative shadow-lg overflow-hidden flex-shrink-0 w-80 sm:w-96 flex flex-col justify-between">
      {/* Background decorations */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-white/5 rounded-full blur-2xl -mr-8 -mt-8" />
      <div className="absolute bottom-0 left-0 w-24 h-24 bg-blue-500/20 rounded-full blur-xl -ml-6 -mb-6" />

      <div className="relative">
        <div className="flex justify-between items-start gap-4">
          <div className="w-12 h-12 bg-white/10 rounded-2xl flex items-center justify-center font-bold text-xl backdrop-blur-md">
            {job.logo}
          </div>
          <span className="text-[10px] font-bold bg-white/25 border border-white/20 backdrop-blur-md px-2.5 py-1 rounded-full uppercase tracking-wider">
            Featured Match · {job.match}%
          </span>
        </div>

        <div className="mt-5">
          <h3 className="font-bold text-base sm:text-lg leading-tight line-clamp-1">
            {job.role}
          </h3>
          <p className="text-blue-200 text-xs mt-1">{job.company}</p>
        </div>

        <div className="flex flex-wrap items-center gap-3 mt-4 text-[11px] text-blue-100">
          <span>{job.location}</span>
          <span>·</span>
          <span>{job.salary}</span>
          <span>·</span>
          <span>{job.type}</span>
        </div>
      </div>

      <div className="flex items-center justify-between mt-8 relative border-t border-white/10 pt-4">
        <span className="text-[10px] text-blue-200">{job.date}</span>
        <div className="flex items-center gap-2">
          <Link
            href={detailLink}
            className="text-xs text-white hover:text-blue-100 font-semibold px-3 py-2 transition-colors"
          >
            Details
          </Link>
          <ApplyButton
            jobId={job.id}
            role={job.role}
            company={job.company}
            logo={job.logo}
            logoColor={job.logoColor}
            salary={job.salary}
            location={job.location}
            className="bg-white text-blue-700 hover:bg-blue-50 border-0"
          />
        </div>
      </div>
    </div>
  );
}
