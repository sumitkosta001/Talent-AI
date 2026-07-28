'use client';

import { useState, useEffect } from 'react';
import { UserSessionData } from '@/types/auth';
import { authService } from '@/services/auth.service';

export function useAuth() {
  const [user, setUser] = useState<UserSessionData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

  useEffect(() => {
    async function loadSession() {
      try {
        const u = await authService.getCurrentUser();
        if (u) {
          setUser(u);
          setIsAuthenticated(true);
        } else {
          setUser(null);
          setIsAuthenticated(false);
        }
      } catch {
        setUser(null);
        setIsAuthenticated(false);
      } finally {
        setLoading(false);
      }
    }
    loadSession();
  }, []);

  const login = async (email: string, pass: string, role: 'candidate' | 'recruiter' = 'candidate') => {
    setLoading(true);
    try {
      const res = await authService.login(email, pass, role);
      setUser(res.user);
      setIsAuthenticated(true);
      return res;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    await authService.logout();
    setUser(null);
    setIsAuthenticated(false);
  };

  return {
    user,
    loading,
    isAuthenticated,
    login,
    logout,
  };
}
