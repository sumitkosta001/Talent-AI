'use client';

import React from 'react';

interface SkillsRequiredProps {
  skills: string[];
}

export default function SkillsRequired({ skills }: SkillsRequiredProps) {
  return (
    <div className="space-y-2 text-left">
      <span className="block text-xs font-bold text-[#64748B] uppercase tracking-wide">Required Skills & Technologies</span>
      <div className="flex flex-wrap gap-2">
        {skills.map(skill => (
          <span key={skill} className="text-xs bg-[#F1F5F9] border border-[#E2E8F0] text-[#0F172A] px-3 py-1.5 rounded-xl font-semibold">
            {skill}
          </span>
        ))}
      </div>
    </div>
  );
}
