'use client';

import { useTheme as useNextTheme } from 'next-themes';
import { useState, useEffect, useContext } from 'react';
import { ThemeSettingsContext } from '@/providers/ThemeProvider';
import { Theme } from '@/types/theme';

export function useTheme() {
  const { theme, setTheme, resolvedTheme } = useNextTheme();
  const context = useContext(ThemeSettingsContext);
  const [mounted, setMounted] = useState(false);

  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }

  const { settings, updateSettings } = context;

  // Load mount state
  useEffect(() => {
    setMounted(true);
  }, []);

  // Keep next-themes theme in sync with settings theme
  useEffect(() => {
    if (!mounted || !settings || theme === undefined) return;

    if (settings.theme && theme !== settings.theme) {
      setTheme(settings.theme);
    }
  }, [mounted, settings?.theme, theme, setTheme]);

  return {
    theme: theme as Theme,
    resolvedTheme,
    setTheme: (t: Theme) => updateSettings({ theme: t }),
    settings,
    updateSettings,
  };
}

