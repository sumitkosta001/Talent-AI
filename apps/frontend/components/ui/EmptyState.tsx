'use client';

import React from 'react';
import { AlertCircle, Plus, RefreshCw } from 'lucide-react';
import Link from 'next/link';

interface EmptyStateProps {
  title: string;
  description: string;
  icon?: React.ReactNode;
  actionText?: string;
  actionHref?: string;
  onAction?: () => void;
  secondaryActionText?: string;
  onSecondaryAction?: () => void;
  className?: string;
}

export default function EmptyState({
  title,
  description,
  icon,
  actionText,
  actionHref,
  onAction,
  secondaryActionText,
  onSecondaryAction,
  className = '',
}: EmptyStateProps) {
  return (
    <div className={`bg-white dark:bg-[#1E293B] border border-dashed border-slate-200 dark:border-slate-800 rounded-3xl p-8 max-w-md mx-auto text-center space-y-4 shadow-xs ${className}`}>
      <div className="w-14 h-14 bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 border border-slate-200 dark:border-slate-700 rounded-2xl flex items-center justify-center mx-auto">
        {icon || <AlertCircle size={28} />}
      </div>

      <div className="space-y-1 text-center">
        <h3 className="text-base sm:text-lg font-black text-slate-900 dark:text-slate-100">{title}</h3>
        <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 leading-relaxed pr-2">{description}</p>
      </div>

      {(actionText || secondaryActionText) && (
        <div className="flex flex-wrap items-center justify-center gap-2 pt-2">
          {actionText && actionHref && (
            <Link href={actionHref}>
              <button className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-xl text-xs shadow-sm transition-colors cursor-pointer inline-flex items-center gap-1.5">
                <Plus size={14} />
                {actionText}
              </button>
            </Link>
          )}

          {actionText && !actionHref && onAction && (
            <button
              onClick={onAction}
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-xl text-xs shadow-sm transition-colors cursor-pointer inline-flex items-center gap-1.5"
            >
              <Plus size={14} />
              {actionText}
            </button>
          )}

          {secondaryActionText && onSecondaryAction && (
            <button
              onClick={onSecondaryAction}
              className="border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-300 font-bold py-2 px-4 rounded-xl text-xs transition-colors cursor-pointer inline-flex items-center gap-1.5"
            >
              <RefreshCw size={12} />
              {secondaryActionText}
            </button>
          )}
        </div>
      )}
    </div>
  );
}
