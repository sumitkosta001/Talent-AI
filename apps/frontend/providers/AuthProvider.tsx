'use client';

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { UserSessionData } from '@/types/auth';
import { authService } from '@/services/auth.service';

interface AuthContextType {
  user: UserSessionData | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (email: string, pass: string, role: 'candidate' | 'recruiter') => Promise<any>;
  logout: () => Promise<void>;
  setUser: React.Dispatch<React.SetStateAction<UserSessionData | null>>;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<UserSessionData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const loadSession = useCallback(async () => {
    try {
      const u = await authService.getCurrentUser();
      if (u) {
        setUser(u);
      } else {
        setUser(null);
      }
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadSession();

    // Listen to changes from centralized API client (e.g. token refresh/expired)
    if (typeof window !== 'undefined') {
      const syncState = () => {
        const stored = localStorage.getItem('talentai_auth_user');
        if (stored) {
          try {
            setUser(JSON.parse(stored));
          } catch {
            setUser(null);
          }
        } else {
          setUser(null);
        }
      };
      window.addEventListener('auth-state-changed', syncState);
      return () => {
        window.removeEventListener('auth-state-changed', syncState);
      };
    }
  }, [loadSession]);

  const login = useCallback(async (email: string, pass: string, role: 'candidate' | 'recruiter' = 'candidate') => {
    setLoading(true);
    try {
      const res = await authService.login(email, pass, role);
      setUser(res.user);
      if (typeof window !== 'undefined') {
        window.dispatchEvent(new Event('auth-state-changed'));
      }
      return res;
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    setLoading(true);
    try {
      await authService.logout();
    } finally {
      setUser(null);
      setLoading(false);
      if (typeof window !== 'undefined') {
        window.dispatchEvent(new Event('auth-state-changed'));
      }
    }
  }, []);

  const value: AuthContextType = {
    user,
    loading,
    isAuthenticated: !!user,
    login,
    logout,
    setUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
