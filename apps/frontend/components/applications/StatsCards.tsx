'use client';

import React from 'react';
import { FileText, Calendar, Award, AlertTriangle, Briefcase } from 'lucide-react';
import { Application } from '@/types/application';

interface StatsCardsProps {
  applications: Application[];
}

export default function StatsCards({ applications }: StatsCardsProps) {
  const total = applications.length;
  const interviews = applications.filter(a => a.status === 'Technical Interview' || a.status === 'Final Interview' || a.status === 'HR Interview').length;
  const offers = applications.filter(a => a.status === 'Offer Received' || a.status === 'Offer Accepted').length;
  const rejected = applications.filter(a => a.status === 'Rejected').length;
  
  // Calculate average ATS Score
  const validAtsApps = applications.filter(a => a.atsScore > 0);
  const averageAts = validAtsApps.length > 0 
    ? Math.round(validAtsApps.reduce((acc, a) => acc + a.atsScore, 0) / validAtsApps.length)
    : 0;

  const stats = [
    { label: 'Total Applications', value: total, icon: Briefcase, color: 'bg-blue-50 text-blue-600 border-blue-100' },
    { label: 'Interviews Scheduled', value: interviews, icon: Calendar, color: 'bg-violet-50 text-violet-600 border-violet-100' },
    { label: 'Offers Received', value: offers, icon: Award, color: 'bg-emerald-50 text-emerald-600 border-emerald-100' },
    { label: 'Rejections', value: rejected, icon: AlertTriangle, color: 'bg-red-50 text-red-600 border-red-100' },
    { label: 'Average ATS Score', value: `${averageAts}%`, icon: FileText, color: 'bg-amber-50 text-amber-600 border-amber-100' },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
      {stats.map(({ label, value, icon: Icon, color }) => (
        <div key={label} className={`bg-white rounded-2xl border border-[#E2E8F0] p-4 text-left shadow-sm flex flex-col justify-between min-h-[110px]`}>
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-[#64748B] line-clamp-1">{label}</span>
            <div className={`w-8 h-8 rounded-xl flex items-center justify-center border flex-shrink-0 ${color}`}>
              <Icon size={16} />
            </div>
          </div>
          <div className="text-2xl font-black text-[#0F172A] mt-2">{value}</div>
        </div>
      ))}
    </div>
  );
}
