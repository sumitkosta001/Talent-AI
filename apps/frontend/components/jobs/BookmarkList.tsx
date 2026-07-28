'use client';

import React from 'react';
import { useBookmarks } from '@/hooks/useBookmarks';
import { MOCK_JOBS } from '@/mock/jobs';
import JobCard from './JobCard';

export default function BookmarkList() {
  const { bookmarkedIds } = useBookmarks();
  
  const savedJobs = MOCK_JOBS.filter(job => bookmarkedIds.includes(job.id));

  if (savedJobs.length === 0) {
    return (
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-8 text-center text-xs text-[#64748B] font-semibold">
        You haven't saved any jobs yet. Browse listings and click bookmark to save positions.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {savedJobs.map(job => (
        <JobCard
          key={job.id}
          job={job}
          isDashboardLink={true}
        />
      ))}
    </div>
  );
}
