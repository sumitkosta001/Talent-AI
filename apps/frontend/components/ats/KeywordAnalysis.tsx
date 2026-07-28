'use client';

import React from 'react';
import MatchedKeywords from './MatchedKeywords';
import MissingKeywords from './MissingKeywords';
import { Keyword } from '@/types/ats';

interface KeywordAnalysisProps {
  keywords: Keyword[];
}

export default function KeywordAnalysis({ keywords }: KeywordAnalysisProps) {
  const matched = keywords.filter((k) => k.matched);
  const missing = keywords.filter((k) => !k.matched);

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-6">
      <div>
        <h2 className="font-semibold text-lg text-[#0F172A]">Keyword Analysis</h2>
        <p className="text-xs text-[#64748B] mt-0.5">Identified technical terminology and competencies compared to industry listings.</p>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        <MatchedKeywords keywords={matched} />
        <MissingKeywords keywords={missing} />
      </div>
    </div>
  );
}
