'use client';

import React from 'react';
import { motion } from 'framer-motion';

interface AnimatedProgressProps {
  value: number;
  color?: string;
  className?: string;
  showLabel?: boolean;
}

export default function AnimatedProgress({
  value,
  color = 'bg-blue-600',
  className = '',
  showLabel = false,
}: AnimatedProgressProps) {
  const percentage = Math.min(Math.max(value, 0), 100);

  return (
    <div className={`w-full space-y-1 ${className}`}>
      {showLabel && (
        <div className="flex justify-between items-center text-xs font-bold text-slate-700 dark:text-slate-300">
          <span>Progress</span>
          <span>{percentage}%</span>
        </div>
      )}
      <div className="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden border border-slate-200/60 dark:border-slate-700/60">
        <motion.div
          initial={{ width: '0%' }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
          className={`h-full rounded-full ${color}`}
        />
      </div>
    </div>
  );
}
