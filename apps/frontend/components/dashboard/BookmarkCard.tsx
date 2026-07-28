'use client';

import React from 'react';
import { BookmarkItem } from '@/types/bookmark';
import { ExternalLink, X } from 'lucide-react';
import { motion } from 'framer-motion';
import Link from 'next/link';

interface BookmarkCardProps {
  item: BookmarkItem;
  getBookmarkIcon: (type: BookmarkItem['type']) => { icon: any; color: string };
  onRemove: (id: string) => void;
}

export default function BookmarkCard({ item, getBookmarkIcon, onRemove }: BookmarkCardProps) {
  const config = getBookmarkIcon(item.type);
  const Icon = config.icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: 5 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -5 }}
      className="p-3 bg-[#F8FAFC] border border-[#E2E8F0] rounded-2xl flex items-center justify-between gap-3 group hover:shadow-sm hover:bg-white transition-all text-left w-full"
    >
      <div className="flex gap-3 min-w-0">
        <div className={`w-9 h-9 rounded-xl flex items-center justify-center border flex-shrink-0 ${config.color}`}>
          <Icon size={16} />
        </div>
        <div className="min-w-0">
          <h4 className="font-extrabold text-[#0F172A] text-xs sm:text-sm truncate">
            {item.title}
          </h4>
          <p className="text-[11px] text-[#64748B] font-medium truncate mt-0.5">
            {item.subtitle}
          </p>
          <span className="text-[9px] text-[#94A3B8] font-bold mt-1 block uppercase tracking-wide">
            Saved: {item.savedDate}
          </span>
        </div>
      </div>

      <div className="flex items-center gap-1.5 flex-shrink-0">
        <Link href={item.url}>
          <button className="p-1.5 border border-[#E2E8F0] hover:bg-slate-50 text-[#64748B] hover:text-[#0F172A] rounded-xl transition-all">
            <ExternalLink size={13} />
          </button>
        </Link>
        <button
          onClick={() => onRemove(item.id)}
          className="p-1.5 hover:bg-red-50 text-[#94A3B8] hover:text-red-600 rounded-xl transition-all"
        >
          <X size={13} />
        </button>
      </div>
    </motion.div>
  );
}
