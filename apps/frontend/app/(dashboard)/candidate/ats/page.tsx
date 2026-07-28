'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { useATS } from '@/hooks/useATS';
import { MOCK_STRENGTHS, MOCK_WEAKNESSES } from '@/mock/atsSuggestions';
import { MOCK_RADAR_DATA } from '@/mock/atsCharts';
import ATSHeader from '@/components/ats/ATSHeader';
import ATSScoreCard from '@/components/ats/ATSScoreCard';
import StrengthCard from '@/components/ats/StrengthCard';
import WeaknessCard from '@/components/ats/WeaknessCard';
import ATSBreakdown from '@/components/ats/ATSBreakdown';
import KeywordAnalysis from '@/components/ats/KeywordAnalysis';
import ATSAnalysisCard from '@/components/ats/ATSAnalysisCard';
import ResumeSectionCard from '@/components/ats/ResumeSectionCard';
import RecommendationCard from '@/components/ats/RecommendationCard';
import ImprovementRoadmap from '@/components/ats/ImprovementRoadmap';
import { Loader } from 'lucide-react';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: { y: 0, opacity: 1, transition: { duration: 0.5, ease: 'easeOut' as const } },
};

export default function ATSPage() {
  const {
    result,
    loading,
    error,
    expandedSuggestions,
    toggleSuggestionExpand,
  } = useATS();

  if (loading) {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center gap-3">
        <Loader className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading ATS Score analysis details...</p>
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3">
        <div className="text-red-500 font-bold text-lg">Error Loading Analysis</div>
        <p className="text-sm text-[#64748B]">{error || 'An unexpected error occurred.'}</p>
        <button
          onClick={() => window.location.reload()}
          className="bg-blue-600 text-white px-4 py-2 rounded-xl text-sm font-semibold"
        >
          Retry
        </button>
      </div>
    );
  }

  // Prep Score breakdowns for progress bars
  const scoreBreakdown = [
    { label: 'Keyword Match', score: result.score.keywordMatch, icon: '🔑', color: 'bg-blue-500' },
    { label: 'Work Experience', score: result.score.experience, icon: '💼', color: 'bg-violet-500' },
    { label: 'Education', score: result.score.education, icon: '🎓', color: 'bg-emerald-500' },
    { label: 'Projects', score: result.score.projects, icon: '🗂️', color: 'bg-amber-500' },
    { label: 'Formatting', score: result.score.formatting, icon: '📋', color: 'bg-rose-500' },
  ];

  const matchedKeywordsCount = result.keywords.filter(k => k.matched).length;

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="p-6 space-y-6 max-w-5xl mx-auto"
    >
      {/* Header */}
      <motion.div variants={itemVariants}>
        <ATSHeader />
      </motion.div>

      {/* Hero Score */}
      <motion.div variants={itemVariants}>
        <ATSScoreCard
          score={{
            overall: result.score.overall,
            keywordMatch: result.score.keywordMatch,
            experience: result.score.experience,
            skills: result.score.skills,
          }}
          keywordsCount={{ matched: matchedKeywordsCount, total: result.keywords.length }}
          experienceYears={result.experience.years}
          missingSkillsCount={result.skills.missing.length}
        />
      </motion.div>

      {/* Strengths & Weaknesses */}
      <motion.div variants={itemVariants} className="grid md:grid-cols-2 gap-6">
        <StrengthCard strengths={MOCK_STRENGTHS} />
        <WeaknessCard weaknesses={MOCK_WEAKNESSES} />
      </motion.div>

      {/* Score Breakdown Progress Bars & Radar Skill Chart */}
      <motion.div variants={itemVariants}>
        <ATSBreakdown
          scoreBreakdown={scoreBreakdown}
          radarData={MOCK_RADAR_DATA}
        />
      </motion.div>

      {/* Keywords Analysis */}
      <motion.div variants={itemVariants}>
        <KeywordAnalysis keywords={result.keywords} />
      </motion.div>

      {/* Layout formatting & Grammar Check */}
      <motion.div variants={itemVariants}>
        <ATSAnalysisCard
          formatting={result.formatting}
          grammar={result.grammar}
        />
      </motion.div>

      {/* Section-by-Section Details Swapping Panels */}
      <motion.div variants={itemVariants}>
        <ResumeSectionCard
          sections={result.sections}
          result={result}
        />
      </motion.div>

      {/* Suggestions List */}
      <motion.div variants={itemVariants}>
        <RecommendationCard
          suggestions={result.suggestions}
          expandedSuggestions={expandedSuggestions}
          onToggleSuggestion={toggleSuggestionExpand}
        />
      </motion.div>

      {/* Optimization Timeline Roadmap */}
      <motion.div variants={itemVariants}>
        <ImprovementRoadmap timeline={result.timeline} />
      </motion.div>
    </motion.div>
  );
}
