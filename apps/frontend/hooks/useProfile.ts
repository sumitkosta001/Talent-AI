'use client';

import { useState, useEffect, useCallback } from 'react';
import { CandidateProfile } from '@/types/profile';
import { CandidateProfileService } from '@/services/profile.service';

export function useProfile() {
  const [profile, setProfile] = useState<CandidateProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProfile = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await CandidateProfileService.getProfile();
      setProfile(data);
    } catch (err: any) {
      setError(err?.message || 'Failed to load profile details');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchProfile();
  }, [fetchProfile]);

  const updateProfile = useCallback(async (updates: Partial<CandidateProfile>) => {
    try {
      const updated = await CandidateProfileService.updateProfile(updates);
      setProfile(updated);
      return true;
    } catch {
      return false;
    }
  }, []);

  return {
    profile,
    loading,
    error,
    updateProfile,
    refetch: fetchProfile,
  };
}
