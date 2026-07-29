'use client';

import React from 'react';
import { useRecruiterDashboard } from '@/hooks/useRecruiterDashboard';
import AnalyticsCharts from '@/components/recruiter/AnalyticsCharts';
import { Loader2 } from 'lucide-react';

export default function RecruiterAnalyticsPage() {
  const { funnel, loading, error } = useRecruiterDashboard();

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading analytics engine trends...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12">
        <h3 className="text-red-500 font-bold text-lg">Error Loading Analytics</h3>
        <p className="text-sm text-[#64748B]">{error}</p>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6 max-w-6xl mx-auto text-[#0F172A] text-left">
      <div className="border-b border-[#E2E8F0] pb-5">
        <h1 className="text-xl sm:text-2xl font-bold">Hiring Analytics Reports</h1>
        <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">Statistical metrics on pipelines conversions and applications yield ratios.</p>
      </div>

      <AnalyticsCharts funnelData={funnel} />
    </div>
  );
}
