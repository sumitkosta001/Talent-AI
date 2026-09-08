'use client';

import { useState, useEffect, useCallback } from 'react';
import { ResumeClassification } from '@/types/ml';
import { MLService } from '@/services/ml.service';

export function useClassification(resumeId?: string | null) {
  const [data, setData] = useState<ResumeClassification | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchClassification = useCallback(async () => {
    if (!resumeId) {
      setData(null);
      setLoading(false);
      setError(null);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const result = await MLService.getClassification(resumeId);
      setData(result);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to load resume classification';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [resumeId]);

  useEffect(() => {
    fetchClassification();
  }, [fetchClassification]);

  return {
    data,
    loading,
    error,
    refetch: fetchClassification,
  };
}
