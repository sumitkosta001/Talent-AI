'use client';

import { useState, useEffect, useCallback } from 'react';
import { StructuredResume } from '@/types/ml';
import { MLService } from '@/services/ml.service';

export function useStructuredResume(resumeId?: string | null) {
  const [data, setData] = useState<StructuredResume | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchStructuredResume = useCallback(async () => {
    if (!resumeId) {
      setData(null);
      setLoading(false);
      setError(null);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const result = await MLService.getStructuredResume(resumeId);
      setData(result);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to load structured resume';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [resumeId]);

  useEffect(() => {
    fetchStructuredResume();
  }, [fetchStructuredResume]);

  return {
    data,
    loading,
    error,
    refetch: fetchStructuredResume,
  };
}
