'use client';

import React from 'react';
import { MOCK_FILTERS } from '@/mock/filters';
import { JobFilter } from '@/types/job';
import { X, SlidersHorizontal } from 'lucide-react';

interface FilterSidebarProps {
  filters: JobFilter;
  updateFilter: (key: keyof JobFilter, value: any) => void;
  resetFilters: () => void;
}

export default function FilterSidebar({
  filters,
  updateFilter,
  resetFilters,
}: FilterSidebarProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-6">
      <div className="flex items-center justify-between border-b border-[#F1F5F9] pb-4">
        <div className="flex items-center gap-2 font-bold text-sm text-[#0F172A]">
          <SlidersHorizontal size={16} className="text-blue-600" />
          Filter Jobs
        </div>
        <button
          onClick={resetFilters}
          className="text-xs font-semibold text-blue-600 hover:underline cursor-pointer"
        >
          Reset All
        </button>
      </div>

      {/* Sorting */}
      <div>
        <label className="block text-xs font-bold text-[#64748B] mb-2 uppercase tracking-wide">Sort By</label>
        <select
          value={filters.sortBy}
          onChange={(e) => updateFilter('sortBy', e.target.value)}
          className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
        >
          <option value="best-match">Best Match</option>
          <option value="newest">Newest Posted</option>
          <option value="highest-salary">Highest Salary</option>
        </select>
      </div>

      {/* Job Type */}
      <div>
        <label className="block text-xs font-bold text-[#64748B] mb-2 uppercase tracking-wide">Job Type</label>
        <select
          value={filters.jobType}
          onChange={(e) => updateFilter('jobType', e.target.value)}
          className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
        >
          <option value="Any">Any Type</option>
          {MOCK_FILTERS.jobTypes.map((type) => (
            <option key={type} value={type}>{type}</option>
          ))}
        </select>
      </div>

      {/* Remote Status */}
      <div>
        <label className="block text-xs font-bold text-[#64748B] mb-2 uppercase tracking-wide">Workplace</label>
        <select
          value={filters.remoteStatus}
          onChange={(e) => updateFilter('remoteStatus', e.target.value)}
          className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
        >
          <option value="Any">Any workplace</option>
          {MOCK_FILTERS.remoteStatuses.map((status) => (
            <option key={status} value={status}>{status}</option>
          ))}
        </select>
      </div>

      {/* Location */}
      <div>
        <label className="block text-xs font-bold text-[#64748B] mb-2 uppercase tracking-wide">Location</label>
        <select
          value={filters.location}
          onChange={(e) => updateFilter('location', e.target.value)}
          className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
        >
          <option value="">Any Location</option>
          {MOCK_FILTERS.locations.map((loc) => (
            <option key={loc} value={loc}>{loc}</option>
          ))}
        </select>
      </div>

      {/* Experience level */}
      <div>
        <label className="block text-xs font-bold text-[#64748B] mb-2 uppercase tracking-wide">Experience</label>
        <select
          value={filters.experience}
          onChange={(e) => updateFilter('experience', e.target.value)}
          className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
        >
          <option value="">Any Experience</option>
          {MOCK_FILTERS.experiences.map((exp) => (
            <option key={exp} value={exp}>{exp}</option>
          ))}
        </select>
      </div>
    </div>
  );
}
