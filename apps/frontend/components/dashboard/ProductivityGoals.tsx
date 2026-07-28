'use client';

import React from 'react';
import { ProductivityGoal } from '@/types/dashboard';
import ProgressRing from './ProgressRing';

interface ProductivityGoalsProps {
  goals: ProductivityGoal[];
}

export default function ProductivityGoals({ goals }: ProductivityGoalsProps) {
  return (
    <div className="bg-white rounded-3xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
      <div className="border-b border-[#F1F5F9] pb-3">
        <h3 className="font-bold text-[#0F172A] text-base sm:text-lg">Productivity Goals</h3>
        <p className="text-xs text-[#64748B] mt-0.5">Track your custom target benchmarks and practice</p>
      </div>

      <div className="space-y-4.5">
        {goals.map((item) => {
          const percent = Math.min(100, Math.round((item.current / item.target) * 100));

          return (
            <div
              key={item.id}
              className="flex items-center justify-between gap-4 p-2 border border-transparent hover:border-[#E2E8F0] hover:bg-[#F8FAFC] rounded-2xl transition-all"
            >
              <div className="flex items-center gap-3">
                <ProgressRing percentage={percent} color={item.color} />

                <div className="min-w-0">
                  <span className="font-bold text-[#334155] text-xs sm:text-sm block truncate">
                    {item.title}
                  </span>
                  <span className="text-[10px] text-[#94A3B8] font-bold uppercase tracking-wider block mt-0.5">
                    Target: {item.target} {item.unit || ''}
                  </span>
                </div>
              </div>

              <div className="text-right">
                <span className="text-sm font-black text-[#0F172A]">
                  {item.current}
                </span>
                <span className="text-xs text-[#94A3B8] font-bold">
                  /{item.target}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
