'use client';

import React from 'react';
import { ReportMetric } from '@/types/weeklyReport';
import { ArrowUp, ArrowDown } from 'lucide-react';

interface ReportCardProps {
  item: ReportMetric;
}

export default function ReportCard({ item }: ReportCardProps) {
  return (
    <div className="p-3.5 bg-[#F8FAFC] border border-[#E2E8F0] rounded-2xl flex flex-col justify-between hover:bg-white transition-colors text-left w-full">
      <div className="flex items-start justify-between gap-2">
        <span className="text-xs font-bold text-[#64748B] leading-tight truncate">
          {item.label}
        </span>
        <span className={`inline-flex items-center gap-0.5 text-[10px] font-black rounded-lg px-1.5 py-0.5 ${
          item.improved
            ? 'text-emerald-700 bg-emerald-50 border border-emerald-100'
            : 'text-slate-500 bg-slate-50 border border-slate-100'
        }`}>
          {item.improved ? <ArrowUp size={10} /> : <ArrowDown size={10} />}
          {item.changePercentage}%
        </span>
      </div>

      <div className="mt-3 flex items-baseline gap-1.5">
        <span className="text-xl font-black text-[#0F172A] tracking-tight leading-none">
          {item.currentValue} {item.unit || ''}
        </span>
        <span className="text-[10px] text-[#94A3B8] font-bold">
          vs {item.previousValue} last week
        </span>
      </div>

      <div className="w-full bg-[#E2E8F0] h-1 rounded-full mt-3 overflow-hidden">
        <div
          className="bg-blue-600 h-full rounded-full transition-all duration-500"
          style={{ width: `${Math.min(100, (item.currentValue / Math.max(1, item.previousValue + 2)) * 105)}%` }}
        />
      </div>
    </div>
  );
}
