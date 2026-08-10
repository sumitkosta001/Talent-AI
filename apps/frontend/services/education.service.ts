import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { CandidateEducation } from '@/types/education';
import { MOCK_EDUCATION } from '@/mock/education';
import { apiClient } from '@/lib/apiClient';

function notifyMutation() {
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new Event('profile-mutated'));
  }
}

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
    const token = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_token') : null;

    if (!token && DEV_MODE) {
      await mockDelay(200);
      return this.getLocalEducation();
    }

    const res = await apiClient.get('/api/v1/candidates/me/education');

    if (!res.ok) {
      if (DEV_MODE) return this.getLocalEducation();
      throw new Error('Failed to retrieve education history');
    }

    const data = await res.json();
    return data.map((edu: any) => ({
      id: edu.id,
      institutionName: edu.institution,
      degree: edu.degree.includes(' in ') ? edu.degree.split(' in ')[0] : edu.degree,
      branch: edu.degree.includes(' in ') ? edu.degree.split(' in ')[1] : '',
      cgpaOrPercentage: edu.grade_or_cgpa || '',
      startYear: edu.start_date ? String(new Date(edu.start_date).getFullYear()) : '',
      endYear: edu.end_date ? String(new Date(edu.end_date).getFullYear()) : '',
      achievements: [],
      relevantCoursework: [],
    }));
  }

  static async addEducation(edu: Partial<CandidateEducation>): Promise<CandidateEducation> {
    const token = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_token') : null;

    if (!token && DEV_MODE) {
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
      notifyMutation();
      return newEdu;
    }

    const payload = {
      institution: edu.institutionName,
      degree: edu.degree + (edu.branch ? ` in ${edu.branch}` : ''),
      grade_or_cgpa: edu.cgpaOrPercentage || null,
      start_date: edu.startYear ? `${edu.startYear}-01-01` : '2020-01-01',
      end_date: edu.endYear ? `${edu.endYear}-01-01` : null,
    };

    const res = await apiClient.post('/api/v1/candidates/me/education', payload);

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData?.detail?.[0]?.msg || errorData?.detail || 'Failed to create education block');
    }

    const added = await res.json();
    notifyMutation();
    return {
      id: added.id,
      institutionName: added.institution,
      degree: added.degree.includes(' in ') ? added.degree.split(' in ')[0] : added.degree,
      branch: added.degree.includes(' in ') ? added.degree.split(' in ')[1] : '',
      cgpaOrPercentage: added.grade_or_cgpa || '',
      startYear: added.start_date ? String(new Date(added.start_date).getFullYear()) : '',
      endYear: added.end_date ? String(new Date(added.end_date).getFullYear()) : '',
      achievements: [],
      relevantCoursework: [],
    };
  }

  static async deleteEducation(id: string): Promise<boolean> {
    const token = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_token') : null;

    if (!token && DEV_MODE) {
      await mockDelay(200);
      const list = this.getLocalEducation();
      const filtered = list.filter((e) => e.id !== id);
      this.saveLocalEducation(filtered);
      notifyMutation();
      return true;
    }

    const res = await apiClient.delete(`/api/v1/candidates/me/education/${id}`);

    if (!res.ok) throw new Error('Failed to delete education block');
    notifyMutation();
    return true;
  }
}
