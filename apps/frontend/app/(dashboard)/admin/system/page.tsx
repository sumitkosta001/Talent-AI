'use client';

import React from 'react';
import { useSystemHealth } from '@/hooks/useSystemHealth';
import SystemHealthCard from '@/components/admin/SystemHealthCard';
import { Loader2 } from 'lucide-react';

export default function AdminSystemHealthPage() {
  const { health, loading, error } = useSystemHealth();

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading platform diagnostics health...</p>
      </div>
    );
  }

  if (error || !health) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12">
        <h3 className="text-red-500 font-bold text-lg">Error Loading Diagnostics</h3>
        <p className="text-sm text-[#64748B]">{error || 'Metrics loading failed'}</p>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6 max-w-5xl mx-auto text-[#0F172A] text-left">
      <div className="border-b border-[#E2E8F0] pb-5">
        <h1 className="text-xl sm:text-2xl font-bold">System Health Diagnostics</h1>
        <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">CPU memory consumption levels, server uptimes counters, and active background error logs.</p>
      </div>

      <SystemHealthCard health={health} />
    </div>
  );
}
