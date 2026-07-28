'use client';

import React from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

const applicationData = [
  { month: 'Feb', applications: 4, interviews: 1 },
  { month: 'Mar', applications: 7, interviews: 2 },
  { month: 'Apr', applications: 12, interviews: 3 },
  { month: 'May', applications: 9, interviews: 4 },
  { month: 'Jun', applications: 18, interviews: 6 },
  { month: 'Jul', applications: 14, interviews: 5 },
];

export default function ApplicationActivityChart() {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5">
      <div className="flex items-center justify-between mb-5">
        <div>
          <h2 className="font-semibold text-[#0F172A]">Application Activity</h2>
          <p className="text-xs text-[#64748B] mt-0.5">Applications vs interviews over 6 months</p>
        </div>
        <div className="flex items-center gap-4 text-xs text-[#64748B]">
          <div className="flex items-center gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full bg-[#2563EB]" />
            Applied
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full bg-[#22C55E]" />
            Interviews
          </div>
        </div>
      </div>
      <div className="w-full" style={{ height: 200 }}>
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={applicationData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="blueGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#2563EB" stopOpacity={0.15} />
                <stop offset="95%" stopColor="#2563EB" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="greenGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#22C55E" stopOpacity={0.15} />
                <stop offset="95%" stopColor="#22C55E" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" vertical={false} />
            <XAxis
              dataKey="month"
              tick={{ fontSize: 12, fill: '#94A3B8' }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              tick={{ fontSize: 12, fill: '#94A3B8' }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip
              contentStyle={{
                borderRadius: 10,
                border: '1px solid #E2E8F0',
                fontSize: 12,
              }}
            />
            <Area
              type="monotone"
              dataKey="applications"
              stroke="#2563EB"
              strokeWidth={2}
              fill="url(#blueGrad)"
            />
            <Area
              type="monotone"
              dataKey="interviews"
              stroke="#22C55E"
              strokeWidth={2}
              fill="url(#greenGrad)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
