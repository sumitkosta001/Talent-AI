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

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const handleMutation = () => {
      // Fetch profile without resetting loading to prevent full-screen layout thrashing/loaders
      CandidateProfileService.getProfile().then(setProfile).catch(() => {});
    };
    window.addEventListener('profile-mutated', handleMutation);
    return () => {
      window.removeEventListener('profile-mutated', handleMutation);
    };
  }, []);

  const updateProfile = useCallback(async (updates: Partial<CandidateProfile>) => {
    try {
      const updated = await CandidateProfileService.updateProfile(updates);
      setProfile(updated);
      if (typeof window !== 'undefined') {
        window.dispatchEvent(new Event('profile-mutated'));
      }
      return true;
    } catch (err: any) {
      alert(err?.message || 'Failed to update profile details');
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
