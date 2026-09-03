'use client';

import { useState, useCallback } from 'react';
import { SimilarityMatchResponse, JobRequirements } from '@/types/ml';
import { MLService } from '@/services/ml.service';

export function useSimilarity(resumeId?: string | null) {
  const [data, setData] = useState<SimilarityMatchResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const calculateSimilarity = useCallback(
    async (jobRequirements: JobRequirements): Promise<SimilarityMatchResponse | null> => {
      if (!resumeId) {
        setError('Resume ID is required to calculate similarity score');
        return null;
      }

      setLoading(true);
      setError(null);
      try {
        const result = await MLService.calculateSimilarityScore(resumeId, jobRequirements);
        setData(result);
        return result;
      } catch (err: unknown) {
        const message = err instanceof Error ? err.message : 'Failed to calculate similarity score';
        setError(message);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [resumeId]
  );

  const reset = useCallback(() => {
    setData(null);
    setLoading(false);
    setError(null);
  }, []);

  return {
    data,
    loading,
    error,
    calculateSimilarity,
    reset,
  };
}
