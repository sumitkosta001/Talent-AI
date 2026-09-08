'use client';

import { useState, useEffect, useCallback } from 'react';
import {
  JobRecommendationResponse,
  CandidateJobRecommendationRequest,
} from '@/types/ml';
import { MLService } from '@/services/ml.service';

export function useJobRecommendations(resumeId?: string | null, autoFetch: boolean = true) {
  const [data, setData] = useState<JobRecommendationResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRecommendations = useCallback(
    async (
      request?: CandidateJobRecommendationRequest,
      topK: number = 10
    ): Promise<JobRecommendationResponse | null> => {
      if (!resumeId) {
        setData(null);
        setLoading(false);
        setError(null);
        return null;
      }

      setLoading(true);
      setError(null);
      try {
        const result = await MLService.getJobRecommendations(resumeId, request, topK);
        setData(result);
        return result;
      } catch (err: unknown) {
        const message = err instanceof Error ? err.message : 'Failed to load job recommendations';
        setError(message);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [resumeId]
  );

  useEffect(() => {
    if (autoFetch && resumeId) {
      fetchRecommendations();
    }
  }, [autoFetch, resumeId, fetchRecommendations]);

  const reset = useCallback(() => {
    setData(null);
    setLoading(false);
    setError(null);
  }, []);

  return {
    data,
    loading,
    error,
    fetchRecommendations,
    refetch: fetchRecommendations,
    reset,
  };
}
