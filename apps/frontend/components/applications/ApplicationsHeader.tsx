'use client';

import React from 'react';

interface ApplicationsHeaderProps {
  totalCount: number;
  offersCount: number;
}

export default function ApplicationsHeader({ totalCount, offersCount }: ApplicationsHeaderProps) {
  return (
    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#E2E8F0] pb-5 text-left">
      <div>
        <h1 className="text-xl sm:text-2xl font-bold text-[#0F172A]">My Applications</h1>
        <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">
          Track and manage your submitted applications, interviews, and active offer letters.
        </p>
      </div>
      {offersCount > 0 && (
        <span className="bg-emerald-50 text-emerald-700 border border-emerald-100 text-xs font-bold px-3.5 py-2 rounded-xl animate-pulse">
          🎉 You have {offersCount} Active Offer{offersCount > 1 ? 's' : ''}!
        </span>
      )}
    </div>
  );
}
