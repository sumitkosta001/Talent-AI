'use client';

import { useState, useEffect, useCallback } from 'react';
import { RecentSearchItem } from '@/types/dashboard';
import { MOCK_RECENT_SEARCHES } from '@/mock/recentSearches';

const SEARCH_STORAGE_KEY = 'talentai_candidate_recent_searches';

export function useRecentSearches() {
  const [searches, setSearches] = useState<RecentSearchItem[]>([]);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const stored = localStorage.getItem(SEARCH_STORAGE_KEY);
    if (!stored) {
      localStorage.setItem(SEARCH_STORAGE_KEY, JSON.stringify(MOCK_RECENT_SEARCHES));
      setSearches(MOCK_RECENT_SEARCHES);
    } else {
      try {
        setSearches(JSON.parse(stored));
      } catch {
        setSearches(MOCK_RECENT_SEARCHES);
      }
    }
  }, []);

  const addSearch = useCallback((query: string, category: 'jobs' | 'companies' | 'skills' | 'locations') => {
    const newItem: RecentSearchItem = {
      id: `search-${Date.now()}`,
      query,
      category,
      timestamp: 'Just now',
    };
    setSearches((prev) => {
      const filtered = prev.filter(
        (item) => !(item.query.toLowerCase() === query.toLowerCase() && item.category === category)
      );
      const updated = [newItem, ...filtered].slice(0, 10);
      localStorage.setItem(SEARCH_STORAGE_KEY, JSON.stringify(updated));
      return updated;
    });
  }, []);

  const deleteSearch = useCallback((id: string) => {
    setSearches((prev) => {
      const updated = prev.filter((item) => item.id !== id);
      localStorage.setItem(SEARCH_STORAGE_KEY, JSON.stringify(updated));
      return updated;
    });
  }, []);

  const clearHistory = useCallback(() => {
    setSearches([]);
    localStorage.setItem(SEARCH_STORAGE_KEY, JSON.stringify([]));
  }, []);

  return {
    searches,
    addSearch,
    deleteSearch,
    clearHistory,
  };
}
