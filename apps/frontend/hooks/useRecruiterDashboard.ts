'use client';

import { useState, useEffect, useCallback } from 'react';
import { RecruiterDashboardStats, HiringFunnelStep, RecentActivity } from '@/types/recruiter';
import { RecruiterDashboardService } from '@/services/recruiter.service';

export function useRecruiterDashboard() {
  const [stats, setStats] = useState<RecruiterDashboardStats | null>(null);
  const [funnel, setFunnel] = useState<HiringFunnelStep[]>([]);
  const [activities, setActivities] = useState<RecentActivity[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboardData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [s, f, a] = await Promise.all([
        RecruiterDashboardService.getStats(),
        RecruiterDashboardService.getFunnel(),
        RecruiterDashboardService.getActivities(),
      ]);
      setStats(s);
      setFunnel(f);
      setActivities(a);
    } catch (err: any) {
      setError(err?.message || 'Failed to fetch dashboard widgets');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  return {
    stats,
    funnel,
    activities,
    loading,
    error,
    refetch: fetchDashboardData,
  };
}
