'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Bookmark, BookmarkPlus } from 'lucide-react';
import { useBookmarks } from '@/hooks/useBookmarks';

interface BookmarkButtonProps {
  jobId: string;
  size?: number;
}

export default function BookmarkButton({ jobId, size = 16 }: BookmarkButtonProps) {
  const { isBookmarked, toggleBookmark } = useBookmarks();
  const active = isBookmarked(jobId);

  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    toggleBookmark(jobId);
  };

  return (
    <motion.button
      whileTap={{ scale: 0.9 }}
      onClick={handleClick}
      className={`p-2 rounded-xl border transition-colors cursor-pointer ${
        active
          ? 'bg-blue-50 text-[#2563EB] border-blue-100'
          : 'bg-white text-[#94A3B8] border-[#E2E8F0] hover:text-[#64748B]'
      }`}
    >
      {active ? <Bookmark size={size} /> : <BookmarkPlus size={size} />}
    </motion.button>
  );
}
