'use client';

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, FileText, UserCheck, HelpCircle } from 'lucide-react';
import { CareerInsightCard } from '@/types/careerInsight';
import InsightCard from './InsightCard';

interface CareerInsightsProps {
  insights: CareerInsightCard[];
  onDismiss: (id: string) => void;
}

export default function CareerInsights({ insights, onDismiss }: CareerInsightsProps) {
  const getInsightIcon = (type: CareerInsightCard['type']) => {
    switch (type) {
      case 'resume':
      case 'ats':
        return { icon: FileText, color: 'text-rose-500 bg-rose-50 border-rose-100' };
      case 'profile':
      case 'portfolio':
        return { icon: UserCheck, color: 'text-blue-500 bg-blue-50 border-blue-100' };
      case 'interview':
        return { icon: HelpCircle, color: 'text-indigo-500 bg-indigo-50 border-indigo-100' };
      default:
        return { icon: Sparkles, color: 'text-amber-500 bg-amber-50 border-amber-100' };
    }
  };

  const getPriorityClass = (priority: CareerInsightCard['priority']) => {
    if (priority === 'high') return 'text-rose-600 bg-rose-50 border-rose-100';
    if (priority === 'medium') return 'text-amber-600 bg-amber-50 border-amber-100';
    return 'text-blue-600 bg-blue-50 border-blue-100';
  };

  return (
    <div className="bg-white rounded-3xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
      <div className="flex items-center justify-between border-b border-[#F1F5F9] pb-3">
        <div className="flex items-center gap-2">
          <Sparkles size={18} className="text-indigo-500" />
          <h3 className="font-bold text-[#0F172A] text-base sm:text-lg">AI Mentor Insights</h3>
        </div>
      </div>

      <div className="space-y-3 max-h-[360px] overflow-y-auto pr-1">
        <AnimatePresence mode="popLayout">
          {insights.length === 0 ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="p-6 text-center bg-[#F8FAFC] rounded-2xl border border-dashed border-[#E2E8F0]"
            >
              <p className="text-xs text-[#94A3B8] italic">All insights addressed! Keep up the great work.</p>
            </motion.div>
          ) : (
            insights.map((item) => (
              <InsightCard
                key={item.id}
                item={item}
                getInsightIcon={getInsightIcon}
                getPriorityClass={getPriorityClass}
                onDismiss={onDismiss}
              />
            ))
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
