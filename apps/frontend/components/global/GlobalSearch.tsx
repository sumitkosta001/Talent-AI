'use client';

import React, { useRef, useEffect } from 'react';
import { Search, Loader2, X, AlertCircle } from 'lucide-react';
import { useGlobalSearch } from '@/hooks/useGlobalSearch';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';

interface GlobalSearchProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function GlobalSearch({ isOpen, onClose }: GlobalSearchProps) {
  const { query, setQuery, category, setCategory, results, loading } = useGlobalSearch();
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isOpen]);

  // Handle Esc key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) {
      window.addEventListener('keydown', handleKeyDown);
    }
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  const categories = [
    { name: 'all', label: 'All Results' },
    { name: 'jobs', label: 'Jobs' },
    { name: 'companies', label: 'Companies' },
    { name: 'tools', label: 'AI Tools' },
    { name: 'bookmarks', label: 'Saved' },
    { name: 'settings', label: 'Settings' },
  ];

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[999] flex items-start justify-center pt-[10vh] p-4 text-left">
          {/* Overlay background */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-slate-900/40 dark:bg-black/60 backdrop-blur-xs"
          />

          {/* Modal layout box */}
          <motion.div
            initial={{ opacity: 0, scale: 0.96, y: -8 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.96, y: -8 }}
            transition={{ duration: 0.15 }}
            className="bg-white dark:bg-[#1E293B] border border-slate-200 dark:border-slate-800 shadow-2xl rounded-2xl w-full max-w-2xl overflow-hidden relative z-10 flex flex-col max-h-[70vh]"
          >
            {/* Search Input bar */}
            <div className="relative border-b border-slate-200 dark:border-slate-800 flex items-center p-4">
              <Search size={18} className="text-slate-400 dark:text-slate-500 mr-3" />
              <input
                ref={inputRef}
                type="text"
                placeholder="Search everywhere (jobs, companies, tools, settings)..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full text-slate-950 dark:text-white bg-transparent text-sm sm:text-base border-none focus:outline-none"
              />
              {loading ? (
                <Loader2 size={16} className="text-slate-400 animate-spin mr-2" />
              ) : query ? (
                <button onClick={() => setQuery('')} className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 mr-2">
                  <X size={16} />
                </button>
              ) : null}
            </div>

            {/* Category selection Tabs */}
            <div className="px-4 py-2 border-b border-slate-100 dark:border-slate-800/60 flex items-center gap-1.5 overflow-x-auto">
              {categories.map((c) => (
                <button
                  key={c.name}
                  onClick={() => setCategory(c.name)}
                  className={`px-3 py-1 rounded-lg text-xs font-bold transition-all uppercase tracking-wide cursor-pointer ${
                    category === c.name
                      ? 'bg-blue-600 text-white shadow-sm'
                      : 'text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800'
                  }`}
                >
                  {c.label}
                </button>
              ))}
            </div>

            {/* Results listing */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {results.length === 0 ? (
                <div className="py-12 text-center text-slate-500 dark:text-slate-400">
                  {query.trim() ? (
                    <div className="space-y-2">
                      <AlertCircle className="w-8 h-8 text-slate-400 mx-auto" />
                      <p className="text-sm font-semibold">No results match "{query}"</p>
                      <p className="text-xs">Adjust your search parameters or query tags.</p>
                    </div>
                  ) : (
                    <div className="space-y-1">
                      <p className="text-sm font-semibold">Search Everything</p>
                      <p className="text-xs">Type a keyword to discover jobs, companies, skills, AI tools, or preferences settings.</p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="space-y-2.5">
                  {results.map((item) => (
                    <Link key={item.id} href={item.route} onClick={onClose}>
                      <div className="p-3 bg-slate-50 dark:bg-slate-800/40 hover:bg-slate-100 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800 rounded-xl flex items-center justify-between cursor-pointer transition-colors group">
                        <div>
                          <h4 className="text-xs sm:text-sm font-bold text-slate-900 dark:text-slate-100 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors leading-tight">
                            {item.title}
                          </h4>
                          <p className="text-[11px] text-slate-500 dark:text-slate-400 font-medium mt-0.5 leading-relaxed">
                            {item.subtitle}
                          </p>
                        </div>
                        <span className="text-[9px] font-black uppercase tracking-widest px-2 py-0.5 rounded-md bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300">
                          {item.category}
                        </span>
                      </div>
                    </Link>
                  ))}
                </div>
              )}
            </div>

            {/* Commands footer info */}
            <div className="bg-slate-50 dark:bg-[#151D2A] px-4 py-2 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between text-[10px] text-slate-400">
              <span>Navigate with arrows, select with Enter</span>
              <span>Esc to close</span>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
