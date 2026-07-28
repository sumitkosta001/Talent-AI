'use client';

import React from 'react';
import { motion } from 'framer-motion';

interface HorizontalProgressProps {
  value: number;
  max?: number;
  color?: string;
  backgroundColor?: string;
  animate?: boolean;
}

export default function HorizontalProgress({
  value,
  max = 100,
  color,
  backgroundColor = 'bg-[#F1F5F9]',
  animate = true,
}: HorizontalProgressProps) {
  const percentage = Math.min((value / max) * 100, 100);

  // Fallback color logic based on percentage
  const barColor = color || (percentage >= 90
    ? 'bg-emerald-500'
    : percentage >= 75
    ? 'bg-blue-500'
    : percentage >= 50
    ? 'bg-amber-500'
    : 'bg-rose-500');

  return (
    <div className={`w-full h-2 ${backgroundColor} rounded-full overflow-hidden`}>
      {animate ? (
        <motion.div
          className={`h-full ${barColor} rounded-full`}
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 1, ease: 'easeOut' }}
        />
      ) : (
        <div className={`h-full ${barColor} rounded-full`} style={{ width: `${percentage}%` }} />
      )}
    </div>
  );
}
