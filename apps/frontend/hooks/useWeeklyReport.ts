'use client';

import { useState, useEffect, useCallback } from 'react';
import { WeeklyReportData } from '@/types/weeklyReport';
import { ReportService } from '@/services/report.service';

export function useWeeklyReport() {
  const [reportData, setReportData] = useState<WeeklyReportData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchReport = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await ReportService.getWeeklyReport();
      setReportData(data);
    } catch (err: any) {
      setError(err?.message || 'Failed to load weekly report');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchReport();
  }, [fetchReport]);

  return {
    reportData,
    loading,
    error,
    refetch: fetchReport,
  };
}
