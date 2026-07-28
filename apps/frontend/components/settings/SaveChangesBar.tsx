'use client';

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Save, RotateCcw } from 'lucide-react';

interface SaveChangesBarProps {
  isVisible: boolean;
  onSave: () => void;
  onDiscard: () => void;
  saving: boolean;
}

export default function SaveChangesBar({ isVisible, onSave, onDiscard, saving }: SaveChangesBarProps) {
  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ y: 100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: 100, opacity: 0 }}
          transition={{ type: 'spring', stiffness: 260, damping: 20 }}
          className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 bg-[#0F172A] text-white px-5 py-3 rounded-2xl border border-slate-800 shadow-2xl flex items-center justify-between gap-6 max-w-lg w-[calc(100%-2rem)]"
        >
          <div className="text-left">
            <h5 className="text-xs font-bold">Unsaved Changes</h5>
            <p className="text-[10px] text-slate-400 mt-0.5">Please save or discard your settings changes.</p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={onDiscard}
              disabled={saving}
              className="inline-flex items-center gap-1 hover:bg-slate-800 text-slate-300 font-bold text-xs px-3 py-1.5 rounded-xl transition-all cursor-pointer border border-slate-700 disabled:opacity-50"
            >
              <RotateCcw size={12} />
              Discard
            </button>
            <button
              onClick={onSave}
              disabled={saving}
              className="inline-flex items-center gap-1 bg-[#2563EB] hover:bg-[#1D4ED8] disabled:opacity-50 text-white font-bold text-xs px-3 py-1.5 rounded-xl transition-all cursor-pointer"
            >
              <Save size={12} />
              {saving ? 'Saving...' : 'Save'}
            </button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
