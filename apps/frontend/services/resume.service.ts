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

    // 1. Fetch candidate profile to get profileCompletion and bio/summary
    const profileRes = await apiClient.get('/api/v1/candidates/me');
    if (!profileRes.ok) throw new Error('Failed to retrieve candidate profile for resume details');
    const profileData = await profileRes.json();

    // 2. Fetch resumes list to check if there is an active/current resume
    const resumesRes = await apiClient.get('/api/v1/candidates/me/resumes?page=1&page_size=10');
    let currentResume: any = null;
    if (resumesRes.ok) {
      const listData = await resumesRes.json();
      const items = listData.items || [];
      // Find the one marked current, or fall back to the first one in the list
      currentResume = items.find((r: any) => r.is_current) || items[0] || null;
    }

    if (!currentResume) {
      return {
        id: '',
        name: 'No resume uploaded',
        uploadDate: 'N/A',
        version: 'N/A',
        atsScore: undefined,
        downloadUrl: '#',
        lastUpdated: 'N/A',
        profileCompletion: profileData.profile_completion_percentage || 0,
        resumeStatus: 'Missing',
        summary: profileData.bio || '',
      };
    }

    return {
      id: currentResume.id,
      name: currentResume.original_filename,
      uploadDate: currentResume.uploaded_at
        ? new Date(currentResume.uploaded_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
        : 'N/A',
      version: `v${currentResume.version}.0`,
      atsScore: currentResume.atsScore || 87, // UI default ATS parsing compatibility score
      downloadUrl: `/api/v1/candidates/me/resumes/${currentResume.id}/download`,
      lastUpdated: currentResume.uploaded_at
        ? new Date(currentResume.uploaded_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
        : 'N/A',
      profileCompletion: profileData.profile_completion_percentage || 0,
      resumeStatus: currentResume.status === 'processed' ? 'Active' : (currentResume.status === 'failed' ? 'Failed' : 'Active'),
      summary: profileData.bio || '',
    };
  }

  static async getResumes(page: number = 1, pageSize: number = 10): Promise<any> {
    if (!RESUME_BACKEND_READY) {
      await mockDelay(200);
      return { items: [this.getLocalResume()], total: 1 };
    }
    const res = await apiClient.get(`/api/v1/candidates/me/resumes?page=${page}&page_size=${pageSize}`);
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to list resumes');
    }
    return res.json();
  }

  static async previewResume(resumeId: string): Promise<Blob> {
    if (!RESUME_BACKEND_READY) {
      await mockDelay(200);
      return new Blob(['Mock PDF Preview Content'], { type: 'application/pdf' });
    }
    const res = await apiClient.get(`/api/v1/candidates/me/resumes/${resumeId}/preview`);
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to fetch resume preview');
    }
    return res.blob();
  }

  static async downloadResume(resumeId: string): Promise<Blob> {
    if (!RESUME_BACKEND_READY) {
      await mockDelay(200);
      return new Blob(['Mock PDF Download Content'], { type: 'application/pdf' });
    }
    const res = await apiClient.get(`/api/v1/candidates/me/resumes/${resumeId}/download`);
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to fetch resume download');
    }
    return res.blob();
  }

  static async uploadResume(file: File): Promise<any> {
    if (!RESUME_BACKEND_READY) {
      await mockDelay(300);
      return { success: true, filename: file.name };
    }

    const formData = new FormData();
    formData.append('file', file);

    const res = await apiClient.post('/api/v1/candidates/me/resumes', formData);
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to upload resume file');
    }
    return res.json();
  }

  static async getCurrentResume(): Promise<any> {
    if (!RESUME_BACKEND_READY) {
      await mockDelay(200);
      return this.getLocalResume();
    }
    const res = await apiClient.get('/api/v1/candidates/me/resumes/current');
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to fetch current resume');
    }
    return res.json();
  }

  static async restoreResumeVersion(resumeId: string): Promise<any> {
    if (!RESUME_BACKEND_READY) {
      await mockDelay(200);
      return { success: true, message: 'Version restored successfully' };
    }
    const res = await apiClient.post(`/api/v1/candidates/me/resumes/${resumeId}/restore`, {});
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to restore resume version');
    }
    return res.json();
  }

  static async deleteResume(resumeId: string): Promise<any> {
    if (!RESUME_BACKEND_READY) {
      await mockDelay(200);
      return { success: true, message: 'Resume deleted successfully' };
    }
    const res = await apiClient.delete(`/api/v1/candidates/me/resumes/${resumeId}`);
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to delete resume');
    }
    return res.json();
  }

  static async getResumeHistory(page: number = 1, pageSize: number = 10): Promise<any> {
    if (!RESUME_BACKEND_READY) {
      await mockDelay(200);
      return { items: [this.getLocalResume()], total: 1 };
    }
    const res = await apiClient.get(`/api/v1/candidates/me/resumes/history?page=${page}&page_size=${pageSize}`);
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to fetch resume history');
    }
    return res.json();
  }

  static async retryResumeProcessing(resumeId: string): Promise<any> {
    if (!RESUME_BACKEND_READY) {
      await mockDelay(300);
      return { success: true, message: 'Processing retried successfully' };
    }
    const res = await apiClient.post(`/api/v1/candidates/me/resumes/${resumeId}/retry`, {});
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to retry resume processing');
    }
    return res.json();
  }
}


