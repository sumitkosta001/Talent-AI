'use client';

import { useState, useEffect } from 'react';
import { MockCommand } from '@/mock/commandPalette';
import { CommandPaletteService } from '@/services/commandPalette.service';

export function useCommandPalette() {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [commands, setCommands] = useState<MockCommand[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let active = true;
    const fetchCommands = async () => {
      setLoading(true);
      try {
        const items = await CommandPaletteService.getCommands(query);
        if (active) {
          setCommands(items);
        }
      } catch (err) {
        console.error(err);
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    };

    fetchCommands();

    return () => {
      active = false;
    };
  }, [query]);

  return {
    isOpen,
    setIsOpen,
    query,
    setQuery,
    commands,
    loading,
  };
}
