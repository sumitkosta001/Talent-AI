import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { CandidateSkill } from '@/types/skill';
import { MOCK_SKILLS } from '@/mock/skills';
import { apiClient } from '@/lib/apiClient';

function notifyMutation() {
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new Event('profile-mutated'));
  }
}

export class CandidateSkillService {
  static getLocalSkills(): CandidateSkill[] {
    if (typeof window === 'undefined') return MOCK_SKILLS;
    const stored = localStorage.getItem('talentai_candidate_skills');
    if (!stored) {
      localStorage.setItem('talentai_candidate_skills', JSON.stringify(MOCK_SKILLS));
      return MOCK_SKILLS;
    }
    return JSON.parse(stored);
  }

  static saveLocalSkills(list: CandidateSkill[]) {
    if (typeof window === 'undefined') return;
    localStorage.setItem('talentai_candidate_skills', JSON.stringify(list));
  }

  static async getSkills(): Promise<CandidateSkill[]> {
    const token = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_token') : null;

    if (!token && DEV_MODE) {
      await mockDelay(200);
      return this.getLocalSkills();
    }

    const res = await apiClient.get('/api/v1/candidates/me/skills');

    if (!res.ok) {
      if (DEV_MODE) return this.getLocalSkills();
      throw new Error('Failed to retrieve candidate skills');
    }

    const data = await res.json();
    return data.map((s: any) => ({
      id: s.id,
      name: s.skill_name,
      level: (s.proficiency.charAt(0).toUpperCase() + s.proficiency.slice(1)) as any,
      yearsOfExperience: 3,
    }));
  }

  static async addSkill(name: string, level: 'Beginner' | 'Intermediate' | 'Expert', exp: number): Promise<CandidateSkill> {
    const token = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_token') : null;

    if (!token && DEV_MODE) {
      await mockDelay(300);
      const list = this.getLocalSkills();
      const newS: CandidateSkill = {
        id: `sk-${Date.now()}`,
        name,
        level,
        yearsOfExperience: exp,
      };
      list.unshift(newS);
      this.saveLocalSkills(list);
      notifyMutation();
      return newS;
    }

    const payload = {
      skill_name: name,
      category: 'programming',
      proficiency: level.toLowerCase(),
    };

    const res = await apiClient.post('/api/v1/candidates/me/skills', payload);

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      if (res.status === 409) {
        throw new Error('This skill tag already exists on your profile.');
      }
      throw new Error(errorData?.detail?.[0]?.msg || errorData?.detail || 'Failed to create skill entry');
    }

    const added = await res.json();
    notifyMutation();
    return {
      id: added.id,
      name: added.skill_name,
      level: (added.proficiency.charAt(0).toUpperCase() + added.proficiency.slice(1)) as any,
      yearsOfExperience: exp,
    };
  }

  static async deleteSkill(id: string): Promise<boolean> {
    const token = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_token') : null;

    if (!token && DEV_MODE) {
      await mockDelay(200);
      const list = this.getLocalSkills();
      const filtered = list.filter((s) => s.id !== id);
      this.saveLocalSkills(filtered);
      notifyMutation();
      return true;
    }

    const res = await apiClient.delete(`/api/v1/candidates/me/skills/${id}`);

    if (!res.ok) throw new Error('Failed to delete skill entry');
    notifyMutation();
    return true;
  }
}
