'use client';

import React from 'react';
import { useCompanies } from '@/hooks/useCompanies';
import CompanyCard from '@/components/company/CompanyCard';
import { Loader2, Search, Building } from 'lucide-react';

export default function CompaniesDirectoryPage() {
  const {
    companies,
    loading,
    error,
    search,
    setSearch,
    industryFilter,
    setIndustryFilter,
    sortBy,
    setSortBy,
  } = useCompanies();

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading corporate directory list...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12">
        <h3 className="text-red-500 font-bold text-lg">Error Loading Directory</h3>
        <p className="text-sm text-[#64748B]">{error}</p>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6 max-w-6xl mx-auto text-[#0F172A] text-left">
      {/* Title */}
      <div className="border-b border-[#E2E8F0] pb-5">
        <h1 className="text-xl sm:text-2xl font-bold flex items-center gap-2">
          <Building className="text-blue-600" />
          Explore Hiring Companies
        </h1>
        <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">Explore corporate profiles, tech stack components, ratings reviews, and open positions before applying.</p>
      </div>

      {/* Search and filters sidebar card */}
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-4 shadow-sm space-y-4">
        <div className="flex flex-col md:flex-row gap-3">
          <div className="flex-1 relative">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#94A3B8]" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search companies by name or industry tags..."
              className="w-full pl-9 pr-3 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          <div className="w-full md:w-48">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="w-full px-3 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer font-semibold"
            >
              <option value="rating">Highest Rated</option>
              <option value="jobs">Most Open Jobs</option>
              <option value="alphabetical">Alphabetical</option>
            </select>
          </div>
        </div>

        {/* Industry selections */}
        <div className="flex items-center gap-3 pt-2 border-t border-[#F1F5F9] text-xs font-semibold">
          <label className="text-[#64748B] uppercase tracking-wider text-[10px] font-bold">Filter Industry:</label>
          <div className="flex flex-wrap gap-1.5">
            {[
              { label: 'All Industries', val: '' },
              { label: 'Financial Tech', val: 'Financial Technology' },
              { label: 'Cloud & DevOps', val: 'Cloud Hosting & DevOps' },
              { label: 'Technology & Search', val: 'Technology & Search' },
            ].map((ind) => (
              <button
                key={ind.label}
                onClick={() => setIndustryFilter(ind.val)}
                className={`px-3 py-1.5 rounded-full border transition-all cursor-pointer ${
                  industryFilter === ind.val
                    ? 'bg-blue-600 text-white border-blue-600'
                    : 'bg-white text-slate-600 border-[#E2E8F0] hover:bg-[#F8FAFC]'
                }`}
              >
                {ind.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Cards list grid */}
      {companies.length === 0 ? (
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-12 text-center shadow-sm">
          <p className="text-sm text-[#64748B] font-semibold">No companies match your query. Try adjusting filters.</p>
        </div>
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {companies.map((company) => (
            <CompanyCard key={company.id} company={company} />
          ))}
        </div>
      )}
    </div>
  );
}
