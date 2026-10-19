'use client';

import { useState, useEffect, useCallback } from 'react';
import { Company } from '@/types/company';
import { CompanyService } from '@/services/company.service';

export function useCompanies() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [search, setSearch] = useState('');
  const [industryFilter, setIndustryFilter] = useState('');
  const [sortBy, setSortBy] = useState<'rating' | 'jobs' | 'alphabetical'>('rating');

  const fetchList = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await CompanyService.getCompanies();
      setCompanies(data);
    } catch (err: any) {
      setError(err?.message || 'Failed to load companies listing');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchList();
  }, [fetchList]);

  const getFilteredAndSorted = useCallback(() => {
    let result = [...companies];

    if (search) {
      const q = search.toLowerCase();
      result = result.filter(
        c =>
          (c.name && c.name.toLowerCase().includes(q)) ||
          (c.industry && c.industry.toLowerCase().includes(q)) ||
          (c.about && c.about.toLowerCase().includes(q)) ||
          (c.description && c.description.toLowerCase().includes(q))
      );
    }

    if (industryFilter) {
      result = result.filter(c => c.industry === industryFilter);
    }

    if (sortBy === 'rating') {
      result.sort((a, b) => (b.rating ?? 0) - (a.rating ?? 0));
    } else if (sortBy === 'jobs') {
      result.sort((a, b) => (b.openPositions ?? 0) - (a.openPositions ?? 0));
    } else if (sortBy === 'alphabetical') {
      result.sort((a, b) => (a.name || '').localeCompare(b.name || ''));
    }

    return result;
  }, [companies, search, industryFilter, sortBy]);

  return {
    companies: getFilteredAndSorted(),
    rawCompanies: companies,
    loading,
    error,
    search,
    setSearch,
    industryFilter,
    setIndustryFilter,
    sortBy,
    setSortBy,
    refetch: fetchList,
  };
}
