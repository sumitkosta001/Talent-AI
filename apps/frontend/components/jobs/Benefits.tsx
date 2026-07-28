'use client';

import React from 'react';
import { Benefit } from '@/types/job';

interface BenefitsProps {
  items?: Benefit[];
}

export default function Benefits({ items = [] }: BenefitsProps) {
  if (items.length === 0) return null;

  return (
    <div className="space-y-4 text-left">
      <h3 className="font-bold text-sm text-[#0F172A] uppercase tracking-wide">Perks & Benefits</h3>
      <div className="grid sm:grid-cols-3 gap-4">
        {items.map((benefit, idx) => (
          <div key={idx} className="bg-[#F8FAFC] border border-[#E2E8F0] p-4 rounded-xl flex items-start gap-3">
            <span className="text-xl flex-shrink-0">{benefit.icon}</span>
            <div>
              <p className="font-bold text-xs text-[#0F172A]">{benefit.label}</p>
              <p className="text-[10px] text-[#64748B] mt-0.5 leading-relaxed">{benefit.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
