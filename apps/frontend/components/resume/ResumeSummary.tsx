import React from 'react';
import { FileText } from 'lucide-react';

interface ResumeSummaryProps {
  summary: string;
}

export default function ResumeSummary({ summary }: ResumeSummaryProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm">
      <div className="flex items-center gap-2 mb-3.5">
        <FileText size={18} className="text-[#2563EB]" />
        <h2 className="font-bold text-[#0F172A] text-base sm:text-lg">Professional Summary</h2>
      </div>
      <p className="text-sm text-[#64748B] leading-relaxed font-normal">
        {summary}
      </p>
    </div>
  );
}
