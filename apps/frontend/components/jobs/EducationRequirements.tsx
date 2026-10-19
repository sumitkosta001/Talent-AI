'use client';

import React from 'react';
import { GraduationCap } from 'lucide-react';

interface EducationRequirementsProps {
  items?: string[];
}

export default function EducationRequirements({ items = [] }: EducationRequirementsProps) {
  const safeItems = Array.isArray(items) ? items.filter(Boolean) : [];
  if (safeItems.length === 0) return null;

  return (
    <div className="space-y-3 text-left">
      <div className="flex items-center gap-2">
        <GraduationCap size={16} className="text-[#64748B]" />
        <h3 className="font-bold text-sm text-[#0F172A] uppercase tracking-wide">Education Requirements</h3>
      </div>
      <ul className="list-disc pl-5 space-y-2 text-xs sm:text-sm text-[#64748B] leading-relaxed">
        {safeItems.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
