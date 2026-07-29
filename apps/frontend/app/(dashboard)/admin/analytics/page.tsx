'use client';

import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const MOCK_PLATFORM_TRENDS = [
  { month: 'Feb', visitors: 1200, signups: 420 },
  { month: 'Mar', visitors: 1500, signups: 580 },
  { month: 'Apr', visitors: 2200, signups: 890 },
  { month: 'May', visitors: 1900, signups: 720 },
  { month: 'Jun', visitors: 2800, signups: 1100 },
  { month: 'Jul', visitors: 3400, signups: 1482 },
];

const COLORS = ['#2563EB', '#8B5CF6', '#10B981', '#EF4444'];

const MOCK_ROLE_DISTRIBUTION = [
  { name: 'Candidates', value: 1482 },
  { name: 'Recruiters', value: 284 },
];

export default function AdminAnalyticsPage() {
  return (
    <div className="p-6 space-y-6 max-w-6xl mx-auto text-[#0F172A] text-left">
      <div className="border-b border-[#E2E8F0] pb-5">
        <h1 className="text-xl sm:text-2xl font-bold">Platform Analytics</h1>
        <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">Statistical metrics on visitor traffic volumes, user signups, and role ratios.</p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Signups and traffic trend area chart */}
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
          <div>
            <h3 className="font-bold text-xs uppercase tracking-wide text-slate-500">Traffic & Signups Trend</h3>
            <p className="text-[10px] text-slate-400 mt-0.5 font-medium">Monthly visitor traffic versus registration conversion stats.</p>
          </div>
          <div className="w-full h-56">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={MOCK_PLATFORM_TRENDS} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="visitorGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#2563EB" stopOpacity={0.12} />
                    <stop offset="95%" stopColor="#2563EB" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="signupGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10B981" stopOpacity={0.12} />
                    <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" vertical={false} />
                <XAxis dataKey="month" tick={{ fontSize: 11, fill: '#94A3B8' }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 11, fill: '#94A3B8' }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ fontSize: 11, borderRadius: 12, border: '1px solid #E2E8F0' }} />
                <Area type="monotone" dataKey="visitors" stroke="#2563EB" strokeWidth={2} fill="url(#visitorGrad)" name="Monthly Visitors" />
                <Area type="monotone" dataKey="signups" stroke="#10B981" strokeWidth={2} fill="url(#signupGrad)" name="User Signups" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Roles count distribution chart */}
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
          <div>
            <h3 className="font-bold text-xs uppercase tracking-wide text-slate-500">Accounts Role Ratios</h3>
            <p className="text-[10px] text-slate-400 mt-0.5 font-medium">Distribution count ratio between candidate users and recruiters.</p>
          </div>
          <div className="flex flex-col sm:flex-row items-center gap-4 pt-4">
            <div className="w-44 h-44 flex-shrink-0 mx-auto sm:mx-0">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={MOCK_ROLE_DISTRIBUTION}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={65}
                    paddingAngle={2}
                    dataKey="value"
                    nameKey="name"
                  >
                    {MOCK_ROLE_DISTRIBUTION.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ fontSize: 11, borderRadius: 12, border: '1px solid #E2E8F0' }} />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* Legends */}
            <div className="space-y-1.5 text-xs text-left">
              {MOCK_ROLE_DISTRIBUTION.map((item, idx) => (
                <div key={item.name} className="flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-sm flex-shrink-0" style={{ backgroundColor: COLORS[idx % COLORS.length] }} />
                  <span className="font-semibold text-slate-700">{item.name}</span>
                  <span className="text-slate-400">({item.value})</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
export type UserStatus = 'Active' | 'Suspended' | 'Deactivated';
