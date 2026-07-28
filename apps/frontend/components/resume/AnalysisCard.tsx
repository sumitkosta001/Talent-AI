import React from 'react';

interface AnalysisCardProps {
  icon: string | React.ReactNode;
  label: string;
  score: number;
  description: string;
  color?: string;
}

export default function AnalysisCard({
  icon,
  label,
  score,
  description,
  color = 'bg-blue-500',
}: AnalysisCardProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 hover:shadow-sm transition-all duration-200">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2.5">
          <span className="text-xl flex items-center justify-center">{icon}</span>
          <h3 className="font-semibold text-[#0F172A] text-sm sm:text-base">{label}</h3>
        </div>
        <span className="text-sm font-bold text-[#0F172A]">{score}%</span>
      </div>
      <p className="text-xs text-[#64748B] leading-relaxed mb-4">{description}</p>
      <div className="w-full h-2 bg-[#F1F5F9] rounded-full overflow-hidden">
        <div
          className={`h-full ${color} rounded-full transition-all duration-500`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  );
}
