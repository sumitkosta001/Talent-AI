'use client';

import React, { use, useState } from 'react';
import { useCompany } from '@/hooks/useCompany';
import { useCompanyReviews } from '@/hooks/useCompanyReviews';
import { useCompanyJobs } from '@/hooks/useCompanyJobs';
import CompanyOverview from '@/components/company/CompanyOverview';
import CompanyCulture from '@/components/company/CompanyCulture';
import CompanyBenefits from '@/components/company/CompanyBenefits';
import CompanyReviews from '@/components/company/CompanyReviews';
import CompanyGallery from '@/components/company/CompanyGallery';
import CompanyJobs from '@/components/company/CompanyJobs';
import FollowCompanyButton from '@/components/company/FollowCompanyButton';
import { Loader2, ArrowLeft, Globe, MapPin, Users, Building, Briefcase, Share2, Star } from 'lucide-react';
import Link from 'next/link';

interface CompanyDetailPageProps {
  params: Promise<{ id: string }>;
}

type TabType = 'about' | 'jobs' | 'culture' | 'benefits' | 'reviews' | 'gallery';

export default function CompanyDetailPage({ params }: CompanyDetailPageProps) {
  const { id } = use(params);
  const { company, culture, benefits, gallery, employees, ratings, loading, error } = useCompany(id);
  const { reviews } = useCompanyReviews(id);
  const { jobs } = useCompanyJobs(id);

  const [activeTab, setActiveTab] = useState<TabType>('about');

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href);
    alert('Company profile page URL copied to clipboard!');
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading corporate profile details...</p>
      </div>
    );
  }

  if (error || !company) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12 text-[#0F172A]">
        <h3 className="text-red-500 font-bold text-lg">Company Profile Not Found</h3>
        <p className="text-sm text-[#64748B]">{error || 'This organization profile does not exist.'}</p>
        <Link href="/companies" className="inline-block bg-blue-600 text-white px-4 py-2 rounded-xl text-xs font-semibold">
          Back to Directory
        </Link>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6 max-w-5xl mx-auto text-[#0F172A] text-left">
      {/* Header back button */}
      <div className="flex items-center gap-3">
        <Link href="/companies" className="text-slate-400 hover:text-[#0F172A] cursor-pointer">
          <ArrowLeft size={18} />
        </Link>
        <h2 className="text-sm sm:text-base font-bold">Company Profile Workspace</h2>
      </div>

      {/* Hero card banner & details */}
      <div className="bg-white rounded-2xl border border-[#E2E8F0] overflow-hidden shadow-sm">
        <div className={`h-36 bg-gradient-to-r ${
          company.id === 'vercel' ? 'from-slate-900 to-black' : 'from-violet-600 to-violet-800'
        }`} />
        <div className="p-5 sm:p-6 -mt-12">
          <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-4">
            <div className={`w-20 h-20 rounded-2xl ${company.logoColor} border-4 border-white flex items-center justify-center text-white text-3xl font-black shadow-lg flex-shrink-0`}>
              {company.logo}
            </div>

            <div className="flex gap-2 self-start sm:self-auto">
              <button
                onClick={handleShare}
                className="p-2 rounded-xl border border-[#E2E8F0] text-[#64748B] hover:bg-[#F8FAFC] cursor-pointer"
                title="Share company profile link"
              >
                <Share2 size={15} />
              </button>
              <FollowCompanyButton companyId={company.id} />
              <a
                href={company.website}
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-1.5 px-4 py-2 rounded-xl border border-[#E2E8F0] text-xs font-bold text-[#64748B] hover:bg-[#F8FAFC]"
              >
                <Globe size={13} />
                Visit Website
              </a>
            </div>
          </div>

          <h1 className="text-2xl font-black text-[#0F172A]">{company.name}</h1>
          <p className="text-xs sm:text-sm text-slate-600 font-semibold mt-1">{company.industry}</p>

          <div className="flex flex-wrap gap-4 mt-4.5 text-xs text-[#64748B] font-bold">
            <div className="flex items-center gap-1.5"><MapPin size={13} /> {company.headquarters}</div>
            <div className="flex items-center gap-1.5"><Users size={13} /> {company.employees}</div>
            <div className="flex items-center gap-1.5"><Building size={13} /> Founded {company.founded}</div>
            <div className="flex items-center gap-1.5 text-amber-600"><Star size={13} fill="currentColor" /> {company.rating} Rating</div>
            <div className="flex items-center gap-1.5 text-blue-600"><Briefcase size={13} /> {company.openPositions} Jobs Open</div>
          </div>
        </div>
      </div>

      {/* Tabs navigation options */}
      <div className="flex gap-2.5 overflow-x-auto pb-1 border-b border-[#E2E8F0] text-xs sm:text-sm">
        {[
          { id: 'about', label: 'About Overview' },
          { id: 'jobs', label: `Open Jobs (${jobs.length})` },
          { id: 'culture', label: 'Culture & Values' },
          { id: 'benefits', label: 'Benefits & Perks' },
          { id: 'reviews', label: `Employee Reviews (${reviews.length})` },
          { id: 'gallery', label: 'Office Gallery' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as TabType)}
            className={`
              pb-3 font-bold border-b-2 transition-all cursor-pointer whitespace-nowrap px-1
              ${
                activeTab === tab.id
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-[#64748B] hover:text-[#0F172A]'
              }
            `}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab panel details */}
      <div className="min-h-[220px]">
        {activeTab === 'about' && <CompanyOverview company={company} />}
        {activeTab === 'jobs' && <CompanyJobs jobs={jobs} />}
        {activeTab === 'culture' && <CompanyCulture culture={culture} />}
        {activeTab === 'benefits' && <CompanyBenefits benefits={benefits} />}
        {activeTab === 'reviews' && <CompanyReviews reviews={reviews} ratings={ratings} />}
        {activeTab === 'gallery' && <CompanyGallery gallery={gallery} />}
      </div>
    </div>
  );
}
