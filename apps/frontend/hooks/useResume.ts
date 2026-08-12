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
    const userStored = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_user') : null;
    const user = userStored ? JSON.parse(userStored) : null;
    const namePrefix = user?.name ? user.name.replace(/\s+/g, '_') : 'Alex_Johnson';
    const mockH: ResumeHistory[] = [
      { id: '1', name: `${namePrefix}_Resume_2026.pdf`, size: '1.2 MB', date: 'Jul 10, 2025', status: 'Parsed', score: 87 },
    ];
    setHistory(mockH);
  }, []);

  const uploadResumeFile = useCallback(async (file: File) => {
    setIsUploading(true);
    setUploadProgress(10);
    setError(null);
    try {
      setUploadProgress(40);
      await CandidateResumeService.uploadResume(file);
      setUploadProgress(100);
      setIsUploaded(true);
      setUploadedFile({ name: file.name, size: `${(file.size / (1024 * 1024)).toFixed(1)} MB` });

      const newItem: ResumeHistory = {
        id: String(Date.now()),
        name: file.name,
        size: `${(file.size / (1024 * 1024)).toFixed(1)} MB`,
        date: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
        status: 'Parsed',
        score: 87,
      };
      setHistory((prev) => [newItem, ...prev]);
      
      // Refetch details to sync dashboard with uploaded resume state
      await fetchResumeData();
    } catch (err: any) {
      setError(err?.message || 'Failed to upload resume file.');
    } finally {
      setIsUploading(false);
    }
  }, [fetchResumeData]);

  const deleteHistoryItem = useCallback((id: string) => {
    setHistory((prev) => prev.filter((item) => item.id !== id));
  }, []);

  useEffect(() => {
    fetchResumeData();
  }, [fetchResumeData]);

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
    fetchResume: fetchResumeData,
    fetchAnalysis: fetchAnalysisData,
    fetchHistory,
    uploadResumeFile,
    deleteHistoryItem,
    refetch: fetchResumeData,
  };
}
