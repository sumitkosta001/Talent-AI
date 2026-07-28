'use client';

import React, { use, useState, useEffect } from 'react';
import { JobsService } from '@/services/jobs.service';
import { CompanyService } from '@/services/company.service';
import { Job } from '@/types/job';
import { Company } from '@/types/company';
import JobDetails from '@/components/jobs/JobDetails';
import RelatedJobs from '@/components/jobs/RelatedJobs';
import RecentJobs, { trackRecentView } from '@/components/jobs/RecentJobs';
import { Loader2, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { MOCK_JOBS } from '@/mock/jobs';

interface JobDetailPageProps {
  params: Promise<{ id: string }>;
}

export default function JobDetailPage({ params }: JobDetailPageProps) {
  const { id } = use(params);

  const [job, setJob] = useState<Job | null>(null);
  const [company, setCompany] = useState<Company | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      setError(null);
      try {
        const jobData = await JobsService.getJobById(id);
        if (jobData) {
          setJob(jobData);
          trackRecentView(id); // track viewed state
          const compData = await CompanyService.getCompanyById(jobData.companyId);
          setCompany(compData);
        } else {
          setError('Job listing not found');
        }
      } catch (err: any) {
        setError(err?.message || 'Failed to fetch job details');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#F8FAFC] flex flex-col items-center justify-center gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Retrieving job information details...</p>
      </div>
    );
  }

  if (error || !job) {
    return (
      <div className="min-h-screen bg-[#F8FAFC] p-6 text-center flex flex-col items-center justify-center gap-4">
        <h2 className="font-bold text-red-500 text-lg">Error Loading Job Details</h2>
        <p className="text-sm text-[#64748B]">{error || 'Job not found'}</p>
        <Link href="/jobs" className="bg-blue-600 text-white px-5 py-2.5 rounded-xl text-sm font-semibold">
          Return to All Jobs
        </Link>
      </div>
    );
  }

  return (
    <div className="bg-[#F8FAFC] min-h-screen text-[#0F172A] py-8">
      <div className="max-w-6xl mx-auto px-4 space-y-6">
        
        {/* Main Details card */}
        <JobDetails
          job={job}
          companyProfile={company}
          onBack={() => window.history.back()}
        />

        {/* Similar matches and history */}
        <div className="grid md:grid-cols-2 gap-6 mt-6">
          <RelatedJobs jobs={MOCK_JOBS} currentJobId={job.id} />
          <RecentJobs />
        </div>

      </div>
    </div>
  );
}
