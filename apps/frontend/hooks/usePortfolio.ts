'use client';

import { useState, useEffect, useCallback } from 'react';
import { CandidatePortfolioItem } from '@/types/portfolio';
import { CandidatePortfolioService } from '@/services/portfolio.service';

export function usePortfolio() {
  const [portfolio, setPortfolio] = useState<CandidatePortfolioItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPortfolio = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await CandidatePortfolioService.getPortfolio();
      setPortfolio(data);
    } catch (err: any) {
      setError(err?.message || 'Failed to load portfolio items');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchPortfolio();
  }, [fetchPortfolio]);

  const addPortfolioItem = useCallback(async (item: Partial<CandidatePortfolioItem>) => {
    try {
      const added = await CandidatePortfolioService.addPortfolioItem(item);
      setPortfolio((prev) => [added, ...prev]);
      return true;
    } catch {
      return false;
    }
  }, []);

  const deletePortfolioItem = useCallback(async (id: string) => {
    try {
      await CandidatePortfolioService.deletePortfolioItem(id);
      setPortfolio((prev) => prev.filter((p) => p.id !== id));
      return true;
    } catch {
      return false;
    }
  }, []);

  return {
    portfolio,
    loading,
    error,
    addPortfolioItem,
    deletePortfolioItem,
    refetch: fetchPortfolio,
  };
}
