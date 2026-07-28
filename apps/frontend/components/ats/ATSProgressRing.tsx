'use client';

import React from 'react';
import CircularProgress from './CircularProgress';

interface ATSProgressRingProps {
  score: number;
}

export default function ATSProgressRing({ score }: ATSProgressRingProps) {
  let color = '#EF4444'; // Red
  if (score >= 90) color = '#22C55E'; // Green
  else if (score >= 75) color = '#2563EB'; // Blue
  else if (score >= 50) color = '#F59E0B'; // Amber

  return (
    <div className="relative flex items-center justify-center p-3 bg-[#F8FAFC] rounded-2xl border border-[#E2E8F0] flex-shrink-0">
      <CircularProgress
        score={score}
        size={140}
        strokeWidth={12}
        color={color}
        backgroundColor="#E2E8F0"
      />
    </div>
  );
}
