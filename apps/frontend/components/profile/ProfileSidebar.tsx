'use client';

import React from 'react';
import ProfileCompletion from './ProfileCompletion';
import { Eye, Shield, Globe, Lock } from 'lucide-react';
import { CandidateProfile, ProfileVisibility } from '@/types/profile';

interface ProfileSidebarProps {
  profile: CandidateProfile;
  onVisibilityChange: (v: ProfileVisibility) => void;
}

export default function ProfileSidebar({ profile, onVisibilityChange }: ProfileSidebarProps) {
  const getIcon = (v: ProfileVisibility) => {
    if (v === 'Public') return Globe;
    if (v === 'Recruiters Only') return Eye;
    return Lock;
  };

  const Icon = getIcon(profile.visibility);

  return (
    <div className="space-y-6 text-[#0F172A] text-left">
      {/* Profile Completeness progress card */}
      <ProfileCompletion percentage={profile.completionPercentage} />

      {/* Visibility Settings card */}
      <div className="bg-white border border-[#E2E8F0] rounded-2xl p-5 shadow-sm space-y-4">
        <h4 className="font-bold text-xs uppercase tracking-wide text-[#64748B] border-b border-[#F1F5F9] pb-2 flex items-center gap-1.5">
          <Shield size={14} className="text-[#2563EB]" />
          Visibility & Privacy
        </h4>

        <div className="space-y-3">
          <div className="flex items-center gap-2.5 p-3 border border-[#F1F5F9] bg-[#F8FAFC]/50 rounded-xl">
            <div className="p-2 bg-blue-50 text-blue-600 rounded-lg flex-shrink-0">
              <Icon size={16} />
            </div>
            <div className="text-xs font-semibold">
              <span className="text-[#64748B] block mb-0.5 font-bold uppercase tracking-wider text-[8px]">Current State</span>
              <span className="text-[#0F172A] font-bold text-xs">{profile.visibility}</span>
            </div>
          </div>

          <div>
            <label className="block text-[10px] font-bold text-[#64748B] mb-1.5 uppercase tracking-wide">Change Visibility</label>
            <select
              value={profile.visibility}
              onChange={(e) => onVisibilityChange(e.target.value as ProfileVisibility)}
              className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] bg-white focus:outline-none focus:border-blue-500 cursor-pointer font-bold"
            >
              <option value="Public">Public (Everyone can see)</option>
              <option value="Recruiters Only">Recruiters Only</option>
              <option value="Private">Private (Only you)</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );
}
export type UserStatus = 'Active' | 'Suspended' | 'Deactivated';
export type UserRole = 'Super Admin' | 'Admin' | 'Moderator' | 'Support' | 'Candidate' | 'Recruiter';
export type ProfileVisibilityOptions = 'Public' | 'Recruiters Only' | 'Private';
