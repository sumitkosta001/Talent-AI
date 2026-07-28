'use client';

import { useState, useEffect } from 'react';
import { SearchResultItem } from '@/types/search';
import { SearchService } from '@/services/search.service';
import { useDebounce } from '@/hooks/useDebounce';

export function useGlobalSearch() {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('all');
  const [results, setResults] = useState<SearchResultItem[]>([]);
  const [loading, setLoading] = useState(false);

  const debouncedQuery = useDebounce(query, 200);

  useEffect(() => {
    if (!debouncedQuery.trim()) {
      setResults([]);
      return;
    }

    let active = true;
    const fetchResults = async () => {
      setLoading(true);
      try {
        const items = await SearchService.search(debouncedQuery, category);
        if (active) {
          setResults(items);
        }
      } catch (err) {
        console.error(err);
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    };

    fetchResults();

    return () => {
      active = false;
    };
  }, [debouncedQuery, category]);

  return {
    isOpen,
    setIsOpen,
    query,
    setQuery,
    category,
    setCategory,
    results,
    loading,
  };
}
