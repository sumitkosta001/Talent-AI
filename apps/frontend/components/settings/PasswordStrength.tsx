'use client';

import React from 'react';

interface PasswordStrengthProps {
  val: string;
}

export default function PasswordStrength({ val }: PasswordStrengthProps) {
  if (!val) return null;

  const requirements = [
    { label: 'Minimum 8 characters', met: val.length >= 8 },
    { label: 'Contains uppercase letter', met: /[A-Z]/.test(val) },
    { label: 'Contains lowercase letter', met: /[a-z]/.test(val) },
    { label: 'Contains numeric character', met: /[0-9]/.test(val) },
    { label: 'Contains special character (@, $, !, %...)', met: /[^A-Za-z0-9]/.test(val) },
  ];

  const score = requirements.filter((r) => r.met).length;

  const getStrengthStyle = (s: number) => {
    if (s <= 2) return { label: 'Weak', barColor: 'bg-red-500', textColor: 'text-red-600' };
    if (s <= 4) return { label: 'Medium', barColor: 'bg-amber-500', textColor: 'text-amber-600' };
    return { label: 'Strong', barColor: 'bg-emerald-500', textColor: 'text-emerald-600' };
  };

  const { label, barColor, textColor } = getStrengthStyle(score);

  return (
    <div className="space-y-3 text-left">
      <div className="flex items-center justify-between text-xs font-semibold">
        <span className="text-[#64748B]">Password Security Strength:</span>
        <span className={textColor}>{label}</span>
      </div>

      {/* Progress indicators bar */}
      <div className="h-1.5 w-full bg-[#E2E8F0] rounded-full overflow-hidden flex gap-0.5">
        {[1, 2, 3, 4, 5].map((step) => (
          <div
            key={step}
            className={`h-full flex-1 transition-all ${
              step <= score ? barColor : 'bg-transparent'
            }`}
          />
        ))}
      </div>

      {/* Checklist specs */}
      <div className="grid sm:grid-cols-2 gap-2 text-[10px] sm:text-xs">
        {requirements.map(({ label, met }) => (
          <div key={label} className="flex items-center gap-1.5">
            <div className={`w-3 h-3 rounded-full flex items-center justify-center text-[8px] font-black border ${
              met ? 'bg-emerald-50 border-emerald-300 text-emerald-600' : 'bg-slate-50 border-slate-200 text-slate-400'
            }`}>
              {met ? '✓' : '•'}
            </div>
            <span className={met ? 'text-slate-700 font-medium' : 'text-slate-400'}>{label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
