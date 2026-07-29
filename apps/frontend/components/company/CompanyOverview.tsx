'use client';

import React from 'react';
import { Company } from '@/types/company';
import { MapPin, Globe, Users, Building, Cpu, CircleDollarSign } from 'lucide-react';

interface CompanyOverviewProps {
  company: Company;
}

export default function CompanyOverview({ company }: CompanyOverviewProps) {
  return (
    <div className="space-y-6 text-[#0F172A] text-left">
      {/* About description */}
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 sm:p-6 shadow-sm space-y-3">
        <h3 className="font-bold text-sm sm:text-base">About {company.name}</h3>
        <p className="text-xs sm:text-sm text-slate-600 leading-relaxed font-medium">
          {company.about}
        </p>
      </div>

      {/* Corporate Metadata specs */}
      <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
        {[
          { label: 'Headquarters', value: company.headquarters, icon: MapPin },
          { label: 'Company Size', value: company.employees, icon: Users },
          { label: 'Founded', value: company.founded, icon: Building },
          { label: 'Corporate Website', value: company.website, icon: Globe },
          { label: 'Operating Stage', value: company.stage || 'Scaleup', icon: Cpu },
          { label: 'Total Raised', value: company.totalRaised || 'Undisclosed', icon: CircleDollarSign },
        ].map(({ label, value, icon: Icon }) => (
          <div key={label} className="bg-white rounded-2xl border border-[#E2E8F0] p-4 shadow-sm flex items-start gap-3">
            <div className="p-2.5 bg-blue-50 text-blue-600 rounded-xl">
              <Icon size={16} />
            </div>
            <div className="text-xs font-semibold">
              <span className="text-[#64748B] block mb-0.5">{label}</span>
              <span className="text-[#0F172A] font-bold">{value}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Tech stack */}
      {company.techStack && (
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 sm:p-6 shadow-sm space-y-3">
          <h3 className="font-bold text-sm">Technology Stack</h3>
          <div className="flex flex-wrap gap-2 pt-1">
            {company.techStack.map((tech) => (
              <span key={tech} className="text-xs font-bold bg-[#F8FAFC] border border-[#E2E8F0] text-slate-600 px-3 py-1.5 rounded-full uppercase tracking-wide">
                {tech}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
