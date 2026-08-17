import React from 'react';

export default function ResumeSkeleton() {
  return (
    <div className="space-y-6 animate-pulse">
      {/* Header Skeleton */}
      <div className="space-y-2">
        <div className="h-7 w-48 bg-slate-200 rounded-lg" />
        <div className="h-4 w-96 bg-slate-100 rounded-md" />
      </div>

      {/* Current Card Skeleton */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 space-y-4">
        <div className="h-4 w-32 bg-slate-200 rounded-md" />
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 bg-slate-200 rounded-2xl" />
          <div className="space-y-2 flex-1">
            <div className="h-5 w-64 bg-slate-200 rounded-md" />
            <div className="h-3 w-40 bg-slate-100 rounded-md" />
          </div>
          <div className="flex gap-2">
            <div className="h-9 w-20 bg-slate-200 rounded-xl" />
            <div className="h-9 w-24 bg-slate-200 rounded-xl" />
          </div>
        </div>
      </div>

      {/* Dropzone Skeleton */}
      <div className="border-2 border-dashed border-slate-200 rounded-2xl p-10 flex flex-col items-center gap-3">
        <div className="w-14 h-14 bg-slate-200 rounded-2xl" />
        <div className="h-4 w-48 bg-slate-200 rounded-md" />
        <div className="h-3 w-32 bg-slate-100 rounded-md" />
      </div>

      {/* Table Skeleton */}
      <div className="bg-white rounded-2xl border border-slate-200 p-5 space-y-3">
        <div className="h-5 w-40 bg-slate-200 rounded-md mb-4" />
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-12 w-full bg-slate-100 rounded-xl" />
        ))}
      </div>
    </div>
  );
}
