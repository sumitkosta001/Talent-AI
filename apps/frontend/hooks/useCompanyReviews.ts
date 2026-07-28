'use client';

import { useState, useEffect, useCallback } from 'react';
import { CompanyReview } from '@/types/companyReview';
import { CompanyReviewService } from '@/services/companyReview.service';

export function useCompanyReviews(companyId: string) {
  const [reviews, setReviews] = useState<CompanyReview[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchReviews = useCallback(async () => {
    if (!companyId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await CompanyReviewService.getReviewsByCompanyId(companyId);
      setReviews(data);
    } catch (err: any) {
      setError(err?.message || 'Failed to retrieve company reviews');
    } finally {
      setLoading(false);
    }
  }, [companyId]);

  useEffect(() => {
    fetchReviews();
  }, [fetchReviews]);

  return {
    reviews,
    loading,
    error,
    refetch: fetchReviews,
  };
}
