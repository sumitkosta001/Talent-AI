'use client';

import React from 'react';
import { AlertCircle } from 'lucide-react';

interface WeaknessItem {
  title: string;
  description: string;
}

interface WeaknessCardProps {
  weaknesses: WeaknessItem[];
}

export default function WeaknessCard({ weaknesses }: WeaknessCardProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
      <h3 className="font-semibold text-[#0F172A] flex items-center gap-2">
        <AlertCircle className="text-red-500" size={18} />
        Critical Weaknesses
      </h3>
      <div className="space-y-3">
        {weaknesses.map(({ title, description }) => (
          <div key={title} className="p-3 bg-red-50/30 border border-red-100 rounded-xl">
            <h4 className="text-xs font-bold text-red-950">{title}</h4>
            <p className="text-[11px] text-red-800/80 mt-0.5">{description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
