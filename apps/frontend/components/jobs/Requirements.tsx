'use client';

import React from 'react';

interface RequirementsProps {
  items?: string[];
}

export default function Requirements({ items = [] }: RequirementsProps) {
  if (items.length === 0) return null;

  return (
    <div className="space-y-3 text-left">
      <h3 className="font-bold text-sm text-[#0F172A] uppercase tracking-wide">Qualifications & Requirements</h3>
      <ul className="list-disc pl-5 space-y-2 text-xs sm:text-sm text-[#64748B] leading-relaxed">
        {items.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
