'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { RecruiterJobsService } from '@/services/jobs.service';
import JobForm from '@/components/recruiter/JobForm';

export default function RecruiterJobCreatePage() {
  const router = useRouter();

  const handlePublish = async (payload: any) => {
    try {
      const created = await RecruiterJobsService.createJob(payload);
      if (created) {
        alert('Job posted successfully!');
        router.push('/recruiter/jobs');
      }
    } catch {
      alert('Failed to publish job. Please try again.');
    }
  };

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <JobForm onSubmit={handlePublish} />
    </div>
  );
}
