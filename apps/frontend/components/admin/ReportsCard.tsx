'use client';

import React from 'react';
import { PlatformReport } from '@/types/report';
import { FileDown, FileText } from 'lucide-react';

interface ReportsCardProps {
  reports: PlatformReport[];
}

export default function ReportsCard({ reports }: ReportsCardProps) {
  const triggerDownload = (title: string, format: string) => {
    alert(`Downloading ${title} formatted as ${format} spreadsheet/document.`);
  };

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
      <div>
        <h3 className="font-bold text-[#0F172A] text-sm sm:text-base">Generated Platform Audits Reports</h3>
        <p className="text-xs text-[#64748B] mt-0.5">Platforms user metrics, growth rates, and activity statistics logs.</p>
      </div>

      <div className="space-y-3.5">
        {reports.map((rep) => (
          <div
            key={rep.id}
            className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-3.5 border border-[#F1F5F9] bg-[#F8FAFC]/50 rounded-xl"
          >
            <div className="flex items-start gap-3">
              <div className="p-2 bg-blue-50 text-blue-600 rounded-lg flex-shrink-0">
                <FileText size={16} />
              </div>
              <div className="text-xs">
                <h4 className="font-bold text-[#0F172A] leading-normal">{rep.title}</h4>
                <p className="text-[#64748B] font-semibold mt-0.5">Generated: {rep.generatedDate} · Size: {rep.fileSize}</p>
              </div>
            </div>

            <div className="flex gap-1.5 self-end sm:self-center">
              {['PDF', 'CSV', 'Excel'].map((fmt) => (
                <button
                  key={fmt}
                  onClick={() => triggerDownload(rep.title, fmt)}
                  className="inline-flex items-center gap-1 bg-white border border-[#E2E8F0] hover:bg-slate-50 text-[#64748B] hover:text-[#0F172A] px-2.5 py-1.5 rounded-lg text-[10px] font-bold cursor-pointer transition-all"
                >
                  <FileDown size={11} />
                  {fmt}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
