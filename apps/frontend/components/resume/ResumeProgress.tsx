import React from 'react';

interface ResumeProgressProps {
  percentage: number;
  type?: 'bar' | 'circle';
  size?: number;
  strokeWidth?: number;
}

export default function ResumeProgress({
  percentage,
  type = 'bar',
  size = 120,
  strokeWidth = 8,
}: ResumeProgressProps) {
  if (type === 'circle') {
    const radius = (size - strokeWidth) / 2;
    const circumference = 2 * Math.PI * radius;
    const strokeDashoffset = circumference - (percentage / 100) * circumference;

    return (
      <div className="relative inline-flex items-center justify-center">
        <svg width={size} height={size} className="-rotate-90">
          {/* Background circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="transparent"
            stroke="#E2E8F0"
            strokeWidth={strokeWidth}
          />
          {/* Progress circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="transparent"
            stroke="#2563EB"
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute flex flex-col items-center justify-center">
          <span className="text-2xl font-bold text-[#0F172A]">{percentage}%</span>
          <span className="text-[10px] text-[#64748B] font-semibold uppercase tracking-wider">Complete</span>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full">
      <div className="flex justify-between items-center text-xs font-semibold text-[#64748B] mb-1.5">
        <span>Completion Progress</span>
        <span>{percentage}%</span>
      </div>
      <div className="w-full h-2.5 bg-[#F1F5F9] rounded-full overflow-hidden">
        <div
          className="h-full bg-[#2563EB] rounded-full transition-all duration-1000 ease-out"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
