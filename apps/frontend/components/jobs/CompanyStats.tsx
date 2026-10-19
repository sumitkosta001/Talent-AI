'use client';

import React from 'react';
import { Company } from '@/types/company';

interface CompanyStatsProps {
  company: Company;
}

export default function CompanyStats({ company }: CompanyStatsProps) {
  const staff = company.employees ? company.employees.split(' ')[0] : null;
  const rating = company.rating ? `${company.rating} / 5.0` : null;
  const totalRaised = company.totalRaised || null;

  if (!staff && !rating && !totalRaised) {
    return null;
  }

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
      <h4 className="font-bold text-sm text-[#0F172A]">Company Performance</h4>
      <div className="grid grid-cols-3 gap-4 pt-1">
        {rating && (
          <div className="bg-[#F8FAFC] border border-[#E2E8F0] p-3.5 rounded-xl text-center">
            <p className="text-sm font-bold text-[#0F172A]">{rating}</p>
            <p className="text-[10px] text-[#64748B] font-medium mt-0.5">Rating Score</p>
          </div>
        )}
        {staff && (
          <div className="bg-[#F8FAFC] border border-[#E2E8F0] p-3.5 rounded-xl text-center">
            <p className="text-sm font-bold text-[#0F172A]">{staff}</p>
            <p className="text-[10px] text-[#64748B] font-medium mt-0.5">Staff size</p>
          </div>
        )}
        {totalRaised && (
          <div className="bg-[#F8FAFC] border border-[#E2E8F0] p-3.5 rounded-xl text-center">
            <p className="text-sm font-bold text-[#0F172A]">{totalRaised}</p>
            <p className="text-[10px] text-[#64748B] font-medium mt-0.5">Total Raised</p>
          </div>
        )}
      </div>
    </div>
  );
}
