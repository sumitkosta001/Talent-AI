import React from 'react';
import Link from 'next/link';
import { Upload } from 'lucide-react';

export default function CandidateHeader() {
  return (
    <div className="flex items-center justify-between">
      <div>
        <h1 className="text-xl font-bold text-[#0F172A]">Good morning, Alex 👋</h1>
        <p className="text-sm text-[#64748B] mt-0.5">Here's what's happening with your job search</p>
      </div>
      <Link
        href="/candidate/resume/upload"
        className="flex items-center gap-2 bg-[#2563EB] text-white px-4 py-2 rounded-xl text-sm font-medium hover:bg-[#1D4ED8] transition-colors"
      >
        <Upload size={15} />
        Update Resume
      </Link>
    </div>
  );
}
