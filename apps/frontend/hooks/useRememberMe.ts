'use client';

import { useState, useEffect } from 'react';

export function useRememberMe() {
  const [rememberMe, setRememberMe] = useState(false);
  const [savedEmail, setSavedEmail] = useState('');

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const isRemember = localStorage.getItem('talentai_remember_me') === 'true';
    const email = localStorage.getItem('talentai_saved_email') || '';
    setRememberMe(isRemember);
    setSavedEmail(email);
  }, []);

  const toggleRemember = (remember: boolean, email = '') => {
    setRememberMe(remember);
    if (typeof window === 'undefined') return;
    if (remember) {
      localStorage.setItem('talentai_remember_me', 'true');
      if (email) localStorage.setItem('talentai_saved_email', email);
    } else {
      localStorage.removeItem('talentai_remember_me');
      localStorage.removeItem('talentai_saved_email');
    }
  };

  return {
    rememberMe,
    savedEmail,
    toggleRemember,
  };
}
