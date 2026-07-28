'use client';

import React from 'react';

interface KeyboardShortcutItemProps {
  keys: string;
  label: string;
}

export default function KeyboardShortcutItem({ keys, label }: KeyboardShortcutItemProps) {
  const parts = keys.split('+').map((k) => k.trim());

  return (
    <div className="flex items-center justify-between gap-4 py-2 border-b border-slate-150 dark:border-slate-800/60 text-left w-full">
      <span className="text-xs font-semibold text-slate-750 dark:text-slate-200">{label}</span>
      <div className="flex items-center gap-1 flex-shrink-0">
        {parts.map((p, idx) => (
          <React.Fragment key={idx}>
            {idx > 0 && <span className="text-[10px] text-slate-400 font-bold">+</span>}
            <kbd className="px-2 py-0.5 text-[10px] font-black bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700 rounded-md shadow-xs">
              {p}
            </kbd>
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}
