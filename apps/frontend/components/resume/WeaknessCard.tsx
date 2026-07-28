import React from 'react';
import { AlertCircle } from 'lucide-react';

interface WeaknessCardProps {
  weaknesses: string[];
}

export default function WeaknessCard({ weaknesses }: WeaknessCardProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5">
      <h3 className="font-semibold text-[#0F172A] mb-4">Areas of Improvement</h3>
      <div className="space-y-3">
        {weaknesses.map((weak, idx) => (
          <div key={idx} className="flex items-start gap-3 p-3 bg-red-50/50 rounded-xl border border-red-100">
            <AlertCircle size={16} className="text-[#EF4444] mt-0.5 flex-shrink-0" />
            <p className="text-xs sm:text-sm text-red-800 leading-relaxed">{weak}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
