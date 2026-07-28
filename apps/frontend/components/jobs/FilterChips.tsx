'use client';

import React from 'react';
import { JobFilter } from '@/types/job';
import { X } from 'lucide-react';

interface FilterChipsProps {
  filters: JobFilter;
  updateFilter: (key: keyof JobFilter, value: any) => void;
  resetFilters: () => void;
}

export default function FilterChips({
  filters,
  updateFilter,
  resetFilters,
}: FilterChipsProps) {
  const activeChips: { key: keyof JobFilter; label: string }[] = [];

  if (filters.location) activeChips.push({ key: 'location', label: `Location: ${filters.location}` });
  if (filters.experience) activeChips.push({ key: 'experience', label: `Experience: ${filters.experience}` });
  if (filters.jobType && filters.jobType !== 'Any') activeChips.push({ key: 'jobType', label: `Type: ${filters.jobType}` });
  if (filters.remoteStatus && filters.remoteStatus !== 'Any') activeChips.push({ key: 'remoteStatus', label: `Workplace: ${filters.remoteStatus}` });

  if (activeChips.length === 0) return null;

  return (
    <div className="flex flex-wrap items-center gap-2 mb-4">
      <span className="text-xs text-[#64748B] font-medium">Active Filters:</span>
      {activeChips.map((chip) => (
        <span
          key={chip.key}
          className="inline-flex items-center gap-1 bg-blue-50 text-[#2563EB] border border-blue-100 px-2.5 py-1 rounded-full text-xs font-semibold"
        >
          {chip.label}
          <button
            onClick={() => updateFilter(chip.key, chip.key === 'jobType' || chip.key === 'remoteStatus' ? 'Any' : '')}
            className="hover:bg-blue-100 rounded-full p-0.5 cursor-pointer"
          >
            <X size={10} />
          </button>
        </span>
      ))}
      <button
        onClick={resetFilters}
        className="text-xs text-slate-500 hover:text-slate-800 font-semibold hover:underline ml-1 cursor-pointer"
      >
        Clear All
      </button>
    </div>
  );
}
