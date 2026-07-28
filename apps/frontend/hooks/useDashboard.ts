'use client';

import { useState, useEffect, useCallback } from 'react';
import { DashboardOverview, UpcomingInterview, ApplicationDeadline, ProductivityGoal } from '@/types/dashboard';
import { DashboardService } from '@/services/dashboard.service';

export function useDashboard() {
  const [overview, setOverview] = useState<DashboardOverview | null>(null);
  const [interviews, setInterviews] = useState<UpcomingInterview[]>([]);
  const [deadlines, setDeadlines] = useState<ApplicationDeadline[]>([]);
  const [goals, setGoals] = useState<ProductivityGoal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboardData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [over, ints, deads, gls] = await Promise.all([
        DashboardService.getOverview(),
        DashboardService.getUpcomingInterviews(),
        DashboardService.getApplicationDeadlines(),
        DashboardService.getProductivityGoals(),
      ]);
      setOverview(over);
      setInterviews(ints);
      setDeadlines(deads);
      setGoals(gls);
    } catch (err: any) {
      setError(err?.message || 'Failed to load dashboard metrics');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  return {
    overview,
    interviews,
    deadlines,
    goals,
    loading,
    error,
    refetch: fetchDashboardData,
  };
}
