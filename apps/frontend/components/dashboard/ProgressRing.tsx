'use client';

import React from 'react';
import { motion } from 'framer-motion';

interface ProgressRingProps {
  radius?: number;
  strokeWidth?: number;
  percentage: number;
  color?: string;
}

export default function ProgressRing({
  radius = 16,
  strokeWidth = 3.5,
  percentage,
  color = '#3B82F6',
}: ProgressRingProps) {
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (Math.min(100, Math.max(0, percentage)) / 100) * circumference;

  return (
    <div className="relative flex items-center justify-center">
      <svg className="w-11 h-11 transform -rotate-90">
        <circle
          cx="22"
          cy="22"
          r={radius}
          className="text-slate-100 stroke-current"
          strokeWidth={strokeWidth}
          fill="transparent"
        />
        <motion.circle
          cx="22"
          cy="22"
          r={radius}
          className="stroke-current"
          strokeWidth={strokeWidth}
          fill="transparent"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 0.6 }}
          style={{ color }}
        />
      </svg>
      <span className="absolute text-[10px] font-black text-[#0F172A]">{percentage}%</span>
    </div>
  );
}
