'use client';

import React from 'react';
import { UpcomingInterview } from '@/types/dashboard';
import { Calendar, Clock, Video } from 'lucide-react';
import { motion } from 'framer-motion';

interface InterviewCardProps {
  item: UpcomingInterview;
}

export default function InterviewCard({ item }: InterviewCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-4 bg-[#F8FAFC] border border-[#E2E8F0] rounded-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-4 group hover:shadow-sm transition-all hover:bg-white text-left"
    >
      <div className="flex gap-3 min-w-0">
        <div
          className="w-10 h-10 rounded-xl flex items-center justify-center text-white font-extrabold flex-shrink-0"
          style={{ backgroundColor: item.logoColor }}
        >
          {item.companyName.charAt(0)}
        </div>
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <span className="font-extrabold text-[#0F172A] text-sm truncate">{item.companyName}</span>
            <span className="text-[10px] bg-slate-100 font-bold text-slate-600 px-2 py-0.5 rounded-full border border-slate-200 uppercase tracking-wide flex-shrink-0">
              {item.type}
            </span>
          </div>
          <p className="text-xs text-[#64748B] font-semibold mt-0.5 truncate">{item.role}</p>

          <div className="flex flex-wrap items-center gap-x-3 gap-y-1 mt-2 text-[10px] text-[#94A3B8] font-medium">
            <span className="flex items-center gap-1">
              <Calendar size={11} />
              {item.date}
            </span>
            <span className="text-[#CBD5E1]">•</span>
            <span className="flex items-center gap-1">
              <Clock size={11} />
              {item.time}
            </span>
          </div>
        </div>
      </div>

      <div className="flex sm:flex-col items-stretch sm:items-end justify-between gap-2.5 flex-shrink-0">
        <span className="text-[11px] font-bold text-blue-600 bg-blue-50 border border-blue-100 rounded-full px-2.5 py-0.5 w-fit uppercase tracking-wide self-center sm:self-auto">
          {item.countdownDays === 0 ? 'Today' : item.countdownDays === 1 ? 'Tomorrow' : `In ${item.countdownDays} days`}
        </span>

        <div className="flex items-center gap-2">
          <button
            onClick={() => alert(`Rescheduling request for ${item.companyName} SSE role submitted.`)}
            className="py-1.5 px-3 border border-[#E2E8F0] hover:bg-slate-50 text-[11px] font-bold text-[#64748B] rounded-xl transition-all"
          >
            Reschedule
          </button>
          {item.meetingLink && (
            <a href={item.meetingLink} target="_blank" rel="noopener noreferrer">
              <button className="py-1.5 px-3 bg-blue-600 hover:bg-blue-700 text-[11px] font-bold text-white rounded-xl shadow-sm transition-all flex items-center gap-1">
                Join
                <Video size={11} />
              </button>
            </a>
          )}
        </div>
      </div>
    </motion.div>
  );
}
