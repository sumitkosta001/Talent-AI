'use client';

import React from 'react';

interface SettingsCardProps {
  title: string;
  description: string;
  children: React.ReactNode;
}

export default function SettingsCard({ title, description, children }: SettingsCardProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 sm:p-6 shadow-sm space-y-4 text-left">
      <div className="border-b border-[#F1F5F9] pb-3.5">
        <h3 className="font-bold text-[#0F172A] text-sm sm:text-base">{title}</h3>
        <p className="text-xs text-[#64748B] mt-0.5 leading-relaxed">{description}</p>
      </div>
      <div className="pt-1">{children}</div>
    </div>
  );
}
