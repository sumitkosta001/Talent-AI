'use client';

import React from 'react';
import { CheckCircle } from 'lucide-react';
import KeywordBadge from './KeywordBadge';
import { Keyword } from '@/types/ats';

interface MatchedKeywordsProps {
  keywords: Keyword[];
}

export default function MatchedKeywords({ keywords }: MatchedKeywordsProps) {
  return (
    <div className="space-y-3">
      <h3 className="text-xs font-semibold text-[#22C55E] flex items-center gap-1.5 uppercase tracking-wide">
        <CheckCircle size={14} /> Matched Keywords ({keywords.length})
      </h3>
      <div className="flex flex-wrap gap-2.5">
        {keywords.map((k) => (
          <KeywordBadge
            key={k.name}
            name={k.name}
            matched={true}
            frequency={k.frequency}
            category={k.category}
            importance={k.importance}
          />
        ))}
      </div>
    </div>
  );
}
