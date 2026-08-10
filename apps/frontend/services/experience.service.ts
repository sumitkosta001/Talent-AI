import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { CandidateExperience } from '@/types/experience';
import { MOCK_EXPERIENCE } from '@/mock/experience';
import { apiClient } from '@/lib/apiClient';

function toISODateString(val?: string): string | null {
  if (!val) return null;
  const trimmed = val.trim();
  if (!trimmed) return null;
  if (/^\d{4}-\d{2}-\d{2}$/.test(trimmed)) return trimmed;
  if (/^\d{4}-\d{2}$/.test(trimmed)) return `${trimmed}-01`;
  if (/^\d{4}$/.test(trimmed)) return `${trimmed}-01-01`;
  try {
    const d = new Date(trimmed);
    if (isNaN(d.getTime())) return null;
    return d.toISOString().split('T')[0];
  } catch {
    return null;
  }
}

function notifyMutation() {
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new Event('profile-mutated'));
  }
}

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
    const token = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_token') : null;

    if (!token && DEV_MODE) {
      await mockDelay(200);
      return this.getLocalExperience();
    }

    const res = await apiClient.get('/api/v1/candidates/me/experience');

    if (!res.ok) {
      if (DEV_MODE) return this.getLocalExperience();
      throw new Error('Failed to retrieve experience timeline');
    }

    const data = await res.json();
    return data.map((exp: any) => ({
      id: exp.id,
      companyName: exp.company,
      jobTitle: exp.job_title,
      employmentType: 'Full-time',
      location: 'Remote',
      startDate: exp.start_date ? exp.start_date.substring(0, 7) : '',
      endDate: exp.end_date ? exp.end_date.substring(0, 7) : '',
      isCurrentJob: !exp.end_date,
      description: exp.description || '',
      achievements: [],
      technologiesUsed: [],
    }));
  }

  static async addExperience(exp: Partial<CandidateExperience>): Promise<CandidateExperience> {
    const token = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_token') : null;

    if (!token && DEV_MODE) {
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
      notifyMutation();
      return newExp;
    }

    const payload = {
      company: exp.companyName,
      job_title: exp.jobTitle,
      start_date: toISODateString(exp.startDate) || '2020-01-01',
      end_date: exp.isCurrentJob ? null : (toISODateString(exp.endDate) || null),
      description: exp.description || null,
    };

    const res = await apiClient.post('/api/v1/candidates/me/experience', payload);

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData?.detail?.[0]?.msg || errorData?.detail || 'Failed to create experience block');
    }

    const added = await res.json();
    notifyMutation();
    return {
      id: added.id,
      companyName: added.company,
      jobTitle: added.job_title,
      employmentType: 'Full-time',
      location: 'Remote',
      startDate: added.start_date ? added.start_date.substring(0, 7) : '',
      endDate: added.end_date ? added.end_date.substring(0, 7) : '',
      isCurrentJob: !added.end_date,
      description: added.description || '',
      achievements: [],
      technologiesUsed: [],
    };
  }

  static async deleteExperience(id: string): Promise<boolean> {
    const token = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_token') : null;

    if (!token && DEV_MODE) {
      await mockDelay(200);
      const list = this.getLocalExperience();
      const filtered = list.filter((e) => e.id !== id);
      this.saveLocalExperience(filtered);
      notifyMutation();
      return true;
    }

    const res = await apiClient.delete(`/api/v1/candidates/me/experience/${id}`);

    if (!res.ok) throw new Error('Failed to delete experience block');
    notifyMutation();
    return true;
  }
}
