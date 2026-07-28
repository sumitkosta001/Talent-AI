import { Variants } from 'framer-motion';

export const fadeInVariants: Variants = {
  hidden: { opacity: 0, y: 12 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.3, ease: [0.16, 1, 0.3, 1] },
  },
  exit: {
    opacity: 0,
    y: 8,
    transition: { duration: 0.2, ease: 'easeIn' },
  },
};

export const slideInVariants = (direction: 'left' | 'right' | 'up' | 'down' = 'left'): Variants => {
  const distance = 24;
  const x = direction === 'left' ? -distance : direction === 'right' ? distance : 0;
  const y = direction === 'up' ? -distance : direction === 'down' ? distance : 0;

  return {
    hidden: { opacity: 0, x, y },
    visible: {
      opacity: 1,
      x: 0,
      y: 0,
      transition: { duration: 0.35, ease: [0.16, 1, 0.3, 1] },
    },
    exit: {
      opacity: 0,
      x: -x,
      y: -y,
      transition: { duration: 0.2, ease: 'easeIn' },
    },
  };
};

export const scaleInVariants: Variants = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.25, ease: [0.16, 1, 0.3, 1] },
  },
  exit: {
    opacity: 0,
    scale: 0.95,
    transition: { duration: 0.15, ease: 'easeIn' },
  },
};

export const staggerContainerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.06,
      delayChildren: 0.05,
    },
  },
};
