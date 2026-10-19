'use client';

import React from 'react';
import { Job } from '@/types/job';
import { Company } from '@/types/company';
import SalaryCard from './SalaryCard';
import JobStats from './JobStats';
import JobDescription from './JobDescription';
import EducationRequirements from './EducationRequirements';
import Responsibilities from './Responsibilities';
import Requirements from './Requirements';
import Benefits from './Benefits';
import SkillsRequired from './SkillsRequired';
import JobMatchCard from './JobMatchCard';
import ATSMatchCard from './ATSMatchCard';
import BookmarkButton from './BookmarkButton';
import ApplyButton from './ApplyButton';
import CompanyInfo from './CompanyInfo';
import CompanyStats from './CompanyStats';
import { ArrowLeft, Share2, MapPin, Briefcase, Building } from 'lucide-react';

interface JobDetailsProps {
  job: Job;
  companyProfile?: Company | null;
  onBack?: () => void;
  isDashboardLink?: boolean;
}

export default function JobDetails({
  job,
  companyProfile,
  onBack,
  isDashboardLink = false,
}: JobDetailsProps) {
  const companyName = companyProfile?.name || job.company || 'Company';
  const roleTitle = job.role || job.title;
  const workMode = job.remoteStatus || job.workMode;

  const handleShare = () => {
    if (typeof navigator !== 'undefined' && navigator.clipboard) {
      navigator.clipboard.writeText(window.location.href);
      alert('Job listing link copied to clipboard!');
    }
  };

  return (
    <div className="space-y-6">
      {/* Back button */}
      {onBack && (
        <button
          type="button"
          onClick={onBack}
          className="flex items-center gap-1.5 text-xs font-semibold text-[#64748B] hover:text-[#0F172A] cursor-pointer transition-colors"
        >
          <ArrowLeft size={14} />
          Back to Listings
        </button>
      )}

      {/* Header card */}
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex gap-4">
          <div className={`w-14 h-14 rounded-2xl ${job.logoColor || 'bg-blue-600'} flex items-center justify-center text-white font-bold text-2xl flex-shrink-0`}>
            {job.logo || companyName.charAt(0).toUpperCase()}
          </div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h1 className="text-lg sm:text-xl font-bold text-[#0F172A]">{roleTitle}</h1>
              {job.status && (
                <span className={`px-2 py-0.5 rounded-md text-[11px] font-semibold ${
                  job.status.toUpperCase() === 'PUBLISHED'
                    ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                    : 'bg-slate-100 text-slate-600 border border-slate-200'
                }`}>
                  {job.status}
                </span>
              )}
            </div>
            <div className="flex flex-wrap items-center gap-2 mt-1.5 text-xs text-[#64748B] font-medium">
              <span className="font-semibold text-[#0F172A]">{companyName}</span>
              <span>·</span>
              <span className="flex items-center gap-1">
                <MapPin size={12} /> {job.location || 'Remote'}
              </span>
              <span>·</span>
              <span className="flex items-center gap-1">
                <Briefcase size={12} /> {job.experience}
              </span>
              {workMode && (
                <>
                  <span>·</span>
                  <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-blue-50 text-blue-700 border border-blue-200">
                    {workMode}
                  </span>
                </>
              )}
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2 flex-wrap sm:flex-nowrap">
          <button
            type="button"
            onClick={handleShare}
            className="p-2.5 rounded-xl border border-[#E2E8F0] text-[#64748B] hover:text-[#0F172A] hover:bg-[#F8FAFC] transition-colors cursor-pointer"
            title="Share Job"
          >
            <Share2 size={16} />
          </button>
          <BookmarkButton jobId={job.id} />
          <ApplyButton
            jobId={job.id}
            role={roleTitle}
            company={companyName}
            logo={job.logo}
            logoColor={job.logoColor}
            salary={job.salary}
            location={job.location}
            status={job.status}
            className="py-2.5 px-6 text-sm"
          />
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Main description details */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-6">
            <JobDescription description={job.description} />
            <EducationRequirements items={job.educationRequirements || job.education_requirements} />
            <Responsibilities items={job.responsibilities} />
            <Requirements items={job.requirements} />
            <Benefits items={job.benefits} />
          </div>
        </div>

        {/* Sidebar panels */}
        <div className="space-y-6">
          {/* Match rating details */}
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
            <h4 className="font-bold text-sm text-[#0F172A]">Candidate Profile Matches</h4>
            <JobMatchCard score={job.match} />
            <ATSMatchCard score={job.match} />
          </div>

          {/* Job specs */}
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4">
            <h4 className="font-bold text-sm text-[#0F172A]">Compensation & Specs</h4>
            <SalaryCard salary={job.salary} />
            <JobStats
              postedDate={job.date}
              status={job.status}
              workMode={workMode}
              deadline={job.deadline}
              applicantsCount={job.applicantsCount}
            />
            <SkillsRequired skills={job.skills} />
          </div>

          {/* Company Profiling */}
          {companyProfile ? (
            <div className="space-y-6">
              <CompanyInfo company={companyProfile} />
              <CompanyStats company={companyProfile} />
            </div>
          ) : (
            <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-2">
              <div className="flex items-center gap-2 text-[#0F172A]">
                <Building size={16} />
                <h4 className="font-bold text-sm">About {companyName}</h4>
              </div>
              <p className="text-xs text-[#64748B]">
                Detailed corporate profile is not available for this employer.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
