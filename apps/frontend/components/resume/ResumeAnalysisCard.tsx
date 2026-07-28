import React from 'react';

interface ResumeAnalysisCardProps {
  score: number;
  skillsScore: number;
  experienceScore: number;
  educationScore: number;
}

export default function ResumeAnalysisCard({
  score,
  skillsScore,
  experienceScore,
  educationScore,
}: ResumeAnalysisCardProps) {
  return (
    <div className="bg-gradient-to-r from-[#2563EB] to-[#7C3AED] rounded-2xl p-6 text-white flex flex-col sm:flex-row items-center justify-between gap-6 shadow-md">
      <div>
        <p className="text-blue-200 text-sm mb-1">Overall Resume Score</p>
        <p className="text-4xl font-bold mb-1">
          {score}<span className="text-2xl">/100</span>
        </p>
        <p className="text-blue-200 text-sm">
          {score >= 90
            ? 'Excellent — Top 5% of candidates'
            : score >= 80
            ? 'Very Good — passes most screens'
            : 'Good — potential for optimization'}
        </p>
      </div>
      <div className="flex items-center gap-6 sm:gap-8">
        {[
          { label: 'Skills', val: skillsScore },
          { label: 'Experience', val: experienceScore },
          { label: 'Education', val: educationScore },
        ].map(({ label, val }) => (
          <div key={label} className="text-center">
            <p className="text-2xl font-bold text-white">{val}%</p>
            <p className="text-xs text-blue-200 font-medium">{label}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
