'use client';

import { useState, useEffect, useCallback } from 'react';

export function useFollowCompany(companyId: string) {
  const [isFollowing, setIsFollowing] = useState(false);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const items = localStorage.getItem('talentai_followed_companies');
    if (items) {
      const parsed: string[] = JSON.parse(items);
      setIsFollowing(parsed.includes(companyId));
    }
  }, [companyId]);

  const toggleFollow = useCallback(() => {
    if (typeof window === 'undefined') return;
    const items = localStorage.getItem('talentai_followed_companies');
    let parsed: string[] = items ? JSON.parse(items) : [];

    if (parsed.includes(companyId)) {
      parsed = parsed.filter(id => id !== companyId);
      setIsFollowing(false);
    } else {
      parsed.push(companyId);
      setIsFollowing(true);
    }
    localStorage.setItem('talentai_followed_companies', JSON.stringify(parsed));
  }, [companyId]);

  return {
    isFollowing,
    toggleFollow,
  };
}
