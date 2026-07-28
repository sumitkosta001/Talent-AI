'use client';

import { useState, useEffect, useCallback } from 'react';
import { CandidateEducation } from '@/types/education';
import { CandidateEducationService } from '@/services/education.service';

export function useEducation() {
  const [education, setEducation] = useState<CandidateEducation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchEducation = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await CandidateEducationService.getEducation();
      setEducation(data);
    } catch (err: any) {
      setError(err?.message || 'Failed to load education history');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchEducation();
  }, [fetchEducation]);

  const addEducation = useCallback(async (edu: Partial<CandidateEducation>) => {
    try {
      const added = await CandidateEducationService.addEducation(edu);
      setEducation((prev) => [added, ...prev]);
      return true;
    } catch {
      return false;
    }
  }, []);

  const deleteEducation = useCallback(async (id: string) => {
    try {
      await CandidateEducationService.deleteEducation(id);
      setEducation((prev) => prev.filter((e) => e.id !== id));
      return true;
    } catch {
      return false;
    }
  }, []);

  return {
    education,
    loading,
    error,
    addEducation,
    deleteEducation,
    refetch: fetchEducation,
  };
}
