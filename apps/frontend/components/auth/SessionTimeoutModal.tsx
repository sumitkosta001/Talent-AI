'use client';

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Clock, LogOut, RefreshCw } from 'lucide-react';
import { useRouter } from 'next/navigation';

interface SessionTimeoutModalProps {
  isOpen: boolean;
  secondsRemaining: number;
  onStayLoggedIn: () => void;
}

export default function SessionTimeoutModal({
  isOpen,
  secondsRemaining,
  onStayLoggedIn,
}: SessionTimeoutModalProps) {
  const router = useRouter();

  const handleLogout = () => {
    router.push('/session-expired');
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-slate-900/60 dark:bg-black/80 backdrop-blur-xs">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="bg-white dark:bg-[#1E293B] border border-slate-200 dark:border-slate-800 shadow-2xl rounded-3xl p-6 sm:p-8 max-w-sm w-full text-center space-y-5"
          >
            <div className="w-14 h-14 bg-amber-50 dark:bg-amber-950/30 text-amber-500 border border-amber-100 dark:border-amber-900/50 rounded-2xl flex items-center justify-center mx-auto animate-bounce">
              <Clock size={28} />
            </div>

            <div className="space-y-1.5">
              <h3 className="text-lg font-black text-slate-900 dark:text-slate-100">
                Session Inactivity Warning
              </h3>
              <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
                Your session will expire due to inactivity in:
              </p>
              <div className="text-3xl font-black text-amber-500 font-mono py-1">
                {secondsRemaining}s
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-2 pt-2 border-t border-slate-100 dark:border-slate-800">
              <button
                onClick={onStayLoggedIn}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2.5 px-4 rounded-xl shadow-sm text-xs sm:text-sm transition-colors cursor-pointer flex items-center justify-center gap-1.5"
              >
                <RefreshCw size={14} />
                Stay Logged In
              </button>
              <button
                onClick={handleLogout}
                className="border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-300 font-bold py-2.5 px-4 rounded-xl text-xs sm:text-sm transition-colors cursor-pointer flex items-center justify-center gap-1.5"
              >
                <LogOut size={14} />
                Logout
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
