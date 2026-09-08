'use client';

import { useState, useCallback } from 'react';
import {
  GeneratedInterviewQuestions,
  InterviewQuestionRequest,
} from '@/types/ml';
import { MLService } from '@/services/ml.service';

export function useInterviewQuestions(resumeId?: string | null) {
  const [data, setData] = useState<GeneratedInterviewQuestions | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const generateQuestions = useCallback(
    async (
      request?: InterviewQuestionRequest
    ): Promise<GeneratedInterviewQuestions | null> => {
      if (!resumeId) {
        setError('Resume ID is required to generate interview questions');
        return null;
      }

      setLoading(true);
      setError(null);
      try {
        const result = await MLService.generateInterviewQuestions(resumeId, request);
        setData(result);
        return result;
      } catch (err: unknown) {
        const message = err instanceof Error ? err.message : 'Failed to generate interview questions';
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
    generateQuestions,
    reset,
  };
}
