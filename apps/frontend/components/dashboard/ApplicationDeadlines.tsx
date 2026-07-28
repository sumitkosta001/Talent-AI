'use client';

import React from 'react';
import { ApplicationDeadline } from '@/types/dashboard';
import DeadlineCard from './DeadlineCard';

interface ApplicationDeadlinesProps {
  deadlines: ApplicationDeadline[];
}

export default function ApplicationDeadlines({ deadlines }: ApplicationDeadlinesProps) {
  // Sort by daysRemaining ascending
  const sorted = [...deadlines].sort((a, b) => a.daysRemaining - b.daysRemaining);

  const getPriorityColor = (p: ApplicationDeadline['priority']) => {
    if (p === 'High') return 'text-rose-600 bg-rose-50 border-rose-100';
    if (p === 'Medium') return 'text-amber-600 bg-amber-50 border-amber-100';
    return 'text-blue-600 bg-blue-50 border-blue-100';
  };

  return (
    <div className="bg-white rounded-3xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left flex flex-col h-full">
      <div className="border-b border-[#F1F5F9] pb-3">
        <h3 className="font-bold text-[#0F172A] text-base sm:text-lg">Application Deadlines</h3>
        <p className="text-xs text-[#64748B] mt-0.5">Keep track of priority closes and take-home deadlines</p>
      </div>

      <div className="space-y-3 flex-1 overflow-y-auto max-h-[380px] pr-1">
        {sorted.map((item) => (
          <DeadlineCard key={item.id} item={item} getPriorityColor={getPriorityColor} />
        ))}
      </div>
    </div>
  );
}
