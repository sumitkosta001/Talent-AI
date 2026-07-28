'use client';

import React from 'react';
import { CheckCircle2 } from 'lucide-react';

interface StrengthItem {
  title: string;
  description: string;
}

interface StrengthCardProps {
  strengths: StrengthItem[];
}

export default function StrengthCard({ strengths }: StrengthCardProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
      <h3 className="font-semibold text-[#0F172A] flex items-center gap-2">
        <CheckCircle2 className="text-green-500" size={18} />
        Key Strengths
      </h3>
      <div className="space-y-3">
        {strengths.map(({ title, description }) => (
          <div key={title} className="p-3 bg-green-50/30 border border-green-100 rounded-xl">
            <h4 className="text-xs font-bold text-green-950">{title}</h4>
            <p className="text-[11px] text-green-800/80 mt-0.5">{description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
