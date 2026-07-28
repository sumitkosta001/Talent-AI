'use client';

import React from 'react';
import { Briefcase, FileText, Bell, Bookmark, Search, Building2, Users, Database, History, AlertTriangle } from 'lucide-react';
import { MOCK_EMPTY_STATES } from '@/mock/emptyStates';
import Link from 'next/link';

interface EmptyStateProps {
  type: keyof typeof MOCK_EMPTY_STATES;
  title?: string;
  description?: string;
  primaryActionText?: string;
  primaryActionUrl?: string;
  secondaryActionText?: string;
  secondaryActionUrl?: string;
}

export default function EmptyState({
  type,
  title,
  description,
  primaryActionText,
  primaryActionUrl,
  secondaryActionText,
  secondaryActionUrl,
}: EmptyStateProps) {
  const config = MOCK_EMPTY_STATES[type] || MOCK_EMPTY_STATES.jobs;

  const displayTitle = title || config.title;
  const displayDescription = description || config.description;
  const pActionText = primaryActionText || config.primaryActionText;
  const pActionUrl = primaryActionUrl || config.primaryActionUrl;
  const sActionText = secondaryActionText || config.secondaryActionText;
  const sActionUrl = secondaryActionUrl || config.secondaryActionUrl;

  const getIcon = () => {
    const iconSize = 28;
    switch (config.iconType) {
      case 'briefcase':
        return <Briefcase size={iconSize} />;
      case 'file-text':
        return <FileText size={iconSize} />;
      case 'bell':
        return <Bell size={iconSize} />;
      case 'bookmark':
        return <Bookmark size={iconSize} />;
      case 'search':
        return <Search size={iconSize} />;
      case 'building':
        return <Building2 size={iconSize} />;
      case 'users':
        return <Users size={iconSize} />;
      case 'database':
        return <Database size={iconSize} />;
      case 'history':
        return <History size={iconSize} />;
      default:
        return <AlertTriangle size={iconSize} />;
    }
  };

  return (
    <div className="flex flex-col items-center justify-center p-8 text-center max-w-md mx-auto space-y-4 border border-dashed border-slate-200 dark:border-slate-800 rounded-3xl bg-slate-50/50 dark:bg-slate-900/10 text-left">
      <div className="w-14 h-14 bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 border border-slate-200 dark:border-slate-700 rounded-2xl flex items-center justify-center">
        {getIcon()}
      </div>

      <div className="space-y-1.5 text-center">
        <h3 className="text-sm sm:text-base font-extrabold text-slate-900 dark:text-slate-100">
          {displayTitle}
        </h3>
        <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 leading-relaxed pr-2">
          {displayDescription}
        </p>
      </div>

      {(pActionText || sActionText) && (
        <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
          {pActionText && pActionUrl && (
            <Link href={pActionUrl}>
              <button className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-xl shadow-sm text-xs transition-colors cursor-pointer">
                {pActionText}
              </button>
            </Link>
          )}
          {pActionText && !pActionUrl && (
            <button className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-xl shadow-sm text-xs transition-colors cursor-pointer">
              {pActionText}
            </button>
          )}

          {sActionText && sActionUrl && (
            <Link href={sActionUrl}>
              <button className="border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-350 font-bold py-2 px-4 rounded-xl text-xs transition-colors cursor-pointer">
                {sActionText}
              </button>
            </Link>
          )}
        </div>
      )}
    </div>
  );
}
