'use client';

import React from 'react';
import { Search, MapPin } from 'lucide-react';
import { JobFilter } from '@/types/job';

interface SearchBarProps {
  filters: JobFilter;
  updateFilter: (key: keyof JobFilter, value: any) => void;
}

export default function SearchBar({ filters, updateFilter }: SearchBarProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-3 shadow-sm flex flex-col md:flex-row gap-2">
      {/* Search Input */}
      <div className="flex-1 relative">
        <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#94A3B8]" />
        <input
          type="text"
          value={filters.search}
          onChange={(e) => updateFilter('search', e.target.value)}
          placeholder="Job title, company, or technical keywords..."
          className="w-full pl-9 pr-3 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500"
        />
      </div>

      {/* Location Input */}
      <div className="w-full md:w-64 relative">
        <MapPin size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#94A3B8]" />
        <input
          type="text"
          value={filters.location}
          onChange={(e) => updateFilter('location', e.target.value)}
          placeholder="City, state, or remote..."
          className="w-full pl-9 pr-3 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500"
        />
      </div>
    </div>
  );
}
