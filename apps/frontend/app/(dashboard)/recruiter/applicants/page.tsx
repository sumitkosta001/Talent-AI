'use client';

import React from 'react';
import { useApplicants } from '@/hooks/useApplicants';
import ApplicantTable from '@/components/recruiter/ApplicantTable';
import { Loader2, Search } from 'lucide-react';

export default function RecruiterApplicantsListPage() {
  const {
    applicants,
    rawApplicants,
    loading,
    error,
    search,
    setSearch,
    status,
    setStatus,
    experience,
    setExperience,
    atsMin,
    setAtsMin,
    sortBy,
    setSortBy,
    updateStatus,
  } = useApplicants();

  const handleShortlist = (id: string) => {
    updateStatus(id, 'Shortlisted');
  };

  const handleReject = (id: string) => {
    updateStatus(id, 'Rejected');
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading applicant pipelines...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12">
        <h3 className="text-red-500 font-bold text-lg">Error Loading Applicants</h3>
        <p className="text-sm text-[#64748B]">{error}</p>
        <button
          onClick={() => window.location.reload()}
          className="bg-blue-600 text-white px-4 py-2 rounded-xl text-xs font-semibold cursor-pointer"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6 max-w-6xl mx-auto text-[#0F172A]">
      {/* Header */}
      <div className="text-left">
        <h1 className="text-xl sm:text-2xl font-bold text-[#0F172A]">Candidate Applicants</h1>
        <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">Filter, search, shortlist, and track applicant processes.</p>
      </div>

      {/* Filter widgets panel */}
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-4 shadow-sm space-y-4">
        <div className="flex flex-col md:flex-row gap-3">
          <div className="flex-1 relative">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#94A3B8]" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search candidates by name, email, or parsed skills..."
              className="w-full pl-9 pr-3 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          <div className="w-full md:w-48">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="w-full px-3 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
            >
              <option value="ats-desc">Highest ATS Score</option>
              <option value="ats-asc">Lowest ATS Score</option>
              <option value="newest">Newest Applied</option>
              <option value="oldest">Oldest Applied</option>
            </select>
          </div>
        </div>

        {/* Dropdowns filters */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-2 border-t border-[#F1F5F9] items-center text-left">
          <div>
            <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Status Stage</label>
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
            >
              <option value="">All Statuses</option>
              <option value="Applied">Applied</option>
              <option value="Under Review">Under Review</option>
              <option value="Shortlisted">Shortlisted</option>
              <option value="Interview Scheduled">Interview Scheduled</option>
              <option value="Offer Sent">Offer Sent</option>
              <option value="Rejected">Rejected</option>
            </select>
          </div>

          <div>
            <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Experience</label>
            <select
              value={experience}
              onChange={(e) => setExperience(e.target.value)}
              className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
            >
              <option value="">All Experience Ranges</option>
              <option value="4 years">4+ years</option>
              <option value="6 years">6+ years</option>
              <option value="8 years">8+ years</option>
            </select>
          </div>

          <div>
            <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Min ATS Score</label>
            <select
              value={atsMin || ''}
              onChange={(e) => setAtsMin(parseInt(e.target.value) || 0)}
              className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
            >
              <option value="">No Minimum</option>
              <option value="70">70% & above</option>
              <option value="80">80% & above</option>
              <option value="90">90% & above</option>
            </select>
          </div>
        </div>
      </div>

      {/* Candidate applicants list table */}
      {applicants.length === 0 ? (
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-12 text-center shadow-sm">
          <p className="text-sm text-[#64748B] font-semibold">No candidates matched the filtering options.</p>
        </div>
      ) : (
        <ApplicantTable
          applicants={applicants}
          onShortlist={handleShortlist}
          onReject={handleReject}
        />
      )}
    </div>
  );
}
