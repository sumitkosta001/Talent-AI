'use client';

import React from 'react';
import Link from 'next/link';
import { RecruiterJob } from '@/types/job';
import { Edit2, Copy, ToggleLeft, Trash2, Eye } from 'lucide-react';

interface JobsTableProps {
  jobs: RecruiterJob[];
  onDuplicate: (id: string) => void;
  onClose: (id: string) => void;
  onDelete: (id: string) => void;
}

export default function JobsTable({ jobs, onDuplicate, onClose, onDelete }: JobsTableProps) {
  const getStatusColor = (s: string) => {
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
    <div className="bg-white rounded-2xl border border-[#E2E8F0] overflow-hidden shadow-sm">
      <div className="overflow-x-auto">
        <table className="w-full text-left">
          <thead className="bg-[#F8FAFC] border-b border-[#E2E8F0] text-xs font-bold text-[#64748B] uppercase tracking-wider">
            <tr>
              <th className="px-5 py-3">Job Listing</th>
              <th className="px-5 py-3">Department</th>
              <th className="px-5 py-3">Applications</th>
              <th className="px-5 py-3">Status</th>
              <th className="px-5 py-3">Deadline</th>
              <th className="px-5 py-3 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#F1F5F9] text-xs sm:text-sm">
            {jobs.map((job) => (
              <tr key={job.id} className="hover:bg-[#F8FAFC]/50 transition-colors">
                <td className="px-5 py-4">
                  <div className="flex items-center gap-3">
                    <div className={`w-8 h-8 rounded-lg ${job.logoColor} flex items-center justify-center text-white font-bold text-xs flex-shrink-0`}>
                      {job.logo}
                    </div>
                    <div>
                      <Link href={`/recruiter/jobs/${job.id}`} className="font-bold text-[#0F172A] hover:text-blue-600 transition-colors">
                        {job.role}
                      </Link>
                      <p className="text-[10px] text-[#64748B] font-semibold mt-0.5">{job.location} · {job.employmentType}</p>
                    </div>
                  </div>
                </td>
                <td className="px-5 py-4 font-semibold text-slate-700">{job.department}</td>
                <td className="px-5 py-4">
                  <span className="font-bold text-[#0F172A]">{job.applicationsCount}</span>
                  <span className="text-[#94A3B8] text-xs"> views: {job.views}</span>
                </td>
                <td className="px-5 py-4">
                  <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full border uppercase tracking-wider ${getStatusColor(job.status)}`}>
                    {job.status}
                  </span>
                </td>
                <td className="px-5 py-4 font-semibold text-slate-600">{job.deadline}</td>
                <td className="px-5 py-4 text-right">
                  <div className="flex items-center justify-end gap-1.5">
                    <Link
                      href={`/recruiter/jobs/${job.id}`}
                      className="p-1 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors cursor-pointer"
                      title="View details"
                    >
                      <Eye size={14} />
                    </Link>
                    <Link
                      href={`/recruiter/jobs/edit/${job.id}`}
                      className="p-1 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors cursor-pointer"
                      title="Edit job listing"
                    >
                      <Edit2 size={14} />
                    </Link>
                    <button
                      onClick={() => onDuplicate(job.id)}
                      className="p-1 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors cursor-pointer"
                      title="Duplicate job listing"
                    >
                      <Copy size={14} />
                    </button>
                    {job.status === 'Published' && (
                      <button
                        onClick={() => onClose(job.id)}
                        className="p-1 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors cursor-pointer"
                        title="Close job listing"
                      >
                        <ToggleLeft size={14} />
                      </button>
                    )}
                    <button
                      onClick={() => onDelete(job.id)}
                      className="p-1 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors cursor-pointer"
                      title="Delete job listing"
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
