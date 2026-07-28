'use client';

import { useState, useEffect } from 'react';
import { ToastItem } from '@/types/toast';
import { ToastService } from '@/services/toast.service';

export function useToast() {
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  useEffect(() => {
    return ToastService.subscribe((currentToasts) => {
      setToasts(currentToasts);
    });
  }, []);

  return {
    toasts,
    success: (msg: string, desc?: string, dur?: number, undo?: () => void) =>
      ToastService.success(msg, desc, dur, undo),
    error: (msg: string, desc?: string, dur?: number) => ToastService.error(msg, desc, dur),
    warning: (msg: string, desc?: string, dur?: number) => ToastService.warning(msg, desc, dur),
    info: (msg: string, desc?: string, dur?: number) => ToastService.info(msg, desc, dur),
    loading: (msg: string, desc?: string) => ToastService.loading(msg, desc),
    dismiss: (id: string) => ToastService.dismiss(id),
    clear: () => ToastService.clear(),
  };
}
