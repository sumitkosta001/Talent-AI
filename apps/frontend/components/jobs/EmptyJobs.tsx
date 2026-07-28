'use client';

import React from 'react';
import { HelpCircle } from 'lucide-react';

interface EmptyJobsProps {
  onReset?: () => void;
}

export default function EmptyJobs({ onReset }: EmptyJobsProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-12 text-center shadow-sm space-y-4 max-w-lg mx-auto mt-6">
      <div className="w-12 h-12 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mx-auto">
        <HelpCircle size={24} />
      </div>
      <div>
        <h3 className="font-bold text-[#0F172A] text-lg">No jobs match your search</h3>
        <p className="text-sm text-[#64748B] mt-1 leading-relaxed">
          Try expanding your keyword definitions, adjusting location selectors, or removing some filters to see matching job positions.
        </p>
      </div>
      {onReset && (
        <button
          onClick={onReset}
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs px-4 py-2.5 rounded-xl cursor-pointer transition-colors inline-block"
        >
          Reset All Filters
        </button>
      )}
    </div>
  );
}
