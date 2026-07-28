'use client';

import React from 'react';
import { motion } from 'framer-motion';

interface ToggleSettingProps {
  label: string;
  description: string;
  checked: boolean;
  onChange: (val: boolean) => void;
}

export default function ToggleSetting({ label, description, checked, onChange }: ToggleSettingProps) {
  return (
    <div className="flex items-start justify-between gap-4 py-2 border-b border-[#F8FAFC] last:border-b-0 text-left">
      <div className="space-y-0.5">
        <span className="text-xs sm:text-sm font-bold text-[#0F172A]">{label}</span>
        <p className="text-[10px] sm:text-xs text-[#64748B] leading-relaxed">{description}</p>
      </div>

      <button
        type="button"
        onClick={() => onChange(!checked)}
        className={`
          w-10 h-6 rounded-full p-0.5 transition-colors duration-200 focus:outline-none flex-shrink-0 cursor-pointer
          ${checked ? 'bg-[#2563EB]' : 'bg-[#E2E8F0]'}
        `}
      >
        <motion.div
          layout
          className="w-5 h-5 bg-white rounded-full shadow-sm"
          animate={{ x: checked ? 16 : 0 }}
          transition={{ type: 'spring', stiffness: 500, damping: 30 }}
        />
      </button>
    </div>
  );
}
