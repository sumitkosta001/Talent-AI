'use client';

import React, { useState } from 'react';
import { ThemeProvider } from '@/providers/ThemeProvider';
import ToastProvider from './ToastProvider';
import OfflineState from './OfflineState';
import ProgressBar from './ProgressBar';
import CommandPalette from './CommandPalette';
import ShortcutModal from './ShortcutModal';
import GlobalSearch from './GlobalSearch';
import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts';

export default function ClientShell({ children }: { children: React.ReactNode }) {
  const [commandPaletteOpen, setCommandPaletteOpen] = useState(false);
  const [shortcutsHelpOpen, setShortcutsHelpOpen] = useState(false);
  const [globalSearchOpen, setGlobalSearchOpen] = useState(false);

  // Register system-wide shortcuts
  useKeyboardShortcuts({
    toggleCommandPalette: () => setCommandPaletteOpen((prev) => !prev),
    toggleShortcutsHelp: () => setShortcutsHelpOpen((prev) => !prev),
  });

  return (
    <ThemeProvider>
      {/* Toast notifications alerts */}
      <ToastProvider />

      {/* Network offline triggers */}
      <OfflineState />

      {/* Page transitions progress bar */}
      <React.Suspense fallback={null}>
        <ProgressBar />
      </React.Suspense>


      {/* Command Palette (Ctrl+K) */}
      <CommandPalette
        isOpen={commandPaletteOpen}
        onClose={() => setCommandPaletteOpen(false)}
        onShowShortcuts={() => {
          setCommandPaletteOpen(false);
          setShortcutsHelpOpen(true);
        }}
      />

      {/* Keyboard Shortcuts Help (Ctrl+/) */}
      <ShortcutModal
        isOpen={shortcutsHelpOpen}
        onClose={() => setShortcutsHelpOpen(false)}
      />

      {/* Global Search dialog trigger */}
      <GlobalSearch
        isOpen={globalSearchOpen}
        onClose={() => setGlobalSearchOpen(false)}
      />

      {/* Provide an easy way for custom components to trigger global search via custom event */}
      <div
        style={{ display: 'none' }}
        id="talentai-search-trigger"
        onClick={() => setGlobalSearchOpen(true)}
      />

      {children}
    </ThemeProvider>
  );
}
