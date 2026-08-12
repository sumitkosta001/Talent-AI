'use client';

import { createContext, useState, useEffect } from 'react';
import { ThemeProvider as NextThemesProvider } from 'next-themes';
import { ThemeSettings } from '@/types/theme';
import { ThemeService } from '@/services/theme.service';

interface ThemeSettingsContextType {
  settings: ThemeSettings | null;
  updateSettings: (newSettings: Partial<ThemeSettings>) => void;
}

export const ThemeSettingsContext = createContext<ThemeSettingsContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [settings, setSettingsState] = useState<ThemeSettings | null>(null);

  // Load settings on mount
  useEffect(() => {
    const activeSettings = ThemeService.getSettings();
    setSettingsState(activeSettings);
  }, []);

  // Sync settings and accessibility class to DOM/localStorage
  useEffect(() => {
    if (!settings) return;

    ThemeService.saveSettings(settings);

    if (settings.accessibility.highContrast) {
      document.documentElement.classList.add('high-contrast');
    } else {
      document.documentElement.classList.remove('high-contrast');
    }
  }, [settings]);

  const updateSettings = (newSettings: Partial<ThemeSettings>) => {
    setSettingsState((prev) => {
      if (!prev) return null;
      return {
        ...prev,
        ...newSettings,
        accessibility: {
          ...prev.accessibility,
          ...(newSettings.accessibility || {}),
        },
      };
    });
  };

  return (
    <ThemeSettingsContext.Provider value={{ settings, updateSettings }}>
      <NextThemesProvider
        attribute="class"
        defaultTheme="system"
        enableSystem
        disableTransitionOnChange
      >
        {children}
      </NextThemesProvider>
    </ThemeSettingsContext.Provider>
  );
}
