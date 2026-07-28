import { ToastItem } from '@/types/toast';

type ToastListener = (toasts: ToastItem[]) => void;

class ToastServiceClass {
  private toasts: ToastItem[] = [];
  private listeners: Set<ToastListener> = new Set();

  subscribe(listener: ToastListener): () => void {
    this.listeners.add(listener);
    listener([...this.toasts]);
    return () => {
      this.listeners.delete(listener);
    };
  }

  private notify() {
    this.listeners.forEach((l) => l([...this.toasts]));
  }

  show(
    type: ToastItem['type'],
    message: string,
    description?: string,
    duration = 4000,
    undoAction?: () => void
  ) {
    const id = `toast-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
    const item: ToastItem = { id, type, message, description, duration, undoAction };
    this.toasts.push(item);
    this.notify();

    if (duration > 0) {
      setTimeout(() => {
        this.dismiss(id);
      }, duration);
    }
    return id;
  }

  success(message: string, description?: string, duration?: number, undoAction?: () => void) {
    return this.show('success', message, description, duration, undoAction);
  }

  error(message: string, description?: string, duration?: number) {
    return this.show('error', message, description, duration);
  }

  warning(message: string, description?: string, duration?: number) {
    return this.show('warning', message, description, duration);
  }

  info(message: string, description?: string, duration?: number) {
    return this.show('info', message, description, duration);
  }

  loading(message: string, description?: string, duration = 0) {
    return this.show('loading', message, description, duration);
  }

  dismiss(id: string) {
    this.toasts = this.toasts.filter((t) => t.id !== id);
    this.notify();
  }

  clear() {
    this.toasts = [];
    this.notify();
  }
}

export const ToastService = new ToastServiceClass();
