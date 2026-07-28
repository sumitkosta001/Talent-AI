'use client';

import { useState, useEffect, useCallback } from 'react';
import { PlatformKPIs } from '@/types/admin';
import { AdminDashboardService } from '@/services/admin.service';

export function useAdminDashboard() {
  const [kpis, setKPIs] = useState<PlatformKPIs | null>(null);
  const [activities, setActivities] = useState<{ id: string; description: string; timestamp: string }[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [k, a] = await Promise.all([
        AdminDashboardService.getKPIs(),
        AdminDashboardService.getRecentActivities(),
      ]);
      setKPIs(k);
      setActivities(a);
    } catch (err: any) {
      setError(err?.message || 'Failed to load platform controls info');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  return {
    kpis,
    activities,
    loading,
    error,
    refetch: loadData,
  };
}
