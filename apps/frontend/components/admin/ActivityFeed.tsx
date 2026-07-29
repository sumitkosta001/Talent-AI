'use client';

import React from 'react';
import { Activity } from 'lucide-react';

interface ActivityFeedProps {
  activities: { id: string; description: string; timestamp: string }[];
}

export default function ActivityFeed({ activities }: ActivityFeedProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
      <div className="flex items-center gap-1.5 border-b border-[#F1F5F9] pb-3">
        <Activity size={18} className="text-[#2563EB]" />
        <h3 className="font-bold text-[#0F172A] text-sm">Recent Platform Activity Log</h3>
      </div>

      <div className="space-y-3">
        {activities.map((act) => (
          <div key={act.id} className="flex items-start justify-between gap-4 text-xs">
            <p className="text-slate-700 leading-relaxed">{act.description}</p>
            <span className="text-[#94A3B8] font-bold whitespace-nowrap">{act.timestamp}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
