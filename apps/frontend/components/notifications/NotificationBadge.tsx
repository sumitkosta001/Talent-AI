'use client';

import React from 'react';

interface NotificationBadgeProps {
  category: string;
}

export default function NotificationBadge({ category }: NotificationBadgeProps) {
  const getBadgeStyle = (cat: string) => {
    switch (cat) {
      case 'Jobs':
        return 'bg-blue-50 text-blue-700 border-blue-100';
      case 'ATS':
        return 'bg-purple-50 text-purple-700 border-purple-100';
      case 'Applications':
        return 'bg-orange-50 text-orange-700 border-orange-100';
      case 'Recruiters':
        return 'bg-pink-50 text-pink-700 border-pink-100';
      case 'Interviews':
        return 'bg-indigo-50 text-indigo-700 border-indigo-100';
      case 'Offers':
        return 'bg-emerald-50 text-emerald-700 border-emerald-100';
      case 'Resume':
        return 'bg-amber-50 text-amber-700 border-amber-100';
      case 'Security':
        return 'bg-red-50 text-red-700 border-red-100';
      default:
        return 'bg-slate-50 text-slate-700 border-slate-100';
    }
  };

  return (
    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border uppercase tracking-wider ${getBadgeStyle(category)}`}>
      {category}
    </span>
  );
}
