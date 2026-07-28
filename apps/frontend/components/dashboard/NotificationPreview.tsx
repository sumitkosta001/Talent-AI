'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bell, X, Check, FileText, Briefcase, Calendar, ShieldCheck, Info } from 'lucide-react';
import { MOCK_NOTIFICATIONS } from '@/mock/notifications';
import Link from 'next/link';

export default function NotificationPreview() {
  const [list, setList] = useState(MOCK_NOTIFICATIONS.slice(0, 4));

  const unreadCount = list.filter((n) => !n.read).length;

  const markAllRead = () => {
    setList((prev) => prev.map((n) => ({ ...n, read: true })));
  };

  const dismissNotif = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    e.preventDefault();
    setList((prev) => prev.filter((n) => n.id !== id));
  };

  const getNotifIcon = (category: string) => {
    switch (category) {
      case 'Applications':
        return Briefcase;
      case 'Interviews':
        return Calendar;
      case 'ATS':
        return ShieldCheck;
      case 'Jobs':
        return FileText;
      default:
        return Info;
    }
  };

  return (
    <div className="bg-white rounded-3xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
      <div className="flex items-center justify-between border-b border-[#F1F5F9] pb-3">
        <div className="flex items-center gap-2">
          <div className="relative">
            <Bell size={18} className="text-slate-700" />
            {unreadCount > 0 && (
              <span className="absolute -top-1.5 -right-1.5 bg-rose-500 text-white font-extrabold text-[8px] w-4.5 h-4.5 rounded-full flex items-center justify-center border border-white animate-bounce">
                {unreadCount}
              </span>
            )}
          </div>
          <h3 className="font-bold text-[#0F172A] text-base sm:text-lg">Recent Alerts</h3>
        </div>
        {unreadCount > 0 && (
          <button
            onClick={markAllRead}
            className="inline-flex items-center gap-1 hover:bg-slate-50 text-[10px] font-bold text-blue-600 rounded-xl px-2 py-1 transition-all border border-transparent hover:border-slate-100"
          >
            <Check size={12} />
            Mark all read
          </button>
        )}
      </div>

      <div className="space-y-2 max-h-[260px] overflow-y-auto pr-1">
        <AnimatePresence mode="popLayout">
          {list.length === 0 ? (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-xs text-[#94A3B8] italic text-center py-4"
            >
              All clean! No new notifications.
            </motion.p>
          ) : (
            list.map((item) => {
              const Icon = getNotifIcon(item.category);
              return (
                <motion.div
                  key={item.id}
                  initial={{ opacity: 0, y: 5 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  className={`p-3 border rounded-2xl flex items-start gap-3 hover:bg-[#F8FAFC]/50 transition-colors relative group ${
                    item.read ? 'bg-white border-[#E2E8F0]' : 'bg-blue-50/20 border-blue-100'
                  }`}
                >
                  <button
                    onClick={(e) => dismissNotif(item.id, e)}
                    className="absolute top-2.5 right-2.5 p-1 hover:bg-slate-100 rounded-lg text-[#94A3B8] hover:text-slate-600 opacity-0 group-hover:opacity-100 transition-opacity"
                    title="Dismiss"
                  >
                    <X size={12} />
                  </button>

                  <div className="flex gap-2.5 min-w-0 flex-1">
                    <div className={`w-8.5 h-8.5 rounded-xl border flex items-center justify-center flex-shrink-0 ${
                      item.read
                        ? 'bg-slate-50 border-slate-100 text-slate-500'
                        : 'bg-blue-50 border-blue-100 text-blue-600'
                    }`}>
                      <Icon size={14} />
                    </div>
                    <div className="min-w-0 space-y-1">
                      <div className="flex items-center gap-1.5">
                        <span className="font-extrabold text-[#0F172A] text-xs sm:text-sm truncate">
                          {item.title}
                        </span>
                        {!item.read && (
                          <span className="w-1.5 h-1.5 rounded-full bg-blue-500 flex-shrink-0" />
                        )}
                      </div>
                      <p className="text-[11px] text-[#64748B] leading-tight pr-4">
                        {item.description}
                      </p>
                      <span className="text-[9px] font-bold text-[#94A3B8] block pt-0.5 uppercase tracking-wide">
                        {item.timestamp}
                      </span>
                    </div>
                  </div>
                </motion.div>
              );
            })
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
