'use client';

import React from 'react';

interface SkillsRequiredProps {
  skills?: string[];
}

export default function SkillsRequired({ skills = [] }: SkillsRequiredProps) {
  const safeSkills = Array.isArray(skills) ? skills.filter(Boolean) : [];

  return (
    <div className="space-y-2 text-left">
      <span className="block text-xs font-bold text-[#64748B] uppercase tracking-wide">
        Required Skills & Technologies
      </span>
      {safeSkills.length > 0 ? (
        <div className="flex flex-wrap gap-2">
          {safeSkills.map(skill => (
            <span
              key={skill}
              className="text-xs bg-[#F1F5F9] border border-[#E2E8F0] text-[#0F172A] px-3 py-1.5 rounded-xl font-semibold"
            >
              {skill}
            </span>
          ))}
        </div>
      ) : (
        <p className="text-xs text-[#94A3B8] italic">No specific skills listed.</p>
      )}
    </div>
  );
}
