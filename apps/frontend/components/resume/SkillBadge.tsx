import React from 'react';
import { Skill } from '../../types/resume';

interface SkillBadgeProps {
  skill: string | Skill;
  isMissing?: boolean;
}

export default function SkillBadge({ skill, isMissing = false }: SkillBadgeProps) {
  const name = typeof skill === 'string' ? skill : skill.name;
  const type = typeof skill === 'string' ? 'technical' : skill.type;

  let colorClasses = 'bg-blue-50 text-[#2563EB] border-blue-100';
  if (isMissing) {
    colorClasses = 'bg-red-50 text-[#EF4444] border-red-100';
  } else if (type === 'soft') {
    colorClasses = 'bg-emerald-50 text-emerald-700 border-emerald-100';
  } else if (type === 'tool') {
    colorClasses = 'bg-violet-50 text-violet-700 border-violet-100';
  } else if (type === 'framework') {
    colorClasses = 'bg-indigo-50 text-indigo-700 border-indigo-100';
  }

  return (
    <span
      className={`inline-flex items-center text-xs font-medium px-3 py-1 rounded-full border ${colorClasses} transition-all duration-200 hover:scale-105`}
    >
      {name}
    </span>
  );
}
