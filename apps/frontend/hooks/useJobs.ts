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
  salaryMax: undefined,
  skills: [],
  sortBy: 'newest',
  page: 1,
  size: 10,
};

export function useJobs() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [totalItems, setTotalItems] = useState<number>(0);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<JobFilter>(initialFilters);

  const fetchJobs = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      let expMonths: number | undefined;
      if (filters.experience) {
        const parsed = parseInt(filters.experience);
        if (!isNaN(parsed)) {
          expMonths = parsed * 12;
        }
      }

      let sort_by = 'published_at';
      let sort_order = 'desc';
      if (filters.sortBy === 'oldest') {
        sort_by = 'published_at';
        sort_order = 'asc';
      } else if (filters.sortBy === 'highest-salary') {
        sort_by = 'salary_max';
        sort_order = 'desc';
      } else if (filters.sortBy === 'lowest-salary') {
        sort_by = 'salary_min';
        sort_order = 'asc';
      }

      let work_mode: 'REMOTE' | 'HYBRID' | 'ONSITE' | undefined;
      if (filters.remoteStatus && filters.remoteStatus !== 'Any') {
        const u = filters.remoteStatus.toUpperCase();
        if (u === 'REMOTE' || u === 'HYBRID' || u === 'ONSITE') {
          work_mode = u as any;
        }
      }

      const res = await JobsService.searchJobs({
        q: filters.search || undefined,
        location: filters.location || undefined,
        skills: filters.skills.length > 0 ? filters.skills.join(',') : undefined,
        experience_months: expMonths,
        salary_min: filters.salaryMin > 0 ? filters.salaryMin : undefined,
        salary_max: filters.salaryMax && filters.salaryMax > 0 ? filters.salaryMax : undefined,
        work_mode,
        page: filters.page || 1,
        size: filters.size || 10,
        sort_by,
        sort_order,
      });

      const mapped = res.items.map(JobsService.mapApiItemToJob);
      setJobs(mapped);
      setTotalItems(res.total);
      setTotalPages(res.total_pages || 1);
    } catch (err: any) {
      console.warn('Direct search API error, trying fallback:', err);
      try {
        const data = await JobsService.getJobs(filters);
        setJobs(data);
        setTotalItems(data.length);
        setTotalPages(1);
      } catch (fallbackErr: any) {
        setError(fallbackErr?.message || 'Failed to fetch jobs list');
      }
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchJobs();
  }, [fetchJobs]);

  const updateFilter = useCallback((key: keyof JobFilter, value: any) => {
    setFilters((prev) => ({
      ...prev,
      [key]: value,
      page: key === 'page' ? value : 1, // Reset page to 1 on filter changes
    }));
  }, []);

  const resetFilters = useCallback(() => {
    setFilters(initialFilters);
  }, []);

  return {
    jobs,
    totalItems,
    totalPages,
    loading,
    error,
    filters,
    updateFilter,
    resetFilters,
    refetch: fetchJobs,
  };
}
