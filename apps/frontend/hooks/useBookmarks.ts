'use client';

import { useState, useEffect, useCallback } from 'react';
import { BookmarkItem } from '@/types/bookmark';
import { BookmarkService } from '@/services/bookmark.service';

export function useBookmarks() {
  const [bookmarks, setBookmarks] = useState<BookmarkItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Job bookmark IDs tracker
  const [bookmarkedIds, setBookmarkedIds] = useState<string[]>([]);

  // Load candidate bookmarks from service
  const fetchBookmarks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await BookmarkService.getBookmarks();
      setBookmarks(data);
    } catch (err: any) {
      setError(err?.message || 'Failed to load saved bookmarks');
    } finally {
      setLoading(false);
    }
  }, []);

  // Load job bookmark IDs from local storage
  useEffect(() => {
    if (typeof window === 'undefined') return;
    const stored = localStorage.getItem('talentai_bookmarks');
    if (!stored) {
      const preloaded = ['google-sde-3'];
      localStorage.setItem('talentai_bookmarks', JSON.stringify(preloaded));
      setBookmarkedIds(preloaded);
    } else {
      try {
        setBookmarkedIds(JSON.parse(stored));
      } catch {
        setBookmarkedIds([]);
      }
    }
  }, []);

  const addBookmark = useCallback(async (item: Omit<BookmarkItem, 'id' | 'savedDate'>) => {
    try {
      const added = await BookmarkService.addBookmark(item);
      setBookmarks((prev) => [added, ...prev]);
      return added;
    } catch (err) {
      console.error(err);
      return null;
    }
  }, []);

  const removeBookmark = useCallback(async (id: string) => {
    try {
      await BookmarkService.removeBookmark(id);
      setBookmarks((prev) => prev.filter((b) => b.id !== id));
      return true;
    } catch (err) {
      console.error(err);
      return false;
    }
  }, []);

  const isBookmarked = useCallback((jobId: string) => {
    return bookmarkedIds.includes(jobId);
  }, [bookmarkedIds]);

  const toggleBookmark = useCallback((jobId: string) => {
    setBookmarkedIds((prev) => {
      const next = prev.includes(jobId) ? prev.filter((id) => id !== jobId) : [...prev, jobId];
      if (typeof window !== 'undefined') {
        localStorage.setItem('talentai_bookmarks', JSON.stringify(next));
      }
      return next;
    });
  }, []);

  useEffect(() => {
    fetchBookmarks();
  }, [fetchBookmarks]);

  return {
    bookmarks,
    loading,
    error,
    addBookmark,
    removeBookmark,
    bookmarkedIds,
    isBookmarked,
    toggleBookmark,
    refetch: fetchBookmarks,
  };
}
