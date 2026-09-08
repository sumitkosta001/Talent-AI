'use client';

import React from 'react';
import Link from 'next/link';
import {
  FileText,
  ChevronRight,
  RefreshCw,
  AlertTriangle,
  Briefcase,
  GraduationCap,
  FolderGit2,
  BrainCircuit,
  ExternalLink,
  GitBranch,
  Mail,
  Phone,
  MapPin,
  CheckCircle2,
  Code2,
} from 'lucide-react';
import { useResume } from '@/hooks/useResume';
import { useStructuredResume } from '@/hooks/useStructuredResume';
import { useClassification } from '@/hooks/useClassification';
import { ResumeClassificationCard } from '@/components/resume/ResumeClassificationCard';

function formatConfidence(val?: number): string {
  if (val === undefined || val === null) return 'N/A';
  const pct = val <= 1 ? Math.round(val * 100) : Math.round(val);
  return `${pct}%`;
}

function formatEnumLabel(val?: string | null): string {
  if (!val) return 'N/A';
  return val
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
}

export default function ResumeAnalysisPage() {
  const { currentResume, loading: resumeLoading, retryProcessing } = useResume();
  const resumeId = currentResume?.id || null;

  const {
    data: structured,
    loading: structuredLoading,
    error: structuredError,
    refetch: refetchStructured,
  } = useStructuredResume(resumeId);

  const {
    data: classification,
    loading: classificationLoading,
    error: classificationError,
    refetch: refetchClassification,
  } = useClassification(resumeId);

  const loading = resumeLoading || (resumeId ? (structuredLoading && classificationLoading) : false);

  // Unprocessed or missing resume guards
  if (resumeLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] gap-3">
        <RefreshCw className="animate-spin text-[#2563EB]" size={36} />
        <p className="text-sm font-semibold text-[#64748B]">Loading resume information...</p>
      </div>
    );
  }

  if (!currentResume) {
    return (
      <div className="p-6 space-y-6 max-w-4xl mx-auto">
        <div className="bg-white border border-[#E2E8F0] rounded-2xl p-8 text-center space-y-4 shadow-sm">
          <div className="w-12 h-12 bg-blue-50 text-[#2563EB] rounded-xl flex items-center justify-center mx-auto">
            <FileText size={24} />
          </div>
          <div>
            <h3 className="font-bold text-[#0F172A] text-lg">No Active Resume Found</h3>
            <p className="text-sm text-[#64748B] mt-1">
              Upload a resume document first to generate AI structured analysis and domain classification.
            </p>
          </div>
          <Link
            href="/candidate/resume"
            className="inline-flex items-center justify-center gap-2 bg-[#2563EB] text-white px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-[#1D4ED8] transition-colors cursor-pointer"
          >
            Upload Resume
          </Link>
        </div>
      </div>
    );
  }

  if (currentResume.status === 'uploaded' || currentResume.status === 'processing') {
    return (
      <div className="p-6 space-y-6 max-w-4xl mx-auto">
        <div className="bg-amber-50 border border-amber-200 rounded-2xl p-8 text-center space-y-4">
          <div className="w-12 h-12 bg-amber-100 text-amber-600 rounded-xl flex items-center justify-center mx-auto">
            <RefreshCw className="animate-spin" size={24} />
          </div>
          <div>
            <h3 className="font-bold text-[#0F172A] text-lg">Resume Processing in Progress</h3>
            <p className="text-sm text-[#64748B] mt-1">
              Your resume <span className="font-semibold">{currentResume.original_filename}</span> is currently being parsed into structured JSON format. Structured analysis will appear automatically once processing completes.
            </p>
          </div>
          <Link
            href="/candidate/resume"
            className="inline-flex items-center justify-center gap-2 border border-amber-300 text-amber-800 px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-amber-100 transition-colors cursor-pointer"
          >
            View Processing Status
          </Link>
        </div>
      </div>
    );
  }

  if (currentResume.status === 'failed') {
    return (
      <div className="p-6 space-y-6 max-w-4xl mx-auto">
        <div className="bg-red-50 border border-red-200 rounded-2xl p-8 text-center space-y-4">
          <div className="w-12 h-12 bg-red-100 text-red-600 rounded-xl flex items-center justify-center mx-auto">
            <AlertTriangle size={24} />
          </div>
          <div>
            <h3 className="font-bold text-[#0F172A] text-lg">Resume Processing Failed</h3>
            <p className="text-sm text-[#64748B] mt-1">
              Processing failed for <span className="font-semibold">{currentResume.original_filename}</span>: {currentResume.failure_reason || 'Document parsing encountered an error.'}
            </p>
          </div>
          <div className="flex justify-center gap-3">
            <button
              onClick={() => retryProcessing(currentResume.id)}
              className="inline-flex items-center justify-center gap-2 bg-[#2563EB] text-white px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-[#1D4ED8] transition-colors cursor-pointer"
            >
              Retry Processing
            </button>
            <Link
              href="/candidate/resume"
              className="inline-flex items-center justify-center gap-2 border border-[#E2E8F0] text-[#0F172A] px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-[#F8FAFC] transition-colors cursor-pointer"
            >
              Manage Resumes
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // Error handling for ML endpoints
  const hasError = structuredError || classificationError;
  const isOverallLoading = structuredLoading && classificationLoading;

  if (hasError && !structured && !classification) {
    return (
      <div className="p-6 space-y-6 max-w-4xl mx-auto">
        <div className="bg-red-50 border border-red-200 rounded-2xl p-8 text-center space-y-4">
          <div className="w-12 h-12 bg-red-100 text-red-600 rounded-xl flex items-center justify-center mx-auto">
            <AlertTriangle size={24} />
          </div>
          <div>
            <h3 className="font-bold text-[#0F172A] text-lg">Failed to Load Structured Analysis</h3>
            <p className="text-sm text-[#64748B] mt-1">
              {structuredError || classificationError || 'Unable to retrieve structured resume details from server.'}
            </p>
          </div>
          <button
            onClick={() => {
              refetchStructured();
              refetchClassification();
            }}
            className="inline-flex items-center justify-center gap-2 bg-[#2563EB] text-white px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-[#1D4ED8] transition-colors cursor-pointer"
          >
            <RefreshCw size={16} />
            Retry Analysis Request
          </button>
        </div>
      </div>
    );
  }

  const skillsList = structured?.skills?.skills || [];
  const skillCategories = structured?.skills?.categories || {};
  const educationList = structured?.education?.education_records || [];
  const experienceList = structured?.experience?.experiences || [];
  const projectList = structured?.projects?.projects || [];

  return (
    <div className="p-4 sm:p-6 space-y-6 max-w-6xl mx-auto">
      {/* Header section */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl sm:text-2xl font-bold text-[#0F172A]">AI Resume Analysis & Classification</h1>
            <span className="bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-semibold px-2.5 py-0.5 rounded-full flex items-center gap-1">
              <CheckCircle2 size={12} />
              PROCESSED
            </span>
          </div>
          <p className="text-xs sm:text-sm text-[#64748B] mt-1">
            <span className="font-semibold text-[#0F172A]">{currentResume.original_filename}</span> (v{currentResume.version}.0) · Audited via Day 28 Structured Pipeline
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <Link
            href="/candidate/ats"
            className="inline-flex items-center gap-2 border border-[#E2E8F0] text-[#0F172A] px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold hover:bg-[#F8FAFC] transition-colors cursor-pointer"
          >
            ATS Score
            <ChevronRight size={14} />
          </Link>
          <a
            href={`/api/v1/candidates/me/resumes/${currentResume.id}/download`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 bg-[#2563EB] text-white px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold hover:bg-[#1D4ED8] transition-colors cursor-pointer"
          >
            Download Document
          </a>
        </div>
      </div>

      {/* Loading state indicator */}
      {isOverallLoading && (
        <div className="flex items-center justify-center p-8 bg-blue-50/50 rounded-2xl border border-blue-100 gap-3 text-[#2563EB]">
          <RefreshCw className="animate-spin" size={20} />
          <span className="text-sm font-semibold">Retrieving structured resume data & classification...</span>
        </div>
      )}

      {/* Day 29 Classification Section */}
      <ResumeClassificationCard
        classification={classification}
        loading={classificationLoading}
        error={classificationError}
        onRetry={refetchClassification}
      />

      {/* Candidate Basic Contact Info & Summary */}
      {structured && (
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[#E2E8F0] pb-4">
            <div>
              <h2 className="font-bold text-[#0F172A] text-lg sm:text-xl">
                {structured.full_name || 'Candidate Profile'}
              </h2>
              <div className="flex flex-wrap gap-4 text-xs sm:text-sm text-[#64748B] mt-1">
                {structured.email && (
                  <span className="flex items-center gap-1.5">
                    <Mail size={14} className="text-[#2563EB]" />
                    {structured.email}
                  </span>
                )}
                {structured.phone && (
                  <span className="flex items-center gap-1.5">
                    <Phone size={14} className="text-[#2563EB]" />
                    {structured.phone}
                  </span>
                )}
                {structured.location && (
                  <span className="flex items-center gap-1.5">
                    <MapPin size={14} className="text-[#2563EB]" />
                    {structured.location}
                  </span>
                )}
              </div>
            </div>
            <div className="flex gap-3 text-xs">
              {structured.github && (
                <a
                  href={structured.github.startsWith('http') ? structured.github : `https://${structured.github}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 text-[#64748B] hover:text-[#0F172A] border border-[#E2E8F0] px-2.5 py-1 rounded-lg"
                >
                  <GitBranch size={14} /> GitHub
                </a>
              )}
              {structured.linkedin && (
                <a
                  href={structured.linkedin.startsWith('http') ? structured.linkedin : `https://${structured.linkedin}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 text-[#2563EB] hover:underline border border-[#E2E8F0] px-2.5 py-1 rounded-lg"
                >
                  LinkedIn
                </a>
              )}
            </div>
          </div>

          {structured.summary && (
            <div>
              <h3 className="text-xs font-semibold uppercase tracking-wider text-[#94A3B8] mb-1">Executive Summary</h3>
              <p className="text-xs sm:text-sm text-[#64748B] leading-relaxed bg-[#F8FAFC] rounded-xl p-3.5 border border-[#E2E8F0]/80">
                {structured.summary}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Extracted Skills Section */}
      {structured && (
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Code2 size={20} className="text-[#2563EB]" />
              <h2 className="font-bold text-[#0F172A] text-lg">Extracted Skills</h2>
            </div>
            <span className="text-xs font-semibold bg-blue-50 text-[#2563EB] px-3 py-1 rounded-full border border-blue-100">
              {structured.skills?.total_count || skillsList.length} Unique Skills
            </span>
          </div>

          {Object.keys(skillCategories).length > 0 ? (
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 pt-2">
              {Object.entries(skillCategories).map(([cat, skills]) => (
                <div key={cat} className="bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl p-4 space-y-2">
                  <span className="text-xs font-bold text-[#0F172A] tracking-wider uppercase">{formatEnumLabel(cat)}</span>
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {skills.map((s) => (
                      <span key={s} className="text-xs bg-white border border-[#E2E8F0] text-[#0F172A] px-2.5 py-1 rounded-lg font-medium shadow-2xs">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          ) : skillsList.length > 0 ? (
            <div className="flex flex-wrap gap-2 pt-2">
              {skillsList.map((skill) => (
                <span key={skill.name} className="text-xs bg-[#F8FAFC] border border-[#E2E8F0] text-[#0F172A] px-3 py-1.5 rounded-xl font-medium">
                  {skill.name}
                  {skill.confidence && <span className="ml-1.5 text-[10px] text-[#94A3B8]">({formatConfidence(skill.confidence)})</span>}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-xs text-[#94A3B8] italic">No skills extracted from document.</p>
          )}
        </div>
      )}

      {/* Extracted Experience & Education Grid */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Work Experience */}
        {structured && (
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-[#E2E8F0] pb-3">
              <div className="flex items-center gap-2">
                <Briefcase size={20} className="text-[#2563EB]" />
                <h2 className="font-bold text-[#0F172A] text-lg">Work Experience</h2>
              </div>
              <span className="text-xs text-[#64748B] font-medium">
                {structured.experience?.total_experience_months
                  ? `${(structured.experience.total_experience_months / 12).toFixed(1)} yrs total`
                  : `${experienceList.length} roles`}
              </span>
            </div>

            {experienceList.length > 0 ? (
              <div className="space-y-4">
                {experienceList.map((exp, idx) => (
                  <div key={idx} className="bg-[#F8FAFC] rounded-xl border border-[#E2E8F0] p-4 space-y-2">
                    <div className="flex flex-wrap items-baseline justify-between gap-1">
                      <h3 className="font-bold text-[#0F172A] text-sm sm:text-base">
                        {exp.job_title || 'Position'}
                      </h3>
                      <span className="text-xs text-[#94A3B8] font-medium">
                        {exp.duration_text || `${exp.start_year || ''} - ${exp.is_current ? 'Present' : exp.end_year || ''}`}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-xs text-[#2563EB] font-semibold">
                      <span>{exp.company || 'Company'}</span>
                      {exp.employment_type && (
                        <span className="text-[10px] bg-blue-50 text-[#2563EB] border border-blue-100 px-2 py-0.5 rounded-md">
                          {formatEnumLabel(exp.employment_type)}
                        </span>
                      )}
                    </div>
                    {exp.responsibilities && exp.responsibilities.length > 0 && (
                      <ul className="text-xs text-[#64748B] space-y-1 pl-4 list-disc pt-1">
                        {exp.responsibilities.map((bullet, bIdx) => (
                          <li key={bIdx}>{bullet}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-[#94A3B8] italic p-4 text-center">No work experience records extracted.</p>
            )}
          </div>
        )}

        {/* Education Records */}
        {structured && (
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-[#E2E8F0] pb-3">
              <div className="flex items-center gap-2">
                <GraduationCap size={20} className="text-[#2563EB]" />
                <h2 className="font-bold text-[#0F172A] text-lg">Education</h2>
              </div>
              <span className="text-xs text-[#64748B] font-medium">
                {educationList.length} records
              </span>
            </div>

            {educationList.length > 0 ? (
              <div className="space-y-4">
                {educationList.map((edu, idx) => (
                  <div key={idx} className="bg-[#F8FAFC] rounded-xl border border-[#E2E8F0] p-4 space-y-2">
                    <div className="flex flex-wrap items-baseline justify-between gap-1">
                      <h3 className="font-bold text-[#0F172A] text-sm sm:text-base">
                        {edu.degree || 'Degree'}
                      </h3>
                      <span className="text-xs text-[#94A3B8] font-medium">
                        {edu.graduation_year || edu.end_year || (edu.start_year ? `${edu.start_year} - ${edu.end_year || ''}` : 'N/A')}
                      </span>
                    </div>
                    <p className="text-xs sm:text-sm text-[#2563EB] font-semibold">
                      {edu.institution || 'Institution'}
                    </p>
                    <div className="flex flex-wrap items-center justify-between gap-2 text-xs text-[#64748B] pt-1">
                      {edu.field_of_study && <span>Field: {edu.field_of_study}</span>}
                      {edu.cgpa !== undefined && edu.cgpa !== null && (
                        <span className="font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200 px-2.5 py-0.5 rounded-full">
                          CGPA: {edu.cgpa}
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-[#94A3B8] italic p-4 text-center">No education records extracted.</p>
            )}
          </div>
        )}
      </div>

      {/* Extracted Projects Section */}
      {structured && (
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-[#E2E8F0] pb-3">
            <div className="flex items-center gap-2">
              <FolderGit2 size={20} className="text-[#2563EB]" />
              <h2 className="font-bold text-[#0F172A] text-lg">Extracted Projects</h2>
            </div>
            <span className="text-xs text-[#64748B] font-medium">
              {projectList.length} Projects
            </span>
          </div>

          {projectList.length > 0 ? (
            <div className="grid sm:grid-cols-2 gap-4">
              {projectList.map((proj, idx) => (
                <div key={idx} className="bg-[#F8FAFC] rounded-xl border border-[#E2E8F0] p-5 space-y-3 flex flex-col justify-between">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between gap-2">
                      <h3 className="font-bold text-[#0F172A] text-base">{proj.name || 'Project'}</h3>
                      {proj.classification && (
                        <span className="text-[10px] bg-blue-50 text-[#2563EB] border border-blue-100 px-2.5 py-0.5 rounded-full font-semibold">
                          {formatEnumLabel(proj.classification)}
                        </span>
                      )}
                    </div>
                    {proj.description && (
                      <p className="text-xs sm:text-sm text-[#64748B] leading-relaxed">
                        {proj.description}
                      </p>
                    )}
                  </div>

                  <div className="space-y-2 pt-2 border-t border-[#E2E8F0]">
                    {proj.technologies && proj.technologies.length > 0 && (
                      <div className="flex flex-wrap gap-1.5">
                        {proj.technologies.map((tech) => (
                          <span key={tech} className="text-[10px] bg-white border border-[#E2E8F0] text-[#0F172A] px-2 py-0.5 rounded-md font-medium">
                            {tech}
                          </span>
                        ))}
                      </div>
                    )}
                    <div className="flex items-center justify-between text-xs text-[#94A3B8] pt-1">
                      <span>{proj.start_year ? `${proj.start_year}${proj.end_year ? ` - ${proj.end_year}` : ''}` : ''}</span>
                      <div className="flex gap-2">
                        {proj.github_url && (
                          <a
                            href={proj.github_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-[#64748B] hover:text-[#0F172A] p-1"
                          >
                            <GitBranch size={15} />
                          </a>
                        )}
                        {proj.project_url && (
                          <a
                            href={proj.project_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-[#2563EB] hover:underline p-1"
                          >
                            <ExternalLink size={15} />
                          </a>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-xs text-[#94A3B8] italic p-4 text-center">No project records extracted.</p>
          )}
        </div>
      )}
    </div>
  );
}
