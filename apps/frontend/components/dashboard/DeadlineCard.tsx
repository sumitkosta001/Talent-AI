'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Calendar, AlertCircle, Bell, ExternalLink } from 'lucide-react';
import { ApplicationDeadline } from '@/types/dashboard';
import Link from 'next/link';

interface DeadlineCardProps {
  item: ApplicationDeadline;
  getPriorityColor: (p: ApplicationDeadline['priority']) => string;
}

export default function DeadlineCard({ item, getPriorityColor }: DeadlineCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-4 bg-[#F8FAFC] border border-[#E2E8F0] rounded-2xl flex flex-col justify-between gap-3 hover:shadow-sm transition-all hover:bg-white text-left"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex gap-3 min-w-0">
          <div
            className="w-10 h-10 rounded-xl flex items-center justify-center text-white font-extrabold flex-shrink-0"
            style={{ backgroundColor: item.logoColor }}
          >
            {item.companyName.charAt(0)}
          </div>
          <div className="min-w-0">
            <h4 className="font-extrabold text-[#0F172A] text-sm truncate">{item.companyName}</h4>
            <p className="text-xs text-[#64748B] font-semibold mt-0.5 truncate">{item.role}</p>

            <div className="flex items-center gap-1.5 mt-2 text-[10px] text-[#94A3B8] font-semibold">
              <Calendar size={11} />
              <span>Closes: {item.deadlineDate}</span>
            </div>
          </div>
        </div>

        <div className="flex flex-col items-end gap-1.5 flex-shrink-0">
          <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full border uppercase tracking-wider ${getPriorityColor(item.priority)}`}>
            {item.priority} Priority
          </span>
          <span className="text-[10px] text-rose-500 font-bold flex items-center gap-0.5">
            <AlertCircle size={10} />
            {item.daysRemaining === 0 ? 'Closes today' : item.daysRemaining === 1 ? '1 day left' : `${item.daysRemaining} days left`}
          </span>
        </div>
      </div>

      {/* Progress bar */}
      <div className="space-y-1.5">
        <div className="flex justify-between items-center text-[10px] font-bold">
          <span className="text-[#64748B]">Application Progress</span>
          <span className="text-[#0F172A]">{item.progress}%</span>
        </div>
        <div className="w-full bg-[#E2E8F0] h-1.5 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-500 ${
              item.daysRemaining <= 3 ? 'bg-rose-500' : 'bg-blue-600'
            }`}
            style={{ width: `${item.progress}%` }}
          />
        </div>
      </div>

      <div className="flex items-center justify-between gap-3 pt-1 border-t border-[#E2E8F0]/60">
        <button
          onClick={() => alert(`Deadline reminder alert set for ${item.companyName} SSE role.`)}
          className="inline-flex items-center gap-1 py-1.5 px-2.5 hover:bg-slate-50 border border-[#E2E8F0] rounded-xl text-xs font-bold text-[#64748B] transition-all"
        >
          <Bell size={12} className="text-[#94A3B8]" />
          Remind Me
        </button>

        <Link href="/candidate/jobs" className="flex-shrink-0">
          <button className="inline-flex items-center gap-1 py-1.5 px-3 bg-slate-900 hover:bg-black text-xs font-bold text-white rounded-xl shadow-sm transition-all">
            Apply Now
            <ExternalLink size={12} />
          </button>
        </Link>
      </div>
    </motion.div>
  );
}
