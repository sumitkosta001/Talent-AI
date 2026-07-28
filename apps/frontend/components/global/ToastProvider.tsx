'use client';

import React from 'react';
import { AnimatePresence } from 'framer-motion';
import { useToast } from '@/hooks/useToast';
import Toast from './Toast';

export default function ToastProvider() {
  const { toasts, dismiss } = useToast();

  return (
    <div className="fixed top-4 right-4 z-[9999] flex flex-col gap-2 w-full max-w-sm pointer-events-none">
      <AnimatePresence mode="popLayout">
        {toasts.map((toast) => (
          <Toast key={toast.id} toast={toast} onDismiss={dismiss} />
        ))}
      </AnimatePresence>
    </div>
  );
}
