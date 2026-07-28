'use client';

import React, { useEffect } from 'react';
import { ShieldAlert, RefreshCw, Home, Mail } from 'lucide-react';
import Link from 'next/link';

export default function ErrorPage({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error('System Error Boundary:', error);
  }, [error]);

  return (
    <div className="min-h-screen bg-[#F8FAFC] dark:bg-[#090D16] flex items-center justify-center p-6 text-center">
      <div className="bg-white dark:bg-[#1E293B] border border-slate-200 dark:border-slate-800 rounded-3xl p-8 max-w-md w-full shadow-2xl space-y-6">
        <div className="w-16 h-16 mx-auto flex items-center justify-center bg-rose-50 dark:bg-rose-955 text-rose-600 dark:text-rose-400 border border-rose-100 dark:border-rose-900/50 rounded-2xl">
          <ShieldAlert size={30} className="animate-pulse" />
        </div>

        <div className="space-y-2">
          <h1 className="text-xl sm:text-2xl font-black text-slate-900 dark:text-white tracking-tight">Something Went Wrong</h1>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
            TalentAI encountered a temporary system processing fault. We apologize for the inconvenience.
          </p>
        </div>

        {error?.message && (
          <div className="p-3 bg-slate-50 dark:bg-[#151D2A] border border-slate-200 dark:border-slate-800 rounded-xl text-left text-[11px] text-slate-400 font-mono overflow-auto max-h-[100px]">
            {error.message}
          </div>
        )}

        <div className="flex flex-col gap-2.5 pt-2 border-t border-slate-150 dark:border-slate-800/60">
          <button
            onClick={reset}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2.5 px-4 rounded-xl shadow-sm text-xs sm:text-sm transition-colors cursor-pointer flex items-center justify-center gap-1.5 bg-blue-600"
          >
            <RefreshCw size={14} />
            Retry Connection
          </button>

          <div className="grid grid-cols-2 gap-2">
            <Link href="/candidate">
              <button className="w-full border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-350 font-bold py-2 px-3 rounded-xl text-xs transition-colors cursor-pointer flex items-center justify-center gap-1 bg-white">
                <Home size={12} />
                Go Dashboard
              </button>
            </Link>
            <a href="mailto:support@talentai.com" className="w-full">
              <button className="w-full border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-350 font-bold py-2 px-3 rounded-xl text-xs transition-colors cursor-pointer flex items-center justify-center gap-1 bg-white">
                <Mail size={12} />
                Contact Support
              </button>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
