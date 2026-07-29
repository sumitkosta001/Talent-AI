'use client';

import React, { use, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { RecruiterJobsService } from '@/services/jobs.service';
import { RecruiterJob } from '@/types/job';
import JobForm from '@/components/recruiter/JobForm';
import { Loader2 } from 'lucide-react';

interface RecruiterJobEditPageProps {
  params: Promise<{ id: string }>;
}

export default function RecruiterJobEditPage({ params }: RecruiterJobEditPageProps) {
  const { id } = use(params);
  const router = useRouter();

  const [job, setJob] = useState<RecruiterJob | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const item = await RecruiterJobsService.getJobById(id);
        setJob(item);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [id]);

  const handleUpdate = async (payload: any) => {
    try {
      const success = await RecruiterJobsService.updateJob(id, payload);
      if (success) {
        alert('Job updated successfully!');
        router.push('/recruiter/jobs');
      }
    } catch {
      alert('Failed to save edits.');
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[40vh] gap-3">
        <Loader2 className="animate-spin text-blue-600" size={32} />
        <p className="text-sm font-semibold text-[#64748B]">Loading job details for editing...</p>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="p-6 text-center max-w-md mx-auto space-y-3 mt-12">
        <h3 className="text-red-500 font-bold text-lg">Job Not Found</h3>
        <button
          onClick={() => router.push('/recruiter/jobs')}
          className="bg-blue-600 text-white px-4 py-2 rounded-xl text-xs font-semibold cursor-pointer"
        >
          Return to List
        </button>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <JobForm initialJob={job} onSubmit={handleUpdate} isEdit />
    </div>
  );
}
