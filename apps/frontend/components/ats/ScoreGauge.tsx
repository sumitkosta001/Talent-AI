'use client';

import React from 'react';
import CircularProgress from './CircularProgress';

interface ScoreGaugeProps {
  label: string;
  score: number;
  description?: string;
  color?: string;
}

export default function ScoreGauge({
  label,
  score,
  description,
  color = '#2563EB',
}: ScoreGaugeProps) {
  return (
    <div className="bg-[#F8FAFC] border border-[#E2E8F0] p-4 rounded-2xl flex items-center gap-4">
      <CircularProgress
        score={score}
        size={80}
        strokeWidth={8}
        color={color}
      />
      <div>
        <h4 className="font-bold text-sm text-[#0F172A]">{label}</h4>
        {description && <p className="text-xs text-[#64748B] mt-0.5 leading-relaxed">{description}</p>}
      </div>
    </div>
  );
}
