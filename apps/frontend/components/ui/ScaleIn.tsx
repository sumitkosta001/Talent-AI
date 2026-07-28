'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { scaleInVariants } from '@/utils/animation';
import { useReducedMotion } from '@/hooks/useReducedMotion';

interface ScaleInProps {
  children: React.ReactNode;
  delay?: number;
  className?: string;
}

export default function ScaleIn({ children, delay = 0, className = '' }: ScaleInProps) {
  const shouldReduceMotion = useReducedMotion();

  if (shouldReduceMotion) {
    return <div className={className}>{children}</div>;
  }

  return (
    <motion.div
      variants={scaleInVariants}
      initial="hidden"
      animate="visible"
      exit="exit"
      transition={{ delay }}
      className={className}
    >
      {children}
    </motion.div>
  );
}
