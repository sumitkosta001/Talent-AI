'use client';

import React, { useState } from 'react';
import { useApplications } from '@/hooks/useApplications';
import { Loader2, Check } from 'lucide-react';

interface ApplyButtonProps {
  jobId: string;
  role: string;
  company: string;
  logo: string;
  logoColor: string;
  salary: string;
  location: string;
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
  className = '',
}: ApplyButtonProps) {
  const { isApplied, applyForJob } = useApplications();
  const [loading, setLoading] = useState(false);
  
  const applied = isApplied(jobId);

  const handleApply = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (applied) return;
    
    setLoading(true);
    const success = await applyForJob(jobId, role, company, logo, logoColor, salary, location);
    setLoading(false);
    
    if (success) {
      alert(`Application to ${company} for ${role} submitted successfully!`);
    } else {
      alert('Failed to submit application. Please try again.');
    }
  };

  return (
    <button
      onClick={handleApply}
      disabled={loading || applied}
      className={`inline-flex items-center justify-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer disabled:opacity-75 disabled:cursor-not-allowed ${
        applied
          ? 'bg-green-50 text-green-700 border border-green-200'
          : 'bg-[#2563EB] text-white hover:bg-[#1D4ED8]'
      } ${className}`}
    >
      {loading ? (
        <>
          <Loader2 size={13} className="animate-spin" />
          Applying...
        </>
      ) : applied ? (
        <>
          <Check size={13} />
          Applied
        </>
      ) : (
        'Apply Now'
      )}
    </button>
  );
}
