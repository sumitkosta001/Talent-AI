'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, Mail, CheckCircle2, ArrowRight } from 'lucide-react';
import { passwordService } from '@/services/password.service';

export default function ForgotPasswordForm() {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setError('Please enter a valid email address');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const res = await passwordService.requestReset(email);
      if (res.success) {
        setSubmitted(true);
      } else {
        setError(res.message);
      }
    } catch {
      setError('Failed to send reset email. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full space-y-4 text-left">
      {submitted ? (
        <div className="bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 text-center space-y-4">
          <div className="w-14 h-14 bg-emerald-50 dark:bg-emerald-950/30 text-emerald-500 border border-emerald-100 dark:border-emerald-900/50 rounded-2xl flex items-center justify-center mx-auto">
            <CheckCircle2 size={28} />
          </div>
          <h3 className="text-lg font-black text-slate-900 dark:text-slate-100">
            Check Your Email
          </h3>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
            We sent password reset instructions to <strong className="text-slate-800 dark:text-slate-200">{email}</strong>.
          </p>
          <div className="pt-2">
            <Link href="/reset-password">
              <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2.5 px-4 rounded-xl text-xs sm:text-sm shadow-sm transition-colors cursor-pointer mb-2">
                Go to Reset Password Screen
              </button>
            </Link>
            <Link href="/login" className="text-xs text-slate-500 hover:text-slate-800 font-bold inline-flex items-center gap-1">
              <ArrowLeft size={12} /> Return to Login
            </Link>
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="p-3 bg-rose-50 text-rose-600 dark:bg-rose-950/30 dark:text-rose-400 rounded-xl text-xs font-semibold border border-rose-100 dark:border-rose-900/50">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-slate-900 dark:text-slate-200 mb-1.5">
              Email Address
            </label>
            <div className="relative">
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="alex@example.com"
                className="w-full pl-9 pr-3.5 py-2.5 border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 rounded-xl text-sm text-slate-900 dark:text-white focus:outline-none focus:border-blue-500"
              />
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading || !email}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-xl shadow-sm text-xs sm:text-sm transition-colors cursor-pointer disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {loading ? 'Sending Instructions...' : 'Send Reset Instructions'}
            {!loading && <ArrowRight size={16} />}
          </button>

          <p className="text-center text-xs sm:text-sm text-slate-500 dark:text-slate-400 pt-2">
            Remember your password?{' '}
            <Link href="/login" className="text-blue-600 dark:text-blue-400 font-bold hover:underline">
              Back to Login
            </Link>
          </p>
        </form>
      )}
    </div>
  );
}
