'use client';

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, AlertCircle } from 'lucide-react';

interface SettingsToastProps {
  message: string | null;
  type: 'success' | 'error';
}

export default function SettingsToast({ message, type }: SettingsToastProps) {
  return (
    <AnimatePresence>
      {message && (
        <motion.div
          initial={{ opacity: 0, y: 50, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 50, scale: 0.95 }}
          className={`
            fixed bottom-6 right-6 z-[100] flex items-center gap-2 px-4 py-3 rounded-2xl border shadow-xl text-xs sm:text-sm font-semibold
            ${type === 'success'
              ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
              : 'bg-red-50 text-red-800 border-red-200'
            }
          `}
        >
          {type === 'success' ? (
            <CheckCircle2 size={16} className="text-emerald-600 flex-shrink-0" />
          ) : (
            <AlertCircle size={16} className="text-red-600 flex-shrink-0" />
          )}
          <span>{message}</span>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
