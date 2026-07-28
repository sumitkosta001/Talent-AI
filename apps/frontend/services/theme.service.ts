import { ThemeSettings, Theme } from '@/types/theme';

const THEME_SETTINGS_KEY = 'talentai_theme_settings';

const DEFAULT_SETTINGS: ThemeSettings = {
  theme: 'system',
  animations: true,
  reducedMotion: false,
  language: 'en',
  accessibility: {
    highContrast: false,
    fontSize: 'normal',
    screenReader: false,
  },
};

export class ThemeService {
  static getSettings(): ThemeSettings {
    if (typeof window === 'undefined') return DEFAULT_SETTINGS;
    const stored = localStorage.getItem(THEME_SETTINGS_KEY);
    if (!stored) return DEFAULT_SETTINGS;
    try {
      return JSON.parse(stored);
    } catch {
      return DEFAULT_SETTINGS;
    }
  }

  static saveSettings(settings: ThemeSettings): void {
    if (typeof window === 'undefined') return;
    localStorage.setItem(THEME_SETTINGS_KEY, JSON.stringify(settings));
  }

  static applyTheme(theme: Theme): void {
    if (typeof window === 'undefined') return;
    const root = window.document.documentElement;
    root.classList.remove('light', 'dark');

    if (theme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      root.classList.add(systemTheme);
    } else {
      root.classList.add(theme);
    }
  }
}
