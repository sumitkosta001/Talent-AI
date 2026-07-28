'use client';

import React from 'react';
import Link from 'next/link';
import { AlertCircle, ArrowLeft, Briefcase, Home } from 'lucide-react';

export default function NotFound() {
  return (
    <div className="min-h-screen bg-[#F8FAFC] dark:bg-[#090D16] flex items-center justify-center p-6 text-center">
      <div className="bg-white dark:bg-[#1E293B] border border-slate-200 dark:border-slate-800 rounded-3xl p-8 max-w-md w-full shadow-2xl space-y-6">
        <div className="w-16 h-16 mx-auto flex items-center justify-center bg-blue-50 dark:bg-blue-950/20 text-blue-600 dark:text-blue-400 border border-blue-100 dark:border-blue-900/50 rounded-2xl">
          <AlertCircle size={30} className="animate-pulse" />
        </div>

        <div className="space-y-2">
          <h1 className="text-4xl font-black text-slate-900 dark:text-white tracking-tight">404</h1>
          <h2 className="text-lg font-bold text-slate-800 dark:text-slate-100">Page Not Found</h2>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
            The page you are looking for doesn’t exist or has been relocated.
          </p>
        </div>

        <div className="flex flex-col gap-2.5 pt-2 border-t border-slate-150 dark:border-slate-800/60">
          <Link href="/candidate">
            <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2.5 px-4 rounded-xl shadow-sm text-xs sm:text-sm transition-colors cursor-pointer flex items-center justify-center gap-1.5 bg-blue-600">
              <Home size={14} />
              Return Home
            </button>
          </Link>

          <div className="grid grid-cols-2 gap-2">
            <Link href="/candidate/jobs">
              <button className="w-full border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-300 font-bold py-2 px-3 rounded-xl text-xs transition-colors cursor-pointer flex items-center justify-center gap-1 bg-white">
                <Briefcase size={12} />
                Search Jobs
              </button>
            </Link>
            <button
              onClick={() => window.history.back()}
              className="w-full border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-300 font-bold py-2 px-3 rounded-xl text-xs transition-colors cursor-pointer flex items-center justify-center gap-1 bg-white"
            >
              <ArrowLeft size={12} />
              Go Back
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
