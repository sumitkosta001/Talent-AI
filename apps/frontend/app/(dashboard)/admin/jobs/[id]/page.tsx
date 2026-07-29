'use client';

import React, { use, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { RecruiterJobsService } from '@/services/jobs.service';
import { RecruiterJob } from '@/types/job';
import { Loader2, ArrowLeft, MapPin, DollarSign, Calendar, Users, Eye } from 'lucide-react';
import Link from 'next/link';

interface AdminJobDetailPageProps {
  params: Promise<{ id: string }>;
}

export default function AdminJobDetailPage({ params }: AdminJobDetailPageProps) {
  const { id } = use(params);
  const router = useRouter();

  const [job, setJob] = useState<RecruiterJob | null>(null);
  const [loading, setLoading] = useState(true);

  async function loadData() {
    try {
      const match = await RecruiterJobsService.getJobById(id);
      setJob(match);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, [id]);

  const handleDelete = async () => {
    if (!job) return;
    const ok = window.confirm('Are you sure you want to permanently delete this job post?');
    if (ok) {
      const res = await RecruiterJobsService.deleteJob(job.id);
      if (res) {
        alert('Job post deleted successfully.');
        router.push('/admin/jobs');
      }
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading job posting details...</p>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12">
        <h3 className="text-red-500 font-bold text-lg">Job Listing Not Found</h3>
        <Link href="/admin/jobs" className="inline-block bg-blue-600 text-white px-4 py-2 rounded-xl text-xs font-semibold">
          Back to list
        </Link>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6 max-w-4xl mx-auto text-[#0F172A] text-left">
      <div className="flex items-center gap-3">
        <Link href="/admin/jobs" className="text-slate-400 hover:text-[#0F172A] cursor-pointer">
          <ArrowLeft size={18} />
        </Link>
        <h2 className="text-lg font-bold">Job post audit inspector</h2>
      </div>

      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
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

        <button
          onClick={handleDelete}
          className="bg-red-600 hover:bg-red-700 text-white font-bold text-xs px-4 py-2 rounded-xl transition-all cursor-pointer"
        >
          Delete Job Post
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {[
          { label: 'Views', val: job.views },
          { label: 'Applications', val: job.applicationsCount },
          { label: 'Shortlisted candidates', val: job.shortlistedCount },
          { label: 'Offers Sent', val: job.offersSentCount },
        ].map(({ label, val }) => (
          <div key={label} className="bg-white border border-[#E2E8F0] rounded-2xl p-4 shadow-sm">
            <span className="text-[10px] font-bold text-[#64748B] uppercase tracking-wide">{label}</span>
            <div className="text-xl sm:text-2xl font-black text-[#0F172A] mt-1">{val}</div>
          </div>
        ))}
      </div>

      {/* Detailed specifications */}
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 sm:p-6 shadow-sm space-y-4">
        <h4 className="font-bold text-xs uppercase tracking-wider text-[#64748B] border-b border-[#F1F5F9] pb-2">
          Position requirements
        </h4>
        <div className="space-y-3.5 text-xs sm:text-sm">
          <div>
            <span className="font-semibold text-slate-500 block mb-0.5">Required Skills</span>
            <div className="flex flex-wrap gap-1 mt-1">
              {job.skills.map((s) => (
                <span key={s} className="bg-slate-50 text-slate-700 border border-slate-100 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wide">
                  {s}
                </span>
              ))}
            </div>
          </div>

          <div className="pt-2">
            <span className="font-semibold text-slate-500 block mb-1">Description summary</span>
            <p className="text-slate-600 leading-relaxed font-medium">{job.description}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
