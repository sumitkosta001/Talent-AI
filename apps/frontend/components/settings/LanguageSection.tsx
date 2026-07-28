'use client';

import React from 'react';
import { MOCK_LANGUAGES } from '@/mock/languages';
import { Globe } from 'lucide-react';

interface LanguageSectionProps {
  language?: string;
  onChange: (val: string) => void;
}

export default function LanguageSection({ language, onChange }: LanguageSectionProps) {
  if (!language) return null;

  return (
    <div className="space-y-4 text-left max-w-xs">
      <div>
        <label className="block text-xs font-bold text-[#475569] mb-1.5 flex items-center gap-1.5">
          <Globe size={14} className="text-[#64748B]" />
          Visual Display Language
        </label>
        <select
          value={language}
          onChange={(e) => onChange(e.target.value)}
          className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white cursor-pointer"
        >
          {MOCK_LANGUAGES.map(({ code, label }) => (
            <option key={code} value={code}>
              {label}
            </option>
          ))}
        </select>
        <p className="text-[10px] text-[#64748B] mt-1.5 leading-relaxed">
          Updates general menu parameters. Future integrations will deploy translated interface elements dynamically.
        </p>
      </div>
    </div>
  );
}
