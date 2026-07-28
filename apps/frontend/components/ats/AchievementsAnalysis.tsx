'use client';

import React from 'react';
import { Trophy, Shield } from 'lucide-react';

export default function AchievementsAnalysis() {
  const items = [
    { title: 'Smart India Hackathon Finalist', val: 'Listed in Achievements section.' },
    { title: 'TCS CodeVita Round 2 Qualifier', val: 'Provides competitive programming validity.' },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-start gap-3">
        <div className="w-10 h-10 rounded-xl bg-violet-50 text-violet-600 flex items-center justify-center flex-shrink-0">
          <Trophy size={20} />
        </div>
        <div>
          <h4 className="font-bold text-sm text-[#0F172A]">Awards & Competitions</h4>
          <p className="text-xs text-[#64748B] font-medium mt-0.5">Proof of competitive excellence</p>
        </div>
      </div>

      <div className="space-y-2">
        {items.map(({ title, val }) => (
          <div key={title} className="p-3 bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl">
            <p className="text-xs font-bold text-[#0F172A]">{title}</p>
            <p className="text-[11px] text-[#64748B] mt-0.5">{val}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
