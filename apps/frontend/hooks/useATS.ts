import { useState, useEffect, useCallback } from 'react';
import { ATSResult } from '@/types/ats';
import { ATSService } from '@/services/ats.service';

export function useATS() {
  const [result, setResult] = useState<ATSResult | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSection, setSelectedSection] = useState<string | null>(null);
  const [expandedSuggestions, setExpandedSuggestions] = useState<string[]>([]);
  const [filterPriority, setFilterPriority] = useState<'all' | 'high' | 'medium' | 'low'>('all');

  const fetchAnalysis = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await ATSService.getATSAnalysis();
      setResult(data);
      if (data.sections.length > 0) {
        setSelectedSection(data.sections[0].sectionName);
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to fetch ATS analysis data');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAnalysis();
  }, [fetchAnalysis]);

  const toggleSuggestionExpand = useCallback((id: string) => {
    setExpandedSuggestions((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  }, []);

  return {
    result,
    loading,
    error,
    selectedSection,
    setSelectedSection,
    expandedSuggestions,
    toggleSuggestionExpand,
    filterPriority,
    setFilterPriority,
    refetch: fetchAnalysis,
  };
}
