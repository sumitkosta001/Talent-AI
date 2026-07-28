'use client';

import { useState, useEffect, useCallback } from 'react';
import { CandidateSkill } from '@/types/skill';
import { MOCK_SKILLS } from '@/mock/skills';

export function useSkills() {
  const [skills, setSkills] = useState<CandidateSkill[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const stored = localStorage.getItem('talentai_candidate_skills');
    if (!stored) {
      localStorage.setItem('talentai_candidate_skills', JSON.stringify(MOCK_SKILLS));
      setSkills(MOCK_SKILLS);
    } else {
      setSkills(JSON.parse(stored));
    }
    setLoading(false);
  }, []);

  const addSkill = useCallback(async (name: string, level: 'Beginner' | 'Intermediate' | 'Expert', exp: number) => {
    if (skills.some((s) => s.name.toLowerCase() === name.toLowerCase())) {
      alert('This skill keywords tag already exists on your profile.');
      return false;
    }
    const newS: CandidateSkill = {
      id: `sk-${Date.now()}`,
      name,
      level,
      yearsOfExperience: exp,
      endorsementsCount: 0,
    };
    const updated = [newS, ...skills];
    setSkills(updated);
    localStorage.setItem('talentai_candidate_skills', JSON.stringify(updated));
    return true;
  }, [skills]);

  const deleteSkill = useCallback(async (id: string) => {
    const updated = skills.filter((s) => s.id !== id);
    setSkills(updated);
    localStorage.setItem('talentai_candidate_skills', JSON.stringify(updated));
    return true;
  }, [skills]);

  return {
    skills,
    loading,
    addSkill,
    deleteSkill,
  };
}
