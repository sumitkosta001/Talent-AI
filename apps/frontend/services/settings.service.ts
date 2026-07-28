import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { CandidateSettings } from '@/types/settings';
import { MOCK_SETTINGS } from '@/mock/settings';

export class SettingsService {
  static getLocalSettings(): CandidateSettings {
    if (typeof window === 'undefined') return MOCK_SETTINGS;
    const stored = localStorage.getItem('talentai_candidate_settings');
    if (!stored) {
      localStorage.setItem('talentai_candidate_settings', JSON.stringify(MOCK_SETTINGS));
      return MOCK_SETTINGS;
    }
    return JSON.parse(stored);
  }

  static saveLocalSettings(settings: CandidateSettings) {
    if (typeof window === 'undefined') return;
    localStorage.setItem('talentai_candidate_settings', JSON.stringify(settings));
  }

  static async getSettings(): Promise<CandidateSettings> {
    if (DEV_MODE) {
      await mockDelay(200);
      return this.getLocalSettings();
    }

    const res = await fetch('/api/profile/settings');
    if (!res.ok) throw new Error('Failed to retrieve settings details');
    return res.json();
  }

  static async updateSettings(settings: CandidateSettings): Promise<CandidateSettings> {
    if (DEV_MODE) {
      await mockDelay(300);
      this.saveLocalSettings(settings);
      
      // Sync theme preference immediately if in browser
      if (typeof window !== 'undefined') {
        if (settings.theme === 'Dark') {
          document.documentElement.classList.add('dark');
        } else {
          document.documentElement.classList.remove('dark');
        }
      }
      return settings;
    }

    const res = await fetch('/api/profile/settings', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(settings),
    });
    if (!res.ok) throw new Error('Failed to save settings modifications');
    return res.json();
  }

  static async changePassword(passwordData: any): Promise<boolean> {
    if (DEV_MODE) {
      await mockDelay(400);
      return true;
    }

    const res = await fetch('/api/profile/password', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(passwordData),
    });
    if (!res.ok) throw new Error('Failed to update account password');
    return true;
  }

  static async deleteAccount(): Promise<boolean> {
    if (DEV_MODE) {
      await mockDelay(500);
      if (typeof window !== 'undefined') {
        localStorage.removeItem('talentai_candidate_settings');
        localStorage.removeItem('talentai_candidate_profile');
      }
      return true;
    }

    const res = await fetch('/api/profile', { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to delete account');
    return true;
  }
}
