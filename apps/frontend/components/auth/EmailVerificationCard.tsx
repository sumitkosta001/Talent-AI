'use client';

import React from 'react';
import { Mail, CheckCircle2, Clock, RefreshCw, ArrowLeft, AlertCircle } from 'lucide-react';
import Link from 'next/link';
import { useEmailVerification } from '@/hooks/useEmailVerification';

export default function EmailVerificationCard() {
  const { email, status, countdown, loading, message, resend } = useEmailVerification();

  return (
    <div className="bg-white dark:bg-[#1E293B] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 sm:p-8 max-w-md w-full text-center space-y-6 shadow-xl">
      <div className="w-16 h-16 bg-blue-50 dark:bg-blue-950/30 text-blue-600 dark:text-blue-400 border border-blue-100 dark:border-blue-900/50 rounded-2xl flex items-center justify-center mx-auto">
        <Mail size={32} />
      </div>

      <div className="space-y-2 text-center">
        <h2 className="text-xl sm:text-2xl font-black text-slate-900 dark:text-slate-100">
          Verify Your Email
        </h2>
        <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
          We sent a verification link to:
        </p>
        <div className="font-extrabold text-slate-900 dark:text-slate-100 text-sm sm:text-base py-1 bg-slate-50 dark:bg-slate-800/60 rounded-xl border border-slate-200/60 dark:border-slate-700/60 inline-block px-4">
          {email}
        </div>
      </div>

      <div className="p-3 bg-slate-50 dark:bg-slate-800/40 border border-slate-200/60 dark:border-slate-700/60 rounded-2xl flex items-center justify-between text-xs">
        <span className="text-slate-500 dark:text-slate-400 font-semibold">Verification Status</span>
        <span className={`font-bold flex items-center gap-1 ${
          status === 'Verified' ? 'text-emerald-500' : status === 'Expired' ? 'text-rose-500' : 'text-amber-500'
        }`}>
          {status === 'Verified' && <CheckCircle2 size={14} />}
          {status === 'Expired' && <AlertCircle size={14} />}
          {status === 'Pending' && <Clock size={14} className="animate-spin" />}
          {status}
        </span>
      </div>

      {message && (
        <p className="text-xs text-emerald-600 dark:text-emerald-400 font-medium text-center">
          {message}
        </p>
      )}

      <div className="space-y-3 pt-2 border-t border-slate-100 dark:border-slate-800">
        <button
          onClick={() => resend()}
          disabled={countdown > 0 || loading}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-xl shadow-sm text-xs sm:text-sm transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
          {countdown > 0 ? `Resend Email (${countdown}s)` : 'Resend Verification Email'}
        </button>

        <div className="flex items-center justify-between text-xs text-slate-500">
          <Link href="/login" className="flex items-center gap-1 hover:text-slate-800 dark:hover:text-slate-200 font-semibold">
            <ArrowLeft size={12} /> Back to Login
          </Link>
          <button
            onClick={() => {
              const newEmail = prompt('Enter new email address:', email);
              if (newEmail) window.location.reload();
            }}
            className="text-blue-600 dark:text-blue-400 hover:underline font-semibold cursor-pointer"
          >
            Change Email
          </button>
        </div>
      </div>
    </div>
  );
}
