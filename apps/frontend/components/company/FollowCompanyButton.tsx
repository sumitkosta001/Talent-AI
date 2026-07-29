'use client';

import React from 'react';
import { useFollowCompany } from '@/hooks/useFollowCompany';
import { Heart } from 'lucide-react';

interface FollowCompanyButtonProps {
  companyId: string;
}

export default function FollowCompanyButton({ companyId }: FollowCompanyButtonProps) {
  const { isFollowing, toggleFollow } = useFollowCompany(companyId);

  return (
    <button
      onClick={(e) => {
        e.preventDefault();
        toggleFollow();
      }}
      className={`
        inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition-all border cursor-pointer
        ${
          isFollowing
            ? 'bg-red-50 text-red-600 border-red-200 hover:bg-red-100'
            : 'bg-white text-slate-600 border-[#E2E8F0] hover:bg-[#F8FAFC]'
        }
      `}
    >
      <Heart size={13} fill={isFollowing ? 'currentColor' : 'none'} />
      <span>{isFollowing ? 'Following' : 'Follow'}</span>
    </button>
  );
}
