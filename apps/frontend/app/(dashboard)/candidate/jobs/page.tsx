'use client';

import React, { useState } from 'react';
import { useJobs } from '@/hooks/useJobs';
import RecommendedJobCard from '@/components/jobs/RecommendedJobCard';
import AppliedJobs from '@/components/jobs/AppliedJobs';
import BookmarkList from '@/components/jobs/BookmarkList';
import RecentJobs from '@/components/jobs/RecentJobs';
import SearchBar from '@/components/jobs/SearchBar';
import FilterChips from '@/components/jobs/FilterChips';
import EmptyJobs from '@/components/jobs/EmptyJobs';
import JobsHeader from '@/components/jobs/JobsHeader';
import { Loader2 } from 'lucide-react';
import { MOCK_RECOMMENDED_JOBS } from '@/mock/recommendedJobs';
import { MOCK_JOB_CATEGORIES } from '@/mock/jobCategories';

type TabType = 'recommended' | 'applied' | 'saved';

export default function CandidateJobsPage() {
  const [activeTab, setActiveTab] = useState<TabType>('recommended');
  
  const {
    jobs,
    loading,
    filters,
    updateFilter,
    resetFilters,
  } = useJobs();

  // Recommended jobs based on high ATS match score (>=85%)
  const recommendations = jobs.filter(j => j.match >= 85);

  const tabs: { id: TabType; label: string }[] = [
    { id: 'recommended', label: 'AI Recommended Jobs' },
    { id: 'applied', label: 'My Applications' },
    { id: 'saved', label: 'Saved Jobs' },
  ];

  return (
    <div className="p-6 space-y-6 max-w-5xl mx-auto text-[#0F172A]">
      
      {/* Page Header */}
      <JobsHeader
        title="Personalized Job Portal"
        subtitle="Manage your applications, saved roles, and explore matching positions."
      />

      {/* Tabs Selector */}
      <div className="flex border-b border-[#E2E8F0]">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-5 py-3.5 text-xs sm:text-sm font-bold border-b-2 transition-all cursor-pointer ${
              activeTab === tab.id
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-[#64748B] hover:text-[#0F172A]'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Grid splits */}
      <div className="grid lg:grid-cols-3 gap-6 items-start">
        {/* Left main content tab section */}
        <div className="lg:col-span-2 space-y-6">
          {activeTab === 'recommended' && (
            <div className="space-y-4">
              <SearchBar filters={filters} updateFilter={updateFilter} />
              <FilterChips
                filters={filters}
                updateFilter={updateFilter}
                resetFilters={resetFilters}
              />

              <div className="space-y-4">
                {loading ? (
                  <div className="flex flex-col items-center justify-center py-12 gap-2">
                    <Loader2 className="animate-spin text-blue-600" size={28} />
                    <p className="text-xs font-semibold text-[#64748B]">Auditing target resume keywords matches...</p>
                  </div>
                ) : recommendations.length === 0 ? (
                  <EmptyJobs onReset={resetFilters} />
                ) : (
                  <div className="grid gap-4">
                    {recommendations.map(job => (
                      <RecommendedJobCard key={job.id} job={job} />
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'applied' && <AppliedJobs />}

          {activeTab === 'saved' && <BookmarkList />}
        </div>

        {/* Right sidebar profiling lists */}
        <div className="space-y-6">
          {/* Recent views tracker list */}
          <RecentJobs isDashboardLink={true} />

          {/* Job categories cards */}
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
            <h4 className="font-bold text-sm text-[#0F172A]">Trending Sectors</h4>
            <div className="space-y-2.5">
              {MOCK_JOB_CATEGORIES.map(cat => (
                <div
                  key={cat.id}
                  className="flex items-center justify-between text-xs py-1 border-b border-[#F1F5F9] last:border-0"
                >
                  <span className="flex items-center gap-1.5">
                    <span>{cat.icon}</span>
                    <span className="font-semibold text-slate-700">{cat.name}</span>
                  </span>
                  <span className="bg-slate-50 text-slate-500 font-bold px-2 py-0.5 rounded border border-slate-200">
                    {cat.count} openings
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

    </div>
  );
}
