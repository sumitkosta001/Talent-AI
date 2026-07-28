'use client';

import { useState, useEffect, useCallback } from 'react';
import { Applicant, ApplicantStatus } from '@/types/applicant';
import { RecruiterApplicantService } from '@/services/applicant.service';

export function useApplicant(id: string) {
  const [applicant, setApplicant] = useState<Applicant | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDetail = useCallback(async () => {
    if (!id) return;
    setLoading(true);
    setError(null);
    try {
      const match = await RecruiterApplicantService.getApplicantById(id);
      if (match) {
        setApplicant(match);
      } else {
        setError('Applicant not found');
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to fetch applicant details');
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchDetail();
  }, [fetchDetail]);

  const handleUpdateStatus = useCallback(async (newStatus: ApplicantStatus) => {
    if (!applicant) return false;
    try {
      const updated = await RecruiterApplicantService.updateStatus(applicant.id, newStatus);
      setApplicant(updated);
      return true;
    } catch (err) {
      console.error(err);
      return false;
    }
  }, [applicant]);

  const handleAddNotes = useCallback(async (notes: string) => {
    if (!applicant) return false;
    try {
      const updated = await RecruiterApplicantService.addNotes(applicant.id, notes);
      setApplicant(updated);
      return true;
    } catch (err) {
      console.error(err);
      return false;
    }
  }, [applicant]);

  return {
    applicant,
    loading,
    error,
    updateStatus: handleUpdateStatus,
    addNotes: handleAddNotes,
    refetch: fetchDetail,
  };
}
