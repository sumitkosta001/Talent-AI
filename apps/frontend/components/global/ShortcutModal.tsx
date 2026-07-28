'use client';

import React from 'react';
import { MOCK_SHORTCUTS } from '@/mock/shortcuts';
import KeyboardShortcutItem from './KeyboardShortcutItem';
import { X, Keyboard } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface ShortcutModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function ShortcutModal({ isOpen, onClose }: ShortcutModalProps) {
  const general = MOCK_SHORTCUTS.filter((s) => s.category === 'general');
  const navigation = MOCK_SHORTCUTS.filter((s) => s.category === 'navigation');

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[999] flex items-center justify-center p-4 text-left">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-slate-900/40 dark:bg-black/60 backdrop-blur-xs"
          />

          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 10 }}
            className="bg-white dark:bg-[#1E293B] border border-slate-200 dark:border-slate-800 shadow-2xl rounded-2xl w-full max-w-md overflow-hidden relative z-10 flex flex-col"
          >
            <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Keyboard className="text-blue-500" size={18} />
                <h3 className="font-bold text-slate-900 dark:text-slate-100 text-sm sm:text-base">Keyboard Shortcuts</h3>
              </div>
              <button onClick={onClose} className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 cursor-pointer">
                <X size={18} />
              </button>
            </div>

            <div className="p-4 overflow-y-auto max-h-[60vh] space-y-5">
              <div>
                <h4 className="text-[10px] font-black text-slate-400 dark:text-slate-500 uppercase tracking-widest mb-2">General Controls</h4>
                <div className="space-y-1">
                  {general.map((s, idx) => (
                    <KeyboardShortcutItem key={idx} keys={s.keys} label={s.label} />
                  ))}
                </div>
              </div>

              <div>
                <h4 className="text-[10px] font-black text-slate-400 dark:text-slate-500 uppercase tracking-widest mb-2">Portal Navigation</h4>
                <div className="space-y-1">
                  {navigation.map((s, idx) => (
                    <KeyboardShortcutItem key={idx} keys={s.keys} label={s.label} />
                  ))}
                </div>
              </div>
            </div>

            <div className="bg-slate-50 dark:bg-[#151D2A] px-4 py-2 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between text-[10px] text-slate-400">
              <span>Press Esc to close</span>
              <span>TalentAI Controls Cheatsheet</span>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
