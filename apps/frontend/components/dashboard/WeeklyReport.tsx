'use client';

import React from 'react';
import { Activity } from 'lucide-react';
import { WeeklyReportData } from '@/types/weeklyReport';
import ReportCard from './ReportCard';

interface WeeklyReportProps {
  report: WeeklyReportData;
}

export default function WeeklyReport({ report }: WeeklyReportProps) {
  return (
    <div className="bg-white rounded-3xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left flex flex-col h-full">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[#F1F5F9] pb-3">
        <div>
          <h3 className="font-bold text-[#0F172A] text-base sm:text-lg">Weekly Performance Report</h3>
          <p className="text-xs text-[#64748B] mt-0.5">
            Overview from {report.weekStartDate} to {report.weekEndDate}
          </p>
        </div>
        <div className="flex items-center gap-2 bg-emerald-50 border border-emerald-100 px-3 py-1 rounded-full w-fit">
          <Activity size={12} className="text-emerald-600" />
          <span className="text-[11px] text-emerald-700 font-extrabold">
            Productivity: {report.productivityScore}% (+{report.productivityScoreChange}% vs last week)
          </span>
        </div>
      </div>

      <div className="grid sm:grid-cols-2 gap-4 flex-1 overflow-y-auto max-h-[300px] pr-1">
        {report.metrics.map((item, idx) => (
          <ReportCard key={idx} item={item} />
        ))}
      </div>
    </div>
  );
}
