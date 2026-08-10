'use client';

import { useState, useEffect, useCallback } from 'react';
import { CandidateSkill } from '@/types/skill';
import { CandidateSkillService } from '@/services/skill.service';

export function useSkills() {
  const [skills, setSkills] = useState<CandidateSkill[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchSkills = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await CandidateSkillService.getSkills();
      setSkills(data);
    } catch (err: any) {
      setError(err?.message || 'Failed to load selected skills');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchSkills();
  }, [fetchSkills]);

  const addSkill = useCallback(async (name: string, level: 'Beginner' | 'Intermediate' | 'Expert', exp: number) => {
    try {
      const added = await CandidateSkillService.addSkill(name, level, exp);
      setSkills((prev) => [added, ...prev]);
      return true;
    } catch (err: any) {
      alert(err?.message || 'Failed to add skill entry');
      return false;
    }
  }, []);

  const deleteSkill = useCallback(async (id: string) => {
    try {
      await CandidateSkillService.deleteSkill(id);
      setSkills((prev) => prev.filter((s) => s.id !== id));
      return true;
    } catch (err: any) {
      alert(err?.message || 'Failed to delete skill entry');
      return false;
    }
  }, []);

  return {
    skills,
    loading,
    error,
    addSkill,
    deleteSkill,
    refetch: fetchSkills,
  };
}
