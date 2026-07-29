'use client';

import React from 'react';
import { Award, Eye, ShieldCheck } from 'lucide-react';

interface CultureValue {
  title: string;
  desc: string;
}

interface CompanyCultureProps {
  culture: CultureValue[];
}

export default function CompanyCulture({ culture }: CompanyCultureProps) {
  const icons = [Award, Eye, ShieldCheck];

  return (
    <div className="space-y-5 text-left text-[#0F172A]">
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm">
        <h3 className="font-bold text-sm sm:text-base mb-1">Company Culture & Values</h3>
        <p className="text-xs text-[#64748B] font-semibold">How we collaborate, solve information obstacles, and design next-generation economic tools.</p>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {culture.map((val, idx) => {
          const Icon = icons[idx % icons.length];
          return (
            <div key={val.title} className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-3">
              <div className="w-9 h-9 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center border border-blue-100 flex-shrink-0">
                <Icon size={16} />
              </div>
              <h4 className="font-bold text-sm text-[#0F172A]">{val.title}</h4>
              <p className="text-xs text-slate-600 leading-relaxed font-semibold">{val.desc}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
