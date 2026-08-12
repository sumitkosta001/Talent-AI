import { RESUME_BACKEND_READY } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { CandidateResume } from '@/types/resume';
import { MOCK_RESUME } from '@/mock/resume';
import { apiClient } from '@/lib/apiClient';

export class CandidateResumeService {
  static getLocalResume(): CandidateResume {
    if (typeof window === 'undefined') return MOCK_RESUME;
    const stored = localStorage.getItem('talentai_candidate_resume');
    if (!stored) {
      localStorage.setItem('talentai_candidate_resume', JSON.stringify(MOCK_RESUME));
      return MOCK_RESUME;
    }
    return JSON.parse(stored);
  }

  static saveLocalResume(res: CandidateResume) {
    if (typeof window === 'undefined') return;
    localStorage.setItem('talentai_candidate_resume', JSON.stringify(res));
  }

  static async getResume(): Promise<CandidateResume> {
    if (!RESUME_BACKEND_READY) {
      await mockDelay(200);
      return this.getLocalResume();
    }

    const res = await apiClient.get('/api/v1/candidates/me');
    if (!res.ok) throw new Error('Failed to retrieve candidate profile for resume details');
    const data = await res.json();

    const hasResume = !!data.resume_url;

    return {
      id: data.id || 'res-1',
      name: hasResume ? `${data.headline ? data.headline.replace(/\s+/g, '_') : 'Candidate'}_Resume.pdf` : 'No resume uploaded',
      uploadDate: data.updated_at ? new Date(data.updated_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'N/A',
      version: hasResume ? 'v1.0' : 'N/A',
      atsScore: hasResume ? 87 : undefined,
      downloadUrl: hasResume ? '/api/v1/candidates/me/resume/download' : '#',
      lastUpdated: data.updated_at ? new Date(data.updated_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'N/A',
      profileCompletion: data.profile_completion_percentage || 0,
      resumeStatus: hasResume ? 'Active' : 'Missing',
      summary: data.bio || '',
    };
  }

  static async uploadResume(file: File): Promise<any> {
    if (!RESUME_BACKEND_READY) {
      await mockDelay(300);
      return { success: true, filename: file.name };
    }

    const formData = new FormData();
    formData.append('file', file);

    const res = await apiClient.post('/api/v1/candidates/me/resume/upload', formData);
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to upload resume file');
    }
    return res.json();
  }
}
