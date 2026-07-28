'use client';

import { useState, useEffect, useCallback } from 'react';
import { Job } from '@/types/job';
import { CompanyJobService } from '@/services/companyJob.service';

export function useCompanyJobs(companyId: string) {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchJobs = useCallback(async () => {
    if (!companyId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await CompanyJobService.getJobsByCompanyId(companyId);
      setJobs(data);
    } catch (err: any) {
      setError(err?.message || 'Failed to retrieve company jobs list');
    } finally {
      setLoading(false);
    }
  }, [companyId]);

  useEffect(() => {
    fetchJobs();
  }, [fetchJobs]);

  return {
    jobs,
    loading,
    error,
    refetch: fetchJobs,
  };
}
