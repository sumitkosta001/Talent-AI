'use client';

import React from 'react';
import { Company } from '@/types/company';

interface CompanyStatsProps {
  company: Company;
}

export default function CompanyStats({ company }: CompanyStatsProps) {
  return (
    <div className="grid grid-cols-3 gap-4 pt-1">
      <div className="bg-[#F8FAFC] border border-[#E2E8F0] p-3.5 rounded-xl text-center">
        <p className="text-sm font-bold text-[#0F172A]">{company.rating} / 5.0</p>
        <p className="text-[10px] text-[#64748B] font-medium mt-0.5">Rating Score</p>
      </div>
      <div className="bg-[#F8FAFC] border border-[#E2E8F0] p-3.5 rounded-xl text-center">
        <p className="text-sm font-bold text-[#0F172A]">{company.employees.split(' ')[0]}</p>
        <p className="text-[10px] text-[#64748B] font-medium mt-0.5">Staff size</p>
      </div>
      <div className="bg-[#F8FAFC] border border-[#E2E8F0] p-3.5 rounded-xl text-center">
        <p className="text-sm font-bold text-[#0F172A]">{company.totalRaised || 'N/A'}</p>
        <p className="text-[10px] text-[#64748B] font-medium mt-0.5">Total Raised</p>
      </div>
    </div>
  );
}
