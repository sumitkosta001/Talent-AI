'use client';

import React from 'react';
import { Search } from 'lucide-react';

interface DashboardSearchProps {
  value: string;
  onChange: (val: string) => void;
}

export default function DashboardSearch({ value, onChange }: DashboardSearchProps) {
  return (
    <div className="relative w-full max-w-md text-left">
      <Search size={18} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#94A3B8]" />
      <input
        type="text"
        placeholder="Global Search (Jobs, companies, applications, skills, AI tools...)"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full pl-10 pr-4 py-2 bg-white border border-[#E2E8F0] rounded-2xl text-xs sm:text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 shadow-sm transition-all"
      />
    </div>
  );
}
