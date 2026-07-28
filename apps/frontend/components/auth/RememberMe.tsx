'use client';

import React from 'react';

interface RememberMeProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
  disabled?: boolean;
}

export default function RememberMe({ checked, onChange, disabled = false }: RememberMeProps) {
  return (
    <div className="flex items-center gap-2">
      <input
        type="checkbox"
        id="remember-me"
        checked={checked}
        disabled={disabled}
        onChange={(e) => onChange(e.target.checked)}
        className="w-4 h-4 rounded border-slate-300 dark:border-slate-700 text-blue-600 focus:ring-blue-500/20 cursor-pointer"
      />
      <label htmlFor="remember-me" className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 select-none cursor-pointer">
        Remember me on this device
      </label>
    </div>
  );
}
