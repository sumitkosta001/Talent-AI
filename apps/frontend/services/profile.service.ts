import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { CandidateProfile } from '@/types/profile';
import { MOCK_PROFILE } from '@/mock/profile';

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
    if (DEV_MODE) {
      await mockDelay(200);
      return this.getLocalProfile();
    }

    const res = await fetch('/api/profile');
    if (!res.ok) throw new Error('Failed to retrieve candidate profile');
    return res.json();
  }

  static async updateProfile(updates: Partial<CandidateProfile>): Promise<CandidateProfile> {
    if (DEV_MODE) {
      await mockDelay(300);
      const profile = this.getLocalProfile();
      const updated = { ...profile, ...updates };
      this.saveLocalProfile(updated);
      return updated;
    }

    const res = await fetch('/api/profile', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates),
    });
    if (!res.ok) throw new Error('Failed to save profile changes');
    return res.json();
  }
}
