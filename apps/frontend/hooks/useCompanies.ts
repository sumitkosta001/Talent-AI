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
          c.name.toLowerCase().includes(q) ||
          c.industry.toLowerCase().includes(q) ||
          c.about.toLowerCase().includes(q)
      );
    }

    if (industryFilter) {
      result = result.filter(c => c.industry === industryFilter);
    }

    if (sortBy === 'rating') {
      result.sort((a, b) => b.rating - a.rating);
    } else if (sortBy === 'jobs') {
      result.sort((a, b) => b.openPositions - a.openPositions);
    } else if (sortBy === 'alphabetical') {
      result.sort((a, b) => a.name.localeCompare(b.name));
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
