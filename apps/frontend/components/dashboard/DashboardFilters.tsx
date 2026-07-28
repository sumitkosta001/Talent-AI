'use client';

import React from 'react';

export type TimeFilter = 'today' | 'week' | 'month';
export type ModuleFilter = 'all' | 'apps' | 'interviews' | 'notifications' | 'bookmarks';

interface DashboardFiltersProps {
  timeFilter: TimeFilter;
  setTimeFilter: (val: TimeFilter) => void;
  moduleFilter: ModuleFilter;
  setModuleFilter: (val: ModuleFilter) => void;
}

export default function DashboardFilters({
  timeFilter,
  setTimeFilter,
  moduleFilter,
  setModuleFilter,
}: DashboardFiltersProps) {
  return (
    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white border border-[#E2E8F0] p-3.5 rounded-3xl shadow-sm text-left">
      <div className="flex items-center gap-1.5 overflow-x-auto pb-2 md:pb-0">
        <span className="text-xs font-extrabold text-[#64748B] uppercase tracking-wider mr-2 flex-shrink-0">Scope:</span>
        {(['all', 'apps', 'interviews', 'notifications', 'bookmarks'] as const).map((t) => (
          <button
            key={t}
            onClick={() => setModuleFilter(t)}
            className={`px-3.5 py-1.5 text-xs font-bold rounded-xl transition-all border uppercase tracking-wider whitespace-nowrap ${
              moduleFilter === t
                ? 'bg-slate-900 border-slate-900 text-white'
                : 'bg-[#F8FAFC] border-[#E2E8F0] text-[#64748B] hover:text-[#0F172A] hover:bg-slate-100'
            }`}
          >
            {t === 'all' ? 'All Sections' : t === 'apps' ? 'Applications' : t}
          </button>
        ))}
      </div>

      <div className="flex items-center gap-1 overflow-x-auto">
        <span className="text-xs font-extrabold text-[#64748B] uppercase tracking-wider mr-2 flex-shrink-0">Period:</span>
        {(['today', 'week', 'month'] as const).map((p) => (
          <button
            key={p}
            onClick={() => setTimeFilter(p)}
            className={`px-3 py-1 text-xs font-bold rounded-lg border transition-all capitalize whitespace-nowrap ${
              timeFilter === p
                ? 'bg-blue-600 border-blue-600 text-white'
                : 'bg-white border-[#E2E8F0] text-[#64748B] hover:text-[#0F172A] hover:bg-slate-50'
            }`}
          >
            This {p === 'today' ? 'Day' : p}
          </button>
        ))}
      </div>
    </div>
  );
}
