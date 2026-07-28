'use client';

import React from 'react';
import SessionExpiredCard from '@/components/auth/SessionExpiredCard';

export default function Page() {
  return (
    <div className="min-h-screen bg-[#F8FAFC] dark:bg-[#090D16] flex items-center justify-center p-6 text-center">
      <SessionExpiredCard />
    </div>
  );
}
