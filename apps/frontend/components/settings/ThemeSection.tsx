'use client';

import React from 'react';
import { MOCK_THEMES } from '@/mock/themes';
import { Sun, Moon, Laptop } from 'lucide-react';

interface ThemeSectionProps {
  theme?: 'Light' | 'Dark' | 'System';
  onChange: (val: 'Light' | 'Dark' | 'System') => void;
}

export default function ThemeSection({ theme, onChange }: ThemeSectionProps) {
  if (!theme) return null;

  const getIcon = (id: string) => {
    switch (id) {
      case 'Light':
        return <Sun size={16} className="text-amber-500" />;
      case 'Dark':
        return <Moon size={16} className="text-blue-500" />;
      default:
        return <Laptop size={16} className="text-slate-500" />;
    }
  };

  return (
    <div className="grid sm:grid-cols-3 gap-4 text-left">
      {MOCK_THEMES.map(({ id, label, description }) => {
        const isActive = theme === id;
        return (
          <button
            key={id}
            type="button"
            onClick={() => onChange(id as any)}
            className={`
              p-4 border rounded-2xl text-left cursor-pointer transition-all flex flex-col justify-between min-h-[110px] hover:shadow-sm
              ${isActive
                ? 'border-[#2563EB] bg-blue-50/10 ring-2 ring-blue-500/20'
                : 'border-[#E2E8F0] bg-white hover:border-slate-300'
              }
            `}
          >
            <div className="flex items-center justify-between w-full">
              <span className="text-xs font-bold text-[#0F172A]">{label}</span>
              <div className="p-1 rounded bg-[#F8FAFC]">
                {getIcon(id)}
              </div>
            </div>
            <p className="text-[10px] text-[#64748B] mt-3 leading-relaxed">{description}</p>
          </button>
        );
      })}
    </div>
  );
}
