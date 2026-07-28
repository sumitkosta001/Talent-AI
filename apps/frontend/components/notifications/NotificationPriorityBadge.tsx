'use client';

import React from 'react';
import { AlertCircle, AlertTriangle, Info } from 'lucide-react';
import { NotificationPriority } from '@/types/notification';

interface NotificationPriorityBadgeProps {
  priority: NotificationPriority;
}

export default function NotificationPriorityBadge({ priority }: NotificationPriorityBadgeProps) {
  const getBadgeStyle = (p: NotificationPriority) => {
    switch (p) {
      case 'High':
        return { style: 'bg-red-50 text-red-700 border-red-100', icon: AlertCircle };
      case 'Medium':
        return { style: 'bg-amber-50 text-amber-700 border-amber-100', icon: AlertTriangle };
      default:
        return { style: 'bg-slate-50 text-slate-700 border-slate-100', icon: Info };
    }
  };

  const { style, icon: Icon } = getBadgeStyle(priority);

  return (
    <span className={`inline-flex items-center gap-1 text-[9px] font-bold px-2 py-0.5 rounded-full border uppercase tracking-wider ${style}`}>
      <Icon size={10} />
      {priority}
    </span>
  );
}
