'use client';

import React from 'react';
import { AlertCircle } from 'lucide-react';
import KeywordBadge from './KeywordBadge';
import { Keyword } from '@/types/ats';

interface MissingKeywordsProps {
  keywords: Keyword[];
}

export default function MissingKeywords({ keywords }: MissingKeywordsProps) {
  return (
    <div className="space-y-3">
      <h3 className="text-xs font-semibold text-[#EF4444] flex items-center gap-1.5 uppercase tracking-wide">
        <AlertCircle size={14} /> Missing Keywords ({keywords.length})
      </h3>
      <div className="flex flex-wrap gap-2.5">
        {keywords.map((k) => (
          <KeywordBadge
            key={k.name}
            name={k.name}
            matched={false}
            importance={k.importance}
            category={k.category}
          />
        ))}
      </div>
    </div>
  );
}
