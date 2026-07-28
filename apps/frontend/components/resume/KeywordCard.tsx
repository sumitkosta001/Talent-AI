import React from 'react';
import { CheckCircle, AlertCircle } from 'lucide-react';

interface KeywordCardProps {
  matchedKeywords: string[];
  missingKeywords: string[];
}

export default function KeywordCard({ matchedKeywords, missingKeywords }: KeywordCardProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5">
      <h3 className="font-semibold text-[#0F172A] mb-4">Keyword Coverage Analysis</h3>
      <div className="grid md:grid-cols-2 gap-6">
        <div>
          <p className="text-xs font-semibold text-[#22C55E] mb-3 flex items-center gap-1.5 uppercase tracking-wider">
            <CheckCircle size={14} /> Matched Keywords ({matchedKeywords.length})
          </p>
          <div className="flex flex-wrap gap-2">
            {matchedKeywords.map((k) => (
              <span
                key={k}
                className="text-xs font-medium bg-green-50 text-green-700 border border-green-100 px-3 py-1 rounded-full"
              >
                {k}
              </span>
            ))}
          </div>
        </div>
        <div>
          <p className="text-xs font-semibold text-[#EF4444] mb-3 flex items-center gap-1.5 uppercase tracking-wider">
            <AlertCircle size={14} /> Missing Keywords ({missingKeywords.length})
          </p>
          <div className="flex flex-wrap gap-2">
            {missingKeywords.map((k) => (
              <span
                key={k}
                className="text-xs font-medium bg-red-50 text-red-700 border border-red-100 px-3 py-1 rounded-full"
              >
                {k}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
