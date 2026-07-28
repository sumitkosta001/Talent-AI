'use client';

import React, { useState } from 'react';
import { useJobs } from '@/hooks/useJobs';
import SearchBar from '@/components/jobs/SearchBar';
import FilterSidebar from '@/components/jobs/FilterSidebar';
import FilterChips from '@/components/jobs/FilterChips';
import JobCard from '@/components/jobs/JobCard';
import FeaturedJobCard from '@/components/jobs/FeaturedJobCard';
import EmptyJobs from '@/components/jobs/EmptyJobs';
import Pagination from '@/components/jobs/Pagination';
import JobsHeader from '@/components/jobs/JobsHeader';
import { Loader2 } from 'lucide-react';

export default function PublicJobsPage() {
  const {
    jobs,
    loading,
    filters,
    updateFilter,
    resetFilters,
  } = useJobs();

  const [page, setPage] = useState(1);
  const itemsPerPage = 6;

  // Filter out featured jobs to show separately
  const featuredJobs = jobs.filter(j => j.isFeatured).slice(0, 3);
  
  // Pagination calculation
  const totalPages = Math.ceil(jobs.length / itemsPerPage);
  const paginatedJobs = jobs.slice((page - 1) * itemsPerPage, page * itemsPerPage);

  const handlePageChange = (p: number) => {
    setPage(p);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="bg-[#F8FAFC] min-h-screen text-[#0F172A]">
      {/* Top Navbar Placeholder / Simple header padding */}
      <div className="max-w-6xl mx-auto px-4 py-8 space-y-6">
        
        {/* Banner Headers */}
        <JobsHeader
          title="TalentAI Careers & Jobs"
          subtitle="Discover modern jobs matching your ATS resume and skill targets."
          totalJobs={jobs.length}
        />

        {/* Global Search Bar */}
        <SearchBar filters={filters} updateFilter={updateFilter} />

        {/* Dynamic Splits */}
        <div className="grid lg:grid-cols-4 gap-6 items-start">
          {/* Filters Sidebar */}
          <div className="lg:col-span-1">
            <FilterSidebar
              filters={filters}
              updateFilter={updateFilter}
              resetFilters={resetFilters}
            />
          </div>

          {/* Job listings lists */}
          <div className="lg:col-span-3 space-y-6">
            <FilterChips
              filters={filters}
              updateFilter={updateFilter}
              resetFilters={resetFilters}
            />

            {/* Featured jobs block (only show on page 1 and when search/filters are not active) */}
            {page === 1 && !filters.search && !filters.location && featuredJobs.length > 0 && (
              <div className="space-y-3 text-left">
                <h2 className="font-bold text-sm text-[#0F172A] uppercase tracking-wide">Featured Positions</h2>
                <div className="flex gap-4 overflow-x-auto pb-4 scrollbar-none">
                  {featuredJobs.map(job => (
                    <FeaturedJobCard key={job.id} job={job} />
                  ))}
                </div>
              </div>
            )}

            {/* Standard Jobs */}
            <div className="space-y-4">
              <h2 className="font-bold text-sm text-[#0F172A] uppercase tracking-wide text-left">Latest Job Openings</h2>
              
              {loading ? (
                <div className="flex flex-col items-center justify-center py-12 gap-3">
                  <Loader2 className="animate-spin text-blue-600" size={32} />
                  <p className="text-sm font-semibold text-[#64748B]">Searching matching roles...</p>
                </div>
              ) : paginatedJobs.length === 0 ? (
                <EmptyJobs onReset={resetFilters} />
              ) : (
                <div className="grid gap-4">
                  {paginatedJobs.map(job => (
                    <JobCard key={job.id} job={job} />
                  ))}
                </div>
              )}

              {!loading && paginatedJobs.length > 0 && (
                <Pagination
                  currentPage={page}
                  totalPages={totalPages}
                  onPageChange={handlePageChange}
                  totalCount={jobs.length}
                />
              )}
            </div>

          </div>
        </div>

      </div>
    </div>
  );
}
