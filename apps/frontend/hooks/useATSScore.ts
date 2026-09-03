'use client';

import { useState, useCallback } from 'react';
import { ATSScoreResponse, JobRequirements } from '@/types/ml';
import { MLService } from '@/services/ml.service';

export function useATSScore(resumeId?: string | null) {
  const [data, setData] = useState<ATSScoreResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const calculateATSScore = useCallback(
    async (jobRequirements: JobRequirements): Promise<ATSScoreResponse | null> => {
      if (!resumeId) {
        setError('Resume ID is required to calculate ATS score');
        return null;
      }

      setLoading(true);
      setError(null);
      try {
        const result = await MLService.calculateATSScore(resumeId, jobRequirements);
        setData(result);
        return result;
      } catch (err: unknown) {
        const message = err instanceof Error ? err.message : 'Failed to calculate ATS score';
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
    calculateATSScore,
    reset,
  };
}
