'use client';

import React, { use, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { RecruiterJobsService } from '@/services/jobs.service';
import { RecruiterApplicantService } from '@/services/applicant.service';
import { RecruiterJob } from '@/types/job';
import { Applicant } from '@/types/applicant';
import ApplicantTable from '@/components/recruiter/ApplicantTable';
import { Loader2, ArrowLeft, Calendar, DollarSign, MapPin, Eye, Check, X } from 'lucide-react';
import Link from 'next/link';

interface RecruiterJobDetailPageProps {
  params: Promise<{ id: string }>;
}

export default function RecruiterJobDetailPage({ params }: RecruiterJobDetailPageProps) {
  const { id } = use(params);
  const router = useRouter();

  const [job, setJob] = useState<RecruiterJob | null>(null);
  const [applicants, setApplicants] = useState<Applicant[]>([]);
  const [loading, setLoading] = useState(true);

  async function loadData() {
    try {
      const [j, apps] = await Promise.all([
        RecruiterJobsService.getJobById(id),
        RecruiterApplicantService.getApplicants(),
      ]);
      setJob(j);
      setApplicants(apps.filter((a) => a.jobId === id));
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, [id]);

  const handleShortlist = async (appId: string) => {
    await RecruiterApplicantService.updateStatus(appId, 'Shortlisted');
    loadData();
  };

  const handleReject = async (appId: string) => {
    await RecruiterApplicantService.updateStatus(appId, 'Rejected');
    loadData();
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[40vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading job and applicant records...</p>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12">
        <h3 className="text-red-500 font-bold text-lg">Job Posting Not Found</h3>
        <button
          onClick={() => router.push('/recruiter/jobs')}
          className="bg-blue-600 text-white px-4 py-2 rounded-xl text-xs font-semibold cursor-pointer"
        >
          Back to Listings
        </button>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6 max-w-5xl mx-auto text-[#0F172A] text-left">
      {/* Header */}
      <div className="flex items-center gap-3">
        <Link href="/recruiter/jobs" className="text-slate-400 hover:text-[#0F172A] cursor-pointer">
          <ArrowLeft size={18} />
        </Link>
        <h2 className="text-lg font-bold">Job Post Tracking</h2>
      </div>

      {/* Info card */}
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex gap-4">
          <div className={`w-12 h-12 rounded-xl ${job.logoColor} flex items-center justify-center text-white font-bold text-lg flex-shrink-0`}>
            {job.logo}
          </div>
          <div>
            <h3 className="font-bold text-sm sm:text-base">{job.role}</h3>
            <div className="flex flex-wrap items-center gap-2 mt-1 text-xs text-[#64748B] font-semibold">
              <span className="text-[#0F172A]">{job.company}</span>
              <span>·</span>
              <span className="flex items-center gap-0.5"><MapPin size={12} /> {job.location}</span>
              <span>·</span>
              <span className="flex items-center gap-0.5"><DollarSign size={12} /> {job.salary}</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2 text-[10px] font-bold">
          <span className="bg-blue-50 text-blue-700 border border-blue-200 px-3 py-1 rounded-full uppercase tracking-wider">
            {job.department}
          </span>
          <span className="bg-slate-50 text-slate-700 border border-slate-200 px-3 py-1 rounded-full uppercase tracking-wider">
            {job.status}
          </span>
        </div>
      </div>

      {/* Job stats counters */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-left">
        {[
          { label: 'Total Views', val: job.views, color: 'border-slate-200' },
          { label: 'Total Applicants', val: job.applicationsCount, color: 'border-blue-200' },
          { label: 'Shortlisted candidates', val: job.shortlistedCount, color: 'border-emerald-200' },
          { label: 'Offers Sent', val: job.offersSentCount, color: 'border-pink-200' },
        ].map(({ label, val, color }) => (
          <div key={label} className={`bg-white rounded-2xl border ${color} p-4`}>
            <span className="text-[10px] sm:text-xs font-bold text-[#64748B] uppercase tracking-wide">{label}</span>
            <div className="text-xl sm:text-2xl font-black text-[#0F172A] mt-1">{val}</div>
          </div>
        ))}
      </div>

      {/* Applicants List */}
      <div className="space-y-3">
        <h3 className="font-bold text-sm uppercase tracking-wider text-[#64748B]">
          Job Applicants ({applicants.length})
        </h3>

        {applicants.length === 0 ? (
          <div className="bg-white border border-[#E2E8F0] p-12 text-center rounded-2xl">
            <p className="text-xs sm:text-sm text-[#64748B] font-semibold">No candidates have applied to this job yet.</p>
          </div>
        ) : (
          <ApplicantTable
            applicants={applicants}
            onShortlist={handleShortlist}
            onReject={handleReject}
          />
        )}
      </div>
    </div>
  );
}
