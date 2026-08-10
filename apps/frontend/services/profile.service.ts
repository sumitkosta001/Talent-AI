import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { CandidateProfile } from '@/types/profile';
import { MOCK_PROFILE } from '@/mock/profile';
import { apiClient } from '@/lib/apiClient';

export class CandidateProfileService {
  static getLocalProfile(): CandidateProfile {
    if (typeof window === 'undefined') return MOCK_PROFILE;
    const stored = localStorage.getItem('talentai_candidate_profile');
    if (!stored) {
      localStorage.setItem('talentai_candidate_profile', JSON.stringify(MOCK_PROFILE));
      return MOCK_PROFILE;
    }
    return JSON.parse(stored);
  }

  static saveLocalProfile(profile: CandidateProfile) {
    if (typeof window === 'undefined') return;
    localStorage.setItem('talentai_candidate_profile', JSON.stringify(profile));
  }

  static async getProfile(): Promise<CandidateProfile> {
    const token = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_token') : null;
    
    // If not logged in and dev mode is enabled, fall back to mock
    if (!token && DEV_MODE) {
      await mockDelay(200);
      return this.getLocalProfile();
    }

    const res = await apiClient.get('/api/v1/candidates/me');

    if (!res.ok) {
      if (res.status === 401 || res.status === 403 || res.status === 404) {
        if (DEV_MODE) return this.getLocalProfile();
      }
      throw new Error('Failed to retrieve candidate profile');
    }

    const data = await res.json();
    const userStored = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_user') : null;
    const user = userStored ? JSON.parse(userStored) : null;

    return {
      id: data.id,
      name: user?.name || 'Candidate User',
      email: user?.email || '',
      phone: data.phone_number || '',
      headline: data.headline || '',
      location: data.location || '',
      bio: data.bio || '',
      portfolioUrl: data.portfolio_url || '',
      completionPercentage: data.profile_completion_percentage || 0,
      visibility: 'Public',
      isOpenToWork: true,
      availabilityStatus: 'Active',
      currentRole: data.headline || '',
    };
  }

  static async updateProfile(updates: Partial<CandidateProfile>): Promise<CandidateProfile> {
    const token = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_token') : null;

    if (!token && DEV_MODE) {
      await mockDelay(300);
      const profile = this.getLocalProfile();
      const updated = { ...profile, ...updates };
      this.saveLocalProfile(updated);
      return updated;
    }

    // Map frontend fields to backend CandidateProfileUpdate schema
    const payload: Record<string, any> = {};
    if (updates.phone !== undefined) payload.phone_number = updates.phone;
    if (updates.location !== undefined) payload.location = updates.location;
    if (updates.headline !== undefined) payload.headline = updates.headline;
    if (updates.bio !== undefined) payload.bio = updates.bio;
    if (updates.portfolioUrl !== undefined) payload.portfolio_url = updates.portfolioUrl;

    const res = await apiClient.patch('/api/v1/candidates/me', payload);

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData?.detail?.[0]?.msg || errorData?.detail || 'Failed to save profile changes');
    }

    const data = await res.json();
    const userStored = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_user') : null;
    const user = userStored ? JSON.parse(userStored) : null;

    return {
      id: data.id,
      name: user?.name || 'Candidate User',
      email: user?.email || '',
      phone: data.phone_number || '',
      headline: data.headline || '',
      location: data.location || '',
      bio: data.bio || '',
      portfolioUrl: data.portfolio_url || '',
      completionPercentage: data.profile_completion_percentage || 0,
      visibility: 'Public',
      isOpenToWork: true,
      availabilityStatus: 'Active',
      currentRole: data.headline || '',
    };
  }
}
