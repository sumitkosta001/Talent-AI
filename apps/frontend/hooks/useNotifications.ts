'use client';

import { useState, useEffect, useCallback } from 'react';
import { Notification, NotificationFilter, NotificationStats } from '@/types/notification';
import { NotificationService } from '@/services/notification.service';
import { calculateNotificationStats } from '@/mock/notificationStats';

const initialFilter: NotificationFilter = {
  search: '',
  readStatus: 'All',
  category: 'All',
  priority: 'All',
  dateRange: 'All',
  sortBy: 'Newest',
};

export function useNotifications() {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [stats, setStats] = useState<NotificationStats | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<NotificationFilter>(initialFilter);

  const fetchNotifications = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const items = await NotificationService.getNotifications();
      setNotifications(items);
      setStats(calculateNotificationStats(items));
    } catch (err: any) {
      setError(err?.message || 'Failed to fetch notifications');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchNotifications();
  }, [fetchNotifications]);

  const updateFilter = useCallback((key: keyof NotificationFilter, value: any) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  }, []);

  const resetFilters = useCallback(() => {
    setFilters(initialFilter);
  }, []);

  const markRead = useCallback(async (id: string, read: boolean) => {
    try {
      const updated = await NotificationService.toggleRead(id, read);
      setNotifications((prev) => {
        const next = prev.map((n) => (n.id === id ? updated : n));
        setStats(calculateNotificationStats(next));
        return next;
      });
    } catch (err) {
      console.error(err);
    }
  }, []);

  const markAllRead = useCallback(async () => {
    try {
      const items = await NotificationService.markAllRead();
      setNotifications(items);
      setStats(calculateNotificationStats(items));
    } catch (err) {
      console.error(err);
    }
  }, []);

  const deleteNotification = useCallback(async (id: string) => {
    try {
      await NotificationService.deleteNotification(id);
      setNotifications((prev) => {
        const next = prev.filter((n) => n.id !== id);
        setStats(calculateNotificationStats(next));
        return next;
      });
    } catch (err) {
      console.error(err);
    }
  }, []);

  const clearAll = useCallback(async () => {
    try {
      await NotificationService.clearAll();
      setNotifications([]);
      setStats(calculateNotificationStats([]));
    } catch (err) {
      console.error(err);
    }
  }, []);

  const getFilteredAndSorted = useCallback(() => {
    let result = [...notifications];

    // Filter by search
    if (filters.search) {
      const s = filters.search.toLowerCase();
      result = result.filter(
        (n) =>
          n.title.toLowerCase().includes(s) ||
          n.description.toLowerCase().includes(s) ||
          n.category.toLowerCase().includes(s)
      );
    }

    // Filter by read status
    if (filters.readStatus === 'Read') {
      result = result.filter((n) => n.read);
    } else if (filters.readStatus === 'Unread') {
      result = result.filter((n) => !n.read);
    }

    // Filter by category
    if (filters.category !== 'All') {
      result = result.filter((n) => n.category === filters.category);
    }

    // Filter by priority
    if (filters.priority !== 'All') {
      result = result.filter((n) => n.priority === filters.priority);
    }

    // Sort
    if (filters.sortBy === 'Newest') {
      // Mock timestamps are parsed relatively, so keep list order or reverse
      // In production we would sort by real ISO strings.
    }

    return result;
  }, [notifications, filters]);

  return {
    notifications: getFilteredAndSorted(),
    rawNotifications: notifications,
    stats,
    loading,
    error,
    filters,
    updateFilter,
    resetFilters,
    markRead,
    markAllRead,
    deleteNotification,
    clearAll,
    refetch: fetchNotifications,
  };
}
