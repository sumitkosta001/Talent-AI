'use client';

import { useState, useEffect, useCallback } from 'react';
import { CandidateResume, ResumeAnalysis, ResumeHistory, Resume } from '@/types/resume';
import { CandidateResumeService } from '@/services/resume.service';
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

      const merged: CandidateResume & Resume = {
        ...data,
        lastUpdated: 'Jul 10, 2025',
        profileCompletion: 85,
        resumeStatus: 'Active',
        summary: 'Senior Software Engineer with 6+ years of experience specializing in React, Next.js, and client developer integrations.',
        candidateName: 'Alex Johnson',
        email: 'alex.johnson@gmail.com',
        phone: '+1 (555) 018-7243',
        location: 'San Francisco, CA',
        website: 'https://alexjohnson.dev',
        github: 'https://github.com/alexjohnson',
        linkedin: 'https://linkedin.com/in/alex-johnson',
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
    const mockH: ResumeHistory[] = [
      { id: '1', name: 'Alex_Johnson_Resume_2026.pdf', size: '1.2 MB', date: 'Jul 10, 2025', status: 'Parsed', score: 87 },
    ];
    setHistory(mockH);
  }, []);

  const uploadResumeFile = useCallback(async (file: File) => {
    setIsUploading(true);
    setUploadProgress(10);
    await mockDelay(100);
    setUploadProgress(50);
    await mockDelay(100);
    setUploadProgress(100);
    setIsUploading(false);
    setIsUploaded(true);
    setUploadedFile({ name: file.name });

    const newItem: ResumeHistory = {
      id: String(Date.now()),
      name: file.name,
      size: `${(file.size / (1024 * 1024)).toFixed(1)} MB`,
      date: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
      status: 'Parsed',
      score: 80,
    };
    setHistory((prev) => [newItem, ...prev]);
  }, []);

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
