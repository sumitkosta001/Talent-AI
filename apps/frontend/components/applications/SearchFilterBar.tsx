'use client';

import React from 'react';
import { Search, MapPin, SlidersHorizontal } from 'lucide-react';
import { ApplicationFilter } from '@/types/application';
import { MOCK_APPLICATION_FILTERS } from '@/mock/applicationFilters';

interface SearchFilterBarProps {
  filters: ApplicationFilter;
  updateFilter: (key: keyof ApplicationFilter, value: any) => void;
  resetFilters: () => void;
  sortBy: string;
  setSortBy: (val: any) => void;
  showArchived: boolean;
  setShowArchived: (val: boolean) => void;
}

export default function SearchFilterBar({
  filters,
  updateFilter,
  resetFilters,
  sortBy,
  setSortBy,
  showArchived,
  setShowArchived,
}: SearchFilterBarProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-4 shadow-sm space-y-4">
      {/* Search InputRow */}
      <div className="flex flex-col md:flex-row gap-3">
        <div className="flex-1 relative">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#94A3B8]" />
          <input
            type="text"
            value={filters.search}
            onChange={(e) => updateFilter('search', e.target.value)}
            placeholder="Search by company, role, location, or recruiter name..."
            className="w-full pl-9 pr-3 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500"
          />
        </div>

        {/* Sort Select */}
        <div className="w-full md:w-48">
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="w-full px-3 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
          >
            <option value="newest">Newest Applied</option>
            <option value="oldest">Oldest Applied</option>
            <option value="best-match">Best AI Match</option>
            <option value="recently-updated">Recently Updated</option>
            <option value="company-name">Company Name</option>
          </select>
        </div>
      </div>

      {/* Select filters */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-2 border-t border-[#F1F5F9] items-center">
        {/* Status */}
        <div>
          <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Status</label>
          <select
            value={filters.status}
            onChange={(e) => updateFilter('status', e.target.value)}
            className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
          >
            <option value="">All Statuses</option>
            {MOCK_APPLICATION_FILTERS.statuses.map(s => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>

        {/* Location */}
        <div>
          <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Location</label>
          <select
            value={filters.location}
            onChange={(e) => updateFilter('location', e.target.value)}
            className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
          >
            <option value="">All Locations</option>
            {MOCK_APPLICATION_FILTERS.locations.map(l => (
              <option key={l} value={l}>{l}</option>
            ))}
          </select>
        </div>

        {/* Workplace type */}
        <div>
          <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Workplace</label>
          <select
            value={filters.workplace}
            onChange={(e) => updateFilter('workplace', e.target.value)}
            className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
          >
            <option value="All">All workplace</option>
            <option value="Remote">Remote</option>
            <option value="Hybrid">Hybrid</option>
            <option value="On-site">On-site</option>
          </select>
        </div>

        {/* Action controls */}
        <div className="flex gap-2 justify-end self-end pt-4">
          <button
            onClick={() => setShowArchived(!showArchived)}
            className={`px-3 py-2 rounded-xl text-xs font-bold border transition-colors cursor-pointer ${
              showArchived
                ? 'bg-blue-50 text-blue-700 border-blue-200'
                : 'bg-white text-slate-600 border-[#E2E8F0] hover:bg-[#F8FAFC]'
            }`}
          >
            {showArchived ? 'View Active' : 'View Archived'}
          </button>
          <button
            onClick={resetFilters}
            className="px-3 py-2 rounded-xl text-xs font-bold text-slate-500 hover:text-slate-800 transition-colors cursor-pointer"
          >
            Reset
          </button>
        </div>
      </div>
    </div>
  );
}
