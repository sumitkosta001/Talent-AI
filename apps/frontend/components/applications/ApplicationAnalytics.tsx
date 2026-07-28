'use client';

import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Analytics } from '@/types/application';
import { MOCK_ATS_TREND } from '@/mock/analytics';

interface ApplicationAnalyticsProps {
  analytics: Analytics;
}

const COLORS = ['#2563EB', '#8B5CF6', '#10B981', '#EF4444', '#F59E0B'];

export default function ApplicationAnalytics({ analytics }: ApplicationAnalyticsProps) {
  const { applicationsPerMonth, statusDistribution, averageAtsScore, successRate, responseRate, interviewRatio } = analytics;

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-6 text-[#0F172A]">
      <div className="text-left border-b border-[#F1F5F9] pb-3">
        <h3 className="font-bold text-base">Application Analytics Dashboard</h3>
        <p className="text-xs text-[#64748B] mt-0.5">Statistical metrics on your job search performance.</p>
      </div>

      {/* Grid counters */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {[
          { label: 'Success Rate', value: `${successRate}%`, color: 'text-emerald-600 bg-emerald-50/50' },
          { label: 'Response Rate', value: `${responseRate}%`, color: 'text-blue-600 bg-blue-50/50' },
          { label: 'Interview Ratio', value: `${interviewRatio}%`, color: 'text-violet-600 bg-violet-50/50' },
          { label: 'Average ATS Score', value: `${averageAtsScore}%`, color: 'text-amber-600 bg-amber-50/50' },
        ].map(({ label, value, color }) => (
          <div key={label} className="p-3 bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl text-center">
            <span className={`text-base font-black ${color} px-2 py-0.5 rounded-md inline-block`}>{value}</span>
            <p className="text-[10px] text-[#64748B] font-bold mt-1.5 uppercase">{label}</p>
          </div>
        ))}
      </div>

      {/* Charts splits */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Area chart */}
        <div className="space-y-3">
          <h4 className="font-bold text-xs text-[#64748B] uppercase tracking-wide text-left">Applications Trend</h4>
          <div className="w-full h-48">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={applicationsPerMonth}>
                <defs>
                  <linearGradient id="colorApps" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#2563EB" stopOpacity={0.2} />
                    <stop offset="95%" stopColor="#2563EB" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" vertical={false} />
                <XAxis dataKey="month" tick={{ fontSize: 11, fill: '#94A3B8' }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 11, fill: '#94A3B8' }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ fontSize: 11, borderRadius: 12, border: '1px solid #E2E8F0' }} />
                <Area type="monotone" dataKey="count" stroke="#2563EB" strokeWidth={2} fillOpacity={1} fill="url(#colorApps)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Pie chart */}
        <div className="space-y-3">
          <h4 className="font-bold text-xs text-[#64748B] uppercase tracking-wide text-left">Status Distribution</h4>
          <div className="flex flex-col sm:flex-row items-center gap-4">
            <div className="w-40 h-40 flex-shrink-0">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={statusDistribution}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={65}
                    paddingAngle={2}
                    dataKey="count"
                  >
                    {statusDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ fontSize: 11, borderRadius: 12, border: '1px solid #E2E8F0' }} />
                </PieChart>
              </ResponsiveContainer>
            </div>
            
            {/* Pie Legends */}
            <div className="space-y-1.5 text-left text-xs">
              {statusDistribution.map((item, idx) => (
                <div key={item.status} className="flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-sm flex-shrink-0" style={{ backgroundColor: COLORS[idx % COLORS.length] }} />
                  <span className="font-semibold text-slate-700">{item.status}</span>
                  <span className="text-slate-400">({item.count})</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
