import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { CandidateExperience } from '@/types/experience';
import { MOCK_EXPERIENCE } from '@/mock/experience';

export class CandidateExperienceService {
  static getLocalExperience(): CandidateExperience[] {
    if (typeof window === 'undefined') return MOCK_EXPERIENCE;
    const stored = localStorage.getItem('talentai_candidate_experience');
    if (!stored) {
      localStorage.setItem('talentai_candidate_experience', JSON.stringify(MOCK_EXPERIENCE));
      return MOCK_EXPERIENCE;
    }
    return JSON.parse(stored);
  }

  static saveLocalExperience(list: CandidateExperience[]) {
    if (typeof window === 'undefined') return;
    localStorage.setItem('talentai_candidate_experience', JSON.stringify(list));
  }

  static async getExperience(): Promise<CandidateExperience[]> {
    if (DEV_MODE) {
      await mockDelay(200);
      return this.getLocalExperience();
    }

    const res = await fetch('/api/profile/experience');
    if (!res.ok) throw new Error('Failed to retrieve experience timeline');
    return res.json();
  }

  static async addExperience(exp: Partial<CandidateExperience>): Promise<CandidateExperience> {
    if (DEV_MODE) {
      await mockDelay(300);
      const list = this.getLocalExperience();
      const newExp: CandidateExperience = {
        id: `exp-${Date.now()}`,
        companyName: exp.companyName || 'New Company',
        companyLogo: 'C',
        jobTitle: exp.jobTitle || 'New Role',
        employmentType: exp.employmentType || 'Full-time',
        location: exp.location || 'Remote',
        startDate: exp.startDate || '',
        endDate: exp.endDate || '',
        isCurrentJob: exp.isCurrentJob || false,
        description: exp.description || '',
        achievements: exp.achievements || [],
        technologiesUsed: exp.technologiesUsed || [],
      };
      list.unshift(newExp);
      this.saveLocalExperience(list);
      return newExp;
    }

    const res = await fetch('/api/profile/experience', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(exp),
    });
    if (!res.ok) throw new Error('Failed to create experience block');
    return res.json();
  }

  static async deleteExperience(id: string): Promise<boolean> {
    if (DEV_MODE) {
      await mockDelay(200);
      const list = this.getLocalExperience();
      const filtered = list.filter((e) => e.id !== id);
      this.saveLocalExperience(filtered);
      return true;
    }

    const res = await fetch(`/api/profile/experience/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to delete experience block');
    return true;
  }
}
