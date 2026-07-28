'use client';

import { useState, useEffect, useCallback } from 'react';
import { CandidateProject } from '@/types/project';
import { CandidateProjectService } from '@/services/project.service';

export function useProjects() {
  const [projects, setProjects] = useState<CandidateProject[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProjects = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await CandidateProjectService.getProjects();
      setProjects(data);
    } catch (err: any) {
      setError(err?.message || 'Failed to load projects list');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchProjects();
  }, [fetchProjects]);

  const addProject = useCallback(async (proj: Partial<CandidateProject>) => {
    try {
      const added = await CandidateProjectService.addProject(proj);
      setProjects((prev) => [added, ...prev]);
      return true;
    } catch {
      return false;
    }
  }, []);

  const deleteProject = useCallback(async (id: string) => {
    try {
      await CandidateProjectService.deleteProject(id);
      setProjects((prev) => prev.filter((p) => p.id !== id));
      return true;
    } catch {
      return false;
    }
  }, []);

  return {
    projects,
    loading,
    error,
    addProject,
    deleteProject,
    refetch: fetchProjects,
  };
}
