'use client';

import { useState, useEffect, useCallback } from 'react';
import { RecruiterJob } from '@/types/job';
import { RecruiterJobsService } from '@/services/jobs.service';

export function useRecruiterJobs() {
  const [jobs, setJobs] = useState<RecruiterJob[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [search, setSearch] = useState('');
  const [department, setDepartment] = useState('');
  const [status, setStatus] = useState('');
  const [sortBy, setSortBy] = useState<'newest' | 'oldest' | 'views' | 'applications'>('newest');

  const fetchJobs = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const items = await RecruiterJobsService.getJobs();
      setJobs(items);
    } catch (err: any) {
      setError(err?.message || 'Failed to fetch recruiter jobs');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchJobs();
  }, [fetchJobs]);

  const handleCreate = useCallback(async (job: Partial<RecruiterJob>) => {
    try {
      const newJob = await RecruiterJobsService.createJob(job);
      setJobs((prev) => [newJob, ...prev]);
      return newJob;
    } catch (err) {
      console.error(err);
      return null;
    }
  }, []);

  const handleUpdate = useCallback(async (id: string, updates: Partial<RecruiterJob>) => {
    try {
      const updated = await RecruiterJobsService.updateJob(id, updates);
      setJobs((prev) => prev.map((j) => (j.id === id ? updated : j)));
      return true;
    } catch (err) {
      console.error(err);
      return false;
    }
  }, []);

  const handleDuplicate = useCallback(async (id: string) => {
    const target = jobs.find(j => j.id === id);
    if (!target) return false;
    
    const duplicateData = {
      ...target,
      role: `${target.role} (Copy)`,
      status: 'Draft' as const,
    };
    const newJob = await handleCreate(duplicateData);
    return !!newJob;
  }, [jobs, handleCreate]);

  const handleClose = useCallback(async (id: string) => {
    return handleUpdate(id, { status: 'Closed' });
  }, [handleUpdate]);

  const handleDelete = useCallback(async (id: string) => {
    try {
      await RecruiterJobsService.deleteJob(id);
      setJobs((prev) => prev.filter((j) => j.id !== id));
      return true;
    } catch (err) {
      console.error(err);
      return false;
    }
  }, []);

  const getFilteredAndSorted = useCallback(() => {
    let result = [...jobs];

    // Search query match
    if (search) {
      const q = search.toLowerCase();
      result = result.filter(
        (j) =>
          j.role.toLowerCase().includes(q) ||
          j.company.toLowerCase().includes(q) ||
          j.location.toLowerCase().includes(q)
      );
    }

    // Department match
    if (department) {
      result = result.filter((j) => j.department === department);
    }

    // Status match
    if (status) {
      result = result.filter((j) => j.status === status);
    }

    // Sorting
    if (sortBy === 'newest') {
      result.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
    } else if (sortBy === 'oldest') {
      result.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
    } else if (sortBy === 'views') {
      result.sort((a, b) => b.views - a.views);
    } else if (sortBy === 'applications') {
      result.sort((a, b) => b.applicationsCount - a.applicationsCount);
    }

    return result;
  }, [jobs, search, department, status, sortBy]);

  return {
    jobs: getFilteredAndSorted(),
    rawJobs: jobs,
    loading,
    error,
    search,
    setSearch,
    department,
    setDepartment,
    status,
    setStatus,
    sortBy,
    setSortBy,
    create: handleCreate,
    update: handleUpdate,
    duplicate: handleDuplicate,
    close: handleClose,
    deleteJob: handleDelete,
    refetch: fetchJobs,
  };
}
