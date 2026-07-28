'use client';

import React from 'react';
import { CandidateProfile } from '@/types/profile';
import { Mail, MapPin, Phone, User, Calendar, Award } from 'lucide-react';

interface ProfileOverviewProps {
  profile: CandidateProfile;
}

export default function ProfileOverview({ profile }: ProfileOverviewProps) {
  return (
    <div className="space-y-6 text-[#0F172A] text-left">
      {/* Summary */}
      <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-3">
        <h3 className="font-bold text-sm sm:text-base">Professional summary</h3>
        <p className="text-xs sm:text-sm text-slate-600 leading-relaxed font-semibold">
          {profile.bio}
        </p>
      </div>

      {/* Personal Info Grid */}
      <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-4">
        <h3 className="font-bold text-xs uppercase tracking-wide text-[#64748B] border-b border-[#F1F5F9] pb-2">
          Personal specs
        </h3>
        <div className="grid sm:grid-cols-2 gap-4 text-xs sm:text-sm">
          <div>
            <span className="font-semibold text-[#64748B] block mb-0.5">Date of Birth</span>
            <span className="font-bold text-[#0F172A] flex items-center gap-1"><Calendar size={13} /> {profile.dob || 'Not declared'}</span>
          </div>
          <div>
            <span className="font-semibold text-[#64748B] block mb-0.5">Nationality</span>
            <span className="font-bold text-[#0F172A] flex items-center gap-1"><Award size={13} /> {profile.nationality || 'Not declared'}</span>
          </div>
          <div>
            <span className="font-semibold text-[#64748B] block mb-0.5">Gender</span>
            <span className="font-bold text-[#0F172A] flex items-center gap-1"><User size={13} /> {profile.gender || 'Not declared'}</span>
          </div>
          <div>
            <span className="font-semibold text-[#64748B] block mb-0.5">Availability Start</span>
            <span className="font-bold text-blue-600">{profile.availabilityStatus}</span>
          </div>
        </div>
      </div>

      {/* Preferences Grid */}
      <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-4">
        <h3 className="font-bold text-xs uppercase tracking-wide text-[#64748B] border-b border-[#F1F5F9] pb-2">
          Work preferences
        </h3>
        <div className="grid sm:grid-cols-2 gap-4 text-xs sm:text-sm">
          <div>
            <span className="font-semibold text-[#64748B] block mb-0.5">Preferred Job Role</span>
            <span className="font-bold text-[#0F172A]">{profile.preferredRole || 'Not declared'}</span>
          </div>
          <div>
            <span className="font-semibold text-[#64748B] block mb-0.5">Work Mode Status</span>
            <span className="font-bold text-[#0F172A]">{profile.preferredWorkMode || 'Not declared'}</span>
          </div>
          <div>
            <span className="font-semibold text-[#64748B] block mb-0.5">Expected Compensation</span>
            <span className="font-bold text-[#0F172A]">{profile.expectedSalary || 'Not declared'}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
