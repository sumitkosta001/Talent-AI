'use client';

import React from 'react';
import { Check, X } from 'lucide-react';

interface KeywordBadgeProps {
  name: string;
  matched: boolean;
  frequency?: number;
  category?: string;
  importance?: 'high' | 'medium' | 'low';
}

export default function KeywordBadge({
  name,
  matched,
  frequency = 0,
  category,
  importance,
}: KeywordBadgeProps) {
  const badgeStyles = matched
    ? 'bg-green-50 text-green-700 border-green-200'
    : 'bg-red-50 text-red-700 border-red-200';

  const importanceBadge = importance && (
    <span className={`text-[9px] font-bold px-1.5 py-0.2 rounded-full uppercase ml-1.5 ${
      importance === 'high'
        ? 'bg-red-100 text-red-700'
        : importance === 'medium'
        ? 'bg-amber-100 text-amber-700'
        : 'bg-blue-100 text-blue-700'
    }`}>
      {importance}
    </span>
  );

  return (
    <div className={`inline-flex items-center gap-1 px-3 py-1.5 rounded-full border text-xs font-semibold ${badgeStyles}`}>
      {matched ? <Check size={11} className="text-green-600" /> : <X size={11} className="text-red-600" />}
      <span>{name}</span>
      {frequency > 0 && <span className="text-[10px] text-slate-500 font-bold ml-1">({frequency}x)</span>}
      {category && <span className="text-[9px] bg-slate-100 text-slate-600 font-medium px-1 rounded-sm ml-1">{category}</span>}
      {importanceBadge}
    </div>
  );
}
