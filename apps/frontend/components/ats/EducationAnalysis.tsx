'use client';

import React from 'react';
import { GraduationCap, AlertCircle } from 'lucide-react';
import { EducationAnalysis as EducationType } from '@/types/ats';

interface EducationAnalysisProps {
  education: EducationType;
}

export default function EducationAnalysis({ education }: EducationAnalysisProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-start gap-3">
        <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center flex-shrink-0">
          <GraduationCap size={20} />
        </div>
        <div>
          <h4 className="font-bold text-sm text-[#0F172A]">{education.degree}</h4>
          <p className="text-xs text-[#64748B] font-medium mt-0.5">{education.university} · GPA {education.cgpa}</p>
        </div>
      </div>

      <div>
        <p className="text-xs font-bold text-[#64748B] mb-2 uppercase tracking-wide">Relevant Coursework</p>
        <div className="flex flex-wrap gap-1.5">
          {education.relevantCoursework.map(c => (
            <span key={c} className="text-xs bg-[#F8FAFC] border border-[#E2E8F0] text-[#64748B] px-2 py-1 rounded-md">{c}</span>
          ))}
        </div>
      </div>

      {education.suggestions.map((s, i) => (
        <div key={i} className="flex gap-2 p-3 bg-amber-50 border border-amber-100 rounded-xl text-xs text-amber-800">
          <AlertCircle size={14} className="text-amber-500 mt-0.5 flex-shrink-0" />
          <span>{s}</span>
        </div>
      ))}
    </div>
  );
}
