'use client';

import React from 'react';
import { Job } from '@/types/job';
import CompactJobCard from './CompactJobCard';

interface RelatedJobsProps {
  jobs: Job[];
  currentJobId?: string;
  isDashboardLink?: boolean;
}

export default function RelatedJobs({
  jobs,
  currentJobId,
  isDashboardLink = false,
}: RelatedJobsProps) {
  const filtered = jobs
    .filter(j => j.id !== currentJobId)
    .slice(0, 4);

  if (filtered.length === 0) return null;

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
      <h4 className="font-bold text-sm text-[#0F172A]">Related Positions</h4>
      <div className="space-y-3">
        {filtered.map(job => (
          <CompactJobCard
            key={job.id}
            job={job}
            isDashboardLink={isDashboardLink}
          />
        ))}
      </div>
    </div>
  );
}
