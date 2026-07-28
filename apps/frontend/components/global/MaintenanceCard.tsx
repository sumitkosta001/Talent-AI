'use client';

import React, { useState } from 'react';
import { MOCK_MAINTENANCE_STATUS } from '@/mock/maintenance';
import { Settings, ShieldAlert, Bell, Mail } from 'lucide-react';
import { ToastService } from '@/services/toast.service';

export default function MaintenanceCard() {
  const [email, setEmail] = useState('');

  const handleNotifySubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim()) return;
    ToastService.success('Notification Subscription Added', `We will email ${email} once maintenance is complete!`);
    setEmail('');
  };

  const status = MOCK_MAINTENANCE_STATUS;

  return (
    <div className="bg-white dark:bg-[#1E293B] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 sm:p-8 max-w-lg w-full text-center space-y-6 shadow-xl text-left">
      <div className="relative w-20 h-20 mx-auto flex items-center justify-center bg-blue-50 dark:bg-blue-950/20 text-blue-600 dark:text-blue-400 border border-blue-100 dark:border-blue-900/50 rounded-2xl">
        <Settings className="w-10 h-10 animate-spin" />
        <ShieldAlert className="w-5 h-5 absolute bottom-1 right-1 text-amber-500" />
      </div>

      <div className="space-y-2 text-center">
        <h2 className="text-xl sm:text-2xl font-black text-slate-900 dark:text-slate-100">
          System Maintenance
        </h2>
        <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 leading-relaxed pr-2">
          {status.systemMessage}
        </p>
      </div>

      {/* Progress Bar */}
      <div className="space-y-1.5 max-w-xs mx-auto text-left">
        <div className="flex justify-between items-center text-[10px] sm:text-xs font-bold">
          <span className="text-slate-500 dark:text-slate-400">Upgrade Progress</span>
          <span className="text-slate-800 dark:text-slate-200">{status.progressPercentage}%</span>
        </div>
        <div className="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden border border-slate-200/60 dark:border-slate-700/60">
          <div
            className="h-full bg-blue-600 rounded-full transition-all duration-500"
            style={{ width: `${status.progressPercentage}%` }}
          />
        </div>
      </div>

      <div className="flex justify-center">
        <div className="bg-slate-50 dark:bg-[#151D2A] p-3 rounded-2xl border border-slate-100 dark:border-slate-800/80 inline-flex flex-col gap-1 w-fit text-center">
          <span className="text-[10px] font-black text-slate-400 uppercase tracking-wider">Estimated Back Time</span>
          <span className="text-xs sm:text-sm font-bold text-slate-800 dark:text-slate-200">{status.estimatedEndTime}</span>
        </div>
      </div>

      {/* Notify form */}
      <form onSubmit={handleNotifySubmit} className="space-y-3 pt-3 border-t border-slate-150 dark:border-slate-800/60">
        <p className="text-[11px] sm:text-xs text-slate-500 dark:text-slate-450 font-semibold text-center">
          Get alert once our system goes live:
        </p>
        <div className="flex gap-2 max-w-md mx-auto">
          <div className="relative flex-1">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 animate-none" size={14} />
            <input
              type="email"
              required
              placeholder="Enter your email address..."
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full pl-9 pr-3 py-2 bg-white dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 rounded-xl text-xs sm:text-sm text-slate-900 dark:text-white focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>
          <button
            type="submit"
            className="py-2 px-4 bg-slate-900 hover:bg-black dark:bg-slate-800 dark:hover:bg-slate-700 hover:shadow-md text-xs sm:text-sm font-bold text-white rounded-xl shadow-sm transition-all flex items-center gap-1 cursor-pointer flex-shrink-0"
          >
            <Bell size={12} />
            Notify Me
          </button>
        </div>
      </form>
    </div>
  );
}
