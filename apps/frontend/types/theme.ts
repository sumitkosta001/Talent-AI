export type Theme = 'light' | 'dark' | 'system';

export interface ThemeSettings {
  theme: Theme;
  animations: boolean;
  reducedMotion: boolean;
  language: string;
  accessibility: {
    highContrast: boolean;
    fontSize: 'normal' | 'large' | 'xlarge';
    screenReader: boolean;
  };
}
