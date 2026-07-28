'use client';

import React from 'react';
import { LucideIcon } from 'lucide-react';
import { motion } from 'framer-motion';

interface StatCardProps {
  label: string;
  value: string | number;
  icon: LucideIcon;
  color: string;
}

export default function StatCard({ label, value, icon: Icon, color }: StatCardProps) {
  return (
    <motion.div
      whileHover={{ y: -3, scale: 1.02 }}
      transition={{ type: 'spring', stiffness: 300, damping: 20 }}
      className="bg-white rounded-2xl border border-[#E2E8F0] p-4 flex flex-col justify-between hover:shadow-md transition-shadow cursor-default text-left"
    >
      <div className="flex items-center justify-between gap-2.5">
        <span className="text-xs font-bold text-[#64748B] tracking-tight truncate">
          {label}
        </span>
        <div className={`w-8 h-8 rounded-xl flex items-center justify-center border flex-shrink-0 ${color}`}>
          <Icon size={16} />
        </div>
      </div>
      <div className="mt-4">
        <h3 className="text-xl sm:text-2xl font-black text-[#0F172A] tracking-tight leading-none">
          {value}
        </h3>
      </div>
    </motion.div>
  );
}
