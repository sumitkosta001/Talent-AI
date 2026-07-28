import React from 'react';
import { CheckCircle } from 'lucide-react';

interface StrengthCardProps {
  strengths: string[];
}

export default function StrengthCard({ strengths }: StrengthCardProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5">
      <h3 className="font-semibold text-[#0F172A] mb-4">Resume Strengths</h3>
      <div className="space-y-3">
        {strengths.map((str, idx) => (
          <div key={idx} className="flex items-start gap-3 p-3 bg-green-50/50 rounded-xl border border-green-100">
            <CheckCircle size={16} className="text-[#22C55E] mt-0.5 flex-shrink-0" />
            <p className="text-xs sm:text-sm text-green-800 leading-relaxed">{str}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
