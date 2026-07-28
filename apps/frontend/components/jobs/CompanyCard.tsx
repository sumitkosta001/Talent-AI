'use client';

import React from 'react';
import { Star, Link as LinkIcon } from 'lucide-react';
import { Company } from '@/types/company';

interface CompanyCardProps {
  company: Company;
}

export default function CompanyCard({ company }: CompanyCardProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
      <div className="flex gap-4">
        <div className={`w-12 h-12 rounded-xl ${company.logoColor} flex items-center justify-center text-white font-bold text-lg flex-shrink-0`}>
          {company.logo}
        </div>
        <div>
          <h3 className="font-bold text-[#0F172A] text-sm sm:text-base">{company.name}</h3>
          <p className="text-xs text-[#64748B] mt-0.5">{company.industry}</p>
        </div>
      </div>

      <p className="text-xs text-[#64748B] leading-relaxed line-clamp-3">{company.about}</p>

      <div className="grid grid-cols-2 gap-3 pt-2 text-center border-t border-[#F1F5F9] text-xs">
        <div>
          <p className="font-bold text-[#0F172A]">{company.employees.split(' ')[0]}</p>
          <p className="text-[10px] text-[#64748B]">Staff Count</p>
        </div>
        <div className="flex flex-col items-center justify-center">
          <span className="flex items-center gap-1 font-bold text-amber-500">
            <Star size={12} fill="currentColor" />
            {company.rating}
          </span>
          <p className="text-[10px] text-[#64748B]">Rating</p>
        </div>
      </div>

      <a
        href={company.website}
        target="_blank"
        rel="noopener noreferrer"
        className="flex items-center justify-center gap-1.5 w-full bg-[#F8FAFC] border border-[#E2E8F0] text-[#0F172A] py-2 rounded-xl text-xs font-semibold hover:bg-[#F1F5F9] transition-all"
      >
        <LinkIcon size={12} />
        Visit Site
      </a>
    </div>
  );
}
