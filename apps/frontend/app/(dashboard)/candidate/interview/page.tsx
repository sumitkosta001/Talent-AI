'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import {
  BrainCircuit,
  FileText,
  Sparkles,
  RefreshCw,
  AlertTriangle,
  HelpCircle,
  CheckCircle2,
  Filter,
  Layers,
  ChevronRight,
  BookOpen,
} from 'lucide-react';
import { useResume } from '@/hooks/useResume';
import { useInterviewQuestions } from '@/hooks/useInterviewQuestions';
import { QuestionCategory, QuestionDifficulty } from '@/types/ml';

function formatCategoryLabel(cat?: string | null): string {
  if (!cat) return 'General';
  return cat
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
}

function getDifficultyBadge(diff?: string | null) {
  switch (diff?.toUpperCase()) {
    case 'EASY':
      return { label: 'Easy', color: 'bg-emerald-50 text-emerald-700 border-emerald-200' };
    case 'HARD':
    case 'EXPERT':
      return { label: diff, color: 'bg-red-50 text-red-700 border-red-200' };
    case 'MEDIUM':
    default:
      return { label: 'Medium', color: 'bg-amber-50 text-amber-700 border-amber-200' };
  }
}

export default function CandidateInterviewPage() {
  const { currentResume, loading: resumeLoading, retryProcessing } = useResume();
  const resumeId = currentResume?.id || null;

  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('ALL');
  const [questionCount, setQuestionCount] = useState<number>(5);

  const { data, loading, error, generateQuestions } = useInterviewQuestions(resumeId);

  const handleGenerate = async () => {
    if (!resumeId) return;

    const requestPayload: {
      count: number;
      category?: QuestionCategory;
      difficulty?: QuestionDifficulty;
    } = {
      count: questionCount,
    };

    if (selectedCategory !== 'ALL') {
      requestPayload.category = selectedCategory as QuestionCategory;
    }

    if (selectedDifficulty !== 'ALL') {
      requestPayload.difficulty = selectedDifficulty as QuestionDifficulty;
    }

    await generateQuestions(requestPayload);
  };

  if (resumeLoading) {
    return (
      <div className="min-h-[400px] flex flex-col items-center justify-center gap-3">
        <RefreshCw className="animate-spin text-[#2563EB]" size={36} />
        <p className="text-sm font-semibold text-[#64748B]">Loading interview workspace...</p>
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
              Upload and process a candidate resume first to generate personalized AI interview questions.
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
      <div className="p-6 max-w-4xl mx-auto space-y-6">
        <div className="bg-amber-50 border border-amber-200 rounded-2xl p-8 text-center space-y-4">
          <div className="w-12 h-12 bg-amber-100 text-amber-600 rounded-xl flex items-center justify-center mx-auto">
            <RefreshCw className="animate-spin" size={24} />
          </div>
          <div>
            <h3 className="font-bold text-[#0F172A] text-lg">Resume Processing in Progress</h3>
            <p className="text-sm text-[#64748B] mt-1">
              Your resume <span className="font-semibold">{currentResume.original_filename}</span> is currently being structured. AI interview questions will be available as soon as parsing completes.
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
      <div className="p-6 max-w-4xl mx-auto space-y-6">
        <div className="bg-red-50 border border-red-200 rounded-2xl p-8 text-center space-y-4">
          <div className="w-12 h-12 bg-red-100 text-red-600 rounded-xl flex items-center justify-center mx-auto">
            <AlertTriangle size={24} />
          </div>
          <div>
            <h3 className="font-bold text-[#0F172A] text-lg">Resume Processing Failed</h3>
            <p className="text-sm text-[#64748B] mt-1">
              Processing failed for <span className="font-semibold">{currentResume.original_filename}</span>: {currentResume.failure_reason || 'Parsing error.'}
            </p>
          </div>
          <button
            onClick={() => retryProcessing(currentResume.id)}
            className="inline-flex items-center justify-center gap-2 bg-[#2563EB] text-white px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-[#1D4ED8] transition-colors cursor-pointer"
          >
            Retry Processing
          </button>
        </div>
      </div>
    );
  }

  const questionsList = data?.questions || [];

  return (
    <div className="p-4 sm:p-6 space-y-6 max-w-5xl mx-auto text-[#0F172A]">
      {/* Header */}
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl sm:text-2xl font-bold text-[#0F172A]">AI Interview Preparation</h1>
            <span className="bg-purple-50 text-purple-700 border border-purple-200 text-xs font-semibold px-2.5 py-0.5 rounded-full flex items-center gap-1">
              <Sparkles size={12} />
              DAY 34 ML
            </span>
          </div>
          <p className="text-xs sm:text-sm text-[#64748B] mt-1">
            Questions generated for <span className="font-semibold text-[#0F172A]">{currentResume.original_filename}</span> (v{currentResume.version}.0) based on extracted skills, projects, and role.
          </p>
        </div>
        <Link
          href="/candidate/resume/analysis"
          className="inline-flex items-center gap-2 border border-[#E2E8F0] text-[#0F172A] px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold hover:bg-[#F8FAFC] transition-colors cursor-pointer"
        >
          Resume Analysis
          <ChevronRight size={14} />
        </Link>
      </div>

      {/* Controls & Filter Section */}
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-[#E2E8F0] pb-3">
          <div className="flex items-center gap-2">
            <Filter size={18} className="text-[#2563EB]" />
            <h2 className="font-bold text-[#0F172A] text-base">Generation Controls & Filters</h2>
          </div>
          <span className="text-xs text-[#64748B]">Configure target question scope</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {/* Category Filter */}
          <div className="space-y-1.5">
            <label className="text-xs font-bold text-[#64748B] uppercase tracking-wider">Category</label>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="w-full bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl px-3 py-2.5 text-xs text-[#0F172A] font-medium focus:outline-none focus:border-[#2563EB]"
            >
              <option value="ALL">All Categories</option>
              <option value="EXPERIENCE">Experience</option>
              <option value="PROJECT">Project</option>
              <option value="ROLE_SPECIFIC">Role Specific</option>
              <option value="SKILL_SPECIFIC">Skill Specific</option>
              <option value="SYSTEM_DESIGN">System Design</option>
            </select>
          </div>

          {/* Difficulty Filter */}
          <div className="space-y-1.5">
            <label className="text-xs font-bold text-[#64748B] uppercase tracking-wider">Difficulty</label>
            <select
              value={selectedDifficulty}
              onChange={(e) => setSelectedDifficulty(e.target.value)}
              className="w-full bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl px-3 py-2.5 text-xs text-[#0F172A] font-medium focus:outline-none focus:border-[#2563EB]"
            >
              <option value="ALL">All Difficulties</option>
              <option value="EASY">Easy</option>
              <option value="MEDIUM">Medium</option>
              <option value="HARD">Hard</option>
            </select>
          </div>

          {/* Count Selector */}
          <div className="space-y-1.5">
            <label className="text-xs font-bold text-[#64748B] uppercase tracking-wider">Count</label>
            <select
              value={questionCount}
              onChange={(e) => setQuestionCount(parseInt(e.target.value))}
              className="w-full bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl px-3 py-2.5 text-xs text-[#0F172A] font-medium focus:outline-none focus:border-[#2563EB]"
            >
              <option value={3}>3 Questions</option>
              <option value={5}>5 Questions</option>
              <option value={8}>8 Questions</option>
              <option value={10}>10 Questions</option>
            </select>
          </div>
        </div>

        <button
          onClick={handleGenerate}
          disabled={loading}
          className="w-full bg-[#2563EB] text-white py-3 rounded-xl font-semibold text-sm hover:bg-[#1D4ED8] transition-colors disabled:opacity-50 flex items-center justify-center gap-2 cursor-pointer shadow-xs"
        >
          {loading ? (
            <>
              <RefreshCw className="animate-spin" size={16} />
              <span>Generating AI Questions...</span>
            </>
          ) : (
            <>
              <BrainCircuit size={16} />
              <span>{data ? 'Generate Again' : 'Generate Questions'}</span>
            </>
          )}
        </button>
      </div>

      {/* Main Content Area */}
      {!data && !loading && !error && (
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-12 text-center space-y-4 shadow-sm">
          <div className="w-14 h-14 bg-purple-50 text-purple-600 rounded-2xl flex items-center justify-center mx-auto border border-purple-100">
            <HelpCircle size={28} />
          </div>
          <div className="max-w-md mx-auto">
            <h3 className="font-bold text-[#0F172A] text-lg">Ready to Practice AI Interview Questions</h3>
            <p className="text-xs sm:text-sm text-[#64748B] mt-1 leading-relaxed">
              Click <span className="font-semibold text-[#2563EB]">"Generate Questions"</span> above to analyze your extracted skills, work history, and projects using backend Day 34 question generation algorithms.
            </p>
          </div>
        </div>
      )}

      {loading && (
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-12 text-center space-y-4 shadow-sm animate-pulse">
          <RefreshCw className="animate-spin text-[#2563EB] mx-auto" size={32} />
          <h3 className="font-bold text-[#0F172A] text-base">Generating Personalized Interview Questions...</h3>
          <p className="text-xs text-[#64748B]">Synthesizing technical, project, and role-specific questions from your resume.</p>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-2xl p-6 text-slate-800 space-y-3">
          <div className="flex items-center gap-2 text-red-600 font-bold">
            <AlertTriangle size={20} />
            <h3>Unable to Generate Interview Questions</h3>
          </div>
          <p className="text-xs text-slate-600">{error}</p>
          <button
            onClick={handleGenerate}
            className="inline-flex items-center gap-2 bg-red-600 text-white px-4 py-2 rounded-xl text-xs font-semibold hover:bg-red-700 transition-colors cursor-pointer"
          >
            <RefreshCw size={14} />
            Try Again
          </button>
        </div>
      )}

      {data && !loading && (
        <div className="space-y-6">
          {/* Metadata Overview Banner */}
          <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 rounded-2xl p-6 text-white shadow-md border border-indigo-900/50 flex flex-wrap items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-xs text-indigo-300 font-semibold uppercase tracking-wider">Candidate Profile Context</span>
                <span className="text-[10px] bg-indigo-500/20 text-indigo-300 border border-indigo-400/30 px-2 py-0.5 rounded-full font-mono">
                  {data.provider || 'Day 34 Engine'}
                </span>
              </div>
              <p className="text-sm font-bold text-white">
                Role: {data.role || 'Full Stack Developer'} · Domain: {data.domain || 'Software Engineering'} · Level: {data.experience_level || 'Intern'}
              </p>
            </div>
            <div className="flex items-center gap-4 text-xs text-indigo-200">
              <span className="bg-white/10 px-3 py-1.5 rounded-xl border border-white/10 font-bold font-mono">
                {questionsList.length} Questions
              </span>
            </div>
          </div>

          {/* Questions Cards List */}
          {questionsList.length > 0 ? (
            <div className="space-y-4">
              {questionsList.map((q, idx) => {
                const badge = getDifficultyBadge(q.difficulty);
                return (
                  <div key={q.id || idx} className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-4">
                    <div className="flex items-start justify-between gap-3 border-b border-[#E2E8F0] pb-3">
                      <div className="flex items-center gap-2">
                        <span className="w-7 h-7 bg-blue-50 text-[#2563EB] font-bold text-xs rounded-lg flex items-center justify-center shrink-0">
                          Q{idx + 1}
                        </span>
                        <span className="text-xs font-bold uppercase tracking-wider text-[#64748B] bg-[#F8FAFC] border border-[#E2E8F0] px-2.5 py-1 rounded-lg">
                          {formatCategoryLabel(q.category || q.question_type)}
                        </span>
                      </div>
                      <span className={`text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${badge.color}`}>
                        {badge.label}
                      </span>
                    </div>

                    <p className="text-base font-semibold text-[#0F172A] leading-relaxed">
                      {q.question}
                    </p>

                    {(q.target_skill || q.target_role || q.rationale) && (
                      <div className="bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl p-3.5 text-xs text-[#64748B] space-y-1">
                        {q.target_skill && (
                          <div className="flex items-center gap-1.5 font-semibold text-[#2563EB]">
                            <span>Target Skill:</span>
                            <span className="bg-white border border-[#E2E8F0] text-[#0F172A] px-2 py-0.5 rounded text-[11px]">
                              {q.target_skill}
                            </span>
                          </div>
                        )}
                        {q.rationale && (
                          <p className="text-[#64748B] italic pt-0.5">
                            <span className="font-semibold not-italic">Rationale:</span> {q.rationale}
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="bg-white rounded-2xl border border-[#E2E8F0] p-8 text-center space-y-3 shadow-sm">
              <p className="text-sm text-[#64748B]">No questions found for the selected category/difficulty filters.</p>
              <button
                onClick={handleGenerate}
                className="inline-flex items-center gap-2 bg-[#2563EB] text-white px-4 py-2 rounded-xl text-xs font-semibold hover:bg-[#1D4ED8]"
              >
                Clear Filters & Regenerate
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
