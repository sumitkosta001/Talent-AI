'use client';

import React from 'react';
import { Job } from '@/types/job';
import JobCard from './JobCard';

interface RecommendedJobCardProps {
  job: Job;
}

export default function RecommendedJobCard({ job }: RecommendedJobCardProps) {
  const getMatchLevel = (match: number) => {
    if (match >= 90) return { label: 'Excellent Match', color: 'bg-green-50 text-green-700 border-green-200' };
    if (match >= 75) return { label: 'Good Match', color: 'bg-blue-50 text-blue-700 border-blue-200' };
    if (match >= 50) return { label: 'Average Match', color: 'bg-amber-50 text-amber-700 border-amber-200' };
    return { label: 'Needs Improvement', color: 'bg-red-50 text-red-700 border-red-200' };
  };

  const level = getMatchLevel(job.match);

  return (
    <div className="relative group">
      {/* Top Banner Indicator */}
      <div className={`absolute top-0 left-6 -translate-y-1/2 z-10 text-[9px] font-bold px-2 py-0.5 rounded-full border uppercase tracking-wider ${level.color}`}>
        {level.label}
      </div>
      <JobCard job={job} isDashboardLink={true} />
    </div>
  );
}
