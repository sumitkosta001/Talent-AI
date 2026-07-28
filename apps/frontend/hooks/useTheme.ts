'use client';

import { useTheme as useNextTheme } from 'next-themes';
import { useState, useEffect } from 'react';
import { ThemeSettings, Theme } from '@/types/theme';
import { ThemeService } from '@/services/theme.service';

export function useTheme() {
  const { theme, setTheme, resolvedTheme } = useNextTheme();
  const [settings, setSettingsState] = useState<ThemeSettings | null>(null);

  useEffect(() => {
    const activeSettings = ThemeService.getSettings();
    setSettingsState(activeSettings);
    if (activeSettings.theme) {
      setTheme(activeSettings.theme);
    }
    if (activeSettings.accessibility.highContrast) {
      document.documentElement.classList.add('high-contrast');
    } else {
      document.documentElement.classList.remove('high-contrast');
    }
  }, [setTheme]);

  const updateSettings = (newSettings: Partial<ThemeSettings>) => {
    setSettingsState((prev) => {
      if (!prev) return null;
      const updated = {
        ...prev,
        ...newSettings,
        accessibility: {
          ...prev.accessibility,
          ...(newSettings.accessibility || {}),
        },
      };
      ThemeService.saveSettings(updated);
      
      if (newSettings.theme) {
        setTheme(newSettings.theme);
      }

      if (newSettings.accessibility?.highContrast !== undefined) {
        if (newSettings.accessibility.highContrast) {
          document.documentElement.classList.add('high-contrast');
        } else {
          document.documentElement.classList.remove('high-contrast');
        }
      }

      return updated;
    });
  };

  return {
    theme: theme as Theme,
    resolvedTheme,
    setTheme: (t: Theme) => updateSettings({ theme: t }),
    settings,
    updateSettings,
  };
}
