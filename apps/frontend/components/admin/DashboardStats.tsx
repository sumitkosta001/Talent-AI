'use client';

import React from 'react';
import { Users, UserCheck, Briefcase, Database, Cpu } from 'lucide-react';
import { PlatformKPIs } from '@/types/admin';

interface DashboardStatsProps {
  kpis: PlatformKPIs;
}

export default function DashboardStats({ kpis }: DashboardStatsProps) {
  const cards = [
    { label: 'Total Platform Users', value: kpis.totalUsers, icon: Users, color: 'bg-blue-50 text-blue-600 border-blue-100' },
    { label: 'Candidates Registered', value: kpis.candidatesCount, icon: UserCheck, color: 'bg-emerald-50 text-emerald-600 border-emerald-100' },
    { label: 'Recruiters Active', value: kpis.recruitersCount, icon: UserCheck, color: 'bg-violet-50 text-violet-600 border-violet-100' },
    { label: 'Active Jobs listings', value: kpis.activeJobsCount, icon: Briefcase, color: 'bg-pink-50 text-pink-600 border-pink-100' },
    { label: 'Daily API Requests', value: kpis.apiRequestsToday, icon: Database, color: 'bg-amber-50 text-amber-600 border-amber-100' },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
      {cards.map(({ label, value, icon: Icon, color }) => (
        <div key={label} className="bg-white rounded-2xl border border-[#E2E8F0] p-4 shadow-sm flex flex-col justify-between min-h-[110px] text-left animate-in fade-in slide-in-from-top-2 duration-150">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-[#64748B] line-clamp-1">{label}</span>
            <div className={`w-8 h-8 rounded-xl flex items-center justify-center border flex-shrink-0 ${color}`}>
              <Icon size={16} />
            </div>
          </div>
          <div className="text-2xl font-black text-[#0F172A] mt-2">
            {typeof value === 'number' ? value.toLocaleString() : value}
          </div>
        </div>
      ))}
    </div>
  );
}
