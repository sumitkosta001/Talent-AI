'use client';

import { useState, useEffect, useCallback } from 'react';
import { Application, ApplicationFilter, Analytics } from '@/types/application';
import { ApplicationService } from '@/services/application.service';

const initialFilters: ApplicationFilter = {
  search: '',
  status: '',
  location: '',
  company: '',
  appliedDate: '',
  workplace: 'All',
  salaryMin: 0,
  interviewStage: '',
};

export function useApplications() {
  const [applications, setApplications] = useState<Application[]>([]);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<ApplicationFilter>(initialFilters);
  const [sortBy, setSortBy] = useState<'newest' | 'oldest' | 'best-match' | 'recently-updated' | 'company-name'>('newest');

  const fetchApplicationsData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const apps = await ApplicationService.getApplications();
      setApplications(apps);
      const stats = await ApplicationService.getAnalytics();
      setAnalytics(stats);
    } catch (err: any) {
      setError(err?.message || 'Failed to fetch application history');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchApplicationsData();
  }, [fetchApplicationsData]);

  const updateFilter = useCallback((key: keyof ApplicationFilter, value: any) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  }, []);

  const resetFilters = useCallback(() => {
    setFilters(initialFilters);
  }, []);

  const handleWithdraw = useCallback(async (id: string, reason: string) => {
    try {
      const updated = await ApplicationService.withdrawApplication(id, reason);
      setApplications((prev) => prev.map((a) => (a.id === id ? updated : a)));
      return true;
    } catch (err) {
      console.error(err);
      return false;
    }
  }, []);

  const handleArchive = useCallback(async (id: string) => {
    try {
      const updated = await ApplicationService.archiveApplication(id);
      setApplications((prev) => prev.map((a) => (a.id === id ? updated : a)));
      return true;
    } catch (err) {
      console.error(err);
      return false;
    }
  }, []);

  const handleRestore = useCallback(async (id: string) => {
    try {
      const updated = await ApplicationService.restoreApplication(id);
      setApplications((prev) => prev.map((a) => (a.id === id ? updated : a)));
      return true;
    } catch (err) {
      console.error(err);
      return false;
    }
  }, []);

  const isApplied = useCallback((jobId: string) => {
    return applications.some(a => a.jobId === jobId);
  }, [applications]);

  const applyForJob = useCallback(async (
    jobId: string,
    jobTitle: string,
    company: string,
    logo: string,
    logoColor: string,
    salary: string,
    location: string
  ) => {
    try {
      const newApp = await ApplicationService.applyForJob(
        jobId,
        jobTitle,
        company,
        logo,
        logoColor,
        salary,
        location
      );
      setApplications(prev => [newApp, ...prev]);
      return true;
    } catch (err) {
      console.error(err);
      return false;
    }
  }, []);

  // Filter & Sort Logic
  const getFilteredAndSorted = useCallback(() => {
    let result = [...applications];

    // Filter by search (Company, Job Title, Location, Recruiter)
    if (filters.search) {
      const s = filters.search.toLowerCase();
      result = result.filter(
        (a) =>
          a.company.toLowerCase().includes(s) ||
          a.jobTitle.toLowerCase().includes(s) ||
          a.location.toLowerCase().includes(s) ||
          a.recruiter.name.toLowerCase().includes(s)
      );
    }

    // Filter by status
    if (filters.status) {
      result = result.filter((a) => a.status === filters.status);
    }

    // Filter by location
    if (filters.location) {
      result = result.filter((a) => a.location.toLowerCase().includes(filters.location.toLowerCase()));
    }

    // Filter by company
    if (filters.company) {
      result = result.filter((a) => a.company === filters.company);
    }

    // Filter by Workplace type
    if (filters.workplace !== 'All') {
      result = result.filter((a) => {
        if (filters.workplace === 'Remote') return a.location.toLowerCase().includes('remote');
        if (filters.workplace === 'Hybrid') return a.location.toLowerCase().includes('hybrid');
        return !a.location.toLowerCase().includes('remote') && !a.location.toLowerCase().includes('hybrid');
      });
    }

    // Filter by Interview Stage
    if (filters.interviewStage) {
      result = result.filter((a) => a.interview?.type === filters.interviewStage);
    }

    // Sort Logic
    if (sortBy === 'newest') {
      result.sort((a, b) => new Date(b.appliedDate).getTime() - new Date(a.appliedDate).getTime());
    } else if (sortBy === 'oldest') {
      result.sort((a, b) => new Date(a.appliedDate).getTime() - new Date(b.appliedDate).getTime());
    } else if (sortBy === 'best-match') {
      result.sort((a, b) => b.matchPercentage - a.matchPercentage);
    } else if (sortBy === 'recently-updated') {
      result.sort((a, b) => new Date(b.lastUpdated).getTime() - new Date(a.lastUpdated).getTime());
    } else if (sortBy === 'company-name') {
      result.sort((a, b) => a.company.localeCompare(b.company));
    }

    return result;
  }, [applications, filters, sortBy]);

  return {
    applications: getFilteredAndSorted(),
    rawApplications: applications,
    analytics,
    loading,
    error,
    filters,
    sortBy,
    setSortBy,
    updateFilter,
    resetFilters,
    isApplied,
    applyForJob,
    withdraw: handleWithdraw,
    archive: handleArchive,
    restore: handleRestore,
    refetch: fetchApplicationsData,
  };
}
