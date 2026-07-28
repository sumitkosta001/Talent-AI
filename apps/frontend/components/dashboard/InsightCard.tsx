'use client';

import React from 'react';
import { CareerInsightCard } from '@/types/careerInsight';
import { Play, X } from 'lucide-react';
import { motion } from 'framer-motion';
import Link from 'next/link';

interface InsightCardProps {
  item: CareerInsightCard;
  getInsightIcon: (type: CareerInsightCard['type']) => { icon: any; color: string };
  getPriorityClass: (priority: CareerInsightCard['priority']) => string;
  onDismiss: (id: string) => void;
}

export default function InsightCard({ item, getInsightIcon, getPriorityClass, onDismiss }: InsightCardProps) {
  const config = getInsightIcon(item.type);
  const Icon = config.icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.2 }}
      className="p-4 bg-gradient-to-r from-white to-[#F8FAFC] border border-[#E2E8F0] rounded-2xl relative hover:shadow-sm transition-all group text-left w-full"
    >
      <button
        onClick={() => onDismiss(item.id)}
        className="absolute top-3 right-3 p-1 hover:bg-slate-100 rounded-lg text-[#94A3B8] hover:text-slate-600 opacity-0 group-hover:opacity-100 transition-opacity"
        title="Dismiss"
      >
        <X size={12} />
      </button>

      <div className="flex gap-3">
        <div className={`w-9 h-9 rounded-xl flex items-center justify-center border flex-shrink-0 ${config.color}`}>
          <Icon size={16} />
        </div>
        <div className="space-y-1.5 flex-1 min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <h4 className="font-extrabold text-[#0F172A] text-xs sm:text-sm truncate">
              {item.title}
            </h4>
            <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded-full border uppercase tracking-wider ${getPriorityClass(item.priority)}`}>
              {item.priority}
            </span>
          </div>
          <p className="text-xs text-[#64748B] leading-relaxed pr-4">
            {item.reason}
          </p>

          <div className="pt-2">
            <Link href={item.actionUrl}>
              <button className="inline-flex items-center gap-1 bg-indigo-600 hover:bg-indigo-700 text-white text-[11px] font-bold py-1.5 px-3 rounded-xl transition-all shadow-sm">
                {item.actionText}
                <Play size={10} className="fill-current text-white/90" />
              </button>
            </Link>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
