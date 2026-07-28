'use client';

import { useState, useEffect, useCallback } from 'react';
import { CareerInsightCard } from '@/types/careerInsight';
import { InsightService } from '@/services/insight.service';

export function useCareerInsights() {
  const [insights, setInsights] = useState<CareerInsightCard[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchInsights = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await InsightService.getInsights();
      setInsights(data);
    } catch (err: any) {
      setError(err?.message || 'Failed to load career insights');
    } finally {
      setLoading(false);
    }
  }, []);

  const dismissInsight = useCallback((id: string) => {
    setInsights((prev) => prev.filter((ins) => ins.id !== id));
  }, []);

  useEffect(() => {
    fetchInsights();
  }, [fetchInsights]);

  return {
    insights,
    loading,
    error,
    dismissInsight,
    refetch: fetchInsights,
  };
}
