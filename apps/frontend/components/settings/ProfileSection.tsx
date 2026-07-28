'use client';

import React from 'react';
import { CandidateProfile } from '@/types/profile';
import ProfilePhotoUploader from './ProfilePhotoUploader';

interface ProfileSectionProps {
  profile?: CandidateProfile;
  onChange: (field: keyof CandidateProfile, value: any) => void;
}

export default function ProfileSection({ profile, onChange }: ProfileSectionProps) {
  if (!profile) return null;

  return (
    <div className="space-y-5">
      {/* Profile Photo */}
      <ProfilePhotoUploader
        initialPic={profile.profilePic}
        onUpdate={(pic) => onChange('profilePic', pic)}
      />

      {/* Grid fields */}
      <div className="grid sm:grid-cols-2 gap-4 text-left">
        {/* First Name */}
        <div>
          <label className="block text-xs font-bold text-[#475569] mb-1.5">First Name</label>
          <input
            type="text"
            value={profile.firstName}
            onChange={(e) => onChange('firstName', e.target.value)}
            className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
          />
        </div>

        {/* Last Name */}
        <div>
          <label className="block text-xs font-bold text-[#475569] mb-1.5">Last Name</label>
          <input
            type="text"
            value={profile.lastName}
            onChange={(e) => onChange('lastName', e.target.value)}
            className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
          />
        </div>

        {/* Email */}
        <div>
          <label className="block text-xs font-bold text-[#475569] mb-1.5">Email Address</label>
          <input
            type="email"
            value={profile.email}
            onChange={(e) => onChange('email', e.target.value)}
            className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
          />
        </div>

        {/* Phone */}
        <div>
          <label className="block text-xs font-bold text-[#475569] mb-1.5">Phone Number</label>
          <input
            type="text"
            value={profile.phone}
            onChange={(e) => onChange('phone', e.target.value)}
            className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
          />
        </div>

        {/* Date of Birth */}
        <div>
          <label className="block text-xs font-bold text-[#475569] mb-1.5">Date of Birth</label>
          <input
            type="date"
            value={profile.dob}
            onChange={(e) => onChange('dob', e.target.value)}
            className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
          />
        </div>

        {/* Gender */}
        <div>
          <label className="block text-xs font-bold text-[#475569] mb-1.5">Gender</label>
          <select
            value={profile.gender}
            onChange={(e) => onChange('gender', e.target.value)}
            className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white cursor-pointer"
          >
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
            <option value="Prefer not to say">Prefer not to say</option>
          </select>
        </div>

        {/* City */}
        <div>
          <label className="block text-xs font-bold text-[#475569] mb-1.5">City</label>
          <input
            type="text"
            value={profile.city}
            onChange={(e) => onChange('city', e.target.value)}
            className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
          />
        </div>

        {/* Country */}
        <div>
          <label className="block text-xs font-bold text-[#475569] mb-1.5">Country</label>
          <input
            type="text"
            value={profile.country}
            onChange={(e) => onChange('country', e.target.value)}
            className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
          />
        </div>

        {/* Headline */}
        <div className="sm:col-span-2">
          <label className="block text-xs font-bold text-[#475569] mb-1.5">Headline</label>
          <input
            type="text"
            value={profile.headline}
            onChange={(e) => onChange('headline', e.target.value)}
            className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
          />
        </div>

        {/* Bio */}
        <div className="sm:col-span-2">
          <label className="block text-xs font-bold text-[#475569] mb-1.5">Profile Biography</label>
          <textarea
            rows={3}
            value={profile.bio}
            onChange={(e) => onChange('bio', e.target.value)}
            className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white resize-none"
          />
        </div>

        {/* Current role */}
        <div>
          <label className="block text-xs font-bold text-[#475569] mb-1.5">Current Role</label>
          <input
            type="text"
            value={profile.currentRole}
            onChange={(e) => onChange('currentRole', e.target.value)}
            className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
          />
        </div>

        {/* Years of Experience */}
        <div>
          <label className="block text-xs font-bold text-[#475569] mb-1.5">Years of Experience</label>
          <input
            type="number"
            value={profile.yearsOfExperience}
            onChange={(e) => onChange('yearsOfExperience', parseInt(e.target.value) || 0)}
            className="w-full px-3 py-2 border border-[#E2E8F0] rounded-xl text-sm text-[#0F172A] focus:outline-none focus:border-blue-500 bg-white"
          />
        </div>
      </div>
    </div>
  );
}
