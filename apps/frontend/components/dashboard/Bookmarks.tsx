'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Briefcase, Building2, BookOpen, GraduationCap } from 'lucide-react';
import { BookmarkItem } from '@/types/bookmark';
import BookmarkCard from './BookmarkCard';

interface BookmarksProps {
  bookmarks: BookmarkItem[];
  onRemove: (id: string) => void;
}

export default function Bookmarks({ bookmarks, onRemove }: BookmarksProps) {
  const [search, setSearch] = useState('');
  const [filterType, setFilterType] = useState<'all' | 'job' | 'company' | 'article' | 'learning'>('all');

  const getBookmarkIcon = (type: BookmarkItem['type']) => {
    switch (type) {
      case 'job':
        return { icon: Briefcase, color: 'text-blue-500 bg-blue-50 border-blue-100' };
      case 'company':
        return { icon: Building2, color: 'text-emerald-500 bg-emerald-50 border-emerald-100' };
      case 'article':
        return { icon: BookOpen, color: 'text-indigo-500 bg-indigo-50 border-indigo-100' };
      default:
        return { icon: GraduationCap, color: 'text-purple-500 bg-purple-50 border-purple-100' };
    }
  };

  const filtered = bookmarks.filter((item) => {
    const matchesSearch =
      item.title.toLowerCase().includes(search.toLowerCase()) ||
      item.subtitle.toLowerCase().includes(search.toLowerCase());
    const matchesFilter = filterType === 'all' || item.type === filterType;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="bg-white rounded-3xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#F1F5F9] pb-3">
        <div>
          <h3 className="font-bold text-[#0F172A] text-base sm:text-lg">Saved Bookmarks</h3>
          <p className="text-xs text-[#64748B] mt-0.5">Quick access to your prioritized resources</p>
        </div>

        <div className="relative max-w-[200px]">
          <Search size={14} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-[#94A3B8]" />
          <input
            type="text"
            placeholder="Search saved..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-8 pr-2.5 py-1.5 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
          />
        </div>
      </div>

      {/* Filter tabs */}
      <div className="flex flex-wrap gap-1">
        {(['all', 'job', 'company', 'article', 'learning'] as const).map((t) => (
          <button
            key={t}
            onClick={() => setFilterType(t)}
            className={`px-3 py-1 text-[10px] sm:text-xs font-bold rounded-full border transition-all uppercase tracking-wide ${
              filterType === t
                ? 'bg-slate-900 border-slate-900 text-white'
                : 'bg-white border-[#E2E8F0] text-[#64748B] hover:text-[#0F172A] hover:bg-slate-50'
            }`}
          >
            {t}s
          </button>
        ))}
      </div>

      <div className="space-y-2 max-h-[300px] overflow-y-auto pr-1">
        <AnimatePresence mode="popLayout">
          {filtered.length === 0 ? (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-xs text-[#94A3B8] italic"
            >
              No saved bookmarks found matching constraints.
            </motion.p>
          ) : (
            filtered.map((item) => (
              <BookmarkCard
                key={item.id}
                item={item}
                getBookmarkIcon={getBookmarkIcon}
                onRemove={onRemove}
              />
            ))
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
