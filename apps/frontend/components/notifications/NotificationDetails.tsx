'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowUpRight, HelpCircle, Bell } from 'lucide-react';
import { Notification } from '@/types/notification';
import NotificationBadge from './NotificationBadge';
import NotificationPriorityBadge from './NotificationPriorityBadge';

interface NotificationDetailsProps {
  notification: Notification | null;
}

export default function NotificationDetails({ notification }: NotificationDetailsProps) {
  if (!notification) {
    return (
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-8 text-center shadow-sm h-full flex flex-col items-center justify-center space-y-3 text-[#64748B] min-h-[300px]">
        <div className="w-10 h-10 bg-slate-50 rounded-full flex items-center justify-center">
          <Bell size={18} className="text-slate-400" />
        </div>
        <p className="text-xs font-semibold">Select a notification to view detailed tracking logs</p>
      </div>
    );
  }

  const { title, description, timestamp, category, priority, relatedRoute } = notification;

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm h-full flex flex-col justify-between text-left space-y-6 min-h-[300px]">
      <div className="space-y-4">
        <div className="flex items-center gap-2 flex-wrap">
          <NotificationBadge category={category} />
          <NotificationPriorityBadge priority={priority} />
          <span className="text-[10px] text-[#64748B] font-semibold ml-auto">{timestamp}</span>
        </div>

        <div className="space-y-2">
          <h3 className="text-base sm:text-lg font-bold text-[#0F172A] leading-tight">{title}</h3>
          <p className="text-xs sm:text-sm text-[#64748B] leading-relaxed">{description}</p>
        </div>
      </div>

      {relatedRoute && (
        <div className="pt-4 border-t border-[#F1F5F9] flex justify-end">
          <Link
            href={relatedRoute}
            className="inline-flex items-center gap-1.5 bg-[#2563EB] hover:bg-[#1D4ED8] text-white px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer"
          >
            Action Needed
            <ArrowUpRight size={14} />
          </Link>
        </div>
      )}
    </div>
  );
}
