'use client';

import { useState, useEffect, useCallback } from 'react';
import { RecentActivityItem } from '@/types/activity';
import { ActivityService } from '@/services/activity.service';

export function useActivity() {
  const [activities, setActivities] = useState<RecentActivityItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchActivities = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const acts = await ActivityService.getActivities();
      setActivities(acts);
    } catch (err: any) {
      setError(err?.message || 'Failed to load activity feed');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchActivities();
  }, [fetchActivities]);

  return {
    activities,
    loading,
    error,
    refetch: fetchActivities,
  };
}
