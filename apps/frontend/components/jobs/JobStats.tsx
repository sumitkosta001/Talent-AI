'use client';

import React from 'react';

interface JobStatsProps {
  postedDate: string;
  status?: string;
  workMode?: string;
  deadline?: string;
  applicantsCount?: number;
}

export default function JobStats({
  postedDate,
  status,
  workMode,
  deadline,
  applicantsCount,
}: JobStatsProps) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-center bg-[#F8FAFC] border border-[#E2E8F0] p-4 rounded-xl text-xs font-semibold">
      <div>
        <p className="text-[#0F172A] text-sm font-bold">{postedDate}</p>
        <p className="text-[10px] text-[#64748B]">Posted Date</p>
      </div>
      <div>
        <p className="text-[#0F172A] text-sm font-bold capitalize">{status?.toLowerCase() || 'Published'}</p>
        <p className="text-[10px] text-[#64748B]">Status</p>
      </div>
      <div className="col-span-2 sm:col-span-1">
        <p className="text-[#0F172A] text-sm font-bold truncate max-w-full">
          {workMode || (applicantsCount !== undefined ? `${applicantsCount}` : deadline || 'Active')}
        </p>
        <p className="text-[10px] text-[#64748B]">
          {workMode ? 'Work Mode' : (applicantsCount !== undefined ? 'Applicants' : 'Deadline')}
        </p>
      </div>
    </div>
  );
}
