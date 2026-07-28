'use client';

import React from 'react';
import { ShieldCheck, Smartphone, Key, Clock } from 'lucide-react';
import { UserSessionData } from '@/types/auth';

interface SecurityBadgeProps {
  session: UserSessionData;
}

export default function SecurityBadge({ session }: SecurityBadgeProps) {
  return (
    <div className="bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 rounded-2xl p-4 space-y-3 text-left">
      <div className="flex items-center gap-2 pb-2 border-b border-slate-200/60 dark:border-slate-700/60">
        <ShieldCheck className="text-emerald-500" size={16} />
        <h4 className="text-xs font-bold text-slate-800 dark:text-slate-200">Security Indicators</h4>
      </div>

      <div className="grid grid-cols-2 gap-2 text-[11px]">
        <div className="flex items-center gap-1.5 text-slate-600 dark:text-slate-400">
          <Smartphone size={12} className="text-blue-500" />
          <span>Device: <strong className="text-slate-800 dark:text-slate-200">{session.lastDevice.split(' ')[0]}</strong></span>
        </div>

        <div className="flex items-center gap-1.5 text-slate-600 dark:text-slate-400">
          <Key size={12} className="text-amber-500" />
          <span>2FA: <strong className={session.twoFactorEnabled ? 'text-emerald-600 dark:text-emerald-400' : 'text-slate-400'}>{session.twoFactorEnabled ? 'Enabled' : 'Disabled'}</strong></span>
        </div>

        <div className="col-span-2 flex items-center gap-1.5 text-slate-500 dark:text-slate-400">
          <Clock size={12} />
          <span>Last active: {session.lastLogin}</span>
        </div>
      </div>
    </div>
  );
}
