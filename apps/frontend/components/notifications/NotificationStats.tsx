'use client';

import React from 'react';
import { Bell, MailOpen, Calendar, ShieldAlert } from 'lucide-react';
import { NotificationStats as StatsType } from '@/types/notification';

interface NotificationStatsProps {
  stats: StatsType | null;
}

export default function NotificationStats({ stats }: NotificationStatsProps) {
  if (!stats) return null;

  const cardItems = [
    { label: 'Unread Alert', value: stats.unread, icon: Bell, color: 'bg-blue-50 text-blue-600 border-blue-100' },
    { label: 'Read Alerts', value: stats.read, icon: MailOpen, color: 'bg-slate-50 text-slate-500 border-slate-100' },
    { label: "Today's", value: stats.today, icon: Calendar, color: 'bg-indigo-50 text-indigo-600 border-indigo-100' },
    { label: 'High Priority', value: stats.highPriority, icon: ShieldAlert, color: 'bg-red-50 text-red-600 border-red-100 font-bold' },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 text-left">
      {cardItems.map(({ label, value, icon: Icon, color }) => (
        <div key={label} className="bg-white rounded-2xl border border-[#E2E8F0] p-4 shadow-sm flex items-center justify-between">
          <div>
            <span className="text-[10px] sm:text-xs font-bold text-[#64748B] uppercase tracking-wide">{label}</span>
            <div className="text-xl sm:text-2xl font-black text-[#0F172A] mt-1">{value}</div>
          </div>
          <div className={`w-10 h-10 rounded-xl flex items-center justify-center border flex-shrink-0 ${color}`}>
            <Icon size={18} />
          </div>
        </div>
      ))}
    </div>
  );
}
