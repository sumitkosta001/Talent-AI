import React from 'react';
import { FileText, Clock, Trash2, Eye } from 'lucide-react';
import { ResumeHistory as HistoryType } from '../../types/resume';
import Link from 'next/link';

interface ResumeHistoryProps {
  history: HistoryType[];
  onDelete: (id: string) => void;
}

export default function ResumeHistory({ history, onDelete }: ResumeHistoryProps) {
  if (history.length === 0) {
    return (
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 text-center">
        <p className="text-[#64748B] text-sm">No upload history found.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm">
      <h2 className="font-bold text-[#0F172A] text-lg mb-4">Upload History</h2>
      <div className="space-y-3">
        {history.map(({ id, name, size, date, status, score }) => (
          <div
            key={id}
            className="flex items-center gap-3.5 p-3 rounded-xl hover:bg-[#F8FAFC] transition-colors border border-transparent hover:border-[#E2E8F0]"
          >
            <div className="w-9 h-9 bg-red-50 rounded-lg flex items-center justify-center flex-shrink-0">
              <FileText size={18} className="text-red-500" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-bold text-[#0F172A] truncate">{name}</p>
              <p className="text-xs text-[#64748B] flex items-center gap-1 mt-0.5">
                <Clock size={11} />
                {date} · {size}
              </p>
            </div>
            <div className="flex items-center gap-4 flex-shrink-0">
              <div className="text-right hidden sm:block">
                <p className="text-[10px] text-[#94A3B8] font-bold uppercase tracking-wider">ATS Score</p>
                <p className="text-sm font-bold text-[#2563EB]">{score}%</p>
              </div>
              <span className="text-xs bg-green-50 text-green-700 font-semibold px-2.5 py-0.5 rounded-full border border-green-100">
                {status}
              </span>
              <div className="flex items-center gap-1">
                <Link
                  href="/candidate/resume/analysis"
                  className="p-1.5 text-[#94A3B8] hover:text-[#2563EB] rounded-lg hover:bg-blue-50 transition-colors"
                  title="View Analysis"
                >
                  <Eye size={15} />
                </Link>
                <button
                  onClick={() => onDelete(id)}
                  className="p-1.5 text-[#94A3B8] hover:text-[#EF4444] rounded-lg hover:bg-red-50 transition-colors cursor-pointer"
                  title="Delete Entry"
                >
                  <Trash2 size={15} />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
