'use client';

import { useState, useEffect, useCallback } from 'react';
import { CandidateExperience } from '@/types/experience';
import { CandidateExperienceService } from '@/services/experience.service';

export function useExperience() {
  const [experience, setExperience] = useState<CandidateExperience[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchExperience = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await CandidateExperienceService.getExperience();
      setExperience(data);
    } catch (err: any) {
      setError(err?.message || 'Failed to load experience history');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchExperience();
  }, [fetchExperience]);

  const addExperience = useCallback(async (exp: Partial<CandidateExperience>) => {
    try {
      const added = await CandidateExperienceService.addExperience(exp);
      setExperience((prev) => [added, ...prev]);
      return true;
    } catch {
      return false;
    }
  }, []);

  const deleteExperience = useCallback(async (id: string) => {
    try {
      await CandidateExperienceService.deleteExperience(id);
      setExperience((prev) => prev.filter((e) => e.id !== id));
      return true;
    } catch {
      return false;
    }
  }, []);

  return {
    experience,
    loading,
    error,
    addExperience,
    deleteExperience,
    refetch: fetchExperience,
  };
}
