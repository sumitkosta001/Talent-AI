'use client';

import React from 'react';

export function CardSkeleton() {
  return (
    <div className="bg-white dark:bg-[#1E293B] border border-slate-200 dark:border-slate-800 rounded-3xl p-5 space-y-4 animate-pulse text-left w-full">
      <div className="flex items-center justify-between">
        <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded-lg w-24" />
        <div className="w-8 h-8 rounded-xl bg-slate-200 dark:bg-slate-700 animate-pulse" />
      </div>
      <div className="h-6 bg-slate-200 dark:bg-slate-700 rounded-lg w-16" />
    </div>
  );
}

export function TableSkeleton() {
  return (
    <div className="bg-white dark:bg-[#1E293B] border border-slate-200 dark:border-slate-800 rounded-3xl p-5 space-y-4 animate-pulse w-full">
      <div className="flex items-center gap-3 pb-3 border-b border-slate-100 dark:border-slate-800">
        <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-1/4" />
        <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-1/4" />
        <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-1/4" />
      </div>
      <div className="space-y-3">
        {[1, 2, 3].map((n) => (
          <div key={n} className="flex items-center gap-3">
            <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-1/3" />
            <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-1/3" />
            <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-1/3" />
          </div>
        ))}
      </div>
    </div>
  );
}

export function ChartSkeleton() {
  return (
    <div className="bg-white dark:bg-[#1E293B] border border-slate-200 dark:border-slate-800 rounded-3xl p-5 space-y-4 animate-pulse w-full">
      <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-1/3" />
      <div className="h-48 bg-slate-100 dark:bg-slate-800 rounded-2xl w-full" />
    </div>
  );
}

export function ProfileSkeleton() {
  return (
    <div className="bg-white dark:bg-[#1E293B] border border-slate-200 dark:border-slate-800 rounded-3xl p-5 space-y-6 animate-pulse w-full text-left">
      <div className="flex items-center gap-4">
        <div className="w-16 h-16 rounded-full bg-slate-200 dark:bg-slate-700" />
        <div className="space-y-2">
          <div className="h-5 bg-slate-200 dark:bg-slate-700 rounded w-32" />
          <div className="h-3 bg-slate-200 dark:bg-slate-700 rounded w-24" />
        </div>
      </div>
      <div className="space-y-3 pt-4 border-t border-slate-150 dark:border-slate-800">
        <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-full" />
        <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-5/6" />
        <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-4/5" />
      </div>
    </div>
  );
}

export default function LoadingSkeleton() {
  return <CardSkeleton />;
}
