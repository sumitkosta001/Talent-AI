'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  FileText,
  Briefcase,
  Search,
  CheckCircle2,
  AlertTriangle,
  RefreshCw,
  Award,
  BarChart3,
  Target,
  Sparkles,
  ChevronRight,
} from 'lucide-react';
import { useResume } from '@/hooks/useResume';
import { useATSScore } from '@/hooks/useATSScore';
import { useSimilarity } from '@/hooks/useSimilarity';
import { JobsService } from '@/services/jobs.service';
import { Job } from '@/types/job';
import { JobRequirements, ATSScoreResponse } from '@/types/ml';

export default function ATSPage() {
  const { currentResume, loading: resumeLoading } = useResume();
  const resumeId = currentResume?.id || null;

  const [jobs, setJobs] = useState<Job[]>([]);
  const [jobsLoading, setJobsLoading] = useState<boolean>(true);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>('');

  const { data: atsResult, loading: atsLoading, error: atsError, calculateATSScore, reset: resetATS } = useATSScore(resumeId);
  const { data: similarityResult, loading: similarityLoading, error: similarityError, calculateSimilarity, reset: resetSimilarity } = useSimilarity(resumeId);

  useEffect(() => {
    async function loadJobs() {
      try {
        setJobsLoading(true);
        const data = await JobsService.getJobs();
        setJobs(data || []);
        if (data && data.length > 0) {
          setSelectedJob(data[0]);
        }
      } catch (err) {
        console.error('Failed to load jobs list:', err);
      } finally {
        setJobsLoading(false);
      }
    }
    loadJobs();
  }, []);

  // Reset ATS score & Similarity when resume or selected job changes
  useEffect(() => {
    resetATS();
    resetSimilarity();
  }, [resumeId, selectedJob?.id, resetATS, resetSimilarity]);

  const handleSelectJob = (job: Job) => {
    setSelectedJob(job);
  };

  const handleCalculate = async () => {
    if (!selectedJob) return;

    const requirements: JobRequirements = {
      job_id: selectedJob.id,
      title: selectedJob.title || selectedJob.role,
      description: selectedJob.description || '',
      required_skills: selectedJob.skills || [],
      preferred_skills: [],
      required_keywords: selectedJob.skills || [],
      preferred_keywords: [],
      required_education: [],
      preferred_education: [],
      required_experience_months: selectedJob.experience ? parseInt(selectedJob.experience) * 12 : undefined,
      required_roles: [selectedJob.role],
      required_domains: selectedJob.category ? [selectedJob.category] : [],
    };

    await Promise.all([
      calculateATSScore(requirements),
      calculateSimilarity(requirements),
    ]);
  };

  const filteredJobs = jobs.filter((j) =>
    (j.title || j.role || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
    (j.company || '').toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (resumeLoading || jobsLoading) {
    return (
      <div className="min-h-[400px] flex flex-col items-center justify-center gap-3">
        <RefreshCw className="animate-spin text-[#2563EB]" size={36} />
        <p className="text-sm font-semibold text-[#64748B]">Loading ATS match environment...</p>
      </div>
    );
  }

  if (!currentResume) {
    return (
      <div className="p-6 max-w-4xl mx-auto space-y-6">
        <div className="bg-white border border-[#E2E8F0] rounded-2xl p-8 text-center space-y-4 shadow-sm">
          <div className="w-12 h-12 bg-blue-50 text-[#2563EB] rounded-xl flex items-center justify-center mx-auto">
            <FileText size={24} />
          </div>
          <div>
            <h3 className="font-bold text-[#0F172A] text-lg">No Active Resume Available</h3>
            <p className="text-sm text-[#64748B] mt-1">
              Please upload and process a candidate resume first to evaluate job-specific ATS match scores.
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

  return (
    <div className="p-4 sm:p-6 space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl sm:text-2xl font-bold text-[#0F172A]">ATS Resume Match & Scoring</h1>
            <span className="bg-blue-50 text-[#2563EB] border border-blue-200 text-xs font-semibold px-2.5 py-0.5 rounded-full flex items-center gap-1">
              <Sparkles size={12} />
              DAY 30 ML
            </span>
          </div>
          <p className="text-xs sm:text-sm text-[#64748B] mt-1">
            Evaluate <span className="font-semibold text-[#0F172A]">{currentResume.original_filename}</span> against target job requirements using backend weighted ATS scoring algorithms.
          </p>
        </div>
        <Link
          href="/candidate/resume/analysis"
          className="inline-flex items-center gap-2 border border-[#E2E8F0] text-[#0F172A] px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold hover:bg-[#F8FAFC] transition-colors cursor-pointer"
        >
          View Classification
          <ChevronRight size={14} />
        </Link>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left Column: Job Selector */}
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-4 h-fit">
          <div className="flex items-center gap-2 border-b border-[#E2E8F0] pb-3">
            <Briefcase size={20} className="text-[#2563EB]" />
            <h2 className="font-bold text-[#0F172A] text-base">Select Target Job</h2>
          </div>

          <div className="relative">
            <Search className="absolute left-3 top-2.5 text-[#94A3B8]" size={16} />
            <input
              type="text"
              placeholder="Search jobs by title or company..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl pl-9 pr-3 py-2 text-xs text-[#0F172A] focus:outline-none focus:border-[#2563EB]"
            />
          </div>

          <div className="space-y-2.5 max-h-[420px] overflow-y-auto pr-1">
            {filteredJobs.length > 0 ? (
              filteredJobs.map((job) => {
                const isSelected = selectedJob?.id === job.id;
                return (
                  <div
                    key={job.id}
                    onClick={() => handleSelectJob(job)}
                    className={`p-3.5 rounded-xl border transition-all cursor-pointer space-y-1.5 ${
                      isSelected
                        ? 'bg-blue-50/70 border-[#2563EB] shadow-xs'
                        : 'bg-white border-[#E2E8F0] hover:bg-[#F8FAFC]'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <h3 className="font-bold text-xs sm:text-sm text-[#0F172A] leading-snug">
                        {job.title || job.role}
                      </h3>
                      {isSelected && <CheckCircle2 size={16} className="text-[#2563EB] shrink-0 mt-0.5" />}
                    </div>
                    <div className="flex items-center justify-between text-[11px] text-[#64748B]">
                      <span>{job.company}</span>
                      <span>{job.location}</span>
                    </div>
                    {job.skills && job.skills.length > 0 && (
                      <div className="flex flex-wrap gap-1 pt-1">
                        {job.skills.slice(0, 3).map((skill) => (
                          <span key={skill} className="text-[10px] bg-white border border-[#E2E8F0] px-1.5 py-0.5 rounded text-[#64748B]">
                            {skill}
                          </span>
                        ))}
                        {job.skills.length > 3 && (
                          <span className="text-[10px] text-[#94A3B8] self-center">+{job.skills.length - 3}</span>
                        )}
                      </div>
                    )}
                  </div>
                );
              })
            ) : (
              <p className="text-xs text-[#94A3B8] italic p-4 text-center">No matching jobs found.</p>
            )}
          </div>

          <button
            onClick={handleCalculate}
            disabled={!selectedJob || atsLoading}
            className="w-full bg-[#2563EB] text-white py-3 rounded-xl font-semibold text-sm hover:bg-[#1D4ED8] transition-colors disabled:opacity-50 flex items-center justify-center gap-2 cursor-pointer shadow-xs"
          >
            {atsLoading ? (
              <>
                <RefreshCw className="animate-spin" size={16} />
                <span>Evaluating ATS Score...</span>
              </>
            ) : (
              <>
                <Target size={16} />
                <span>Calculate ATS Score</span>
              </>
            )}
          </button>
        </div>

        {/* Right Column: ATS Evaluation Results */}
        <div className="lg:col-span-2 space-y-6">
          {!atsResult && !atsLoading && !atsError && (
            <div className="bg-white rounded-2xl border border-[#E2E8F0] p-12 text-center space-y-4 shadow-sm">
              <div className="w-14 h-14 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center mx-auto border border-indigo-100">
                <Target size={28} />
              </div>
              <div className="max-w-md mx-auto">
                <h3 className="font-bold text-[#0F172A] text-lg">Ready to Evaluate ATS Compatibility</h3>
                <p className="text-xs sm:text-sm text-[#64748B] mt-1 leading-relaxed">
                  Selected Job: <span className="font-semibold text-[#0F172A]">{selectedJob?.title || selectedJob?.role || 'None'}</span> ({selectedJob?.company})
                </p>
                <p className="text-xs text-[#94A3B8] mt-2">
                  Click <span className="font-semibold text-[#2563EB]">"Calculate ATS Score"</span> to run real-time backend keyword matching, skill coverage, and experience evaluation.
                </p>
              </div>
            </div>
          )}

          {atsLoading && (
            <div className="bg-white rounded-2xl border border-[#E2E8F0] p-12 text-center space-y-4 shadow-sm animate-pulse">
              <RefreshCw className="animate-spin text-[#2563EB] mx-auto" size={32} />
              <h3 className="font-bold text-[#0F172A] text-base">Running Day 30 ATS Evaluator...</h3>
              <p className="text-xs text-[#64748B]">Matching skills, experience, education, and keywords against target job specs.</p>
            </div>
          )}

          {atsError && (
            <div className="bg-red-50 border border-red-200 rounded-2xl p-6 text-slate-800 space-y-3">
              <div className="flex items-center gap-2 text-red-600 font-bold">
                <AlertTriangle size={20} />
                <h3>Unable to Calculate ATS Score</h3>
              </div>
              <p className="text-xs text-slate-600">{atsError}</p>
              <button
                onClick={handleCalculate}
                className="inline-flex items-center gap-2 bg-red-600 text-white px-4 py-2 rounded-xl text-xs font-semibold hover:bg-red-700 transition-colors cursor-pointer"
              >
                <RefreshCw size={14} />
                Try Again
              </button>
            </div>
          )}

          {atsResult && !atsLoading && (
            <div className="space-y-6">
              {/* Main Overall ATS Score Card */}
              <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 rounded-2xl p-6 text-white shadow-md space-y-6 border border-indigo-900/50">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-4">
                  <div>
                    <span className="text-xs text-indigo-300 font-medium uppercase tracking-wider">Target Job Evaluation</span>
                    <h2 className="text-xl font-bold text-white mt-0.5">{selectedJob?.title || selectedJob?.role}</h2>
                    <p className="text-xs text-indigo-200/80">{selectedJob?.company} · {selectedJob?.location}</p>
                  </div>
                  <div className="text-right bg-white/10 backdrop-blur-sm px-5 py-3 rounded-xl border border-white/10">
                    <span className="text-[10px] text-indigo-200 font-semibold uppercase block">Overall ATS Score</span>
                    <span className="text-3xl font-extrabold text-emerald-400 font-mono">
                      {Math.round(atsResult.score)}<span className="text-lg text-indigo-200">/100</span>
                    </span>
                  </div>
                </div>

                {/* Day 31 Semantic Vector Similarity Score Badge */}
                {similarityResult && (
                  <div className="bg-indigo-900/40 rounded-xl p-4 border border-indigo-500/30 flex items-center justify-between gap-4">
                    <div className="space-y-0.5">
                      <div className="flex items-center gap-2">
                        <Sparkles size={14} className="text-indigo-400" />
                        <span className="text-xs font-bold text-indigo-200 uppercase tracking-wider">Day 31 Semantic Vector Match</span>
                      </div>
                      <p className="text-xs text-indigo-300/80">
                        {similarityResult.similarity_tier ? `Tier: ${similarityResult.similarity_tier}` : 'Vector embedding similarity'} · Model: {similarityResult.model_name || 'SentenceTransformers'}
                      </p>
                    </div>
                    <div className="text-right shrink-0">
                      <span className="text-2xl font-black text-indigo-300 font-mono">
                        {Math.round(similarityResult.similarity_score <= 1 ? similarityResult.similarity_score * 100 : similarityResult.similarity_score)}%
                      </span>
                      <span className="text-[10px] text-indigo-400 block font-mono">Cosine Similarity</span>
                    </div>
                  </div>
                )}

                {/* Score Breakdown Metrics */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  {[
                    { label: 'Skills Score', val: atsResult.skill_score },
                    { label: 'Keywords Score', val: atsResult.keyword_score },
                    { label: 'Education Score', val: atsResult.education_score },
                    { label: 'Experience Score', val: atsResult.experience_score },
                  ].map((item) => {
                    const scorePct = Math.round(item.val <= 1 ? item.val * 100 : item.val);
                    return (
                      <div key={item.label} className="bg-white/10 rounded-xl p-3.5 border border-white/10 space-y-2">
                        <div className="flex justify-between items-center text-[11px] text-indigo-200 font-semibold">
                          <span>{item.label}</span>
                          <span className="text-emerald-400 font-bold font-mono">{scorePct}%</span>
                        </div>
                        <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                          <div
                            className="bg-gradient-to-r from-indigo-500 to-emerald-400 h-full rounded-full"
                            style={{ width: `${Math.min(100, Math.max(0, scorePct))}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Matched & Missing Skills Cards */}
              <div className="grid md:grid-cols-2 gap-6">
                {/* Matched Skills */}
                <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-3">
                  <div className="flex items-center justify-between border-b border-[#E2E8F0] pb-3">
                    <h3 className="font-bold text-[#0F172A] text-base flex items-center gap-2">
                      <CheckCircle2 size={18} className="text-emerald-600" />
                      Matched Skills
                    </h3>
                    <span className="text-xs font-semibold bg-emerald-50 text-emerald-700 px-2.5 py-0.5 rounded-full border border-emerald-200">
                      {(atsResult.matched_required_skills || []).length + (atsResult.matched_preferred_skills || []).length} Matched
                    </span>
                  </div>

                  {[...(atsResult.matched_required_skills || []), ...(atsResult.matched_preferred_skills || [])].length > 0 ? (
                    <div className="flex flex-wrap gap-2 pt-1">
                      {[...(atsResult.matched_required_skills || []), ...(atsResult.matched_preferred_skills || [])].map((skill) => (
                        <span key={skill} className="text-xs bg-emerald-50 border border-emerald-200 text-emerald-800 px-3 py-1 rounded-xl font-medium flex items-center gap-1">
                          ✓ {skill}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <p className="text-xs text-[#94A3B8] italic p-2">No matching skills identified.</p>
                  )}
                </div>

                {/* Missing Skills */}
                <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-3">
                  <div className="flex items-center justify-between border-b border-[#E2E8F0] pb-3">
                    <h3 className="font-bold text-[#0F172A] text-base flex items-center gap-2">
                      <AlertTriangle size={18} className="text-amber-600" />
                      Missing Skills
                    </h3>
                    <span className="text-xs font-semibold bg-amber-50 text-amber-700 px-2.5 py-0.5 rounded-full border border-amber-200">
                      {(atsResult.missing_required_skills || []).length + (atsResult.missing_preferred_skills || []).length} Missing
                    </span>
                  </div>

                  {[...(atsResult.missing_required_skills || []), ...(atsResult.missing_preferred_skills || [])].length > 0 ? (
                    <div className="flex flex-wrap gap-2 pt-1">
                      {[...(atsResult.missing_required_skills || []), ...(atsResult.missing_preferred_skills || [])].map((skill) => (
                        <span key={skill} className="text-xs bg-amber-50 border border-amber-200 text-amber-800 px-3 py-1 rounded-xl font-medium flex items-center gap-1">
                          • {skill}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <p className="text-xs text-emerald-600 font-medium p-2">No critical missing skills! Excellent match.</p>
                  )}
                </div>
              </div>

              {/* Match Explanation & Recommendations */}
              {(atsResult.explanation || (atsResult.recommendations && atsResult.recommendations.length > 0)) && (
                <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-4">
                  {atsResult.explanation && (
                    <div className="space-y-1.5">
                      <h3 className="text-xs font-bold uppercase tracking-wider text-[#94A3B8]">Match Explanation</h3>
                      <p className="text-xs sm:text-sm text-[#64748B] leading-relaxed bg-[#F8FAFC] rounded-xl p-4 border border-[#E2E8F0]">
                        {atsResult.explanation}
                      </p>
                    </div>
                  )}

                  {atsResult.recommendations && atsResult.recommendations.length > 0 && (
                    <div className="space-y-2 pt-2 border-t border-[#E2E8F0]">
                      <h3 className="text-xs font-bold uppercase tracking-wider text-[#94A3B8]">Optimization Recommendations</h3>
                      <ul className="space-y-2 text-xs sm:text-sm text-[#0F172A]">
                        {atsResult.recommendations.map((rec, idx) => (
                          <li key={idx} className="flex items-start gap-2 bg-blue-50/50 rounded-xl p-3 border border-blue-100">
                            <span className="text-[#2563EB] font-bold mt-0.5">•</span>
                            <span className="text-[#334155]">{rec}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

