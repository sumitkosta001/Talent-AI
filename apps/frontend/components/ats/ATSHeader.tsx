'use client';

import React from 'react';
import { Download } from 'lucide-react';

interface ATSHeaderProps {
  onDownloadReport?: () => void;
}

export default function ATSHeader({ onDownloadReport }: ATSHeaderProps) {
  const handleDownload = () => {
    if (onDownloadReport) {
      onDownloadReport();
    } else {
      alert('Generating PDF score breakdown reports...');
    }
  };

  return (
    <div className="flex items-center justify-between border-b border-[#E2E8F0] pb-5">
      <div>
        <h1 className="text-xl font-bold text-[#0F172A]">ATS Score Card</h1>
        <p className="text-sm text-[#64748B] mt-0.5">Applicant Tracking System compatibility analysis</p>
      </div>
      <button
        onClick={handleDownload}
        className="flex items-center gap-2 bg-[#2563EB] text-white px-4 py-2 rounded-xl text-sm font-medium hover:bg-[#1D4ED8] transition-colors cursor-pointer"
      >
        <Download size={15} />
        Download Report
      </button>
    </div>
  );
}
