import { RESUME_BACKEND_READY } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import {
  BackendResume,
  PaginatedResumeResponse,
  ResumeProcessingResponse,
  ResumeRestoreResponse,
  CandidateResume,
} from '@/types/resume';
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

  /**
   * Fetch legacy merged CandidateResume representation for profile & preview compatibility.
   */
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
    let currentResume: BackendResume | null = null;
    if (resumesRes.ok) {
      const listData = await resumesRes.json();
      const items: BackendResume[] = listData.items || [];
      currentResume = items.find((r) => r.is_current) || items[0] || null;
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
      atsScore: 87, // UI default ATS parsing compatibility score
      downloadUrl: `/api/v1/candidates/me/resumes/${currentResume.id}/download`,
      lastUpdated: currentResume.uploaded_at
        ? new Date(currentResume.uploaded_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
        : 'N/A',
      profileCompletion: profileData.profile_completion_percentage || 0,
      resumeStatus: currentResume.status === 'processed' ? 'Active' : (currentResume.status === 'failed' ? 'Failed' : 'Active'),
      summary: profileData.bio || '',
    };
  }

  /**
   * List candidate resumes with pagination and sorting.
   */
  static async getResumes(
    page: number = 1,
    pageSize: number = 10,
    sortBy: string = 'uploaded_at',
    sortOrder: 'asc' | 'desc' = 'desc'
  ): Promise<PaginatedResumeResponse> {
    if (!RESUME_BACKEND_READY) {
      await mockDelay(200);
      const mock = this.getLocalResume();
      return {
        items: [
          {
            id: mock.id || '1',
            candidate_profile_id: 'default',
            original_filename: mock.name,
            mime_type: 'application/pdf',
            file_extension: '.pdf',
            file_size_bytes: 1240000,
            status: 'processed',
            version: 1,
            is_current: true,
            uploaded_at: new Date().toISOString(),
            created_at: new Date().toISOString(),
          },
        ],
        total: 1,
        page: 1,
        page_size: pageSize,
        total_pages: 1,
        has_next: false,
        has_previous: false,
      };
    }
    const res = await apiClient.get(
      `/api/v1/candidates/me/resumes?page=${page}&page_size=${pageSize}&sort_by=${sortBy}&sort_order=${sortOrder}`
    );
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to list resumes');
    }
    return res.json();
  }

  /**
   * Retrieve the candidate's active/current resume.
   */
  static async getCurrentResume(): Promise<BackendResume | null> {
    if (!RESUME_BACKEND_READY) {
      await mockDelay(200);
      const mock = this.getLocalResume();
      return {
        id: mock.id || '1',
        candidate_profile_id: 'default',
        original_filename: mock.name,
        mime_type: 'application/pdf',
        file_extension: '.pdf',
        file_size_bytes: 1240000,
        status: 'processed',
        version: 1,
        is_current: true,
        uploaded_at: new Date().toISOString(),
        created_at: new Date().toISOString(),
      };
    }
    const res = await apiClient.get('/api/v1/candidates/me/resumes/current');
    if (!res.ok) {
      if (res.status === 404) {
        return null;
      }
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to fetch current resume');
    }
    return res.json();
  }

  /**
   * Upload a new PDF/DOCX resume.
   */
  static async uploadResume(file: File): Promise<BackendResume> {
    if (!RESUME_BACKEND_READY) {
      await mockDelay(300);
      return {
        id: 'mock-id',
        candidate_profile_id: 'default',
        original_filename: file.name,
        mime_type: file.type || 'application/pdf',
        file_extension: file.name.endsWith('.docx') ? '.docx' : '.pdf',
        file_size_bytes: file.size,
        status: 'uploaded',
        version: 1,
        is_current: true,
        uploaded_at: new Date().toISOString(),
        created_at: new Date().toISOString(),
      };
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

  /**
   * Retrieve secure preview blob for a resume.
   */
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

  /**
   * Retrieve secure download blob for a resume.
   */
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

  /**
   * Delete a candidate resume.
   */
  static async deleteResume(resumeId: string): Promise<{ success: boolean; message: string }> {
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

  /**
   * Restore an older resume version to become current.
   */
  static async restoreResumeVersion(resumeId: string): Promise<ResumeRestoreResponse> {
    if (!RESUME_BACKEND_READY) {
      await mockDelay(200);
      return {
        success: true,
        message: 'Version restored successfully',
        resume: {
          id: resumeId,
          candidate_profile_id: 'default',
          original_filename: 'restored.pdf',
          mime_type: 'application/pdf',
          file_extension: '.pdf',
          file_size_bytes: 1200000,
          status: 'processed',
          version: 1,
          is_current: true,
          uploaded_at: new Date().toISOString(),
          created_at: new Date().toISOString(),
        },
      };
    }
    const res = await apiClient.post(`/api/v1/candidates/me/resumes/${resumeId}/restore`, {});
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to restore resume version');
    }
    return res.json();
  }

  /**
   * Trigger processing on an uploaded resume.
   */
  static async processResume(resumeId: string): Promise<ResumeProcessingResponse> {
    if (!RESUME_BACKEND_READY) {
      await mockDelay(300);
      return {
        success: true,
        message: 'Resume processed successfully',
        resume: {
          id: resumeId,
          candidate_profile_id: 'default',
          original_filename: 'resume.pdf',
          mime_type: 'application/pdf',
          file_extension: '.pdf',
          file_size_bytes: 1200000,
          status: 'processed',
          version: 1,
          is_current: true,
          uploaded_at: new Date().toISOString(),
          created_at: new Date().toISOString(),
        },
      };
    }
    const res = await apiClient.post(`/api/v1/candidates/me/resumes/${resumeId}/process`, {});
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to process resume');
    }
    return res.json();
  }

  /**
   * Retrieve upload history and processing lifecycle metadata.
   */
  static async getResumeHistory(
    page: number = 1,
    pageSize: number = 10,
    sortBy: string = 'uploaded_at',
    sortOrder: 'asc' | 'desc' = 'desc'
  ): Promise<PaginatedResumeResponse> {
    if (!RESUME_BACKEND_READY) {
      await mockDelay(200);
      return this.getResumes(page, pageSize, sortBy, sortOrder);
    }
    const res = await apiClient.get(
      `/api/v1/candidates/me/resumes/history?page=${page}&page_size=${pageSize}&sort_by=${sortBy}&sort_order=${sortOrder}`
    );
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to fetch resume history');
    }
    return res.json();
  }

  /**
   * Retry processing for a failed resume.
   */
  static async retryResumeProcessing(resumeId: string): Promise<ResumeProcessingResponse> {
    if (!RESUME_BACKEND_READY) {
      await mockDelay(300);
      return {
        success: true,
        message: 'Processing retried successfully',
        resume: {
          id: resumeId,
          candidate_profile_id: 'default',
          original_filename: 'resume.pdf',
          mime_type: 'application/pdf',
          file_extension: '.pdf',
          file_size_bytes: 1200000,
          status: 'processed',
          version: 1,
          is_current: true,
          uploaded_at: new Date().toISOString(),
          created_at: new Date().toISOString(),
        },
      };
    }
    const res = await apiClient.post(`/api/v1/candidates/me/resumes/${resumeId}/retry`, {});
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to retry resume processing');
    }
    return res.json();
  }
}
