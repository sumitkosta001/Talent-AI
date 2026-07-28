'use client';

import React, { useState, useEffect } from 'react';
import { WifiOff, AlertTriangle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function OfflineState() {
  const [isOffline, setIsOffline] = useState(false);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    
    const handleOnline = () => setIsOffline(false);
    const handleOffline = () => setIsOffline(true);

    setIsOffline(!navigator.onLine);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return (
    <AnimatePresence>
      {isOffline && (
        <div className="fixed inset-0 z-[99999] flex items-center justify-center p-4 bg-slate-900/60 dark:bg-black/80 backdrop-blur-xs">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="bg-white dark:bg-[#1E293B] border border-slate-200 dark:border-slate-800 shadow-2xl rounded-3xl p-6 sm:p-8 max-w-sm w-full text-center space-y-4"
          >
            <div className="w-14 h-14 bg-amber-50 dark:bg-amber-950/30 text-amber-500 border border-amber-100 dark:border-amber-900/50 rounded-2xl flex items-center justify-center mx-auto animate-bounce">
              <WifiOff size={26} />
            </div>

            <div className="space-y-1.5">
              <h3 className="text-lg font-black text-slate-900 dark:text-slate-100">
                You are Offline
              </h3>
              <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
                Check your network connection. TalentAI will automatically restore your workspace when you connect.
              </p>
            </div>

            <div className="pt-2">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-amber-50 dark:bg-amber-950/20 text-[10px] sm:text-xs font-bold text-amber-700 dark:text-amber-400 rounded-full border border-amber-100 dark:border-amber-900/50">
                <AlertTriangle size={12} />
                Reconnecting...
              </span>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
