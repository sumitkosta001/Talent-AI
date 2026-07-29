'use client';

import React, { use } from 'react';
import { useApplicant } from '@/hooks/useApplicant';
import ApplicantProfile from '@/components/recruiter/ApplicantProfile';
import { Loader2, ArrowLeft } from 'lucide-react';
import Link from 'next/link';

interface RecruiterApplicantDetailPageProps {
  params: Promise<{ id: string }>;
}

export default function RecruiterApplicantDetailPage({ params }: RecruiterApplicantDetailPageProps) {
  const { id } = use(params);
  const { applicant, loading, error, updateStatus, addNotes } = useApplicant(id);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading candidate file details...</p>
      </div>
    );
  }

  if (error || !applicant) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12">
        <h3 className="text-red-500 font-bold text-lg">Candidate Profile Not Found</h3>
        <p className="text-sm text-[#64748B]">{error || 'Failed to retrieve record'}</p>
        <Link href="/recruiter/applicants" className="inline-block bg-blue-600 text-white px-4 py-2 rounded-xl text-xs font-semibold">
          Return to pipelines
        </Link>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      <div className="flex items-center gap-3 text-left">
        <Link href="/recruiter/applicants" className="text-slate-400 hover:text-[#0F172A] cursor-pointer">
          <ArrowLeft size={18} />
        </Link>
        <h2 className="text-lg font-bold">Candidate Evaluation Workspace</h2>
      </div>

      <ApplicantProfile
        applicant={applicant}
        onStatusChange={updateStatus}
        onAddNote={addNotes}
      />
    </div>
  );
}
