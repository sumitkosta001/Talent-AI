'use client';

import React from 'react';
import { Calendar, Users, Eye } from 'lucide-react';

interface JobStatsProps {
  postedDate: string;
  deadline?: string;
  applicantsCount?: number;
}

export default function JobStats({
  postedDate,
  deadline = 'Open until filled',
  applicantsCount = 12,
}: JobStatsProps) {
  return (
    <div className="grid grid-cols-3 gap-3 text-center bg-[#F8FAFC] border border-[#E2E8F0] p-4 rounded-xl text-xs font-semibold">
      <div>
        <p className="text-[#0F172A] text-sm font-bold">{postedDate}</p>
        <p className="text-[10px] text-[#64748B]">Posted Date</p>
      </div>
      <div>
        <p className="text-[#0F172A] text-sm font-bold">{applicantsCount}</p>
        <p className="text-[10px] text-[#64748B]">Applicants</p>
      </div>
      <div>
        <p className="text-[#0F172A] text-sm font-bold truncate max-w-full">{deadline}</p>
        <p className="text-[10px] text-[#64748B]">Deadline</p>
      </div>
    </div>
  );
}
