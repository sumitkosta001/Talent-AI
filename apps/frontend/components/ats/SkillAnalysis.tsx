'use client';

import React from 'react';
import { Award, Star, TrendingUp, AlertCircle } from 'lucide-react';
import { SkillAnalysis as SkillType } from '@/types/ats';

interface SkillAnalysisProps {
  skills: SkillType;
}

export default function SkillAnalysis({ skills }: SkillAnalysisProps) {
  return (
    <div className="space-y-5">
      <div>
        <h4 className="font-bold text-sm text-[#0F172A] mb-2 flex items-center gap-1.5"><Star size={15} className="text-blue-500" /> Extracted Skills</h4>
        <div className="flex flex-wrap gap-2">
          {skills.technical.map(s => (
            <span key={s} className="text-xs bg-[#F8FAFC] border border-[#E2E8F0] text-slate-700 px-2.5 py-1.5 rounded-lg font-medium">{s}</span>
          ))}
        </div>
      </div>

      <div className="grid sm:grid-cols-2 gap-4">
        <div className="p-4 bg-red-50/50 border border-red-100 rounded-2xl">
          <h5 className="font-bold text-xs text-red-700 mb-2.5 flex items-center gap-1.5">
            <AlertCircle size={14} /> Missing Tech Skills
          </h5>
          <div className="flex flex-wrap gap-1.5">
            {skills.missing.map(s => (
              <span key={s} className="text-[11px] font-semibold bg-red-100 text-red-700 px-2 py-1 rounded-md">{s}</span>
            ))}
          </div>
        </div>

        <div className="p-4 bg-blue-50/50 border border-blue-100 rounded-2xl">
          <h5 className="font-bold text-xs text-blue-700 mb-2.5 flex items-center gap-1.5">
            <TrendingUp size={14} /> Recommended Trending Skills
          </h5>
          <div className="flex flex-wrap gap-1.5">
            {skills.recommended.map(s => (
              <span key={s} className="text-[11px] font-semibold bg-blue-100 text-blue-700 px-2 py-1 rounded-md">{s}</span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
