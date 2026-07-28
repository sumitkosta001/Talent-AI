'use client';

import React from 'react';
import { MOCK_ACTIVITIES } from '@/mock/activity';
import { Activity, Clock } from 'lucide-react';

export default function ActivityTimeline() {
  return (
    <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-4 text-left text-[#0F172A]">
      <h3 className="font-bold text-sm sm:text-base border-b border-[#F1F5F9] pb-3 flex items-center gap-1.5">
        <Activity size={16} className="text-[#2563EB]" />
        Activity Feed Log
      </h3>

      <div className="space-y-4">
        {MOCK_ACTIVITIES.map((act) => (
          <div key={act.id} className="flex gap-3 text-xs sm:text-sm font-semibold">
            <div className="p-1.5 bg-[#F1F5F9] rounded-lg text-[#64748B] flex-shrink-0 self-start">
              <Clock size={14} />
            </div>
            <div className="space-y-0.5">
              <p className="text-[#0F172A] leading-normal">{act.description}</p>
              <span className="text-[10px] text-slate-400 font-bold block">{act.timestamp}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
