'use client';

import React from 'react';
import { Check, Loader, Circle } from 'lucide-react';
import { Timeline } from '@/types/ats';

interface TimelineCardProps {
  step: Timeline;
  isLast?: boolean;
}

export default function TimelineCard({ step, isLast = false }: TimelineCardProps) {
  const { title, description, status } = step;

  const statusIcons = {
    completed: (
      <div className="w-8 h-8 rounded-full bg-green-500 border-2 border-white text-white flex items-center justify-center shadow-sm">
        <Check size={14} />
      </div>
    ),
    'in-progress': (
      <div className="w-8 h-8 rounded-full bg-blue-500 border-2 border-white text-white flex items-center justify-center shadow-sm animate-pulse">
        <Loader size={14} className="animate-spin" />
      </div>
    ),
    pending: (
      <div className="w-8 h-8 rounded-full bg-slate-100 border-2 border-slate-300 text-slate-400 flex items-center justify-center shadow-sm">
        <Circle size={10} />
      </div>
    ),
  };

  return (
    <div className="relative flex gap-4">
      {/* Node indicator */}
      <div className="flex flex-col items-center flex-shrink-0">
        <div className="z-10">{statusIcons[status]}</div>
        {!isLast && <div className="w-0.5 flex-1 bg-[#E2E8F0] mt-1.5 -mb-1.5" />}
      </div>

      {/* Detail contents */}
      <div className="pb-6">
        <h4 className={`text-sm font-bold ${
          status === 'completed'
            ? 'text-slate-500 line-through'
            : status === 'in-progress'
            ? 'text-blue-600'
            : 'text-[#0F172A]'
        }`}>
          Step {step.step}: {title}
        </h4>
        <p className="text-xs text-[#64748B] mt-0.5 leading-relaxed">{description}</p>
      </div>
    </div>
  );
}
