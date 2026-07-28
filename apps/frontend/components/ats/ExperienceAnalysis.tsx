'use client';

import React from 'react';
import { Briefcase, AlertCircle, Award } from 'lucide-react';
import { ExperienceAnalysis as ExpType } from '@/types/ats';

interface ExperienceAnalysisProps {
  experience: ExpType;
}

export default function ExperienceAnalysis({ experience }: ExperienceAnalysisProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-start gap-3">
        <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center flex-shrink-0">
          <Briefcase size={20} />
        </div>
        <div>
          <h4 className="font-bold text-sm text-[#0F172A]">{experience.years} Years Total Experience</h4>
          <p className="text-xs text-[#64748B] font-medium mt-0.5">{experience.leadership}</p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-3 bg-[#F8FAFC] border border-[#E2E8F0] p-3 rounded-xl text-center">
        <div>
          <p className="text-sm font-bold text-[#0F172A]">{experience.achievementsCount}</p>
          <p className="text-[10px] text-[#64748B]">Achievements</p>
        </div>
        <div>
          <p className="text-sm font-bold text-[#0F172A]">{experience.quantifiedResultsCount}</p>
          <p className="text-[10px] text-[#64748B]">Quantified Metrics</p>
        </div>
        <div>
          <p className="text-sm font-bold text-[#0F172A]">{experience.actionVerbsCount}</p>
          <p className="text-[10px] text-[#64748B]">Action Verbs</p>
        </div>
      </div>

      {experience.suggestions.map((s, i) => (
        <div key={i} className="flex gap-2 p-3 bg-amber-50 border border-amber-100 rounded-xl text-xs text-amber-800">
          <AlertCircle size={14} className="text-amber-500 mt-0.5 flex-shrink-0" />
          <span>{s}</span>
        </div>
      ))}
    </div>
  );
}
