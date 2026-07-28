'use client';

import React from 'react';
import { CheckCircle2, AlertCircle } from 'lucide-react';

interface ProfileCompletionProps {
  percentage: number;
}

export default function ProfileCompletion({ percentage }: ProfileCompletionProps) {
  const missing = [
    'Add LeetCode social profile URL link.',
    'Add alternate contact numbers.',
  ];

  return (
    <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-4 text-left text-[#0F172A]">
      <div className="flex items-center justify-between border-b border-[#F1F5F9] pb-2">
        <h4 className="font-bold text-xs uppercase tracking-wide text-[#64748B]">Profile Completeness</h4>
        <span className="text-xs font-black text-blue-600 bg-blue-50 px-2 py-0.5 rounded-full border border-blue-100">{percentage}% Complete</span>
      </div>

      <div className="space-y-3.5">
        <div className="h-2 bg-[#F1F5F9] rounded-full overflow-hidden">
          <div className="h-full bg-blue-600 rounded-full" style={{ width: `${percentage}%` }} />
        </div>

        {/* Suggestion list */}
        <div className="space-y-2 text-[11px] font-semibold text-[#64748B]">
          {missing.map((text) => (
            <div key={text} className="flex items-start gap-1.5">
              <AlertCircle size={13} className="text-amber-500 flex-shrink-0 mt-0.5" />
              <p className="leading-relaxed">{text}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
