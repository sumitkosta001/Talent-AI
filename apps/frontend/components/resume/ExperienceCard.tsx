import React from 'react';
import { Experience } from '../../types/resume';

interface ExperienceCardProps {
  experience: Experience;
}

export default function ExperienceCard({ experience }: ExperienceCardProps) {
  const { company, role, duration, description, technologies } = experience;

  return (
    <div className="bg-white rounded-xl border border-[#E2E8F0] p-4 hover:shadow-sm transition-all duration-200">
      <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1 mb-2">
        <h3 className="font-bold text-[#0F172A] text-sm sm:text-base">{role}</h3>
        <span className="text-xs text-[#94A3B8] font-medium">{duration}</span>
      </div>
      <p className="text-xs sm:text-sm text-[#2563EB] font-semibold mb-2">{company}</p>
      <p className="text-xs sm:text-sm text-[#64748B] leading-relaxed mb-3">{description}</p>
      {technologies && technologies.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {technologies.map((tech) => (
            <span
              key={tech}
              className="text-[10px] sm:text-xs bg-[#F8FAFC] border border-[#E2E8F0] text-[#64748B] px-2 py-0.5 rounded-full"
            >
              {tech}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
