'use client';

import React from 'react';
import Link from 'next/link';
import { HelpCircle } from 'lucide-react';

export default function EmptyApplications() {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-12 text-center shadow-sm space-y-4 max-w-lg mx-auto mt-6">
      <div className="w-12 h-12 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mx-auto">
        <HelpCircle size={24} />
      </div>
      <div>
        <h3 className="font-bold text-[#0F172A] text-lg">No applications submitted</h3>
        <p className="text-sm text-[#64748B] mt-1 leading-relaxed">
          You haven't applied for any positions yet. Explore open roles on the job portal and start submitting.
        </p>
      </div>
      <Link
        href="/candidate/jobs"
        className="bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-semibold text-xs px-4 py-2.5 rounded-xl transition-colors inline-block cursor-pointer"
      >
        Browse Jobs
      </Link>
    </div>
  );
}
