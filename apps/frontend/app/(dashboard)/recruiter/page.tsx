'use client';

import React from 'react';
import { useRecruiterDashboard } from '@/hooks/useRecruiterDashboard';
import DashboardStats from '@/components/recruiter/DashboardStats';
import QuickActions from '@/components/recruiter/QuickActions';
import HiringFunnel from '@/components/recruiter/HiringFunnel';
import { Loader2, Calendar, Clock, Activity, ArrowRight } from 'lucide-react';
import Link from 'next/link';

export default function RecruiterDashboardPage() {
  const { stats, funnel, activities, loading, error } = useRecruiterDashboard();

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading recruiter dashboard analytics...</p>
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12">
        <h3 className="text-red-500 font-bold text-lg">Error Loading Dashboard</h3>
        <p className="text-sm text-[#64748B]">{error || 'Stats failed'}</p>
        <button
          onClick={() => window.location.reload()}
          className="bg-[#2563EB] text-white px-4 py-2 rounded-xl text-sm font-semibold cursor-pointer"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6 max-w-6xl mx-auto text-[#0F172A]">
      {/* Greet recruiter */}
      <div className="text-left">
        <h1 className="text-xl sm:text-2xl font-bold text-[#0F172A]">Welcome Back, Sarah Mitchell 👋</h1>
        <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">
          You have {stats.todayApplications} new candidate applications submitted today to review.
        </p>
      </div>

      {/* Counters Stats Cards */}
      <DashboardStats stats={stats} />

      {/* Columns splits */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left Funnel and Actions */}
        <div className="lg:col-span-2 space-y-6">
          <HiringFunnel funnel={funnel} />

          {/* Recent activity log */}
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
            <div className="flex items-center gap-1.5 border-b border-[#F1F5F9] pb-3">
              <Activity size={18} className="text-[#2563EB]" />
              <h3 className="font-bold text-[#0F172A] text-sm">Recent Recruiter Activity</h3>
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
        </div>

        {/* Right Sidebar */}
        <div className="space-y-6">
          <QuickActions />

          {/* Upcoming Interview schedules */}
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
            <h3 className="font-bold text-[#0F172A] text-sm">Upcoming Interview Loop</h3>
            
            <div className="space-y-3 text-xs border border-slate-100 p-3.5 bg-slate-50/50 rounded-2xl">
              <div className="flex items-center gap-2">
                <Calendar size={14} className="text-[#64748B]" />
                <span className="font-bold text-[#0F172A]">Alex Johnson</span>
              </div>
              <div className="flex items-center gap-2">
                <Clock size={14} className="text-[#64748B]" />
                <span className="font-semibold text-slate-600">Tomorrow at 04:00 PM</span>
              </div>
              <p className="text-[10px] text-slate-500 italic mt-1 leading-relaxed">
                Role: Full Stack Engineer (Payments) · Code interview panel
              </p>
              <Link
                href="/recruiter/applicants/app-alex-johnson"
                className="text-[10px] font-bold text-blue-600 hover:underline flex items-center gap-0.5 pt-1.5"
              >
                Inspect Candidate
                <ArrowRight size={10} />
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
