'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle2, XCircle, AlertTriangle, Info, Loader2, X, RotateCcw } from 'lucide-react';
import { ToastItem } from '@/types/toast';

interface ToastProps {
  toast: ToastItem;
  onDismiss: (id: string) => void;
}

export default function Toast({ toast, onDismiss }: ToastProps) {
  const getIcon = () => {
    switch (toast.type) {
      case 'success':
        return <CheckCircle2 className="w-5 h-5 text-emerald-500" />;
      case 'error':
        return <XCircle className="w-5 h-5 text-rose-500" />;
      case 'warning':
        return <AlertTriangle className="w-5 h-5 text-amber-500" />;
      case 'info':
        return <Info className="w-5 h-5 text-blue-500" />;
      case 'loading':
        return <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />;
    }
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: -20, scale: 0.9 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9, y: -10 }}
      className="bg-white dark:bg-[#1E293B] border border-slate-200 dark:border-slate-800 shadow-lg rounded-2xl p-4 flex gap-3 max-w-sm w-full pointer-events-auto text-left"
    >
      <div className="flex-shrink-0 mt-0.5">{getIcon()}</div>
      <div className="flex-1 min-w-0 text-left">
        <h4 className="text-sm font-bold text-slate-900 dark:text-slate-100 leading-tight">
          {toast.message}
        </h4>
        {toast.description && (
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 leading-relaxed">
            {toast.description}
          </p>
        )}
        {toast.undoAction && (
          <button
            onClick={() => {
              toast.undoAction?.();
              onDismiss(toast.id);
            }}
            className="mt-2.5 inline-flex items-center gap-1 text-[11px] font-bold text-blue-600 dark:text-blue-400 hover:underline"
          >
            <RotateCcw size={10} />
            Undo Action
          </button>
        )}
      </div>
      <button
        onClick={() => onDismiss(toast.id)}
        className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 flex-shrink-0 self-start"
      >
        <X size={14} />
      </button>
    </motion.div>
  );
}
