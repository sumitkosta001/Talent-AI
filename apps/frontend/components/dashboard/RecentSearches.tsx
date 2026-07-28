'use client';

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Trash2, RotateCcw, X, MapPin, Briefcase, Building2, Code } from 'lucide-react';
import { RecentSearchItem } from '@/types/dashboard';

interface RecentSearchesProps {
  searches: RecentSearchItem[];
  onDelete: (id: string) => void;
  onClear: () => void;
  onSelect: (query: string) => void;
}

export default function RecentSearches({ searches, onDelete, onClear, onSelect }: RecentSearchesProps) {
  const getCategoryIcon = (cat: RecentSearchItem['category']) => {
    switch (cat) {
      case 'jobs':
        return Briefcase;
      case 'companies':
        return Building2;
      case 'skills':
        return Code;
      default:
        return MapPin;
    }
  };

  return (
    <div className="bg-white rounded-3xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
      <div className="flex items-center justify-between border-b border-[#F1F5F9] pb-3">
        <div>
          <h3 className="font-bold text-[#0F172A] text-base sm:text-lg">Recent Searches</h3>
          <p className="text-xs text-[#64748B] mt-0.5">Quick relaunch for your frequent queries</p>
        </div>
        {searches.length > 0 && (
          <button
            onClick={onClear}
            className="inline-flex items-center gap-1 py-1.5 px-2.5 hover:bg-red-50 text-[10px] font-bold text-red-600 rounded-xl transition-all border border-transparent hover:border-red-100"
          >
            <Trash2 size={12} />
            Clear All
          </button>
        )}
      </div>

      <div className="space-y-2 max-h-[220px] overflow-y-auto pr-1">
        <AnimatePresence mode="popLayout">
          {searches.length === 0 ? (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-xs text-[#94A3B8] italic"
            >
              Search history is empty.
            </motion.p>
          ) : (
            searches.map((item) => {
              const Icon = getCategoryIcon(item.category);
              return (
                <motion.div
                  key={item.id}
                  initial={{ opacity: 0, y: 5 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -5 }}
                  className="flex items-center justify-between gap-3 p-2 hover:bg-[#F8FAFC] border border-transparent hover:border-[#E2E8F0] rounded-xl group transition-all"
                >
                  <button
                    onClick={() => onSelect(item.query)}
                    className="flex items-center gap-2.5 min-w-0 flex-1 text-left"
                  >
                    <div className="w-7 h-7 bg-slate-50 border border-slate-150 rounded-lg flex items-center justify-center flex-shrink-0 text-slate-400 group-hover:text-blue-500 group-hover:bg-blue-50 transition-colors">
                      <Icon size={14} />
                    </div>
                    <div className="min-w-0">
                      <span className="font-semibold text-[#0F172A] text-xs sm:text-sm truncate block">
                        {item.query}
                      </span>
                      <span className="text-[10px] text-[#94A3B8] uppercase tracking-wide">
                        {item.category}
                      </span>
                    </div>
                  </button>

                  <div className="flex items-center gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={() => onSelect(item.query)}
                      title="Run Search Again"
                      className="p-1.5 hover:bg-slate-100 rounded-lg text-[#64748B] hover:text-[#0F172A] transition-colors"
                    >
                      <RotateCcw size={13} />
                    </button>
                    <button
                      onClick={() => onDelete(item.id)}
                      title="Delete Search"
                      className="p-1.5 hover:bg-red-50 rounded-lg text-[#94A3B8] hover:text-red-600 transition-colors"
                    >
                      <X size={13} />
                    </button>
                  </div>
                </motion.div>
              );
            })
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
