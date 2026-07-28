import { UserSessionData } from '@/types/auth';
import { MOCK_USER_SESSION, MOCK_RECRUITER_SESSION } from '@/mock/auth';

const DEV_MODE = true;

export const authService = {
  async login(email: string, pass: string, role: 'candidate' | 'recruiter' = 'candidate'): Promise<{ user: UserSessionData; token: string }> {
    if (DEV_MODE) {
      await new Promise((r) => setTimeout(r, 600));
      const user = role === 'recruiter' ? MOCK_RECRUITER_SESSION : { ...MOCK_USER_SESSION, email: email || MOCK_USER_SESSION.email };
      if (typeof window !== 'undefined') {
        localStorage.setItem('talentai_auth_user', JSON.stringify(user));
        localStorage.setItem('talentai_auth_token', 'mock-jwt-token-xyz-123');
      }
      return { user, token: 'mock-jwt-token-xyz-123' };
    }
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password: pass, role }),
    });
    if (!res.ok) throw new Error('Invalid email or password');
    return res.json();
  },

  async register(data: { name: string; email: string; pass: string; role: string }): Promise<{ success: boolean; message: string }> {
    if (DEV_MODE) {
      await new Promise((r) => setTimeout(r, 700));
      return { success: true, message: 'Account registered successfully. Verification link sent.' };
    }
    const res = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Registration failed. Email may already be in use.');
    return res.json();
  },

  async logout(): Promise<void> {
    if (DEV_MODE) {
      await new Promise((r) => setTimeout(r, 200));
      if (typeof window !== 'undefined') {
        localStorage.removeItem('talentai_auth_token');
        localStorage.removeItem('talentai_auth_user');
        localStorage.removeItem('talentai_remember_user');
      }
      return;
    }
    await fetch('/api/auth/logout', { method: 'POST' });
  },

  async getCurrentUser(): Promise<UserSessionData | null> {
    if (DEV_MODE) {
      const stored = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_user') : null;
      if (stored) {
        try {
          return JSON.parse(stored);
        } catch {
          return MOCK_USER_SESSION;
        }
      }
      return MOCK_USER_SESSION;
    }
    const res = await fetch('/api/auth/session');
    if (!res.ok) return null;
    return res.json();
  },
};
