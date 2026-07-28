'use client';

import React from 'react';
import { PenTool, CheckCircle, AlertTriangle } from 'lucide-react';
import { GrammarScore } from '@/types/ats';
import HorizontalProgress from './HorizontalProgress';

interface GrammarCardProps {
  grammar: GrammarScore;
}

export default function GrammarCard({ grammar }: GrammarCardProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-5">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
          <PenTool size={20} />
        </div>
        <div className="flex-1">
          <h3 className="font-semibold text-[#0F172A]">Grammar & Spelling</h3>
          <p className="text-xs text-[#64748B]">{grammar.sentenceStructure}</p>
        </div>
        <div className="text-right">
          <span className="text-xl font-bold text-emerald-600">{grammar.score}%</span>
          <p className="text-[10px] text-[#64748B] font-semibold">Quality Rate</p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-3 border-t border-b border-[#F1F5F9] py-4 text-center">
        <div>
          <p className="text-lg font-bold text-red-500">{grammar.spellingErrors}</p>
          <p className="text-xs text-[#64748B] font-semibold">Spelling Errors</p>
        </div>
        <div>
          <p className="text-lg font-bold text-blue-500">{grammar.actionVerbs}</p>
          <p className="text-xs text-[#64748B] font-semibold">Action Verbs</p>
        </div>
        <div>
          <p className="text-lg font-bold text-violet-500">{grammar.readability}</p>
          <p className="text-xs text-[#64748B] font-semibold">Readability</p>
        </div>
      </div>

      {grammar.suggestions.length > 0 && (
        <div className="space-y-2">
          <p className="text-xs font-bold text-[#64748B] uppercase tracking-wider">Grammar Warnings</p>
          <div className="space-y-2">
            {grammar.suggestions.map((s, index) => (
              <div key={index} className="flex gap-2 p-3 bg-amber-50/50 border border-amber-100 rounded-xl">
                <AlertTriangle size={15} className="text-amber-500 flex-shrink-0 mt-0.5" />
                <p className="text-xs text-amber-800 leading-relaxed">{s}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
