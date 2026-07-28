'use client';

import React from 'react';
import { passwordService } from '@/services/password.service';
import { Check, X } from 'lucide-react';

interface PasswordStrengthProps {
  password?: string;
  showRules?: boolean;
}

export default function PasswordStrength({ password = '', showRules = true }: PasswordStrengthProps) {
  if (!password) return null;

  const { level, score, rules } = passwordService.evaluateStrength(password);

  const getMeterColor = () => {
    switch (score) {
      case 1:
        return 'bg-rose-500';
      case 2:
        return 'bg-amber-500';
      case 3:
        return 'bg-yellow-500';
      case 4:
        return 'bg-emerald-500';
      case 5:
        return 'bg-blue-600';
      default:
        return 'bg-slate-200 dark:bg-slate-700';
    }
  };

  return (
    <div className="space-y-2.5 mt-2 text-left">
      <div className="flex items-center justify-between text-xs font-semibold">
        <span className="text-slate-500 dark:text-slate-400">Password Strength</span>
        <span className="text-slate-800 dark:text-slate-200">{level}</span>
      </div>

      <div className="flex gap-1.5 h-1.5 w-full">
        {[1, 2, 3, 4, 5].map((idx) => (
          <div
            key={idx}
            className={`flex-1 rounded-full transition-all duration-300 ${
              idx <= score ? getMeterColor() : 'bg-slate-200 dark:bg-slate-700'
            }`}
          />
        ))}
      </div>

      {showRules && (
        <div className="grid grid-cols-2 gap-1.5 pt-2 text-[11px]">
          {[
            { key: 'minLength', label: '8+ characters', pass: rules.minLength },
            { key: 'hasUppercase', label: 'Uppercase (A-Z)', pass: rules.hasUppercase },
            { key: 'hasLowercase', label: 'Lowercase (a-z)', pass: rules.hasLowercase },
            { key: 'hasNumber', label: 'Number (0-9)', pass: rules.hasNumber },
            { key: 'hasSpecial', label: 'Special symbol (!@#)', pass: rules.hasSpecial },
          ].map((item) => (
            <div key={item.key} className="flex items-center gap-1.5">
              {item.pass ? (
                <Check size={12} className="text-emerald-500 flex-shrink-0" />
              ) : (
                <X size={12} className="text-slate-400 flex-shrink-0" />
              )}
              <span className={item.pass ? 'text-emerald-600 dark:text-emerald-400 font-medium' : 'text-slate-400'}>
                {item.label}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
