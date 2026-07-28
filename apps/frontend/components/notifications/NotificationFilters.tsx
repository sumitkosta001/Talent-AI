'use client';

import React from 'react';
import { NotificationFilter } from '@/types/notification';
import { MOCK_NOTIFICATION_CATEGORIES } from '@/mock/notificationCategories';

interface NotificationFiltersProps {
  filters: NotificationFilter;
  updateFilter: (key: keyof NotificationFilter, value: any) => void;
  resetFilters: () => void;
}

export default function NotificationFilters({
  filters,
  updateFilter,
  resetFilters,
}: NotificationFiltersProps) {
  return (
    <div className="bg-white border border-[#E2E8F0] rounded-2xl p-4 shadow-sm grid grid-cols-2 sm:grid-cols-4 gap-3 text-left">
      {/* Category Select */}
      <div>
        <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Category</label>
        <select
          value={filters.category}
          onChange={(e) => updateFilter('category', e.target.value)}
          className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
        >
          <option value="All">All Categories</option>
          {MOCK_NOTIFICATION_CATEGORIES.map(c => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </div>

      {/* Priority Select */}
      <div>
        <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Priority</label>
        <select
          value={filters.priority}
          onChange={(e) => updateFilter('priority', e.target.value)}
          className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
        >
          <option value="All">All Priorities</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>
      </div>

      {/* Date filter select */}
      <div>
        <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Date Range</label>
        <select
          value={filters.dateRange}
          onChange={(e) => updateFilter('dateRange', e.target.value)}
          className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
        >
          <option value="All">All Time</option>
          <option value="Today">Today</option>
          <option value="Last 7 Days">Last 7 Days</option>
          <option value="Last 30 Days">Last 30 Days</option>
        </select>
      </div>

      {/* Sort selection */}
      <div className="flex items-end justify-between gap-2">
        <div className="flex-1">
          <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Sort By</label>
          <select
            value={filters.sortBy}
            onChange={(e) => updateFilter('sortBy', e.target.value)}
            className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
          >
            <option value="Newest">Newest First</option>
            <option value="Oldest">Oldest First</option>
          </select>
        </div>
        <button
          onClick={resetFilters}
          className="px-2.5 py-2 hover:bg-slate-50 border border-transparent hover:border-[#E2E8F0] rounded-xl text-xs text-[#64748B] hover:text-[#0F172A] font-bold transition-all h-9 cursor-pointer flex items-center justify-center"
        >
          Reset
        </button>
      </div>
    </div>
  );
}
