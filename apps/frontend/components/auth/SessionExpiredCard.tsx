'use client';

import React from 'react';
import { ShieldAlert, LogIn, Home } from 'lucide-react';
import Link from 'next/link';

export default function SessionExpiredCard() {
  return (
    <div className="bg-white dark:bg-[#1E293B] border border-slate-200 dark:border-slate-800 rounded-3xl p-8 max-w-md w-full text-center space-y-6 shadow-xl">
      <div className="w-16 h-16 bg-amber-50 dark:bg-amber-950/30 text-amber-500 border border-amber-100 dark:border-amber-900/50 rounded-2xl flex items-center justify-center mx-auto">
        <ShieldAlert size={32} />
      </div>

      <div className="space-y-2">
        <h2 className="text-xl sm:text-2xl font-black text-slate-900 dark:text-slate-100">
          Session Expired
        </h2>
        <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
          Your security session has timed out due to inactivity. Please log back in to continue working securely.
        </p>
      </div>

      <div className="flex flex-col gap-2.5 pt-2 border-t border-slate-100 dark:border-slate-800">
        <Link href="/login">
          <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-xl shadow-sm text-xs sm:text-sm transition-colors cursor-pointer flex items-center justify-center gap-2">
            <LogIn size={16} />
            Login Again
          </button>
        </Link>
        <Link href="/">
          <button className="w-full border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-300 font-bold py-2.5 px-4 rounded-xl text-xs sm:text-sm transition-colors cursor-pointer flex items-center justify-center gap-2">
            <Home size={14} />
            Return Home
          </button>
        </Link>
      </div>
    </div>
  );
}
