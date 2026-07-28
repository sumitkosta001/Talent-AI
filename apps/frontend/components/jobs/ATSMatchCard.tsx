'use client';

import React from 'react';
import Link from 'next/link';
import { Bot, ArrowRight } from 'lucide-react';

interface ATSMatchCardProps {
  score: number;
}

export default function ATSMatchCard({ score }: ATSMatchCardProps) {
  return (
    <div className="bg-violet-50/50 border border-violet-200 p-5 rounded-2xl text-left space-y-3">
      <div className="flex items-center gap-2 text-violet-700">
        <Bot size={18} />
        <h4 className="font-bold text-sm">AI Resume Parser Compatibility</h4>
      </div>
      
      <p className="text-xs text-[#64748B] leading-relaxed">
        Our resume auditor scanned your profile and estimated an ATS parser match of <strong className="text-violet-800">{score}%</strong>.
      </p>

      <Link
        href="/candidate/ats"
        className="inline-flex items-center gap-1 text-xs font-bold text-violet-700 hover:text-violet-950 transition-colors cursor-pointer"
      >
        View Complete ATS Score Audit Report
        <ArrowRight size={13} />
      </Link>
    </div>
  );
}
