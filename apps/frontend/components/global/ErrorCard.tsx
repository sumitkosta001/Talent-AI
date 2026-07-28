'use client';

import React from 'react';
import { AlertCircle, Home } from 'lucide-react';
import Link from 'next/link';
import RetryButton from './RetryButton';

interface ErrorCardProps {
  error?: Error | null;
  resetErrorBoundary?: () => void;
}

export default function ErrorCard({ error, resetErrorBoundary }: ErrorCardProps) {
  return (
    <div className="bg-white dark:bg-[#1E293B] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 sm:p-8 max-w-lg w-full text-center space-y-5 shadow-xl">
      <div className="w-14 h-14 bg-rose-50 dark:bg-rose-950/30 text-rose-500 dark:text-rose-450 border border-rose-100 dark:border-rose-900/50 rounded-2xl flex items-center justify-center mx-auto">
        <AlertCircle size={26} />
      </div>

      <div className="space-y-2">
        <h3 className="text-lg sm:text-xl font-black text-slate-900 dark:text-slate-100">
          An Unexpected Error Occurred
        </h3>
        <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
          {error?.message || 'We encountered a problem loading this layout view or component. Your data is safe.'}
        </p>
      </div>

      {error?.stack && process.env.NODE_ENV === 'development' && (
        <div className="p-3 bg-slate-50 dark:bg-[#151D2A] border border-slate-250 dark:border-slate-850 rounded-xl text-left overflow-x-auto max-h-[140px]">
          <pre className="text-[10px] text-slate-450 font-mono leading-tight">
            {error.stack}
          </pre>
        </div>
      )}

      <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2 border-t border-slate-100 dark:border-slate-800/60">
        {resetErrorBoundary && (
          <RetryButton onRetry={resetErrorBoundary} />
        )}
        <Link href="/candidate">
          <button className="inline-flex items-center gap-1.5 py-2 px-4 hover:bg-slate-50 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl text-xs sm:text-sm font-bold text-slate-650 dark:text-slate-300 transition-all cursor-pointer">
            <Home size={14} />
            Go Dashboard
          </button>
        </Link>
      </div>
    </div>
  );
}
