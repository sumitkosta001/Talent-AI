'use client';

import React, { useState } from 'react';
import { Key, CheckCircle2, ArrowRight } from 'lucide-react';
import { MOCK_RECOVERY_CODES } from '@/mock/twoFactor';

export default function RecoveryCodeCard() {
  const [code, setCode] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (MOCK_RECOVERY_CODES.includes(code.trim().toUpperCase())) {
      setSuccess(true);
      setError('');
    } else {
      setError('Invalid recovery code. Please check your backup codes list.');
      setSuccess(false);
    }
  };

  return (
    <div className="bg-white dark:bg-[#1E293B] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 sm:p-8 max-w-md w-full shadow-xl text-left">
      <div className="w-14 h-14 bg-amber-50 dark:bg-amber-950/30 text-amber-500 border border-amber-100 dark:border-amber-900/50 rounded-2xl flex items-center justify-center mx-auto mb-4">
        <Key size={28} />
      </div>

      <div className="text-center space-y-1.5 mb-6">
        <h2 className="text-xl sm:text-2xl font-black text-slate-900 dark:text-slate-100">
          Emergency Recovery Code
        </h2>
        <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
          Enter one of your 12-character backup recovery codes to access your account.
        </p>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-rose-50 text-rose-600 dark:bg-rose-950/30 dark:text-rose-400 rounded-xl text-xs font-semibold border border-rose-100 dark:border-rose-900/50">
          {error}
        </div>
      )}

      {success && (
        <div className="mb-4 p-3 bg-emerald-50 text-emerald-600 dark:bg-emerald-950/30 dark:text-emerald-400 rounded-xl text-xs font-semibold border border-emerald-100 dark:border-emerald-900/50 flex items-center gap-2">
          <CheckCircle2 size={16} /> Recovery Code Accepted! Logging in...
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1.5 uppercase tracking-wider">
            Recovery Code
          </label>
          <input
            type="text"
            required
            placeholder="XXXX-XXXX-XXXX"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="w-full font-mono text-center font-bold px-3 py-3 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-sm sm:text-base text-slate-900 dark:text-white uppercase tracking-widest focus:outline-none focus:border-blue-500"
          />
        </div>

        <button
          type="submit"
          disabled={!code.trim() || success}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-xl shadow-sm text-xs sm:text-sm transition-colors cursor-pointer disabled:opacity-50 flex items-center justify-center gap-2"
        >
          Verify Recovery Code
          <ArrowRight size={16} />
        </button>
      </form>
    </div>
  );
}
