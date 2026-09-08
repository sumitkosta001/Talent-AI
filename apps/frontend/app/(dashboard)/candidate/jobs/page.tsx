'use client';

import React, { useState } from 'react';
import { useResume } from '@/hooks/useResume';
import { useJobRecommendations } from '@/hooks/useJobRecommendations';
import { useJobs } from '@/hooks/useJobs';
import RecommendedJobCard from '@/components/jobs/RecommendedJobCard';
import AppliedJobs from '@/components/jobs/AppliedJobs';
import BookmarkList from '@/components/jobs/BookmarkList';
import RecentJobs from '@/components/jobs/RecentJobs';
import SearchBar from '@/components/jobs/SearchBar';
import FilterChips from '@/components/jobs/FilterChips';
import EmptyJobs from '@/components/jobs/EmptyJobs';
import JobsHeader from '@/components/jobs/JobsHeader';
import { Loader2, ArrowUpDown, ChevronLeft, ChevronRight, AlertCircle, RefreshCw } from 'lucide-react';
import { MOCK_JOB_CATEGORIES } from '@/mock/jobCategories';

type TabType = 'search' | 'recommended' | 'applied' | 'saved';

export default function CandidateJobsPage() {
  const [activeTab, setActiveTab] = useState<TabType>('search');
  
  const { currentResume } = useResume();
  const resumeId = currentResume?.id || null;
  const { data: recData, loading: recLoading } = useJobRecommendations(resumeId);

  const {
    jobs,
    totalItems,
    totalPages,
    loading: jobsLoading,
    error: jobsError,
  const { data: recData, loading: recLoading, error: recError } = useJobRecommendations(resumeId);

  const {
    jobs,
    loading: jobsLoading,
    filters,
    updateFilter,
    resetFilters,
    refetch,
  } = useJobs();

  const loading = jobsLoading || recLoading;

  // Use real backend Day 33 job recommendations if available, otherwise filter jobs
  const realRecs = recData?.recommendations || [];
  const recommendations = realRecs.length > 0
    ? realRecs.map((rec) => {
        const found = jobs.find((j) => j.id === rec.job_id);
        return {
          id: rec.job_id,
          companyId: found?.companyId || 'company',
          company: rec.company || found?.company || 'Company',
          role: rec.title || found?.role || 'Job Role',
          title: rec.title || found?.title || 'Job Role',
          salary: found?.salary || '₹8L – ₹15L',
          salary: found?.salary || '$120K–$160K',
          match: Math.round(rec.recommendation_score <= 1 ? rec.recommendation_score * 100 : rec.recommendation_score),
          location: found?.location || 'Remote',
          logo: found?.logo || 'J',
          logoColor: found?.logoColor || 'bg-blue-600',
          experience: found?.experience || '3+ years',
          skills: rec.matched_skills.length > 0 ? rec.matched_skills : (found?.skills || []),
          bookmarked: false,
          applied: false,
          description: rec.explanation?.summary || found?.description || '',
          responsibilities: found?.responsibilities || [],
          requirements: found?.requirements || [],
          benefits: found?.benefits || [],
          date: 'Recent',
          type: found?.type || 'Full-time',
          remoteStatus: found?.remoteStatus || 'Remote',
          deadline: 'Open',
          applicantsCount: found?.applicantsCount || 10,
          isFeatured: true,
          category: found?.category || 'Engineering',
        };
      })
    : jobs.filter((j) => j.match >= 85);

  const tabs: { id: TabType; label: string }[] = [
    { id: 'search', label: 'Find Jobs (Backend Search)' },
    { id: 'recommended', label: 'AI Recommended Jobs' },
    { id: 'applied', label: 'My Applications' },
    { id: 'saved', label: 'Saved Jobs' },
  ];

  return (
    <div className="p-6 space-y-6 max-w-5xl mx-auto text-[#0F172A]">
      
      {/* Page Header */}
      <JobsHeader
        title="Candidate Job Discovery Portal"
        subtitle="Search published positions, explore AI recommendations, and manage saved roles."
      />

      {/* Tabs Selector */}
      <div className="flex border-b border-[#E2E8F0] overflow-x-auto">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-5 py-3 text-xs sm:text-sm font-bold border-b-2 transition-all cursor-pointer whitespace-nowrap ${
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
          {activeTab === 'search' && (
            <div className="space-y-4">
              <SearchBar filters={filters} updateFilter={updateFilter} />
              <FilterChips
                filters={filters}
                updateFilter={updateFilter}
                resetFilters={resetFilters}
              />

              {/* Sorting Bar & Total Count */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-semibold text-[#64748B]">
                <div>
                  Showing <span className="font-bold text-[#0F172A]">{jobs.length}</span> of{' '}
                  <span className="font-bold text-[#0F172A]">{totalItems}</span> jobs
                </div>
                <div className="flex items-center gap-2">
                  <ArrowUpDown size={14} className="text-slate-400" />
                  <span>Sort by:</span>
                  <select
                    value={filters.sortBy}
                    onChange={(e) => updateFilter('sortBy', e.target.value)}
                    className="bg-white border border-[#E2E8F0] rounded-lg px-2 py-1 text-xs font-bold text-[#0F172A] focus:outline-none focus:border-blue-500 cursor-pointer"
                  >
                    <option value="newest">Newest</option>
                    <option value="oldest">Oldest</option>
                    <option value="highest-salary">Salary: High to Low</option>
                    <option value="lowest-salary">Salary: Low to High</option>
                  </select>
                </div>
              </div>

              {/* Jobs List / Loading / Error / Empty States */}
              <div className="space-y-4">
                {jobsLoading ? (
                  <div className="flex flex-col items-center justify-center py-16 gap-3 bg-white rounded-2xl border border-slate-200">
                    <Loader2 className="animate-spin text-blue-600" size={32} />
                    <p className="text-xs font-semibold text-slate-500">Searching active job database...</p>
                  </div>
                ) : jobsError ? (
                  <div className="flex flex-col items-center justify-center py-12 gap-3 bg-red-50/50 rounded-2xl border border-red-200 text-center p-6">
                    <AlertCircle className="text-red-500" size={32} />
                    <h4 className="font-bold text-slate-900">Unable to load jobs</h4>
                    <p className="text-xs text-slate-600">{jobsError}</p>
                    <button
                      onClick={() => refetch()}
                      className="mt-2 inline-flex items-center gap-1.5 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-xl text-xs font-bold transition-all cursor-pointer"
                    >
                      <RefreshCw size={14} /> Retry Request
                    </button>
                  </div>
                ) : jobs.length === 0 ? (
                  <EmptyJobs onReset={resetFilters} />
                ) : (
                  <div className="grid gap-4">
                    {jobs.map((job) => (
                      <RecommendedJobCard key={job.id} job={job} />
                    ))}
                  </div>
                )}
              </div>

              {/* Pagination Controls */}
              {totalPages > 1 && !jobsLoading && !jobsError && (
                <div className="flex items-center justify-between border-t border-slate-200 pt-4 px-2">
                  <button
                    disabled={(filters.page || 1) <= 1}
                    onClick={() => updateFilter('page', (filters.page || 1) - 1)}
                    className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg border border-slate-200 bg-white text-xs font-bold text-slate-700 hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
                  >
                    <ChevronLeft size={14} /> Previous
                  </button>

                  <span className="text-xs font-bold text-slate-600">
                    Page <span className="text-blue-600 font-extrabold">{filters.page || 1}</span> of {totalPages}
                  </span>

                  <button
                    disabled={(filters.page || 1) >= totalPages}
                    onClick={() => updateFilter('page', (filters.page || 1) + 1)}
                    className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg border border-slate-200 bg-white text-xs font-bold text-slate-700 hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
                  >
                    Next <ChevronRight size={14} />
                  </button>
                </div>
              )}
            </div>
          )}

          {activeTab === 'recommended' && (
            <div className="space-y-4">
              {recLoading ? (
                <div className="flex flex-col items-center justify-center py-12 gap-2">
                  <Loader2 className="animate-spin text-blue-600" size={28} />
                  <p className="text-xs font-semibold text-[#64748B]">Auditing target resume keywords matches</p>
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
          )}

          {activeTab === 'applied' && <AppliedJobs />}

          {activeTab === 'saved' && <BookmarkList />}
        </div>

        {/* Right sidebar profiling lists */}
        <div className="space-y-6">
          <RecentJobs isDashboardLink={true} />

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
