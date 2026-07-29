'use client';

import React from 'react';
import Link from 'next/link';
import { MapPin, Users, Briefcase, Star } from 'lucide-react';
import { Company } from '@/types/company';
import FollowCompanyButton from './FollowCompanyButton';

interface CompanyCardProps {
  company: Company;
}

export default function CompanyCard({ company }: CompanyCardProps) {
  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] overflow-hidden hover:shadow-md transition-all text-left flex flex-col justify-between">
      {/* Banner */}
      <div className={`h-24 bg-gradient-to-r ${
        company.id === 'vercel' ? 'from-slate-900 to-black' : 'from-violet-600 to-indigo-700'
      }`} />

      {/* Main details body */}
      <div className="p-5 -mt-8 flex-1 flex flex-col justify-between">
        <div>
          <div className="flex justify-between items-end mb-3">
            <div className={`w-14 h-14 rounded-xl ${company.logoColor} border-4 border-white flex items-center justify-center text-white text-xl font-bold shadow-md`}>
              {company.logo}
            </div>
            <FollowCompanyButton companyId={company.id} />
          </div>

          <Link href={`/companies/${company.id}`} className="block">
            <h3 className="font-bold text-base text-[#0F172A] hover:text-blue-600 transition-colors">
              {company.name}
            </h3>
          </Link>
          <p className="text-xs text-[#64748B] font-semibold mt-0.5">{company.industry}</p>

          <p className="text-xs text-slate-600 mt-3 line-clamp-2 leading-relaxed font-medium">
            {company.about}
          </p>
        </div>

        {/* Footnotes */}
        <div className="border-t border-[#F1F5F9] pt-3.5 mt-4 grid grid-cols-2 gap-2 text-[11px] text-[#64748B] font-bold">
          <div className="flex items-center gap-1"><MapPin size={12} /> {company.headquarters}</div>
          <div className="flex items-center gap-1"><Users size={12} /> {company.employees}</div>
          <div className="flex items-center gap-1 text-amber-600"><Star size={12} fill="currentColor" /> {company.rating} Rating</div>
          <div className="flex items-center gap-1 text-blue-600"><Briefcase size={12} /> {company.openPositions} Jobs Open</div>
        </div>
      </div>
    </div>
  );
}
