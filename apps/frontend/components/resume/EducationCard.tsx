import React from 'react';
import { Education } from '../../types/resume';

interface EducationCardProps {
  education: Education;
}

export default function EducationCard({ education }: EducationCardProps) {
  const { university, degree, gpa, year, location } = education;

  return (
    <div className="bg-white rounded-xl border border-[#E2E8F0] p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:shadow-sm transition-all duration-200">
      <div>
        <h3 className="font-bold text-[#0F172A] text-sm sm:text-base">{degree}</h3>
        <p className="text-xs sm:text-sm text-[#2563EB] font-semibold mt-0.5">{university}</p>
        <p className="text-xs text-[#64748B] mt-1">{location} · Graduation Year: {year}</p>
      </div>
      <div className="flex-shrink-0 self-start sm:self-center">
        <span className="text-xs font-semibold bg-blue-50 text-[#2563EB] border border-blue-100 px-3 py-1 rounded-full">
          GPA {gpa}
        </span>
      </div>
    </div>
  );
}
