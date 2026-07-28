export interface ToastItem {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info' | 'loading';
  message: string;
  description?: string;
  duration?: number;
  undoAction?: () => void;
}
