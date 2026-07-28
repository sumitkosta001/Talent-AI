'use client';

import React from 'react';
import { motion } from 'framer-motion';

interface FloatingButtonProps {
  icon: React.ReactNode;
  onClick: () => void;
  label?: string;
  className?: string;
}

export default function FloatingButton({
  icon,
  onClick,
  label,
  className = '',
}: FloatingButtonProps) {
  return (
    <motion.button
      whileHover={{ scale: 1.08 }}
      whileTap={{ scale: 0.92 }}
      onClick={onClick}
      className={`fixed bottom-6 right-6 z-[90] bg-blue-600 hover:bg-blue-700 text-white p-3.5 sm:px-5 sm:py-3 rounded-full shadow-2xl flex items-center gap-2 font-bold text-xs sm:text-sm cursor-pointer transition-colors ${className}`}
      aria-label={label || 'Quick Action'}
    >
      {icon}
      {label && <span className="hidden sm:inline">{label}</span>}
    </motion.button>
  );
}
