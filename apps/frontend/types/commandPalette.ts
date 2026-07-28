import { LucideIcon } from 'lucide-react';

export interface CommandPaletteItem {
  id: string;
  title: string;
  subtitle?: string;
  icon: LucideIcon;
  shortcut?: string;
  category: 'pages' | 'actions' | 'tools' | 'settings';
  action: () => void;
}
