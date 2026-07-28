'use client';

import { useState, useEffect, useCallback } from 'react';
import { PlatformReport } from '@/types/report';
import { AdminReportService } from '@/services/report.service';

export function useReports() {
  const [reports, setReports] = useState<PlatformReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchReports = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await AdminReportService.getReports();
      setReports(data);
    } catch (err: any) {
      setError(err?.message || 'Failed to retrieve platform reports log');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchReports();
  }, [fetchReports]);

  return {
    reports,
    loading,
    error,
    refetch: fetchReports,
  };
}
