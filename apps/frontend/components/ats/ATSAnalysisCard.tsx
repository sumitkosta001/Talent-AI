'use client';

import React from 'react';
import { FormattingScore, GrammarScore } from '@/types/ats';
import FormattingCard from './FormattingCard';
import GrammarCard from './GrammarCard';

interface ATSAnalysisCardProps {
  formatting: FormattingScore;
  grammar: GrammarScore;
}

export default function ATSAnalysisCard({ formatting, grammar }: ATSAnalysisCardProps) {
  return (
    <div className="grid lg:grid-cols-2 gap-6">
      <FormattingCard formatting={formatting} />
      <GrammarCard grammar={grammar} />
    </div>
  );
}
