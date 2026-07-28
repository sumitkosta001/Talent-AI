'use client';

import React from 'react';
import { Star, ShieldAlert } from 'lucide-react';
import CircularProgress from '../ats/CircularProgress';

interface JobMatchCardProps {
  score: number;
}

export default function JobMatchCard({ score }: JobMatchCardProps) {
  const getRating = (val: number) => {
    if (val >= 90) return { label: 'Excellent Match', color: 'text-green-600', bg: 'bg-green-50/50 border-green-200' };
    if (val >= 75) return { label: 'Good Match', color: 'text-blue-600', bg: 'bg-blue-50/50 border-blue-200' };
    if (val >= 50) return { label: 'Average Match', color: 'text-amber-600', bg: 'bg-amber-50/50 border-amber-200' };
    return { label: 'Needs Improvement', color: 'text-red-600', bg: 'bg-red-50/50 border-red-200' };
  };

  const level = getRating(score);

  return (
    <div className={`p-5 rounded-2xl border text-left flex items-center gap-4 ${level.bg}`}>
      <CircularProgress
        score={score}
        size={80}
        strokeWidth={8}
        color={score >= 90 ? '#22C55E' : score >= 75 ? '#2563EB' : '#F59E0B'}
      />
      <div>
        <h4 className={`font-bold text-sm ${level.color}`}>{level.label}</h4>
        <p className="text-xs text-[#64748B] mt-0.5 leading-relaxed">
          Your profile matches {score}% of the requirements listed for this position.
        </p>
      </div>
    </div>
  );
}
