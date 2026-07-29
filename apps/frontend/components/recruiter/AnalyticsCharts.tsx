'use client';

import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

interface AnalyticsChartsProps {
  funnelData: { stage: string; count: number }[];
}

const COLORS = ['#2563EB', '#8B5CF6', '#10B981', '#EF4444', '#F59E0B', '#64748B'];

const MOCK_MONTHLY_DATA = [
  { month: 'Feb', applications: 120, hired: 4 },
  { month: 'Mar', applications: 150, hired: 6 },
  { month: 'Apr', applications: 180, hired: 8 },
  { month: 'May', applications: 240, hired: 12 },
  { month: 'Jun', applications: 210, hired: 10 },
  { month: 'Jul', applications: 284, hired: 15 },
];

export default function AnalyticsCharts({ funnelData }: AnalyticsChartsProps) {
  return (
    <div className="space-y-6 text-[#0F172A] text-left">
      <div className="grid md:grid-cols-2 gap-6">
        {/* Monthly Trend Area Chart */}
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
          <div>
            <h3 className="font-bold text-xs uppercase tracking-wide text-slate-500">Monthly Applications Volume</h3>
            <p className="text-[10px] text-slate-400 mt-0.5">Total candidate applications submitted by month.</p>
          </div>
          <div className="w-full h-52">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={MOCK_MONTHLY_DATA}>
                <defs>
                  <linearGradient id="colorRecApps" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#2563EB" stopOpacity={0.2} />
                    <stop offset="95%" stopColor="#2563EB" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" vertical={false} />
                <XAxis dataKey="month" tick={{ fontSize: 11, fill: '#94A3B8' }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 11, fill: '#94A3B8' }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ fontSize: 11, borderRadius: 12, border: '1px solid #E2E8F0' }} />
                <Area type="monotone" dataKey="applications" stroke="#2563EB" strokeWidth={2} fillOpacity={1} fill="url(#colorRecApps)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Funnel distribution Pie chart */}
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
          <div>
            <h3 className="font-bold text-xs uppercase tracking-wide text-slate-500">Stages Funnel Distribution</h3>
            <p className="text-[10px] text-slate-400 mt-0.5">Distribution counts across matching loops.</p>
          </div>
          <div className="flex flex-col sm:flex-row items-center gap-4">
            <div className="w-40 h-40 flex-shrink-0">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={funnelData}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={65}
                    paddingAngle={2}
                    dataKey="count"
                    nameKey="stage"
                  >
                    {funnelData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ fontSize: 11, borderRadius: 12, border: '1px solid #E2E8F0' }} />
                </PieChart>
              </ResponsiveContainer>
            </div>
            
            {/* Pie Legends */}
            <div className="space-y-1.5 text-left text-xs">
              {funnelData.map((item, idx) => (
                <div key={item.stage} className="flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-sm flex-shrink-0" style={{ backgroundColor: COLORS[idx % COLORS.length] }} />
                  <span className="font-semibold text-slate-700">{item.stage}</span>
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
