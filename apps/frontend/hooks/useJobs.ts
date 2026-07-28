'use client';

import { useState, useEffect, useCallback } from 'react';
import { Job, JobFilter } from '@/types/job';
import { JobsService } from '@/services/jobs.service';

const initialFilters: JobFilter = {
  search: '',
  location: '',
  experience: '',
  jobType: 'Any',
  remoteStatus: 'Any',
  salaryMin: 0,
  skills: [],
  sortBy: 'best-match',
};

export function useJobs() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<JobFilter>(initialFilters);

  const fetchJobs = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await JobsService.getJobs(filters);
      setJobs(data);
    } catch (err: any) {
      setError(err?.message || 'Failed to fetch jobs list');
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchJobs();
  }, [fetchJobs]);

  const updateFilter = useCallback((key: keyof JobFilter, value: any) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  }, []);

  const resetFilters = useCallback(() => {
    setFilters(initialFilters);
  }, []);

  return {
    jobs,
    loading,
    error,
    filters,
    updateFilter,
    resetFilters,
    refetch: fetchJobs,
  };
}
