'use client';

import React, { useRef, useEffect } from 'react';
import { useCommandPalette } from '@/hooks/useCommandPalette';
import { useTheme } from '@/hooks/useTheme';
import { useRouter } from 'next/navigation';
import { Search, Loader2, Navigation, Activity, Sparkles, Monitor, Sun, Moon, LogOut, Keyboard } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  onShowShortcuts: () => void;
}

export default function CommandPalette({ isOpen, onClose, onShowShortcuts }: CommandPaletteProps) {
  const { query, setQuery, commands, loading } = useCommandPalette();
  const { setTheme } = useTheme();
  const router = useRouter();
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isOpen]);

  const getCommandIcon = (cat: string, actionId?: string) => {
    if (actionId === 'logout') return LogOut;
    if (actionId === 'show-shortcuts') return Keyboard;
    if (actionId?.startsWith('set-theme')) {
      if (actionId.endsWith('light')) return Sun;
      if (actionId.endsWith('dark')) return Moon;
      return Monitor;
    }
    if (cat === 'tools') return Sparkles;
    if (cat === 'settings') return Activity;
    return Navigation;
  };

  const handleCommandSelect = (cmd: any) => {
    onClose();
    if (cmd.route) {
      router.push(cmd.route);
    } else if (cmd.actionId) {
      switch (cmd.actionId) {
        case 'logout':
          alert('Logging out...');
          router.push('/login');
          break;
        case 'show-shortcuts':
          onShowShortcuts();
          break;
        case 'set-theme-light':
          setTheme('light');
          break;
        case 'set-theme-dark':
          setTheme('dark');
          break;
        case 'set-theme-system':
          setTheme('system');
          break;
        default:
          break;
      }
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[999] flex items-start justify-center pt-[15vh] p-4 text-left">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-slate-900/40 dark:bg-black/60 backdrop-blur-xs"
          />

          <motion.div
            initial={{ opacity: 0, scale: 0.97, y: -10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.97, y: -10 }}
            transition={{ duration: 0.15 }}
            className="bg-white dark:bg-[#1E293B] border border-slate-200 dark:border-slate-800 shadow-2xl rounded-2xl w-full max-w-xl overflow-hidden relative z-10 flex flex-col max-h-[55vh]"
          >
            <div className="relative border-b border-slate-200 dark:border-slate-800 flex items-center p-4">
              <Search size={18} className="text-slate-400 dark:text-slate-500 mr-3 flex-shrink-0" />
              <input
                ref={inputRef}
                type="text"
                placeholder="Type a command or search actions..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full text-slate-950 dark:text-white bg-transparent text-sm sm:text-base border-none focus:outline-none"
              />
              {loading && (
                <Loader2 size={16} className="text-slate-400 animate-spin flex-shrink-0" />
              )}
            </div>

            <div className="flex-1 overflow-y-auto p-3 space-y-3">
              {commands.length === 0 ? (
                <p className="text-center text-xs text-slate-400 dark:text-slate-500 py-6">
                  No commands matching "{query}"
                </p>
              ) : (
                <div className="space-y-1">
                  {commands.map((cmd) => {
                    const Icon = getCommandIcon(cmd.category, cmd.actionId);
                    return (
                      <button
                        key={cmd.id}
                        onClick={() => handleCommandSelect(cmd)}
                        className="w-full p-2.5 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-xl flex items-center justify-between cursor-pointer transition-colors group text-left"
                      >
                        <div className="flex items-center gap-2.5 min-w-0">
                          <div className="w-7 h-7 rounded-lg border border-slate-200 dark:border-slate-800 flex items-center justify-center flex-shrink-0 text-slate-400 dark:text-slate-500 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors bg-slate-50 dark:bg-slate-800/40">
                            <Icon size={14} />
                          </div>
                          <span className="text-xs sm:text-sm font-bold text-slate-700 dark:text-slate-200 group-hover:text-slate-900 dark:group-hover:text-white truncate">
                            {cmd.title}
                          </span>
                        </div>
                        {cmd.shortcut && (
                          <span className="text-[10px] font-black text-slate-400 dark:text-slate-500 bg-slate-100 dark:bg-slate-800 px-2 py-0.5 rounded border border-slate-200 dark:border-slate-700">
                            {cmd.shortcut}
                          </span>
                        )}
                      </button>
                    );
                  })}
                </div>
              )}
            </div>

            <div className="bg-slate-50 dark:bg-[#151D2A] px-4 py-2 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between text-[10px] text-slate-400">
              <span>Press Esc to exit palette</span>
              <span>Linear Style Menu</span>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
