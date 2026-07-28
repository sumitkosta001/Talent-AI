'use client';

import React, { useState } from 'react';
import { ShieldCheck, Smartphone, Mail, Key, ArrowRight, CheckCircle2 } from 'lucide-react';
import { useRouter } from 'next/navigation';
import OTPInput from './OTPInput';
import CountdownTimer from './CountdownTimer';
import { useOTP } from '@/hooks/useOTP';
import { useTwoFactor } from '@/hooks/useTwoFactor';

export default function TwoFactorCard() {
  const router = useRouter();
  const { method, setMethod, verifyCode } = useTwoFactor();
  const [rememberDevice, setRememberDevice] = useState(true);

  const { digits, loading, error, success, countdown, inputRefs, handleChange, handleKeyDown, handlePaste, resend } = useOTP(6, async (code) => {
    const isOk = await verifyCode(code, rememberDevice);
    if (isOk) {
      setTimeout(() => {
        router.push('/candidate');
      }, 800);
    }
  });

  const handleManualSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const isOk = await verifyCode(digits.join(''), rememberDevice);
    if (isOk) {
      setTimeout(() => {
        router.push('/candidate');
      }, 800);
    }
  };

  return (
    <div className="bg-white dark:bg-[#1E293B] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 sm:p-8 max-w-md w-full shadow-xl text-left">
      <div className="w-14 h-14 bg-blue-50 dark:bg-blue-950/30 text-blue-600 dark:text-blue-400 border border-blue-100 dark:border-blue-900/50 rounded-2xl flex items-center justify-center mx-auto mb-4">
        <ShieldCheck size={28} />
      </div>

      <div className="text-center space-y-1.5 mb-6">
        <h2 className="text-xl sm:text-2xl font-black text-slate-900 dark:text-slate-100">
          Two-Factor Authentication
        </h2>
        <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
          Enter the 6-digit security code from your authenticator app.
        </p>
      </div>

      <div className="grid grid-cols-3 gap-1.5 p-1 bg-slate-100 dark:bg-slate-800 rounded-2xl mb-5 text-xs">
        <button
          type="button"
          onClick={() => setMethod('authenticator')}
          className={`py-2 px-2 rounded-xl font-bold transition-all flex items-center justify-center gap-1 cursor-pointer ${
            method === 'authenticator'
              ? 'bg-white dark:bg-slate-700 text-blue-600 dark:text-blue-400 shadow-xs'
              : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
          }`}
        >
          <Smartphone size={14} /> App
        </button>

        <button
          type="button"
          onClick={() => setMethod('sms')}
          className={`py-2 px-2 rounded-xl font-bold transition-all flex items-center justify-center gap-1 cursor-pointer ${
            method === 'sms'
              ? 'bg-white dark:bg-slate-700 text-blue-600 dark:text-blue-400 shadow-xs'
              : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
          }`}
        >
          <Mail size={14} /> SMS
        </button>

        <button
          type="button"
          onClick={() => setMethod('recovery')}
          className={`py-2 px-2 rounded-xl font-bold transition-all flex items-center justify-center gap-1 cursor-pointer ${
            method === 'recovery'
              ? 'bg-white dark:bg-slate-700 text-blue-600 dark:text-blue-400 shadow-xs'
              : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
          }`}
        >
          <Key size={14} /> Code
        </button>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-rose-50 text-rose-600 dark:bg-rose-950/30 dark:text-rose-400 rounded-xl text-xs font-semibold border border-rose-100 dark:border-rose-900/50">
          {error}
        </div>
      )}

      {success && (
        <div className="mb-4 p-3 bg-emerald-50 text-emerald-600 dark:bg-emerald-950/30 dark:text-emerald-400 rounded-xl text-xs font-semibold border border-emerald-100 dark:border-emerald-900/50 flex items-center gap-2">
          <CheckCircle2 size={16} /> 2FA Verified! Redirecting...
        </div>
      )}

      <form onSubmit={handleManualSubmit} className="space-y-4">
        <OTPInput
          digits={digits}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          onPaste={handlePaste}
          inputRefs={inputRefs}
          error={!!error}
          disabled={loading || success}
        />

        <CountdownTimer seconds={countdown} onResend={() => resend()} disabled={loading} />

        <div className="flex items-center gap-2 pt-2">
          <input
            type="checkbox"
            id="remember-device"
            checked={rememberDevice}
            onChange={(e) => setRememberDevice(e.target.checked)}
            className="w-4 h-4 rounded border-slate-300 dark:border-slate-700 text-blue-600 focus:ring-blue-500/20 cursor-pointer"
          />
          <label htmlFor="remember-device" className="text-xs text-slate-600 dark:text-slate-400 select-none cursor-pointer">
            Trust this device for 30 days
          </label>
        </div>

        <button
          type="submit"
          disabled={loading || success || digits.join('').length < 6}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-xl shadow-sm text-xs sm:text-sm transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {loading ? 'Verifying...' : 'Verify Code'}
          {!loading && <ArrowRight size={16} />}
        </button>
      </form>
    </div>
  );
}
