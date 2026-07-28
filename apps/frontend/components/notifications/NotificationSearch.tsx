'use client';

import React from 'react';
import { Search } from 'lucide-react';

interface NotificationSearchProps {
  value: string;
  onChange: (val: string) => void;
}

export default function NotificationSearch({ value, onChange }: NotificationSearchProps) {
  return (
    <div className="relative flex-1">
      <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#94A3B8]" />
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Search notifications by title, description, or category..."
        className="w-full pl-9 pr-3 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
      />
    </div>
  );
}
