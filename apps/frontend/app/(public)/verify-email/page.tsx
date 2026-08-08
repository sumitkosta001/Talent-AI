'use client';

import React, { Suspense } from 'react';
import EmailVerificationCard from '@/components/auth/EmailVerificationCard';

export default function Page() {
  return (
    <div className="min-h-screen bg-[#F8FAFC] dark:bg-[#090D16] flex items-center justify-center p-6 text-center">
      <Suspense fallback={
        <div className="bg-white dark:bg-[#1E293B] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 sm:p-8 max-w-md w-full text-center space-y-6 shadow-xl animate-pulse">
          <div className="w-16 h-16 bg-slate-200 dark:bg-slate-700 rounded-2xl mx-auto"></div>
          <div className="h-6 bg-slate-200 dark:bg-slate-700 rounded w-1/2 mx-auto"></div>
          <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-3/4 mx-auto"></div>
          <div className="h-10 bg-slate-200 dark:bg-slate-700 rounded-xl w-full pt-2"></div>
        </div>
      }>
        <EmailVerificationCard />
      </Suspense>
    </div>
  );
}
