'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export function useKeyboardShortcuts(actions: {
  toggleCommandPalette: () => void;
  toggleShortcutsHelp: () => void;
}) {
  const router = useRouter();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Check command palette: Ctrl + K or Cmd + K
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        actions.toggleCommandPalette();
      }

      // Check shortcuts helper: Ctrl + / or Cmd + /
      if ((e.ctrlKey || e.metaKey) && e.key === '/') {
        e.preventDefault();
        actions.toggleShortcutsHelp();
      }

      // Navigation shortcuts (Alt key bindings)
      if (e.altKey) {
        switch (e.key.toLowerCase()) {
          case 'h':
            e.preventDefault();
            router.push('/candidate');
            break;
          case 'j':
            e.preventDefault();
            router.push('/candidate/jobs');
            break;
          case 'a':
            e.preventDefault();
            router.push('/candidate/applications');
            break;
          case 'n':
            e.preventDefault();
            router.push('/candidate/notifications');
            break;
          case 'p':
            e.preventDefault();
            router.push('/candidate/profile');
            break;
          case 's':
            e.preventDefault();
            router.push('/candidate/settings');
            break;
          case 'r':
            e.preventDefault();
            router.push('/candidate/resume');
            break;
          case 'i':
            e.preventDefault();
            router.push('/candidate/ai/resume-builder');
            break;
          default:
            break;
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [actions, router]);
}
