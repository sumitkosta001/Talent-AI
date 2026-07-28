'use client';

import React from 'react';
import { Check, Calendar } from 'lucide-react';

interface TimelineStep {
  stage: string;
  date: string;
  completed: boolean;
  notes?: string;
}

interface JobTimelineProps {
  timeline: TimelineStep[];
}

export default function JobTimeline({ timeline }: JobTimelineProps) {
  return (
    <div className="space-y-4">
      <h4 className="font-bold text-xs text-[#64748B] uppercase tracking-wide">Application Progress History</h4>
      <div className="relative pl-6 space-y-4">
        {timeline.map((step, idx) => (
          <div key={idx} className="relative">
            {/* Connector line */}
            {idx < timeline.length - 1 && (
              <div className="absolute left-[-17px] top-6 bottom-[-20px] w-0.5 bg-slate-200" />
            )}
            
            {/* Step node indicator */}
            <div className={`absolute left-[-23px] top-1.5 w-3.5 h-3.5 rounded-full flex items-center justify-center border-2 ${
              step.completed
                ? 'bg-blue-600 border-white text-white shadow-sm'
                : 'bg-white border-slate-300'
            }`}>
              {step.completed && <Check size={8} className="stroke-[3]" />}
            </div>

            {/* Step details content */}
            <div>
              <div className="flex items-center gap-2">
                <span className={`text-xs font-bold ${step.completed ? 'text-[#0F172A]' : 'text-[#64748B]'}`}>
                  {step.stage}
                </span>
                <span className="text-[9px] bg-slate-100 text-[#64748B] font-semibold px-1.5 py-0.2 rounded flex items-center gap-0.5">
                  <Calendar size={8} />
                  {step.date}
                </span>
              </div>
              {step.notes && <p className="text-[10px] text-[#64748B] mt-0.5">{step.notes}</p>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
