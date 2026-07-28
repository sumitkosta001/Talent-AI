'use client';

import React from 'react';
import { Calendar, Clock, Video, User, CheckCircle2 } from 'lucide-react';
import { Interview } from '@/types/application';

interface InterviewSectionProps {
  interview?: Interview;
}

export default function InterviewSection({ interview }: InterviewSectionProps) {
  if (!interview) {
    return (
      <div className="bg-[#F8FAFC] border border-[#E2E8F0] p-6 rounded-2xl text-center text-xs text-[#64748B] font-semibold">
        No active interviews are currently scheduled for this position.
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
      <div className="flex items-center justify-between border-b border-[#F1F5F9] pb-3">
        <h4 className="font-bold text-sm text-[#0F172A] flex items-center gap-1.5">
          <Calendar size={18} className="text-[#2563EB]" />
          Interview Schedule
        </h4>
        <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border uppercase tracking-wider ${
          interview.status === 'Scheduled'
            ? 'bg-blue-50 text-blue-700 border-blue-200 animate-pulse'
            : 'bg-green-50 text-green-700 border-green-200'
        }`}>
          {interview.status}
        </span>
      </div>

      <div className="grid sm:grid-cols-2 gap-4 text-xs">
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <Calendar size={14} className="text-[#64748B]" />
            <span className="font-semibold text-slate-700">Date:</span>
            <span className="font-bold text-[#0F172A]">{interview.date}</span>
          </div>
          <div className="flex items-center gap-2">
            <Clock size={14} className="text-[#64748B]" />
            <span className="font-semibold text-slate-700">Time:</span>
            <span className="font-bold text-[#0F172A]">{interview.time}</span>
          </div>
          <div className="flex items-center gap-2">
            <User size={14} className="text-[#64748B]" />
            <span className="font-semibold text-slate-700">Interviewer:</span>
            <span className="font-bold text-[#0F172A]">{interview.interviewer}</span>
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <Video size={14} className="text-[#64748B]" />
            <span className="font-semibold text-slate-700">Type:</span>
            <span className="font-bold text-[#2563EB] bg-blue-50 px-2 py-0.5 rounded border border-blue-100 uppercase text-[10px]">
              {interview.type} Interview
            </span>
          </div>
          {interview.link && (
            <div className="flex items-center gap-2">
              <span className="font-semibold text-slate-700">Link:</span>
              <a
                href={interview.link}
                target="_blank"
                rel="noopener noreferrer"
                className="font-bold text-blue-600 hover:underline break-all"
              >
                Join Video Meeting
              </a>
            </div>
          )}
        </div>
      </div>

      {interview.prepNotes && (
        <div className="p-3 bg-violet-50/50 border border-violet-100 rounded-xl space-y-1.5 text-xs">
          <p className="font-bold text-violet-950 flex items-center gap-1.5">
            <CheckCircle2 size={13} />
            Recruiter's Preparation Tips:
          </p>
          <p className="text-violet-900/80 leading-relaxed">{interview.prepNotes}</p>
        </div>
      )}
    </div>
  );
}
