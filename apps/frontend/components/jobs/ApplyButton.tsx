'use client';

import React from 'react';
import { Send } from 'lucide-react';

interface ApplyButtonProps {
  jobId: string;
  role: string;
  company: string;
  logo?: string;
  logoColor?: string;
  salary?: string;
  location?: string;
  status?: string;
  className?: string;
}

export default function ApplyButton({
  jobId,
  role,
  company,
  logo,
  logoColor,
  salary,
  location,
  status = 'PUBLISHED',
  className = '',
}: ApplyButtonProps) {
  const isClosed = status ? status.toUpperCase() === 'CLOSED' : false;

  const handleApply = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (isClosed) return;

    // Phase 6 entry point placeholder.
    // Do not call ApplicationService.applyForJob(), create an application record, or claim an application was submitted.
    alert('Application submission will be enabled in Phase 6. Applications cannot be submitted yet.');
  };

  return (
    <button
      type="button"
      onClick={handleApply}
      disabled={isClosed}
      title={isClosed ? 'This position is closed' : 'Apply Now (Phase 6 entry point)'}
      className={`inline-flex items-center justify-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer disabled:opacity-60 disabled:cursor-not-allowed ${
        isClosed
          ? 'bg-slate-200 text-slate-500 border border-slate-300'
          : 'bg-[#2563EB] text-white hover:bg-[#1D4ED8]'
      } ${className}`}
    >
      <Send size={13} />
      {isClosed ? 'Position Closed' : 'Apply Now'}
    </button>
  );
}
