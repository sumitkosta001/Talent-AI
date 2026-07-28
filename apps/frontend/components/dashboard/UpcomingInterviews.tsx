'use client';

import React from 'react';
import { UpcomingInterview } from '@/types/dashboard';
import InterviewCard from './InterviewCard';

interface UpcomingInterviewsProps {
  interviews: UpcomingInterview[];
}

export default function UpcomingInterviews({ interviews }: UpcomingInterviewsProps) {
  return (
    <div className="bg-white rounded-3xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left flex flex-col h-full">
      <div className="border-b border-[#F1F5F9] pb-3">
        <h3 className="font-bold text-[#0F172A] text-base sm:text-lg">Upcoming Interviews</h3>
        <p className="text-xs text-[#64748B] mt-0.5">Prepare with our mock tools before joining the call</p>
      </div>

      <div className="space-y-3 flex-1 overflow-y-auto max-h-[380px] pr-1">
        {interviews.map((item) => (
          <InterviewCard key={item.id} item={item} />
        ))}
      </div>
    </div>
  );
}
