'use client';

import React, { useState, useEffect } from 'react';
import { Job } from '@/types/job';
import { MOCK_JOBS } from '@/mock/jobs';
import CompactJobCard from './CompactJobCard';

interface RecentJobsProps {
  isDashboardLink?: boolean;
}

export default function RecentJobs({ isDashboardLink = false }: RecentJobsProps) {
  const [recentJobs, setRecentJobs] = useState<Job[]>([]);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const stored = localStorage.getItem('talentai_recent_views');
    if (stored) {
      const ids: string[] = JSON.parse(stored);
      const matches = ids
        .map(id => MOCK_JOBS.find(j => j.id === id))
        .filter((j): j is Job => !!j)
        .slice(0, 4);
      setRecentJobs(matches);
    }
  }, []);

  if (recentJobs.length === 0) return null;

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
      <h4 className="font-bold text-sm text-[#0F172A]">Recently Viewed</h4>
      <div className="space-y-3">
        {recentJobs.map(job => (
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
export function trackRecentView(jobId: string) {
  if (typeof window === 'undefined') return;
  const stored = localStorage.getItem('talentai_recent_views');
  let ids: string[] = stored ? JSON.parse(stored) : [];
  ids = [jobId, ...ids.filter(id => id !== jobId)].slice(0, 8);
  localStorage.setItem('talentai_recent_views', JSON.stringify(ids));
}
