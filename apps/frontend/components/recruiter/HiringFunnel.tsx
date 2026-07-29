'use client';

import React from 'react';
import { HiringFunnelStep } from '@/types/recruiter';

interface HiringFunnelProps {
  funnel: HiringFunnelStep[];
}

export default function HiringFunnel({ funnel }: HiringFunnelProps) {
  const maxCount = funnel.length > 0 ? funnel[0].count : 1;

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
      <div>
        <h3 className="font-bold text-[#0F172A] text-sm sm:text-base">Hiring Funnel Status</h3>
        <p className="text-xs text-[#64748B] mt-0.5">Distribution of candidates across hiring pipelines.</p>
      </div>

      <div className="space-y-3.5">
        {funnel.map(({ stage, count }) => {
          const widthPct = Math.max(8, Math.round((count / maxCount) * 100));
          return (
            <div key={stage} className="space-y-1 text-xs">
              <div className="flex items-center justify-between font-semibold">
                <span className="text-slate-700">{stage}</span>
                <span className="text-[#0F172A] font-bold">{count} candidates</span>
              </div>
              <div className="h-2 w-full bg-slate-50 border border-slate-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-blue-600 rounded-full transition-all duration-500"
                  style={{ width: `${widthPct}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
