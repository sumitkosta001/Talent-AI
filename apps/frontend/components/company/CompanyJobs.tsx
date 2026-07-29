'use client';

import React from 'react';
import { Job } from '@/types/job';
import { Briefcase, MapPin, DollarSign, ArrowRight } from 'lucide-react';
import Link from 'next/link';

interface CompanyJobsProps {
  jobs: Job[];
}

export default function CompanyJobs({ jobs }: CompanyJobsProps) {
  return (
    <div className="space-y-4 text-left text-[#0F172A]">
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm">
        <h3 className="font-bold text-sm sm:text-base mb-1">Open Positions ({jobs.length})</h3>
        <p className="text-xs text-[#64748B] font-semibold">Join us to scale economic infrastructure systems for internet software.</p>
      </div>

      {jobs.length === 0 ? (
        <div className="bg-white rounded-2xl border border-[#E2E8F0] p-8 text-center text-xs text-[#64748B] font-semibold shadow-sm">
          No open job listings recorded currently. Check back later.
        </div>
      ) : (
        <div className="space-y-3">
          {jobs.map((job) => (
            <div
              key={job.id}
              className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm hover:shadow-md transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4"
            >
              <div className="space-y-1">
                <h4 className="font-bold text-sm text-[#0F172A] leading-normal">{job.role}</h4>
                <div className="flex flex-wrap items-center gap-3 text-xs text-[#64748B] font-semibold pt-0.5">
                  <span className="flex items-center gap-0.5"><MapPin size={12} /> {job.location}</span>
                  <span>·</span>
                  <span>{job.type}</span>
                  <span>·</span>
                  <span className="flex items-center gap-0.5"><DollarSign size={12} /> {job.salary}</span>
                </div>
              </div>

              <div className="flex items-center justify-between gap-4 self-end sm:self-center">
                <span className="text-[10px] text-emerald-600 bg-emerald-50 px-2 py-0.5 border border-emerald-200 font-bold rounded">
                  {job.match}% AI match
                </span>
                <Link
                  href={`/jobs/${job.id}`}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all inline-flex items-center gap-1 cursor-pointer"
                >
                  Apply Now
                  <ArrowRight size={13} />
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
