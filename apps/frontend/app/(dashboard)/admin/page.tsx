'use client';

import React from 'react';
import { useAdminDashboard } from '@/hooks/useAdminDashboard';
import DashboardStats from '@/components/admin/DashboardStats';
import ActivityFeed from '@/components/admin/ActivityFeed';
import QuickActions from '@/components/admin/QuickActions';
import { Loader2, Shield } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const MOCK_PLATFORM_GROWTH = [
  { name: 'Feb', candidates: 400, recruiters: 80 },
  { name: 'Mar', candidates: 700, recruiters: 120 },
  { name: 'Apr', candidates: 1200, recruiters: 180 },
  { name: 'May', candidates: 900, recruiters: 220 },
  { name: 'Jun', candidates: 1800, recruiters: 260 },
  { name: 'Jul', candidates: 1482, recruiters: 284 },
];

export default function AdminDashboardPage() {
  const { kpis, activities, loading, error } = useAdminDashboard();

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading platform administration dials...</p>
      </div>
    );
  }

  if (error || !kpis) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12">
        <h3 className="text-red-500 font-bold text-lg">Error Loading Admin Panel</h3>
        <p className="text-sm text-[#64748B]">{error || 'Stats failed'}</p>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6 max-w-6xl mx-auto text-[#0F172A] text-left">
      {/* Header Title */}
      <div className="border-b border-[#E2E8F0] pb-5">
        <h1 className="text-xl sm:text-2xl font-bold flex items-center gap-2">
          <Shield className="text-[#2563EB]" />
          Platform Control center
        </h1>
        <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">Platform diagnostics, usage metrics, and user accounts authorization controls.</p>
      </div>

      {/* Stats counter widget */}
      <DashboardStats kpis={kpis} />

      {/* Columns splits */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left Growth charts and logs */}
        <div className="lg:col-span-2 space-y-6">
          {/* Growth Area Chart */}
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
            <div>
              <h3 className="font-bold text-xs uppercase tracking-wide text-slate-500">Platform Accounts Growth</h3>
              <p className="text-[10px] text-slate-400 mt-0.5 font-medium">Growth index of candidates and recruiter registrations over 6 months.</p>
            </div>
            <div className="w-full h-52">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={MOCK_PLATFORM_GROWTH} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="candGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#2563EB" stopOpacity={0.12} />
                      <stop offset="95%" stopColor="#2563EB" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="recGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#7C3AED" stopOpacity={0.12} />
                      <stop offset="95%" stopColor="#7C3AED" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" vertical={false} />
                  <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#94A3B8' }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fontSize: 11, fill: '#94A3B8' }} axisLine={false} tickLine={false} />
                  <Tooltip contentStyle={{ borderRadius: 12, border: '1px solid #E2E8F0', fontSize: 11 }} />
                  <Area type="monotone" dataKey="candidates" stroke="#2563EB" strokeWidth={2} fill="url(#candGrad)" name="Candidates" />
                  <Area type="monotone" dataKey="recruiters" stroke="#7C3AED" strokeWidth={2} fill="url(#recGrad)" name="Recruiters" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Activity Feeds */}
          <ActivityFeed activities={activities} />
        </div>

        {/* Right Console Shortcuts */}
        <div className="space-y-6">
          <QuickActions />
        </div>
      </div>
    </div>
  );
}
