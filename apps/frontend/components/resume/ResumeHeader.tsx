import React from 'react';
import { Calendar, Tag } from 'lucide-react';

interface ResumeHeaderProps {
  title: string;
  version: string;
  lastUpdated: string;
  fileName?: string;
}

export default function ResumeHeader({ title, version, lastUpdated, fileName }: ResumeHeaderProps) {
  return (
    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-5 border-b border-[#E2E8F0] mb-6">
      <div>
        <h1 className="text-xl sm:text-2xl font-bold text-[#0F172A]">{title}</h1>
        {fileName && (
          <p className="text-xs sm:text-sm text-[#64748B] mt-1 font-mono">{fileName}</p>
        )}
      </div>
      <div className="flex items-center gap-3">
        <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 bg-blue-50 text-[#2563EB] rounded-full border border-blue-100">
          <Tag size={12} />
          Version {version}
        </span>
        <span className="inline-flex items-center gap-1 text-xs text-[#64748B]">
          <Calendar size={12} />
          Updated {lastUpdated}
        </span>
      </div>
    </div>
  );
}
