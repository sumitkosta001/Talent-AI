'use client';

import React from 'react';
import { Application } from '@/types/application';
import TimelineStep from './TimelineStep';
import InterviewSection from './InterviewSection';
import OfferLetter from './OfferLetter';
import RejectedFeedback from './RejectedFeedback';
import { MapPin, DollarSign, Calendar, Mail, FileText, ArrowLeft, Bot } from 'lucide-react';
import Link from 'next/link';

interface ApplicationDetailsProps {
  application: Application;
  onBack?: () => void;
}

export default function ApplicationDetails({
  application,
  onBack,
}: ApplicationDetailsProps) {
  const {
    company,
    jobTitle,
    location,
    salary,
    appliedDate,
    status,
    atsScore,
    matchPercentage,
    recruiter,
    notes,
    timeline,
    interview,
    offer,
    rejectionReason,
    rejectionFeedback,
    rejectionImprovement,
  } = application;

  const getStatusColor = (s: string) => {
    switch (s) {
      case 'Offer Received':
      case 'Offer Accepted':
        return 'bg-green-50 text-green-700 border-green-200';
      case 'Technical Interview':
      case 'HR Interview':
      case 'Final Interview':
        return 'bg-violet-50 text-violet-700 border-violet-200';
      case 'Rejected':
        return 'bg-red-50 text-red-700 border-red-200';
      case 'Withdrawn':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      default:
        return 'bg-blue-50 text-blue-700 border-blue-200';
    }
  };

  return (
    <div className="space-y-6 text-[#0F172A]">
      {/* Back button */}
      {onBack && (
        <button
          onClick={onBack}
          className="flex items-center gap-1.5 text-xs font-semibold text-[#64748B] hover:text-[#0F172A] cursor-pointer transition-colors"
        >
          <ArrowLeft size={14} />
          Back to Applications
        </button>
      )}

      {/* Header layout */}
      <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex gap-4">
          <div className={`w-14 h-14 rounded-2xl ${application.logoColor} flex items-center justify-center text-white font-bold text-2xl flex-shrink-0`}>
            {application.logo}
          </div>
          <div className="text-left">
            <h2 className="text-lg sm:text-xl font-bold">{jobTitle}</h2>
            <div className="flex flex-wrap items-center gap-2 mt-1 text-xs text-[#64748B] font-semibold">
              <span className="text-[#0F172A]">{company}</span>
              <span>·</span>
              <span className="flex items-center gap-0.5"><MapPin size={12} /> {location}</span>
              <span>·</span>
              <span className="flex items-center gap-0.5"><DollarSign size={12} /> {salary}</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className={`text-[10px] font-bold px-3 py-1 rounded-full border uppercase tracking-wider ${getStatusColor(status)}`}>
            {status}
          </span>
          <span className="text-[10px] font-bold bg-green-50 text-green-700 border border-green-200 px-3 py-1 rounded-full uppercase tracking-wider">
            {matchPercentage}% Match Rate
          </span>
        </div>
      </div>

      {/* Columns split */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left timeline & notes content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Timeline tracking stages */}
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-5">
            <h3 className="font-bold text-sm text-[#0F172A] border-b border-[#F1F5F9] pb-3 uppercase tracking-wide">
              Application Timeline Journey
            </h3>
            <TimelineStep timeline={timeline} />
          </div>

          {/* Notes & details */}
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm space-y-4 text-left">
            <h3 className="font-bold text-sm text-[#0F172A] border-b border-[#F1F5F9] pb-3 uppercase tracking-wide">
              Candidate Notes & Specifications
            </h3>
            {notes ? (
              <p className="text-xs sm:text-sm text-[#64748B] leading-relaxed">{notes}</p>
            ) : (
              <p className="text-xs text-[#94A3B8] italic">No custom notes specified for this role.</p>
            )}
          </div>
        </div>

        {/* Right sidebar profiling selectors */}
        <div className="space-y-6">
          {/* Rejections, Interview section, or Offer Letter depending on status */}
          {status === 'Rejected' && (
            <RejectedFeedback
              reason={rejectionReason}
              feedback={rejectionFeedback}
              improvement={rejectionImprovement}
            />
          )}

          {offer && (
            <OfferLetter offer={offer} />
          )}

          {interview && (
            <InterviewSection interview={interview} />
          )}

          {/* Recruiter info */}
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
            <h4 className="font-bold text-sm text-[#0F172A]">Assigned Recruiter</h4>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-blue-500 text-white font-bold flex items-center justify-center text-xs">
                {recruiter.avatar || recruiter.name.split(' ').map(n => n[0]).join('')}
              </div>
              <div>
                <p className="font-bold text-[#0F172A] text-xs sm:text-sm">{recruiter.name}</p>
                <p className="text-[10px] text-[#64748B] font-semibold flex items-center gap-1 mt-0.5">
                  <Mail size={11} />
                  {recruiter.email}
                </p>
              </div>
            </div>
          </div>

          {/* Audit compatibility details */}
          <div className="bg-white rounded-2xl border border-[#E2E8F0] p-5 shadow-sm space-y-4 text-left">
            <h4 className="font-bold text-sm text-[#0F172A] flex items-center gap-1.5">
              <Bot size={18} className="text-violet-600" />
              ATS Audit Report
            </h4>
            <div className="flex items-center gap-4">
              <div className="text-center bg-[#F8FAFC] border border-[#E2E8F0] px-4 py-2.5 rounded-xl">
                <span className="text-lg font-black text-[#0F172A]">{atsScore}%</span>
                <p className="text-[9px] text-[#64748B] font-bold mt-0.5 uppercase">ATS Score</p>
              </div>
              <p className="text-xs text-[#64748B] leading-relaxed">
                Resume parsed matching keywords index. Audit reports show excellent compatibility metrics.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
