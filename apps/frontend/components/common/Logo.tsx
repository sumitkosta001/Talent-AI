import React from 'react';
import { Bot } from 'lucide-react';

interface LogoProps {
  lightText?: boolean;
}

export default function Logo({ lightText = false }: LogoProps) {
  return (
    <div className="flex items-center gap-2">
      <div className="w-8 h-8 bg-[#2563EB] rounded-lg flex items-center justify-center">
        <Bot size={16} className="text-white" />
      </div>
      <span className={`font-bold text-lg ${lightText ? 'text-white' : 'text-[#0F172A]'}`}>
        TalentAI
      </span>
    </div>
  );
}
