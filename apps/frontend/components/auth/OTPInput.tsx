'use client';

import React from 'react';
import { motion } from 'framer-motion';

interface OTPInputProps {
  digits: string[];
  onChange: (index: number, val: string) => void;
  onKeyDown: (index: number, e: React.KeyboardEvent<HTMLInputElement>) => void;
  onPaste: (e: React.ClipboardEvent<HTMLInputElement>) => void;
  inputRefs: React.MutableRefObject<(HTMLInputElement | null)[]>;
  error?: boolean;
  disabled?: boolean;
}

export default function OTPInput({
  digits,
  onChange,
  onKeyDown,
  onPaste,
  inputRefs,
  error = false,
  disabled = false,
}: OTPInputProps) {
  return (
    <div className="flex items-center justify-between gap-2 sm:gap-3 my-4">
      {digits.map((digit, idx) => (
        <motion.input
          key={idx}
          ref={(el) => {
            inputRefs.current[idx] = el;
          }}
          type="text"
          inputMode="numeric"
          maxLength={1}
          value={digit}
          disabled={disabled}
          onChange={(e) => onChange(idx, e.target.value)}
          onKeyDown={(e) => onKeyDown(idx, e)}
          onPaste={idx === 0 ? onPaste : undefined}
          whileFocus={{ scale: 1.05 }}
          className={`w-11 h-13 sm:w-12 sm:h-14 text-center font-mono font-extrabold text-xl sm:text-2xl rounded-2xl border bg-white dark:bg-slate-800 text-slate-900 dark:text-white transition-all outline-none ${
            error
              ? 'border-rose-500 text-rose-500 bg-rose-50/50 dark:bg-rose-950/20'
              : digit
              ? 'border-blue-500 bg-blue-50/30 dark:bg-blue-950/20 text-blue-600 dark:text-blue-400'
              : 'border-slate-200 dark:border-slate-700 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10'
          }`}
        />
      ))}
    </div>
  );
}
