'use client';

import React, { useState } from 'react';
import { Search, MapPin, Briefcase, DollarSign, Filter, X } from 'lucide-react';
import { JobFilter } from '@/types/job';

interface SearchBarProps {
  filters: JobFilter;
  updateFilter: (key: keyof JobFilter, value: any) => void;
}

export default function SearchBar({ filters, updateFilter }: SearchBarProps) {
  const [skillInput, setSkillInput] = useState('');

  const handleAddSkill = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && skillInput.trim()) {
      e.preventDefault();
      const val = skillInput.trim();
      if (!filters.skills.includes(val)) {
        updateFilter('skills', [...filters.skills, val]);
      }
      setSkillInput('');
    }
  };

  const handleRemoveSkill = (skillToRemove: string) => {
    updateFilter(
      'skills',
      filters.skills.filter((s) => s !== skillToRemove)
    );
  };

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-4 shadow-sm space-y-3 text-[#0F172A]">
      {/* Top Search Inputs Row */}
      <div className="flex flex-col md:flex-row gap-3">
        {/* Free-text Search Input (q) */}
        <div className="flex-1 relative">
          <Search size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#94A3B8]" />
          <input
            type="text"
            value={filters.search}
            onChange={(e) => updateFilter('search', e.target.value)}
            placeholder="Search job title, description, company..."
            className="w-full pl-9 pr-3 py-2 border border-[#E2E8F0] rounded-xl text-sm font-medium text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500"
          />
        </div>

        {/* Location Input */}
        <div className="w-full md:w-56 relative">
          <MapPin size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#94A3B8]" />
          <input
            type="text"
            value={filters.location}
            onChange={(e) => updateFilter('location', e.target.value)}
            placeholder="Location (e.g. Bangalore)..."
            className="w-full pl-9 pr-3 py-2 border border-[#E2E8F0] rounded-xl text-sm font-medium text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500"
          />
        </div>

        {/* Work Mode Dropdown */}
        <div className="w-full md:w-44 relative">
          <Briefcase size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#94A3B8]" />
          <select
            value={filters.remoteStatus}
            onChange={(e) => updateFilter('remoteStatus', e.target.value)}
            className="w-full pl-9 pr-3 py-2 border border-[#E2E8F0] rounded-xl text-sm font-semibold text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 appearance-none cursor-pointer"
          >
            <option value="Any">All Work Modes</option>
            <option value="Remote">Remote</option>
            <option value="Hybrid">Hybrid</option>
            <option value="On-site">On-site</option>
          </select>
        </div>
      </div>

      {/* Advanced Filters Row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 border-t border-slate-100">
        {/* Skills Tag Input */}
        <div className="space-y-1">
          <label className="text-[11px] font-bold uppercase tracking-wider text-[#64748B]">
            Skills (Press Enter)
          </label>
          <input
            type="text"
            value={skillInput}
            onChange={(e) => setSkillInput(e.target.value)}
            onKeyDown={handleAddSkill}
            placeholder="Add skill (e.g. React)..."
            className="w-full px-3 py-1.5 border border-[#E2E8F0] rounded-lg text-xs font-medium text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500"
          />
        </div>

        {/* Experience Dropdown */}
        <div className="space-y-1">
          <label className="text-[11px] font-bold uppercase tracking-wider text-[#64748B]">
            Experience
          </label>
          <select
            value={filters.experience}
            onChange={(e) => updateFilter('experience', e.target.value)}
            className="w-full px-3 py-1.5 border border-[#E2E8F0] rounded-lg text-xs font-semibold text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
          >
            <option value="">No preference</option>
            <option value="0">0+ years</option>
            <option value="1">1+ years</option>
            <option value="2">2+ years</option>
            <option value="3">3+ years</option>
            <option value="5">5+ years</option>
          </select>
        </div>

        {/* Salary Range Min & Max */}
        <div className="space-y-1">
          <label className="text-[11px] font-bold uppercase tracking-wider text-[#64748B]">
            Salary Range (₹ / Year)
          </label>
          <div className="flex gap-2 items-center">
            <input
              type="number"
              value={filters.salaryMin || ''}
              onChange={(e) => updateFilter('salaryMin', e.target.value ? Number(e.target.value) : 0)}
              placeholder="Min (e.g. 500000)"
              className="w-1/2 px-2.5 py-1.5 border border-[#E2E8F0] rounded-lg text-xs font-medium text-[#0F172A] focus:outline-none focus:border-blue-500"
            />
            <span className="text-xs text-slate-400 font-bold">–</span>
            <input
              type="number"
              value={filters.salaryMax || ''}
              onChange={(e) => updateFilter('salaryMax', e.target.value ? Number(e.target.value) : undefined)}
              placeholder="Max (e.g. 1500000)"
              className="w-1/2 px-2.5 py-1.5 border border-[#E2E8F0] rounded-lg text-xs font-medium text-[#0F172A] focus:outline-none focus:border-blue-500"
            />
          </div>
        </div>
      </div>

      {/* Selected Skills Chips */}
      {filters.skills.length > 0 && (
        <div className="flex flex-wrap items-center gap-1.5 pt-1">
          <span className="text-xs font-bold text-slate-500">Filter Skills:</span>
          {filters.skills.map((skill) => (
            <span
              key={skill}
              className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold"
            >
              {skill}
              <button
                onClick={() => handleRemoveSkill(skill)}
                className="hover:text-blue-900 rounded p-0.5 cursor-pointer"
              >
                <X size={10} />
              </button>
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
