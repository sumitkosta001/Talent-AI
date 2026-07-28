'use client';

import React from 'react';
import { motion } from 'framer-motion';

interface HoverCardProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
}

export default function HoverCard({ children, className = '', onClick }: HoverCardProps) {
  return (
    <motion.div
      whileHover={{ y: -4, scale: 1.01 }}
      whileTap={{ scale: 0.99 }}
      transition={{ duration: 0.2, ease: 'easeInOut' }}
      onClick={onClick}
      className={`transition-shadow hover:shadow-xl cursor-pointer ${className}`}
    >
      {children}
    </motion.div>
  );
}
