'use client';

import React from 'react';
import { DollarSign } from 'lucide-react';

interface SalaryCardProps {
  salary: string;
}

export default function SalaryCard({ salary }: SalaryCardProps) {
  return (
    <div className="bg-[#F8FAFC] border border-[#E2E8F0] p-4 rounded-xl flex items-center gap-3">
      <div className="w-10 h-10 rounded-lg bg-green-50 text-green-600 flex items-center justify-center flex-shrink-0">
        <DollarSign size={20} />
      </div>
      <div>
        <p className="text-base font-bold text-[#0F172A]">{salary}</p>
        <p className="text-[10px] text-[#64748B] font-semibold">Compensation Range</p>
      </div>
    </div>
  );
}
