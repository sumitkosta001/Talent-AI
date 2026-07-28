'use client';

import React from 'react';
import { CheckCheck, Trash2, RefreshCw } from 'lucide-react';

interface NotificationsHeaderProps {
  onMarkAllRead: () => void;
  onClearAll: () => void;
  onRefresh: () => void;
}

export default function NotificationsHeader({
  onMarkAllRead,
  onClearAll,
  onRefresh,
}: NotificationsHeaderProps) {
  const handleClearAll = () => {
    if (confirm('Are you sure you want to delete all notifications?')) {
      onClearAll();
    }
  };

  return (
    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#E2E8F0] pb-5 text-left">
      <div>
        <h1 className="text-xl sm:text-2xl font-bold text-[#0F172A]">Notification Center</h1>
        <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">
          Stay updated with job postings, resume changes, application statuses, and messages.
        </p>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <button
          onClick={onRefresh}
          className="inline-flex items-center gap-1 bg-white border border-[#E2E8F0] text-[#64748B] hover:text-[#0F172A] px-3 py-2 rounded-xl text-xs font-semibold hover:bg-slate-50 transition-colors cursor-pointer"
        >
          <RefreshCw size={13} />
          Refresh
        </button>
        <button
          onClick={onMarkAllRead}
          className="inline-flex items-center gap-1 bg-white border border-[#E2E8F0] text-[#2563EB] hover:text-blue-800 px-3 py-2 rounded-xl text-xs font-semibold hover:bg-slate-50 transition-colors cursor-pointer"
        >
          <CheckCheck size={13} />
          Mark All Read
        </button>
        <button
          onClick={handleClearAll}
          className="inline-flex items-center gap-1 bg-red-50 hover:bg-red-100 border border-red-100 text-red-700 px-3 py-2 rounded-xl text-xs font-semibold transition-colors cursor-pointer"
        >
          <Trash2 size={13} />
          Clear All
        </button>
      </div>
    </div>
  );
}
