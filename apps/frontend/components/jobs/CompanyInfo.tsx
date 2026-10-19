'use client';

import React from 'react';
import { Company } from '@/types/company';
import { Building2, MapPin, Globe, Briefcase } from 'lucide-react';

interface CompanyInfoProps {
  company: Company;
}

export default function CompanyInfo({ company }: CompanyInfoProps) {
  const location = company.location || company.headquarters;
  const about = company.about || company.description;
  const techStack = Array.isArray(company.techStack) ? company.techStack : [];

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
      <div className="flex items-center gap-2">
        <Building2 size={16} className="text-blue-600" />
        <h4 className="font-bold text-sm text-[#0F172A]">{company.name || 'Company Profile'}</h4>
      </div>

      <div className="space-y-2 text-xs">
        {location && (
          <div className="flex justify-between py-1 border-b border-[#F1F5F9]">
            <span className="text-[#64748B] flex items-center gap-1"><MapPin size={12} /> Location</span>
            <span className="font-semibold text-[#0F172A]">{location}</span>
          </div>
        )}
        {company.industry && (
          <div className="flex justify-between py-1 border-b border-[#F1F5F9]">
            <span className="text-[#64748B] flex items-center gap-1"><Briefcase size={12} /> Industry</span>
            <span className="font-semibold text-[#0F172A]">{company.industry}</span>
          </div>
        )}
        {company.website && (
          <div className="flex justify-between py-1 border-b border-[#F1F5F9]">
            <span className="text-[#64748B] flex items-center gap-1"><Globe size={12} /> Website</span>
            <a
              href={company.website.startsWith('http') ? company.website : `https://${company.website}`}
              target="_blank"
              rel="noopener noreferrer"
              className="font-semibold text-blue-600 hover:underline truncate max-w-[170px]"
            >
              {company.website.replace(/^https?:\/\//, '')}
            </a>
          </div>
        )}
        {company.founded && (
          <div className="flex justify-between py-1 border-b border-[#F1F5F9]">
            <span className="text-[#64748B]">Founded Year</span>
            <span className="font-semibold text-[#0F172A]">{company.founded}</span>
          </div>
        )}
        {company.stage && (
          <div className="flex justify-between py-1 border-b border-[#F1F5F9]">
            <span className="text-[#64748B]">Market Stage</span>
            <span className="font-semibold text-[#0F172A]">{company.stage}</span>
          </div>
        )}
        {company.valuation && (
          <div className="flex justify-between py-1 border-b border-[#F1F5F9]">
            <span className="text-[#64748B]">Valuation</span>
            <span className="font-semibold text-[#0F172A]">{company.valuation}</span>
          </div>
        )}
      </div>

      {about && (
        <div className="space-y-1 pt-1 border-t border-[#F1F5F9]">
          <span className="block text-[11px] font-bold text-[#64748B] uppercase tracking-wide">About Company</span>
          <p className="text-xs text-[#64748B] leading-relaxed line-clamp-4">{about}</p>
        </div>
      )}

      {techStack.length > 0 && (
        <div className="space-y-2 pt-1 border-t border-[#F1F5F9]">
          <span className="block text-xs font-bold text-[#64748B] uppercase tracking-wide">Tech Stack</span>
          <div className="flex flex-wrap gap-1">
            {techStack.map(s => (
              <span key={s} className="text-[10px] bg-slate-50 border border-slate-200 text-slate-700 px-2 py-0.5 rounded-md font-medium">{s}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
