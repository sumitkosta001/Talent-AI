'use client';

import { useState, useEffect, useCallback } from 'react';
import { CalendarEvent } from '@/types/calendar';
import { CalendarService } from '@/services/calendar.service';

export function useCalendar() {
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDate, setSelectedDate] = useState<string | null>(null);

  const fetchEvents = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const evs = await CalendarService.getEvents();
      setEvents(evs);
    } catch (err: any) {
      setError(err?.message || 'Failed to load calendar events');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchEvents();
  }, [fetchEvents]);

  return {
    events,
    loading,
    error,
    selectedDate,
    setSelectedDate,
    refetch: fetchEvents,
  };
}
