export interface KeyboardShortcut {
  keys: string;
  label: string;
  category: 'navigation' | 'actions' | 'general';
  action?: () => void;
}
