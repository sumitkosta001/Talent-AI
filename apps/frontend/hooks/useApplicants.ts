'use client';

import { useState, useEffect, useCallback } from 'react';
import { Applicant, ApplicantStatus } from '@/types/applicant';
import { RecruiterApplicantService } from '@/services/applicant.service';

export function useApplicants() {
  const [applicants, setApplicants] = useState<Applicant[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('');
  const [experience, setExperience] = useState('');
  const [atsMin, setAtsMin] = useState<number>(0);
  const [location, setLocation] = useState('');
  const [sortBy, setSortBy] = useState<'newest' | 'oldest' | 'ats-desc' | 'ats-asc'>('ats-desc');

  const fetchApplicants = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const items = await RecruiterApplicantService.getApplicants();
      setApplicants(items);
    } catch (err: any) {
      setError(err?.message || 'Failed to retrieve candidate applicants list');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchApplicants();
  }, [fetchApplicants]);

  const handleUpdateStatus = useCallback(async (id: string, newStatus: ApplicantStatus) => {
    try {
      const updated = await RecruiterApplicantService.updateStatus(id, newStatus);
      setApplicants((prev) => prev.map((a) => (a.id === id ? updated : a)));
      return true;
    } catch (err) {
      console.error(err);
      return false;
    }
  }, []);

  const getFilteredAndSorted = useCallback(() => {
    let result = [...applicants];

    // Search query matches (name, email, skills)
    if (search) {
      const q = search.toLowerCase();
      result = result.filter(
        (a) =>
          a.name.toLowerCase().includes(q) ||
          a.email.toLowerCase().includes(q) ||
          a.skills.some((s) => s.toLowerCase().includes(q))
      );
    }

    // Status match
    if (status) {
      result = result.filter((a) => a.status === status);
    }

    // Experience matching
    if (experience) {
      result = result.filter((a) => a.experience.includes(experience));
    }

    // Location match
    if (location) {
      result = result.filter((a) => a.timeline.some(t => t.notes?.includes(location)) || a.name.toLowerCase().includes(location.toLowerCase()));
    }

    // ATS minimum score
    if (atsMin > 0) {
      result = result.filter((a) => a.atsScore >= atsMin);
    }

    // Sorting
    if (sortBy === 'newest') {
      result.sort((a, b) => new Date(b.appliedDate).getTime() - new Date(a.appliedDate).getTime());
    } else if (sortBy === 'oldest') {
      result.sort((a, b) => new Date(a.appliedDate).getTime() - new Date(b.appliedDate).getTime());
    } else if (sortBy === 'ats-desc') {
      result.sort((a, b) => b.atsScore - a.atsScore);
    } else if (sortBy === 'ats-asc') {
      result.sort((a, b) => a.atsScore - b.atsScore);
    }

    return result;
  }, [applicants, search, status, experience, atsMin, location, sortBy]);

  return {
    applicants: getFilteredAndSorted(),
    rawApplicants: applicants,
    loading,
    error,
    search,
    setSearch,
    status,
    setStatus,
    experience,
    setExperience,
    atsMin,
    setAtsMin,
    location,
    setLocation,
    sortBy,
    setSortBy,
    updateStatus: handleUpdateStatus,
    refetch: fetchApplicants,
  };
}
