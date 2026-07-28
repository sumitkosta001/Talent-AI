'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { slideInVariants } from '@/utils/animation';
import { useReducedMotion } from '@/hooks/useReducedMotion';

interface SlideInProps {
  children: React.ReactNode;
  direction?: 'left' | 'right' | 'up' | 'down';
  delay?: number;
  className?: string;
}

export default function SlideIn({
  children,
  direction = 'left',
  delay = 0,
  className = '',
}: SlideInProps) {
  const shouldReduceMotion = useReducedMotion();

  if (shouldReduceMotion) {
    return <div className={className}>{children}</div>;
  }

  return (
    <motion.div
      variants={slideInVariants(direction)}
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
