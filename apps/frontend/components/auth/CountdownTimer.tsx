'use client';

import React from 'react';
import { Clock } from 'lucide-react';

interface CountdownTimerProps {
  seconds: number;
  onResend: () => void;
  disabled?: boolean;
}

export default function CountdownTimer({ seconds, onResend, disabled = false }: CountdownTimerProps) {
  const isExpired = seconds <= 0;

  return (
    <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
      <div className="flex items-center gap-1">
        <Clock size={12} className={!isExpired ? 'animate-pulse text-blue-500' : ''} />
        {isExpired ? (
          <span>Code expired</span>
        ) : (
          <span>Resend code in <strong className="text-slate-800 dark:text-slate-200">{seconds}s</strong></span>
        )}
      </div>

      <button
        type="button"
        disabled={!isExpired || disabled}
        onClick={onResend}
        className="font-bold text-blue-600 dark:text-blue-400 hover:underline disabled:opacity-40 disabled:no-underline cursor-pointer disabled:cursor-not-allowed"
      >
        Resend Code
      </button>
    </div>
  );
}
