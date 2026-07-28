'use client';

import React from 'react';
import { TrendingUp, Award, Clock } from 'lucide-react';
import ATSProgressRing from './ATSProgressRing';

interface ATSScoreCardProps {
  score: {
    overall: number;
    keywordMatch: number;
    experience: number;
    skills: number;
  };
  keywordsCount: { matched: number; total: number };
  experienceYears: number;
  missingSkillsCount: number;
}

export default function ATSScoreCard({
  score,
  keywordsCount,
  experienceYears,
  missingSkillsCount,
}: ATSScoreCardProps) {
  const getRating = (val: number) => {
    if (val >= 90) return { label: 'Excellent Score', color: 'bg-green-50 text-[#22C55E]' };
    if (val >= 75) return { label: 'Good Score', color: 'bg-blue-50 text-[#2563EB]' };
    if (val >= 50) return { label: 'Average Score', color: 'bg-amber-50 text-[#F59E0B]' };
    return { label: 'Poor Score', color: 'bg-red-50 text-[#EF4444]' };
  };

  const rating = getRating(score.overall);

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 flex flex-col md:flex-row items-center gap-8 shadow-sm">
      <ATSProgressRing score={score.overall} />
      
      <div className="flex-1">
        <div className={`inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full mb-3 ${rating.color}`}>
          <TrendingUp size={12} />
          {rating.label}
        </div>
        <h2 className="text-xl font-bold text-[#0F172A] mb-2">Your resume is highly optimized</h2>
        <p className="text-[#64748B] text-sm mb-4 leading-relaxed">
          Your score ranks in the top 5% of candidates. Your resume effectively aligns with primary industry parser filters, standard formatting indexes, and technical tags.
        </p>

        <div className="grid grid-cols-3 gap-4 border-t border-[#F1F5F9] pt-4">
          <div className="text-center md:text-left">
            <p className="text-lg font-bold text-[#22C55E]">{keywordsCount.matched}/{keywordsCount.total}</p>
            <p className="text-xs text-[#64748B] font-medium">Keywords Match</p>
          </div>
          <div className="text-center md:text-left">
            <p className="text-lg font-bold text-[#2563EB]">{experienceYears} Years</p>
            <p className="text-xs text-[#64748B] font-medium">Experience</p>
          </div>
          <div className="text-center md:text-left">
            <p className="text-lg font-bold text-[#EF4444]">{missingSkillsCount}</p>
            <p className="text-xs text-[#64748B] font-medium">Missing Skills</p>
          </div>
        </div>
      </div>
    </div>
  );
}
