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
  const activeChips: { key: keyof JobFilter; label: string; clearVal: any }[] = [];

  if (filters.search) activeChips.push({ key: 'search', label: `Search: ${filters.search}`, clearVal: '' });
  if (filters.location) activeChips.push({ key: 'location', label: `Location: ${filters.location}`, clearVal: '' });
  if (filters.experience) activeChips.push({ key: 'experience', label: `Exp: ${filters.experience}+ yrs`, clearVal: '' });
  if (filters.remoteStatus && filters.remoteStatus !== 'Any') activeChips.push({ key: 'remoteStatus', label: `Work Mode: ${filters.remoteStatus}`, clearVal: 'Any' });
  if (filters.salaryMin > 0) activeChips.push({ key: 'salaryMin', label: `Min ₹${(filters.salaryMin / 100000).toFixed(1)}L`, clearVal: 0 });
  if (filters.salaryMax && filters.salaryMax > 0) activeChips.push({ key: 'salaryMax', label: `Max ₹${(filters.salaryMax / 100000).toFixed(1)}L`, clearVal: undefined });

  if (activeChips.length === 0 && filters.skills.length === 0) return null;

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
            onClick={() => updateFilter(chip.key, chip.clearVal)}
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
        Clear Filters
      </button>
    </div>
  );
}
