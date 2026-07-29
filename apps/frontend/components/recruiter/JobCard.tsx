'use client';

import React from 'react';
import Link from 'next/link';
import { RecruiterJob } from '@/types/job';
import { Eye, Edit2, Copy, ToggleLeft, Trash2 } from 'lucide-react';

interface JobCardProps {
  job: RecruiterJob;
  onDuplicate: (id: string) => void;
  onClose: (id: string) => void;
  onDelete: (id: string) => void;
}

export default function JobCard({ job, onDuplicate, onClose, onDelete }: JobCardProps) {
  const getStatusStyle = (s: string) => {
    switch (s) {
      case 'Published':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'Closed':
        return 'bg-red-50 text-red-700 border-red-200';
      default:
        return 'bg-slate-50 text-slate-600 border-slate-200';
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm hover:shadow-md transition-all text-left space-y-4">
      <div className="flex items-start justify-between gap-4">
        <div className="flex gap-3.5">
          <div className={`w-11 h-11 rounded-xl ${job.logoColor} flex items-center justify-center text-white font-bold text-lg flex-shrink-0`}>
            {job.logo}
          </div>
          <div>
            <Link href={`/recruiter/jobs/${job.id}`}>
              <h4 className="font-bold text-[#0F172A] text-sm sm:text-base hover:text-blue-600 transition-colors line-clamp-1">
                {job.role}
              </h4>
            </Link>
            <p className="text-xs text-[#64748B] mt-0.5">{job.department} · {job.location}</p>
          </div>
        </div>

        <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full border uppercase tracking-wider ${getStatusStyle(job.status)}`}>
          {job.status}
        </span>
      </div>

      <div className="grid grid-cols-3 gap-3 border-y border-[#F1F5F9] py-3 text-center text-xs">
        <div>
          <span className="text-[#64748B] text-[10px] font-semibold uppercase tracking-wider block">Views</span>
          <span className="font-bold text-[#0F172A] text-sm mt-0.5 block">{job.views}</span>
        </div>
        <div>
          <span className="text-[#64748B] text-[10px] font-semibold uppercase tracking-wider block">Applications</span>
          <span className="font-bold text-[#0F172A] text-sm mt-0.5 block">{job.applicationsCount}</span>
        </div>
        <div>
          <span className="text-[#64748B] text-[10px] font-semibold uppercase tracking-wider block">Shortlisted</span>
          <span className="font-bold text-emerald-600 text-sm mt-0.5 block">{job.shortlistedCount}</span>
        </div>
      </div>

      <div className="flex items-center justify-between text-xs pt-1">
        <span className="text-[#64748B] font-semibold">Deadline: {job.deadline}</span>

        {/* Action icons bar */}
        <div className="flex items-center gap-1">
          <Link
            href={`/recruiter/jobs/edit/${job.id}`}
            className="p-1.5 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors cursor-pointer"
            title="Edit job listing"
          >
            <Edit2 size={13} />
          </Link>
          <button
            onClick={() => onDuplicate(job.id)}
            className="p-1.5 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors cursor-pointer"
            title="Duplicate job listing"
          >
            <Copy size={13} />
          </button>
          {job.status === 'Published' && (
            <button
              onClick={() => onClose(job.id)}
              className="p-1.5 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors cursor-pointer"
              title="Close job listing"
            >
              <ToggleLeft size={13} />
            </button>
          )}
          <button
            onClick={() => onDelete(job.id)}
            className="p-1.5 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors cursor-pointer"
            title="Delete job listing"
          >
            <Trash2 size={13} />
          </button>
        </div>
      </div>
    </div>
  );
}
