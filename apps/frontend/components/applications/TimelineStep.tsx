'use client';

import React from 'react';
import { Check, Clock, User, AlertCircle, Award } from 'lucide-react';
import { ApplicationTimeline } from '@/types/application';

interface TimelineStepProps {
  timeline: ApplicationTimeline[];
}

export default function TimelineStep({ timeline }: TimelineStepProps) {
  const getIcon = (status: string) => {
    switch (status) {
      case 'Offer Received':
      case 'Offer Accepted':
        return <Award size={13} className="text-emerald-600" />;
      case 'Rejected':
        return <AlertCircle size={13} className="text-red-600" />;
      case 'Application Viewed':
        return <User size={13} className="text-blue-600" />;
      default:
        return <Check size={13} className="text-blue-600" />;
    }
  };

  const getBorderColor = (status: string) => {
    switch (status) {
      case 'Offer Received':
      case 'Offer Accepted':
        return 'border-emerald-500 bg-emerald-50';
      case 'Rejected':
        return 'border-red-500 bg-red-50';
      default:
        return 'border-blue-500 bg-blue-50';
    }
  };

  return (
    <div className="relative pl-6 space-y-5 text-left">
      {/* Central line */}
      <div className="absolute left-[9px] top-2 bottom-2 w-0.5 bg-slate-200" />

      {timeline.map((step, idx) => (
        <div key={idx} className="relative flex flex-col sm:flex-row sm:items-start justify-between gap-2">
          {/* Node node marker */}
          <div className={`absolute left-[-23px] top-1 w-5.5 h-5.5 rounded-full flex items-center justify-center border-2 ${
            step.completed
              ? getBorderColor(step.status)
              : 'bg-white border-slate-300'
          }`}>
            {getIcon(step.status)}
          </div>

          <div>
            <h4 className="font-bold text-[#0F172A] text-xs sm:text-sm">{step.status}</h4>
            <p className="text-xs text-[#64748B] mt-0.5 max-w-xl leading-relaxed">{step.description}</p>
          </div>

          <div className="flex items-center gap-1.5 flex-shrink-0 text-[10px] sm:text-xs text-[#64748B] font-semibold bg-[#F8FAFC] border border-[#E2E8F0] px-2 py-0.5 rounded-md h-fit">
            <Clock size={11} />
            <span>{step.date} {step.time ? `· ${step.time}` : ''}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
