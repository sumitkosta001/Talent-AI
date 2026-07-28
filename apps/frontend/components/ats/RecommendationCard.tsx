'use client';

import React, { useState } from 'react';
import { Suggestion } from '@/types/ats';
import SuggestionCard from './SuggestionCard';

interface RecommendationCardProps {
  suggestions: Suggestion[];
  expandedSuggestions: string[];
  onToggleSuggestion: (id: string) => void;
}

export default function RecommendationCard({
  suggestions,
  expandedSuggestions,
  onToggleSuggestion,
}: RecommendationCardProps) {
  const [filter, setFilter] = useState<'all' | 'high' | 'medium' | 'low'>('all');

  const filtered = suggestions.filter((s) => {
    if (filter === 'all') return true;
    return s.priority === filter;
  });

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="font-semibold text-lg text-[#0F172A]">AI Improvements & Suggestions</h2>
          <p className="text-xs text-[#64748B] mt-0.5">Step-by-step guidance to optimize your resume matches.</p>
        </div>

        {/* Priority Filter */}
        <div className="flex gap-1 bg-[#F1F5F9] p-1 rounded-xl w-fit flex-shrink-0">
          {(['all', 'high', 'medium', 'low'] as const).map((val) => (
            <button
              key={val}
              onClick={() => setFilter(val)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold uppercase transition-all cursor-pointer ${
                filter === val
                  ? 'bg-white text-[#0F172A] shadow-sm'
                  : 'text-[#64748B] hover:text-[#0F172A]'
              }`}
            >
              {val}
            </button>
          ))}
        </div>
      </div>

      <div className="grid sm:grid-cols-2 gap-4">
        {filtered.map((suggestion) => (
          <SuggestionCard
            key={suggestion.id}
            suggestion={suggestion}
            isExpanded={expandedSuggestions.includes(suggestion.id)}
            onToggle={() => onToggleSuggestion(suggestion.id)}
          />
        ))}
      </div>
    </div>
  );
}
