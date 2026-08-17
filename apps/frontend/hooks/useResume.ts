'use client';

import { useState, useEffect, useCallback } from 'react';
import { CandidateResume, ResumeAnalysis, ResumeHistory, Resume } from '@/types/resume';
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
  const [resume, setResume] = useState<(CandidateResume & Resume) | null>(null);
  const [analysis, setAnalysis] = useState<ResumeAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Upload module states
  const [history, setHistory] = useState<ResumeHistory[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploaded, setIsUploaded] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<any>(null);

  // Preview and Download states
  const [previewBlobUrl, setPreviewBlobUrl] = useState<string | null>(null);
  const [previewLoading, setPreviewLoading] = useState(false);
  const [previewError, setPreviewError] = useState<string | null>(null);

  const fetchResumeData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await CandidateResumeService.getResume();

      // Map profiles database records to parse schema with IDs
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
        type: (s.name.toLowerCase() === 'react' || s.name.toLowerCase() === 'next.js' || s.name.toLowerCase() === 'typescript')
          ? ('framework' as const)
          : ('technical' as const),
      }));

      const userStored = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_user') : null;
      const user = userStored ? JSON.parse(userStored) : null;
 
      let profileData = null;
      try {
        profileData = await CandidateProfileService.getProfile();
      } catch (e) {
        console.error("Failed to load profile details in useResume:", e);
      }

      const merged: CandidateResume & Resume = {
        ...data,
        lastUpdated: data.lastUpdated || 'N/A',
        profileCompletion: data.profileCompletion || 85,
        resumeStatus: data.resumeStatus || 'Active',
        summary: data.summary || '',
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

  const fetchHistory = useCallback(async () => {
    setError(null);
    try {
      const data = await CandidateResumeService.getResumes(1, 20);
      const items = data.items || [];
      const mapped: ResumeHistory[] = items.map((item: any) => {
        const sizeKb = (item.file_size_bytes || 0) / 1024;
        const sizeStr = sizeKb > 1024 ? `${(sizeKb / 1024).toFixed(1)} MB` : `${sizeKb.toFixed(1)} KB`;
        
        let statusStr: 'Parsed' | 'Processing' | 'Failed' | 'Analyzed' = 'Parsed';
        if (item.status === 'processed') {
          statusStr = 'Parsed';
        } else if (item.status === 'failed') {
          statusStr = 'Failed';
        } else {
          statusStr = 'Processing';
        }

        return {
          id: item.id,
          name: item.original_filename,
          size: sizeStr,
          date: item.uploaded_at 
            ? new Date(item.uploaded_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
            : 'N/A',
          status: statusStr,
          score: item.atsScore || 87,
        };
      });
      setHistory(mapped);
    } catch (err: any) {
      console.error('Failed to retrieve upload history:', err);
      // Fallback for DEV mode only if backend request crashed
      if (!RESUME_BACKEND_READY) {
        const userStored = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_user') : null;
        const user = userStored ? JSON.parse(userStored) : null;
        const namePrefix = user?.name ? user.name.replace(/\s+/g, '_') : 'Alex_Johnson';
        setHistory([
          { id: '1', name: `${namePrefix}_Resume_2026.pdf`, size: '1.2 MB', date: 'Jul 10, 2025', status: 'Parsed', score: 87 }
        ]);
      }
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

  const uploadResumeFile = useCallback(async (file: File) => {
    setIsUploading(true);
    setUploadProgress(10);
    setError(null);
    try {
      setUploadProgress(40);
      await CandidateResumeService.uploadResume(file);
      setUploadProgress(80);
      
      // Refetch history and active resume to sync dashboard with uploaded resume state
      await fetchHistory();
      await fetchResumeData();
      
      setUploadProgress(100);
      setIsUploaded(true);
      setUploadedFile({ name: file.name, size: `${(file.size / (1024 * 1024)).toFixed(1)} MB` });
    } catch (err: any) {
      setError(err?.message || 'Failed to upload resume file.');
    } finally {
      setIsUploading(false);
    }
  }, [fetchHistory, fetchResumeData]);

  const deleteHistoryItem = useCallback((id: string) => {
    setHistory((prev) => prev.filter((item) => item.id !== id));
  }, []);

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
    resume,
    analysis,
    loading,
    error,
    history,
    isUploading,
    uploadProgress,
    isUploaded,
    uploadedFile,
    previewBlobUrl,
    previewLoading,
    previewError,
    fetchResume: fetchResumeData,
    fetchAnalysis: fetchAnalysisData,
    fetchHistory,
    uploadResumeFile,
    deleteHistoryItem,
    previewResumeFile,
    downloadResumeFile,
    clearPreview,
    refetch: fetchResumeData,
  };
}
