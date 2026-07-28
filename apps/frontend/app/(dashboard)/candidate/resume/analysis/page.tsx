'use client';

import React, { useEffect } from 'react';
import Link from 'next/link';
import { Download, ChevronRight, FileText, Code, RefreshCw, AlertTriangle } from 'lucide-react';
import { useResume } from '@/hooks/useResume';
import ResumeHeader from '@/components/resume/ResumeHeader';
import ResumeAnalysisCard from '@/components/resume/ResumeAnalysisCard';
import AnalysisCard from '@/components/resume/AnalysisCard';
import KeywordCard from '@/components/resume/KeywordCard';
import StrengthCard from '@/components/resume/StrengthCard';
import WeaknessCard from '@/components/resume/WeaknessCard';
import SuggestionCard from '@/components/resume/SuggestionCard';

export default function ResumeAnalysisPage() {
  const { analysis, loading, error, fetchAnalysis } = useResume();

  useEffect(() => {
    fetchAnalysis();
  }, [fetchAnalysis]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] gap-3">
        <RefreshCw className="animate-spin text-[#2563EB]" size={36} />
        <p className="text-sm font-semibold text-[#64748B]">Running AI resume audit...</p>
      </div>
    );
  }

  if (error || !analysis) {
    return (
      <div className="p-6 space-y-6 max-w-4xl mx-auto">
        <div className="bg-red-50 border border-red-200 rounded-2xl p-6 text-center space-y-4">
          <div className="w-12 h-12 bg-red-100 text-red-600 rounded-xl flex items-center justify-center mx-auto">
            <AlertTriangle size={24} />
          </div>
          <div>
            <h3 className="font-bold text-[#0F172A] text-lg">Failed to load analysis</h3>
            <p className="text-sm text-[#64748B] mt-1">{error || 'No analysis data could be retrieved.'}</p>
          </div>
          <button
            onClick={() => fetchAnalysis()}
            className="inline-flex items-center justify-center gap-2 bg-[#2563EB] text-white px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-[#1D4ED8] transition-colors cursor-pointer"
          >
            Retry Audit
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 sm:p-6 space-y-6 max-w-5xl mx-auto">
      {/* Header section */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-[#0F172A]">AI Resume Analysis</h1>
          <p className="text-xs sm:text-sm text-[#64748B] mt-1">
            Alex_Johnson_Resume_v3.pdf · Audited Jul 10, 2025
          </p>
        </div>
        <div className="flex gap-3">
          <Link
            href="/candidate/ats"
            className="inline-flex items-center gap-2 border border-[#E2E8F0] text-[#0F172A] px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold hover:bg-[#F8FAFC] transition-colors cursor-pointer"
          >
            ATS Score
            <ChevronRight size={14} />
          </Link>
          <button
            className="inline-flex items-center gap-2 bg-[#2563EB] text-white px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold hover:bg-[#1D4ED8] transition-colors cursor-pointer"
            onClick={() => alert('Downloading PDF Audit Report...')}
          >
            <Download size={15} />
            Download Report
          </button>
        </div>
      </div>

      {/* Main overall score banner */}
      <ResumeAnalysisCard
        score={analysis.overallScore}
        skillsScore={analysis.skillScore}
        experienceScore={analysis.experienceScore}
        educationScore={analysis.educationScore}
      />

      <div className="grid lg:grid-cols-3 gap-6 animate-in fade-in duration-300">
        {/* Left column: summaries, sub scores, and keywords */}
        <div className="lg:col-span-2 space-y-6">
          {/* Summary Audit */}
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-3">
            <div className="flex items-center gap-2">
              <FileText size={18} className="text-[#2563EB]" />
              <h2 className="font-bold text-[#0F172A] text-base">Summary Audit</h2>
            </div>
            <p className="text-xs sm:text-sm text-[#64748B] leading-relaxed">
              Your professional summary covers the core requirements: years of experience, primary framework specialization (React/Next), and high-level team achievements. Adding metrics here could boost matching.
            </p>
          </div>

          {/* Sub-scores grid */}
          <div className="grid sm:grid-cols-2 gap-4">
            <AnalysisCard
              icon="💼"
              label="Experience Analysis"
              score={analysis.experienceScore}
              description="Impact-driven descriptions detected. Add more details about cloud setups."
              color="bg-violet-500"
            />
            <AnalysisCard
              icon="🔑"
              label="Keyword Coverage"
              score={analysis.keywordCoverageScore}
              description="Excellent match across standard web terms. Missing some cloud and DevOps keys."
              color="bg-blue-500"
            />
            <AnalysisCard
              icon="🎓"
              label="Education Analysis"
              score={analysis.educationScore}
              description="Proper degree formats, Stanford credentials parsed with correct GPAs."
              color="bg-emerald-500"
            />
            <AnalysisCard
              icon="📋"
              label="Formatting Optimization"
              score={analysis.formattingScore}
              description="Clean document layouts, standard margin styles, and standard fonts detected."
              color="bg-rose-500"
            />
          </div>

          {/* Keyword Matcher Columns */}
          <KeywordCard
            matchedKeywords={analysis.matchedKeywords}
            missingKeywords={analysis.missingKeywords}
          />
        </div>

        {/* Right column: Strengths, Weaknesses, Suggestions */}
        <div className="space-y-6">
          <StrengthCard strengths={analysis.strengths} />
          <WeaknessCard weaknesses={analysis.weaknesses} />
          <SuggestionCard suggestions={analysis.suggestions} />
        </div>
      </div>
    </div>
  );
}
