'use client';

import React, { useState } from 'react';
import { useRecruiterJobs } from '@/hooks/useRecruiterJobs';
import JobsTable from '@/components/recruiter/JobsTable';
import JobCard from '@/components/recruiter/JobCard';
import { Loader2, Plus, Search } from 'lucide-react';
import Link from 'next/link';

export default function RecruiterJobsListPage() {
  const {
    jobs,
    rawJobs,
    loading,
    error,
    search,
    setSearch,
    department,
    setDepartment,
    status,
    setStatus,
    sortBy,
    setSortBy,
    duplicate,
    close,
    deleteJob,
  } = useRecruiterJobs();

  const [viewMode, setViewMode] = useState<'table' | 'cards'>('table');

  const departmentsList = Array.from(new Set(rawJobs.map((j) => j.department)));

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading job listings...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12">
        <h3 className="text-red-500 font-bold text-lg">Error Loading Jobs</h3>
        <p className="text-sm text-[#64748B]">{error}</p>
        <button
          onClick={() => window.location.reload()}
          className="bg-[#2563EB] text-white px-4 py-2 rounded-xl text-sm font-semibold cursor-pointer"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6 max-w-6xl mx-auto text-[#0F172A]">
      {/* Header */}
      <div className="flex items-center justify-between text-left">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-[#0F172A]">Manage Job Postings</h1>
          <p className="text-xs sm:text-sm text-[#64748B] mt-0.5">Create, edit, duplicate, and manage your hiring roles.</p>
        </div>
        <Link
          href="/recruiter/jobs/create"
          className="inline-flex items-center gap-1.5 bg-[#2563EB] text-white px-4 py-2.5 rounded-xl text-xs font-semibold hover:bg-[#1D4ED8] transition-colors cursor-pointer"
        >
          <Plus size={14} />
          Create Job Post
        </Link>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-4 shadow-sm space-y-4">
        <div className="flex flex-col md:flex-row gap-3">
          <div className="flex-1 relative">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#94A3B8]" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by job title, location, or keyword..."
              className="w-full pl-9 pr-3 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] placeholder-[#94A3B8] focus:outline-none focus:border-blue-500 bg-white"
            />
          </div>

          <div className="w-full md:w-48">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="w-full px-3 py-2.5 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
            >
              <option value="newest">Newest First</option>
              <option value="oldest">Oldest First</option>
              <option value="views">Most Views</option>
              <option value="applications">Most Applications</option>
            </select>
          </div>
        </div>

        {/* Dropdowns */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-2 border-t border-[#F1F5F9] items-center text-left">
          <div>
            <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Department</label>
            <select
              value={department}
              onChange={(e) => setDepartment(e.target.value)}
              className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
            >
              <option value="">All Departments</option>
              {departmentsList.map(d => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Status</label>
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer"
            >
              <option value="">All Statuses</option>
              <option value="Published">Published</option>
              <option value="Draft">Draft</option>
              <option value="Closed">Closed</option>
            </select>
          </div>

          <div className="flex gap-2 justify-end self-end pt-4 ml-auto sm:col-span-2">
            <button
              onClick={() => setViewMode(viewMode === 'table' ? 'cards' : 'table')}
              className="px-3.5 py-2 border border-[#E2E8F0] bg-white rounded-xl text-xs text-slate-600 font-semibold hover:bg-slate-50 transition-colors cursor-pointer"
            >
              {viewMode === 'table' ? 'Grid Cards View' : 'Table List View'}
            </button>
          </div>
        </div>
      </div>

      {/* Grid or Cards */}
      {jobs.length === 0 ? (
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-12 text-center shadow-sm">
          <p className="text-sm text-[#64748B] font-semibold">No open listings matched your search criteria.</p>
        </div>
      ) : viewMode === 'table' ? (
        <JobsTable
          jobs={jobs}
          onDuplicate={duplicate}
          onClose={close}
          onDelete={deleteJob}
        />
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {jobs.map((job) => (
            <JobCard
              key={job.id}
              job={job}
              onDuplicate={duplicate}
              onClose={close}
              onDelete={deleteJob}
            />
          ))}
        </div>
      )}
    </div>
  );
}
