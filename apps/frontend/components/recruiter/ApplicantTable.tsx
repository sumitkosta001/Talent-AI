'use client';

import React from 'react';
import Link from 'next/link';
import { Applicant } from '@/types/applicant';
import { Eye, Check, X, Calendar } from 'lucide-react';

interface ApplicantTableProps {
  applicants: Applicant[];
  onShortlist: (id: string) => void;
  onReject: (id: string) => void;
}

export default function ApplicantTable({ applicants, onShortlist, onReject }: ApplicantTableProps) {
  const getStatusColor = (s: string) => {
    switch (s) {
      case 'Offer Sent':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'Interview Scheduled':
        return 'bg-violet-50 text-violet-700 border-violet-200';
      case 'Shortlisted':
        return 'bg-blue-50 text-blue-700 border-blue-200';
      case 'Rejected':
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
              <th className="px-5 py-3">Candidate</th>
              <th className="px-5 py-3">Applied Job</th>
              <th className="px-5 py-3">ATS Score</th>
              <th className="px-5 py-3">Experience</th>
              <th className="px-5 py-3">Status</th>
              <th className="px-5 py-3 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#F1F5F9] text-xs sm:text-sm">
            {applicants.map((app) => (
              <tr key={app.id} className="hover:bg-[#F8FAFC]/50 transition-colors">
                {/* Candidate Initials & Info */}
                <td className="px-5 py-4">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-blue-500 text-white font-bold flex items-center justify-center text-xs flex-shrink-0">
                      {app.name.split(' ').map((n) => n[0]).join('')}
                    </div>
                    <div>
                      <Link href={`/recruiter/applicants/${app.id}`} className="font-bold text-[#0F172A] hover:text-blue-600 transition-colors">
                        {app.name}
                      </Link>
                      <p className="text-[10px] text-[#64748B] font-semibold mt-0.5">{app.email}</p>
                    </div>
                  </div>
                </td>

                <td className="px-5 py-4 font-semibold text-slate-700">{app.jobTitle}</td>

                {/* ATS score gauge */}
                <td className="px-5 py-4">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-[#0F172A]">{app.atsScore}%</span>
                    <div className="w-12 h-1.5 bg-[#E2E8F0] rounded-full overflow-hidden hidden sm:block">
                      <div className="h-full bg-blue-600 rounded-full" style={{ width: `${app.atsScore}%` }} />
                    </div>
                  </div>
                </td>

                <td className="px-5 py-4 font-semibold text-slate-600">{app.experience}</td>

                <td className="px-5 py-4">
                  <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full border uppercase tracking-wider ${getStatusColor(app.status)}`}>
                    {app.status}
                  </span>
                </td>

                {/* Option links */}
                <td className="px-5 py-4 text-right">
                  <div className="flex items-center justify-end gap-1.5">
                    <Link
                      href={`/recruiter/applicants/${app.id}`}
                      className="p-1 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors cursor-pointer"
                      title="View details profile"
                    >
                      <Eye size={14} />
                    </Link>
                    {app.status === 'Applied' && (
                      <>
                        <button
                          onClick={() => onShortlist(app.id)}
                          className="p-1 text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors cursor-pointer"
                          title="Shortlist candidate"
                        >
                          <Check size={14} />
                        </button>
                        <button
                          onClick={() => onReject(app.id)}
                          className="p-1 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors cursor-pointer"
                          title="Reject candidate"
                        >
                          <X size={14} />
                        </button>
                      </>
                    )}
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
