'use client';

import React from 'react';

interface JobDescriptionProps {
  description: string;
}

export default function JobDescription({ description }: JobDescriptionProps) {
  return (
    <div className="space-y-2 text-left">
      <h3 className="font-bold text-sm text-[#0F172A] uppercase tracking-wide">About The Role</h3>
      <p className="text-xs sm:text-sm text-[#64748B] leading-relaxed">{description}</p>
    </div>
  );
}
