'use client';

import React from 'react';
import Link from 'next/link';
import { MapPin, DollarSign, Briefcase, Calendar } from 'lucide-react';
import { Job } from '@/types/job';
import BookmarkButton from './BookmarkButton';
import ApplyButton from './ApplyButton';

interface JobCardProps {
  job: Job;
  isDashboardLink?: boolean;
}

export default function JobCard({ job, isDashboardLink = false }: JobCardProps) {
  const detailLink = isDashboardLink 
    ? `/candidate/jobs/${job.id}` 
    : `/jobs/${job.id}`;

  const getMatchColor = (match: number) => {
    if (match >= 90) return 'bg-green-50 text-green-700 border-green-100';
    if (match >= 75) return 'bg-blue-50 text-blue-700 border-blue-100';
    if (match >= 50) return 'bg-amber-50 text-amber-700 border-amber-100';
    return 'bg-red-50 text-red-700 border-red-100';
  };

  return (
    <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 hover:shadow-md hover:border-[#CBD5E1] transition-all relative">
      <div className="flex items-start gap-4">
        {/* Company logo */}
        <div className={`w-12 h-12 rounded-xl ${job.logoColor} flex items-center justify-center text-white font-bold text-lg flex-shrink-0`}>
          {job.logo}
        </div>

        {/* Content details */}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-3">
            <div>
              <Link href={detailLink} className="block group">
                <h3 className="font-semibold text-sm sm:text-base text-[#0F172A] group-hover:text-blue-600 transition-colors line-clamp-1">
                  {job.role}
                </h3>
              </Link>
              <p className="text-xs text-[#64748B] mt-0.5">{job.company}</p>
            </div>
            
            <div className="flex items-center gap-2 flex-shrink-0">
              <span className={`text-[10px] sm:text-xs font-semibold px-2 py-0.5 rounded-full border ${getMatchColor(job.match)}`}>
                {job.match}% Match
              </span>
              <BookmarkButton jobId={job.id} />
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3 mt-3 text-[11px] text-[#64748B]">
            <span className="flex items-center gap-1">
              <MapPin size={12} />
              {job.location}
            </span>
            <span className="flex items-center gap-1">
              <DollarSign size={12} />
              {job.salary}
            </span>
            <span className="flex items-center gap-1">
              <Briefcase size={12} />
              {job.experience}
            </span>
            <span className="flex items-center gap-1">
              <Calendar size={12} />
              {job.date}
            </span>
          </div>

          <div className="flex items-center justify-between mt-4 pt-4 border-t border-[#F1F5F9]">
            <div className="flex flex-wrap gap-1 max-w-[70%]">
              {job.skills.slice(0, 3).map(skill => (
                <span key={skill} className="text-[10px] bg-[#F8FAFC] border border-[#E2E8F0] text-[#64748B] px-2 py-0.5 rounded-md">
                  {skill}
                </span>
              ))}
              {job.skills.length > 3 && (
                <span className="text-[10px] text-[#94A3B8] font-semibold px-1 py-0.5">
                  +{job.skills.length - 3} more
                </span>
              )}
            </div>

            <div className="flex items-center gap-2">
              <Link
                href={detailLink}
                className="text-xs text-[#64748B] hover:text-[#0F172A] font-semibold px-3 py-2 transition-colors"
              >
                Details
              </Link>
              <ApplyButton
                jobId={job.id}
                role={job.role}
                company={job.company}
                logo={job.logo}
                logoColor={job.logoColor}
                salary={job.salary}
                location={job.location}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
