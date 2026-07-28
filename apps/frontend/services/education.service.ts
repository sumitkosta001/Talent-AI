import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { CandidateEducation } from '@/types/education';
import { MOCK_EDUCATION } from '@/mock/education';

export class CandidateEducationService {
  static getLocalEducation(): CandidateEducation[] {
    if (typeof window === 'undefined') return MOCK_EDUCATION;
    const stored = localStorage.getItem('talentai_candidate_education');
    if (!stored) {
      localStorage.setItem('talentai_candidate_education', JSON.stringify(MOCK_EDUCATION));
      return MOCK_EDUCATION;
    }
    return JSON.parse(stored);
  }

  static saveLocalEducation(list: CandidateEducation[]) {
    if (typeof window === 'undefined') return;
    localStorage.setItem('talentai_candidate_education', JSON.stringify(list));
  }

  static async getEducation(): Promise<CandidateEducation[]> {
    if (DEV_MODE) {
      await mockDelay(200);
      return this.getLocalEducation();
    }

    const res = await fetch('/api/profile/education');
    if (!res.ok) throw new Error('Failed to retrieve education history');
    return res.json();
  }

  static async addEducation(edu: Partial<CandidateEducation>): Promise<CandidateEducation> {
    if (DEV_MODE) {
      await mockDelay(300);
      const list = this.getLocalEducation();
      const newEdu: CandidateEducation = {
        id: `edu-${Date.now()}`,
        institutionName: edu.institutionName || 'New Institution',
        degree: edu.degree || 'Degree',
        branch: edu.branch || 'Field',
        cgpaOrPercentage: edu.cgpaOrPercentage || '3.5 GPA',
        startYear: edu.startYear || '',
        endYear: edu.endYear || '',
        achievements: edu.achievements || [],
        relevantCoursework: edu.relevantCoursework || [],
      };
      list.unshift(newEdu);
      this.saveLocalEducation(list);
      return newEdu;
    }

    const res = await fetch('/api/profile/education', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(edu),
    });
    if (!res.ok) throw new Error('Failed to create education block');
    return res.json();
  }

  static async deleteEducation(id: string): Promise<boolean> {
    if (DEV_MODE) {
      await mockDelay(200);
      const list = this.getLocalEducation();
      const filtered = list.filter((e) => e.id !== id);
      this.saveLocalEducation(filtered);
      return true;
    }

    const res = await fetch(`/api/profile/education/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to delete education block');
    return true;
  }
}
