'use client';

import { useState, useEffect, useCallback } from 'react';
import { SystemHealthMetrics } from '@/types/systemHealth';
import { AdminSystemService } from '@/services/system.service';

export function useSystemHealth() {
  const [health, setHealth] = useState<SystemHealthMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchMetrics = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await AdminSystemService.getHealthMetrics();
      setHealth(data);
    } catch (err: any) {
      setError(err?.message || 'Failed to retrieve diagnostics parameters');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchMetrics();
  }, [fetchMetrics]);

  return {
    health,
    loading,
    error,
    refetch: fetchMetrics,
  };
}
