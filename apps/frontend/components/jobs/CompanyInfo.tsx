'use client';

import React from 'react';
import { Company } from '@/types/company';

interface CompanyInfoProps {
  company: Company;
}

export default function CompanyInfo({ company }: CompanyInfoProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
      <h4 className="font-bold text-sm text-[#0F172A]">Company Profile</h4>
      <div className="space-y-2 text-xs">
        <div className="flex justify-between py-1 border-b border-[#F1F5F9]">
          <span className="text-[#64748B]">Headquarters</span>
          <span className="font-semibold text-[#0F172A]">{company.headquarters}</span>
        </div>
        <div className="flex justify-between py-1 border-b border-[#F1F5F9]">
          <span className="text-[#64748B]">Founded Year</span>
          <span className="font-semibold text-[#0F172A]">{company.founded}</span>
        </div>
        <div className="flex justify-between py-1 border-b border-[#F1F5F9]">
          <span className="text-[#64748B]">Market Stage</span>
          <span className="font-semibold text-[#0F172A]">{company.stage}</span>
        </div>
        {company.valuation && (
          <div className="flex justify-between py-1 border-b border-[#F1F5F9]">
            <span className="text-[#64748B]">Valuation</span>
            <span className="font-semibold text-[#0F172A]">{company.valuation}</span>
          </div>
        )}
      </div>

      <div className="space-y-2">
        <span className="block text-xs font-bold text-[#64748B] uppercase tracking-wide">Tech Stack</span>
        <div className="flex flex-wrap gap-1">
          {company.techStack.map(s => (
            <span key={s} className="text-[10px] bg-slate-50 border border-slate-200 text-slate-700 px-2 py-0.5 rounded-md font-medium">{s}</span>
          ))}
        </div>
      </div>
    </div>
  );
}
