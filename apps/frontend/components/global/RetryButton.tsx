'use client';

import React from 'react';
import { RefreshCw } from 'lucide-react';

interface RetryButtonProps {
  onRetry: () => void;
  loading?: boolean;
}

export default function RetryButton({ onRetry, loading = false }: RetryButtonProps) {
  return (
    <button
      onClick={onRetry}
      disabled={loading}
      className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-5 rounded-2xl shadow-sm transition-all disabled:opacity-50 cursor-pointer text-xs sm:text-sm"
    >
      <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
      <span>Retry Action</span>
    </button>
  );
}
