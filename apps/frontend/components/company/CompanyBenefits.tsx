'use client';

import React from 'react';
import { CompanyBenefit } from '@/types/companyBenefit';
import { Heart, Calendar, Clock, Laptop, GraduationCap, Home } from 'lucide-react';

interface CompanyBenefitsProps {
  benefits: CompanyBenefit[];
}

export default function CompanyBenefits({ benefits }: CompanyBenefitsProps) {
  const getIcon = (iconName: string) => {
    switch (iconName) {
      case 'heart':
        return Heart;
      case 'calendar':
        return Calendar;
      case 'clock':
        return Clock;
      case 'laptop':
        return Laptop;
      case 'graduation-cap':
        return GraduationCap;
      default:
        return Home;
    }
  };

  return (
    <div className="space-y-5 text-left text-[#0F172A]">
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm">
        <h3 className="font-bold text-sm sm:text-base mb-1">Company Benefits & Perks</h3>
        <p className="text-xs text-[#64748B] font-semibold">Curated benefits focused on wellness, workspace comfort, and learning resources.</p>
      </div>

      <div className="grid sm:grid-cols-2 gap-4">
        {benefits.map((ben) => {
          const Icon = getIcon(ben.icon);
          return (
            <div key={ben.id} className="bg-white rounded-2xl border border-[#E2E8F0] p-4.5 shadow-sm flex items-start gap-3">
              <div className="p-2.5 bg-blue-50 text-blue-600 rounded-xl flex-shrink-0 border border-blue-100">
                <Icon size={16} />
              </div>
              <div className="text-xs font-semibold">
                <h4 className="font-bold text-[#0F172A] text-sm">{ben.label}</h4>
                <p className="text-slate-500 mt-1 leading-relaxed">{ben.description}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
