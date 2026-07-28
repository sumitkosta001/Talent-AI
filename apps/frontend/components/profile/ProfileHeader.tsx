'use client';

import React from 'react';
import { CandidateProfile } from '@/types/profile';
import { Mail, MapPin, Phone, ShieldCheck, Share2 } from 'lucide-react';

interface ProfileHeaderProps {
  profile: CandidateProfile;
  onEditToggle: () => void;
}

export default function ProfileHeader({ profile, onEditToggle }: ProfileHeaderProps) {
  const handleShare = () => {
    const link = `https://talentai.app/profile/${profile.id}`;
    navigator.clipboard.writeText(link);
    alert(`Profile URL copied to clipboard:\n${link}`);
  };

  return (
    <div className="p-5 sm:p-6 bg-white border border-[#E2E8F0] border-t-0 rounded-b-2xl shadow-sm text-[#0F172A] text-left">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-5">
        {/* Photo + Details */}
        <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center -mt-16 md:-mt-20">
          <div className="w-20 h-20 sm:w-24 sm:h-24 rounded-full bg-blue-600 border-4 border-white text-white font-black text-2xl sm:text-3xl flex items-center justify-center shadow-lg flex-shrink-0">
            {profile.name.split(' ').map(n => n[0]).join('')}
          </div>

          <div className="pt-2 sm:pt-12 md:pt-14 space-y-1">
            <div className="flex items-center gap-1.5 flex-wrap">
              <h2 className="text-lg sm:text-xl font-bold">{profile.name}</h2>
              <span className="inline-flex items-center gap-0.5 text-[9px] font-bold text-blue-600 bg-blue-50 px-1.5 py-0.5 rounded border border-blue-200 uppercase tracking-wide">
                <ShieldCheck size={10} /> Verified
              </span>
              {profile.isOpenToWork && (
                <span className="inline-flex items-center text-[9px] font-bold text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200 uppercase tracking-wide">
                  Open to work
                </span>
              )}
            </div>

            <p className="text-xs sm:text-sm text-slate-600 font-semibold">{profile.headline}</p>

            <div className="flex flex-wrap items-center gap-3 pt-1 text-[11px] text-[#64748B] font-bold">
              <span className="flex items-center gap-0.5"><MapPin size={12} /> {profile.location}</span>
              <span>·</span>
              <span className="flex items-center gap-0.5"><Mail size={12} /> {profile.email}</span>
              <span>·</span>
              <span className="flex items-center gap-0.5"><Phone size={12} /> {profile.phone}</span>
            </div>
          </div>
        </div>

        {/* Buttons */}
        <div className="flex items-center gap-2 pt-2 md:pt-0">
          <button
            onClick={handleShare}
            className="p-2 border border-[#E2E8F0] hover:bg-[#F8FAFC] text-[#64748B] hover:text-[#0F172A] rounded-xl transition-all cursor-pointer"
            title="Share profile link"
          >
            <Share2 size={15} />
          </button>
          <button
            onClick={onEditToggle}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs px-4.5 py-2 rounded-xl transition-all cursor-pointer"
          >
            Edit Profile
          </button>
        </div>
      </div>
    </div>
  );
}
