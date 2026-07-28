export interface MockShortcutItem {
  keys: string;
  label: string;
  category: 'general' | 'navigation' | 'actions';
}

export const MOCK_SHORTCUTS: MockShortcutItem[] = [
  // General
  { keys: 'Ctrl + K', label: 'Open Command Palette', category: 'general' },
  { keys: 'Ctrl + /', label: 'Show Keyboard Shortcuts Help', category: 'general' },
  { keys: 'Esc', label: 'Close Active Dialog or Menu', category: 'general' },
  
  // Navigation Shortcuts
  { keys: 'Alt + H', label: 'Navigate to Dashboard Home', category: 'navigation' },
  { keys: 'Alt + J', label: 'Browse Jobs List', category: 'navigation' },
  { keys: 'Alt + A', label: 'Open Applications Dashboard', category: 'navigation' },
  { keys: 'Alt + N', label: 'Open Notifications Center', category: 'navigation' },
  { keys: 'Alt + P', label: 'Edit Candidate Profile Page', category: 'navigation' },
  { keys: 'Alt + S', label: 'Open Settings Portal', category: 'navigation' },
  { keys: 'Alt + R', label: 'Open Resume Module', category: 'navigation' },
  { keys: 'Alt + I', label: 'Open Flagship AI Career Tools', category: 'navigation' },
];
