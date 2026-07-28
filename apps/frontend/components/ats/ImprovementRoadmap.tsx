'use client';

import React from 'react';
import { Timeline } from '@/types/ats';
import TimelineCard from './TimelineCard';

interface ImprovementRoadmapProps {
  timeline: Timeline[];
}

export default function ImprovementRoadmap({ timeline }: ImprovementRoadmapProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-6">
      <div>
        <h2 className="font-semibold text-lg text-[#0F172A]">Optimization Roadmap</h2>
        <p className="text-xs text-[#64748B] mt-0.5">Follow this structured plan to maximize your resume score value.</p>
      </div>

      <div className="flex flex-col pt-2">
        {timeline.map((step, index) => (
          <TimelineCard
            key={step.step}
            step={step}
            isLast={index === timeline.length - 1}
          />
        ))}
      </div>
    </div>
  );
}
