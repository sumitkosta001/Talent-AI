'use client';

import React, { useState, useEffect } from 'react';
import { Job } from '@/types/job';
import CompactJobCard from './CompactJobCard';

interface RecentJobsProps {
  isDashboardLink?: boolean;
}

export default function RecentJobs({ isDashboardLink = false }: RecentJobsProps) {
  const [recentJobs, setRecentJobs] = useState<Job[]>([]);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    try {
      const stored = localStorage.getItem('talentai_recent_job_items');
      if (stored) {
        const jobs: Job[] = JSON.parse(stored);
        if (Array.isArray(jobs)) {
          setRecentJobs(jobs.slice(0, 4));
        }
      }
    } catch {
      // safely ignore invalid local storage
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

export function trackRecentView(jobId: string, job?: Job) {
  if (typeof window === 'undefined') return;
  try {
    if (job) {
      const stored = localStorage.getItem('talentai_recent_job_items');
      let jobs: Job[] = stored ? JSON.parse(stored) : [];
      if (!Array.isArray(jobs)) jobs = [];
      jobs = [job, ...jobs.filter(j => j.id !== job.id)].slice(0, 8);
      localStorage.setItem('talentai_recent_job_items', JSON.stringify(jobs));
    }
    
    // Also track ID list for backwards compatibility
    const storedIds = localStorage.getItem('talentai_recent_views');
    let ids: string[] = storedIds ? JSON.parse(storedIds) : [];
    if (!Array.isArray(ids)) ids = [];
    ids = [jobId, ...ids.filter(id => id !== jobId)].slice(0, 8);
    localStorage.setItem('talentai_recent_views', JSON.stringify(ids));
  } catch {
    // safely ignore local storage errors
  }
}
