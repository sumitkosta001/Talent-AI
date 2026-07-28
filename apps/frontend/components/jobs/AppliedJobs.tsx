'use client';

import React, { useState } from 'react';
import { useApplications } from '@/hooks/useApplications';
import JobTimeline from './JobTimeline';
import { Calendar, Briefcase, MapPin, DollarSign, Clock, HelpCircle, ChevronDown, ChevronUp } from 'lucide-react';
import Link from 'next/link';

export default function AppliedJobs() {
  const { applications, loading } = useApplications();
  const [expandedId, setExpandedId] = useState<string | null>(null);

  if (loading) {
    return <div className="text-xs text-[#64748B] font-semibold py-4">Loading applied positions...</div>;
  }

  if (applications.length === 0) {
    return (
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-8 text-center text-xs text-[#64748B] font-semibold">
        You haven't submitted any job applications yet.
      </div>
    );
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Offer': return 'bg-green-50 text-green-700 border-green-200';
      case 'Shortlisted': return 'bg-blue-50 text-blue-700 border-blue-200';
      case 'Interview': return 'bg-violet-50 text-violet-700 border-violet-200';
      case 'Rejected': return 'bg-red-50 text-red-700 border-red-200';
      default: return 'bg-slate-50 text-slate-700 border-slate-200';
    }
  };

  return (
    <div className="space-y-4">
      {applications.map((app) => (
        <div key={app.id} className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
          <div className="flex items-start justify-between gap-3">
            <div className="flex gap-4">
              <div className={`w-11 h-11 rounded-xl ${app.logoColor} flex items-center justify-center text-white font-bold text-base flex-shrink-0`}>
                {app.logo}
              </div>
              <div className="text-left">
                <Link href={`/candidate/jobs/${app.jobId}`}>
                  <h4 className="font-bold text-[#0F172A] text-sm hover:text-blue-600 transition-colors">{app.jobTitle}</h4>
                </Link>
                <p className="text-xs text-[#64748B] mt-0.5">{app.company} · {app.location}</p>
                <div className="flex items-center gap-2 mt-2 text-[10px] text-[#64748B] font-semibold">
                  <span className="flex items-center gap-0.5"><Clock size={11} /> Applied {app.appliedDate}</span>
                </div>
              </div>
            </div>

            <div className="text-right flex flex-col items-end gap-1.5 flex-shrink-0">
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border uppercase tracking-wider ${getStatusColor(app.status)}`}>
                {app.status}
              </span>
              <button
                onClick={() => setExpandedId(expandedId === app.id ? null : app.id)}
                className="text-[10px] font-bold text-blue-600 flex items-center gap-0.5 hover:underline cursor-pointer"
              >
                {expandedId === app.id ? (
                  <>Hide Timeline <ChevronUp size={11} /></>
                ) : (
                  <>Track Stages <ChevronDown size={11} /></>
                )}
              </button>
            </div>
          </div>

          {expandedId === app.id && (
            <div className="border-t border-[#F1F5F9] pt-4 animate-in fade-in duration-300">
              <JobTimeline
                timeline={app.timeline.map((step) => ({
                  stage: step.status,
                  date: step.date,
                  completed: step.completed,
                  notes: step.description,
                }))}
              />
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
