'use client';

import { useState, useEffect, useCallback } from 'react';
import {
  BackendResume,
  PaginatedResumeResponse,
  CandidateResume,
  ResumeAnalysis,
  ResumeHistory,
  Resume,
} from '@/types/resume';
import { CandidateResumeService } from '@/services/resume.service';
import { CandidateProfileService } from '@/services/profile.service';
import { MOCK_RESUME_ANALYSIS } from '@/mock/ResumeAnalysis';
import { MOCK_EXPERIENCE } from '@/mock/experience';
import { MOCK_EDUCATION } from '@/mock/education';
import { MOCK_PROJECTS } from '@/mock/projects';
import { MOCK_PORTFOLIO } from '@/mock/portfolio';
import { MOCK_SKILLS } from '@/mock/skills';
import { mockDelay } from '@/lib/mockDelay';
import { RESUME_BACKEND_READY } from '@/lib/config';

export function useResume() {
  // Backend entities
  const [resumes, setResumes] = useState<BackendResume[]>([]);
  const [currentResume, setCurrentResume] = useState<BackendResume | null>(null);
  const [pagination, setPagination] = useState({
    page: 1,
    pageSize: 10,
    total: 0,
    totalPages: 0,
    hasNext: false,
    hasPrevious: false,
  });
  const [sortBy, setSortBy] = useState<string>('uploaded_at');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  // Legacy merged resume object for ATS / Viewer tabs
  const [resume, setResume] = useState<(CandidateResume & Resume) | null>(null);
  const [analysis, setAnalysis] = useState<ResumeAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Upload module states
  const [history, setHistory] = useState<ResumeHistory[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploaded, setIsUploaded] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<{ name: string; size: string } | null>(null);

  // Granular action spinners: e.g. { 'uuid-123': 'delete' }
  const [actionLoading, setActionLoading] = useState<{ [id: string]: string }>({});

  // Preview and Download states
  const [previewBlobUrl, setPreviewBlobUrl] = useState<string | null>(null);
  const [previewLoading, setPreviewLoading] = useState(false);
  const [previewError, setPreviewError] = useState<string | null>(null);

  /**
   * Fetch all resumes with current pagination and sorting parameters.
   */
  const fetchResumesList = useCallback(
    async (page = pagination.page, pageSize = pagination.pageSize, field = sortBy, order = sortOrder) => {
      try {
        const data: PaginatedResumeResponse = await CandidateResumeService.getResumes(page, pageSize, field, order);
        const items = data.items || [];
        setResumes(items);
        setPagination({
          page: data.page,
          pageSize: data.page_size,
          total: data.total,
          totalPages: data.total_pages,
          hasNext: data.has_next,
          hasPrevious: data.has_previous,
        });

        // Also map to legacy ResumeHistory for backward compatibility
        const mappedHistory: ResumeHistory[] = items.map((item) => {
          const sizeKb = (item.file_size_bytes || 0) / 1024;
          const sizeStr = sizeKb > 1024 ? `${(sizeKb / 1024).toFixed(1)} MB` : `${sizeKb.toFixed(1)} KB`;
          let statusStr: 'Parsed' | 'Processing' | 'Failed' | 'Analyzed' = 'Parsed';
          if (item.status === 'processed') statusStr = 'Parsed';
          else if (item.status === 'failed') statusStr = 'Failed';
          else statusStr = 'Processing';

          return {
            id: item.id,
            name: item.original_filename,
            size: sizeStr,
            date: item.uploaded_at
              ? new Date(item.uploaded_at).toLocaleDateString('en-US', {
                  month: 'short',
                  day: 'numeric',
                  year: 'numeric',
                })
              : 'N/A',
            status: statusStr,
            score: 87,
          };
        });
        setHistory(mappedHistory);

        // Find active/current
        const active = items.find((r) => r.is_current) || items[0] || null;
        setCurrentResume(active);
        return data;
      } catch (err: any) {
        console.error('Failed to list resumes:', err);
        setError(err?.message || 'Failed to list resumes');
        return null;
      }
    },
    [pagination.page, pagination.pageSize, sortBy, sortOrder]
  );

  /**
   * Fetch current active resume from dedicated endpoint.
   */
  const fetchCurrentResume = useCallback(async () => {
    try {
      const active = await CandidateResumeService.getCurrentResume();
      setCurrentResume(active);
      return active;
    } catch (err: any) {
      console.error('Failed to get current resume:', err);
      return null;
    }
  }, []);

  /**
   * Fetch legacy resume data for profile analysis tabs.
   */
  const fetchResumeData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [legacyData, resumesData] = await Promise.all([
        CandidateResumeService.getResume(),
        CandidateResumeService.getResumes(1, 10, 'uploaded_at', 'desc'),
      ]);

      const items = resumesData.items || [];
      setResumes(items);
      setPagination({
        page: resumesData.page,
        pageSize: resumesData.page_size,
        total: resumesData.total,
        totalPages: resumesData.total_pages,
        hasNext: resumesData.has_next,
        hasPrevious: resumesData.has_previous,
      });

      const active = items.find((r) => r.is_current) || items[0] || null;
      setCurrentResume(active);

      const mappedExperience = MOCK_EXPERIENCE.map((e) => ({
        id: e.id,
        company: e.companyName,
        role: e.jobTitle,
        duration: `${e.startDate} - ${e.endDate || 'Present'}`,
        description: e.description,
        technologies: e.technologiesUsed,
      }));

      const mappedProjects = MOCK_PROJECTS.map((p) => ({
        id: p.id,
        name: p.projectName,
        description: p.description,
        techStack: p.technologies,
        github: p.githubUrl,
        liveLink: p.liveUrl,
        duration: p.duration,
      }));

      const mappedEducation = MOCK_EDUCATION.map((edu) => ({
        id: edu.id,
        university: edu.institutionName,
        degree: `${edu.degree} in ${edu.branch}`,
        gpa: edu.cgpaOrPercentage.replace(' GPA', ''),
        year: edu.endYear,
        location: 'Stanford, CA',
      }));

      const mappedCertificates = MOCK_PORTFOLIO.filter((p) => p.type === 'Certificate').map((c) => ({
        id: c.id,
        certificate: c.title,
        issuer: 'Frontend Masters',
        issueDate: c.date,
      }));

      const mappedSkills = MOCK_SKILLS.map((s) => ({
        name: s.name,
        type:
          s.name.toLowerCase() === 'react' ||
          s.name.toLowerCase() === 'next.js' ||
          s.name.toLowerCase() === 'typescript'
            ? ('framework' as const)
            : ('technical' as const),
      }));

      const userStored = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_user') : null;
      const user = userStored ? JSON.parse(userStored) : null;

      let profileData = null;
      try {
        profileData = await CandidateProfileService.getProfile();
      } catch (e) {
        console.error('Failed to load profile details in useResume:', e);
      }

      const merged: CandidateResume & Resume = {
        ...legacyData,
        lastUpdated: legacyData.lastUpdated || 'N/A',
        profileCompletion: legacyData.profileCompletion || 85,
        resumeStatus: legacyData.resumeStatus || 'Active',
        summary: legacyData.summary || '',
        candidateName: user?.name || '',
        email: user?.email || '',
        phone: profileData?.phone || '',
        location: profileData?.location || '',
        website: profileData?.portfolioUrl || '',
        github: profileData?.githubUrl || '',
        linkedin: profileData?.linkedinUrl || '',
        experience: mappedExperience,
        projects: mappedProjects,
        education: mappedEducation,
        certificates: mappedCertificates,
        skills: mappedSkills,
        languages: ['English', 'Spanish'],
        achievements: ['Awarded first place at Vercel framework hackathon 2023.'],
      };

      setResume(merged);
      return merged;
    } catch (err: any) {
      setError(err?.message || 'Failed to retrieve resume details');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchAnalysisData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      await mockDelay(300);
      setAnalysis(MOCK_RESUME_ANALYSIS);
      return MOCK_RESUME_ANALYSIS;
    } catch (err: any) {
      setError(err?.message || 'Failed to retrieve resume audit analysis');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const previewResumeFile = useCallback(async (id: string): Promise<string | null> => {
    setPreviewLoading(true);
    setPreviewError(null);
    try {
      const blob = await CandidateResumeService.previewResume(id);
      const url = URL.createObjectURL(blob);
      setPreviewBlobUrl(url);
      return url;
    } catch (err: any) {
      setPreviewError(err?.message || 'Failed to open file preview.');
      return null;
    } finally {
      setPreviewLoading(false);
    }
  }, []);

  const downloadResumeFile = useCallback(async (id: string, filename: string): Promise<void> => {
    try {
      const blob = await CandidateResumeService.downloadResume(id);
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.parentNode?.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (err: any) {
      alert(err?.message || 'Failed to download file.');
    }
  }, []);

  const clearPreview = useCallback(() => {
    if (previewBlobUrl) {
      URL.revokeObjectURL(previewBlobUrl);
      setPreviewBlobUrl(null);
    }
    setPreviewError(null);
  }, [previewBlobUrl]);

  /**
   * Upload a new resume file, refreshing the active state and resume list.
   */
  const uploadResumeFile = useCallback(
    async (file: File): Promise<BackendResume | null> => {
      setIsUploading(true);
      setUploadProgress(15);
      setError(null);
      try {
        setUploadProgress(45);
        const uploaded = await CandidateResumeService.uploadResume(file);
        setUploadProgress(85);

        // Instant refresh
        await fetchResumesList(1, pagination.pageSize);
        await fetchCurrentResume();

        setUploadProgress(100);
        setIsUploaded(true);
        setUploadedFile({ name: file.name, size: `${(file.size / (1024 * 1024)).toFixed(1)} MB` });
        return uploaded;
      } catch (err: any) {
        const msg = err?.message || 'Failed to upload resume file.';
        setError(msg);
        throw new Error(msg);
      } finally {
        setIsUploading(false);
      }
    },
    [fetchResumesList, fetchCurrentResume, pagination.pageSize]
  );

  /**
   * Delete a resume with granular loading indicator.
   */
  const deleteResume = useCallback(
    async (id: string): Promise<boolean> => {
      setActionLoading((prev) => ({ ...prev, [id]: 'delete' }));
      setError(null);
      try {
        await CandidateResumeService.deleteResume(id);
        await fetchResumesList();
        await fetchCurrentResume();
        return true;
      } catch (err: any) {
        const msg = err?.message || 'Failed to delete resume.';
        setError(msg);
        throw new Error(msg);
      } finally {
        setActionLoading((prev) => {
          const next = { ...prev };
          delete next[id];
          return next;
        });
      }
    },
    [fetchResumesList, fetchCurrentResume]
  );

  /**
   * Restore an older version as the active resume.
   */
  const restoreVersion = useCallback(
    async (id: string): Promise<boolean> => {
      setActionLoading((prev) => ({ ...prev, [id]: 'restore' }));
      setError(null);
      try {
        await CandidateResumeService.restoreResumeVersion(id);
        await fetchResumesList();
        await fetchCurrentResume();
        return true;
      } catch (err: any) {
        const msg = err?.message || 'Failed to restore resume version.';
        setError(msg);
        throw new Error(msg);
      } finally {
        setActionLoading((prev) => {
          const next = { ...prev };
          delete next[id];
          return next;
        });
      }
    },
    [fetchResumesList, fetchCurrentResume]
  );

  /**
   * Trigger processing on an uploaded resume.
   */
  const processResume = useCallback(
    async (id: string): Promise<boolean> => {
      setActionLoading((prev) => ({ ...prev, [id]: 'process' }));
      setError(null);
      try {
        await CandidateResumeService.processResume(id);
        await fetchResumesList();
        await fetchCurrentResume();
        return true;
      } catch (err: any) {
        const msg = err?.message || 'Failed to process resume.';
        setError(msg);
        throw new Error(msg);
      } finally {
        setActionLoading((prev) => {
          const next = { ...prev };
          delete next[id];
          return next;
        });
      }
    },
    [fetchResumesList, fetchCurrentResume]
  );

  /**
   * Retry failed resume processing.
   */
  const retryProcessing = useCallback(
    async (id: string): Promise<boolean> => {
      setActionLoading((prev) => ({ ...prev, [id]: 'retry' }));
      setError(null);
      try {
        await CandidateResumeService.retryResumeProcessing(id);
        await fetchResumesList();
        await fetchCurrentResume();
        return true;
      } catch (err: any) {
        const msg = err?.message || 'Failed to retry resume processing.';
        setError(msg);
        throw new Error(msg);
      } finally {
        setActionLoading((prev) => {
          const next = { ...prev };
          delete next[id];
          return next;
        });
      }
    },
    [fetchResumesList, fetchCurrentResume]
  );

  const setPage = useCallback(
    (page: number) => {
      fetchResumesList(page, pagination.pageSize, sortBy, sortOrder);
    },
    [fetchResumesList, pagination.pageSize, sortBy, sortOrder]
  );

  const setSorting = useCallback(
    (field: string, order: 'asc' | 'desc') => {
      setSortBy(field);
      setSortOrder(order);
      fetchResumesList(1, pagination.pageSize, field, order);
    },
    [fetchResumesList, pagination.pageSize]
  );

  const refreshAll = useCallback(async () => {
    setIsRefreshing(true);
    await Promise.all([fetchResumesList(), fetchCurrentResume()]);
    setIsRefreshing(false);
  }, [fetchResumesList, fetchCurrentResume]);

  useEffect(() => {
    fetchResumeData();
  }, [fetchResumeData]);

  // Clean up blob URLs to prevent memory leaks
  useEffect(() => {
    return () => {
      if (previewBlobUrl) {
        URL.revokeObjectURL(previewBlobUrl);
      }
    };
  }, [previewBlobUrl]);

  return {
    resumes,
    currentResume,
    pagination,
    sortBy,
    sortOrder,
    resume,
    analysis,
    loading,
    isRefreshing,
    error,
    history,
    isUploading,
    uploadProgress,
    isUploaded,
    uploadedFile,
    actionLoading,
    previewBlobUrl,
    previewLoading,
    previewError,
    fetchResume: fetchResumeData,
    fetchResumesList,
    fetchCurrentResume,
    fetchAnalysis: fetchAnalysisData,
    fetchHistory: fetchResumesList,
    uploadResumeFile,
    deleteResume,
    restoreVersion,
    processResume,
    retryProcessing,
    setPage,
    setSorting,
    refreshAll,
    previewResumeFile,
    downloadResumeFile,
    clearPreview,
    refetch: fetchResumeData,
    deleteHistoryItem: (id: string) => deleteResume(id),
  };
}
