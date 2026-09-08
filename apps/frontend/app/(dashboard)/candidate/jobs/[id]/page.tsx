'use client';

import React, { use, useState, useEffect } from 'react';
import { JobsService } from '@/services/jobs.service';
import { CompanyService } from '@/services/company.service';
import { Job } from '@/types/job';
import { Company } from '@/types/company';
import JobDetails from '@/components/jobs/JobDetails';
import RecentJobs, { trackRecentView } from '@/components/jobs/RecentJobs';
import { Loader2, ArrowLeft, AlertCircle, RefreshCw, Search } from 'lucide-react';
import Link from 'next/link';

interface CandidateJobDetailPageProps {
  params: Promise<{ id: string }>;
}

export default function CandidateJobDetailPage({ params }: CandidateJobDetailPageProps) {
  const { id } = use(params);

  const [job, setJob] = useState<Job | null>(null);
  const [company, setCompany] = useState<Company | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [is404, setIs404] = useState(false);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    setIs404(false);
    try {
      const jobData = await JobsService.getJobById(id);
      if (jobData) {
        setJob(jobData);
        trackRecentView(id);
        if (jobData.companyId) {
          try {
            const compData = await CompanyService.getCompanyById(jobData.companyId);
            setCompany(compData);
          } catch {
            // Company details optional if endpoint unavailable
          }
        }
      } else {
        setIs404(true);
      }
    } catch (err: any) {
      if (err?.message?.includes('404') || err?.message?.includes('not found')) {
        setIs404(true);
      } else {
        setError(err?.message || 'Unable to load this job');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center p-6 gap-3 text-center">
        <Loader2 className="animate-spin text-blue-600" size={36} />
        <p className="text-xs font-semibold text-[#64748B]">Loading job posting details...</p>
      </div>
    );
  }

  if (is404) {
    return (
      <div className="min-h-[70vh] p-6 text-center flex flex-col items-center justify-center gap-4 max-w-md mx-auto">
        <div className="w-12 h-12 rounded-2xl bg-amber-50 border border-amber-200 text-amber-600 flex items-center justify-center">
          <Search size={24} />
        </div>
        <div className="space-y-1">
          <h3 className="font-bold text-[#0F172A] text-lg">Job Not Found</h3>
          <p className="text-xs text-[#64748B]">
            This job listing may have been removed, closed, or is no longer available.
          </p>
        </div>
        <Link
          href="/candidate/jobs"
          className="inline-flex items-center gap-1.5 bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-xl text-xs font-bold transition-all cursor-pointer shadow-sm"
        >
          <ArrowLeft size={14} /> Browse Available Jobs
        </Link>
      </div>
    );
  }

  if (error || !job) {
    return (
      <div className="min-h-[70vh] p-6 text-center flex flex-col items-center justify-center gap-4 max-w-md mx-auto">
        <div className="w-12 h-12 rounded-2xl bg-red-50 border border-red-200 text-red-600 flex items-center justify-center">
          <AlertCircle size={24} />
        </div>
        <div className="space-y-1">
          <h3 className="font-bold text-[#0F172A] text-lg">Unable to Load Job</h3>
          <p className="text-xs text-[#64748B]">{error || 'An unexpected error occurred while retrieving details.'}</p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={loadData}
            className="inline-flex items-center gap-1.5 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer"
          >
            <RefreshCw size={13} /> Retry
          </button>
          <Link
            href="/candidate/jobs"
            className="inline-flex items-center gap-1.5 bg-slate-100 hover:bg-slate-200 text-[#0F172A] px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer"
          >
            <ArrowLeft size={13} /> Back to Jobs
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6 text-[#0F172A]">
      <Link
        href="/candidate/jobs"
        className="inline-flex items-center gap-1.5 text-xs font-bold text-[#64748B] hover:text-blue-600 transition-colors"
      >
        <ArrowLeft size={14} /> Back to Jobs
      </Link>

      <JobDetails
        job={job}
        companyProfile={company}
        isDashboardLink={true}
      />

      <div className="pt-4 border-t border-slate-200">
        <RecentJobs isDashboardLink={true} />
      </div>
    </div>
  );
}
