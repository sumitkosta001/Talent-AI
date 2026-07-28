'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, ChevronUp, AlertCircle, HelpCircle } from 'lucide-react';
import { Suggestion } from '@/types/ats';

interface SuggestionCardProps {
  suggestion: Suggestion;
  isExpanded: boolean;
  onToggle: () => void;
}

export default function SuggestionCard({
  suggestion,
  isExpanded,
  onToggle,
}: SuggestionCardProps) {
  const { priority, text, category } = suggestion;

  const colors = {
    high: 'border-red-200 bg-red-50/50 hover:bg-red-50',
    medium: 'border-amber-200 bg-amber-50/50 hover:bg-amber-50',
    low: 'border-blue-200 bg-blue-50/50 hover:bg-blue-50',
  };

  const badges = {
    high: 'bg-red-100 text-red-700 border-red-200',
    medium: 'bg-amber-100 text-amber-700 border-amber-200',
    low: 'bg-blue-100 text-blue-700 border-blue-200',
  };

  return (
    <div
      onClick={onToggle}
      className={`border rounded-2xl p-4 transition-all cursor-pointer select-none ${colors[priority]}`}
    >
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase border ${badges[priority]}`}>
            {priority}
          </span>
          <span className="text-[10px] bg-slate-100 text-slate-600 font-semibold px-2 py-0.5 rounded-md border border-slate-200 uppercase">
            {category}
          </span>
        </div>
        <div>
          {isExpanded ? <ChevronUp size={16} className="text-[#64748B]" /> : <ChevronDown size={16} className="text-[#64748B]" />}
        </div>
      </div>

      <p className="text-sm font-semibold text-[#0F172A] mt-2.5 leading-snug">
        {text.split('.')[0]}.
      </p>

      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25 }}
            className="overflow-hidden"
          >
            <div className="pt-3.5 border-t border-[#F1F5F9] mt-3 text-xs text-[#64748B] leading-relaxed space-y-2">
              <p>{text}</p>
              <div className="flex items-center gap-1.5 text-blue-600 font-medium cursor-pointer hover:underline">
                <HelpCircle size={13} />
                <span>Learn how to resolve this optimization warning</span>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
