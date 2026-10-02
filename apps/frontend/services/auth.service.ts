import { UserSessionData } from '@/types/auth';
import { MOCK_USER_SESSION, MOCK_RECRUITER_SESSION } from '@/mock/auth';

const DEV_MODE = false;

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

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
    const res = await fetch(`${API_URL}/api/v1/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({ email, password: pass }),
    });

    const body = await res.json();
    if (!res.ok) {
      throw new Error(body?.error?.message || body?.detail || 'Invalid email or password');
    }

    const userSession: UserSessionData = {
      id: body.user.id,
      email: body.user.email,
      role: body.user.role,
      name: body.user.full_name,
      accountState: body.user.is_verified ? 'Active' : 'EmailNotVerified',
      twoFactorEnabled: false,
      lastLogin: new Date().toISOString(),
      lastDevice: 'Chrome (Windows)',
      trustedDevices: [],
    };

    const token = body.tokens.access_token;

    if (typeof window !== 'undefined') {
      localStorage.setItem('talentai_auth_user', JSON.stringify(userSession));
      localStorage.setItem('talentai_auth_token', token);
      localStorage.setItem('talentai_auth_refresh_token', body.tokens.refresh_token);
    }

    return { user: userSession, token };
  },

  async register(data: { name: string; email: string; pass: string; role: string }): Promise<{ success: boolean; message: string; user?: any; verification_sent?: boolean }> {
    if (DEV_MODE) {
      await new Promise((r) => setTimeout(r, 700));
      return { success: true, message: 'Account registered successfully. Verification link sent.' };
    }
    const nameParts = data.name.trim().split(/\s+/);
    const first_name = nameParts[0] || 'First';
    const last_name = nameParts.slice(1).join(' ') || 'User';

    const res = await fetch(`${API_URL}/api/v1/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({
        email: data.email,
        password: data.pass,
        confirm_password: data.pass,
        first_name,
        last_name,
        role: data.role || 'candidate',
      }),
    });

    const body = await res.json();
    if (!res.ok) {
      throw new Error(body?.error?.message || body?.detail || 'Registration failed. Email may already be in use.');
    }

    return {
      success: true,
      message: body.message || 'Account registered successfully. Verification link sent.',
      user: body.user,
      verification_sent: body.verification_sent,
    };
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
    const refreshToken = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_refresh_token') : null;
    if (refreshToken) {
      await fetch(`${API_URL}/api/v1/auth/logout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });
    }
    if (typeof window !== 'undefined') {
      localStorage.removeItem('talentai_auth_token');
      localStorage.removeItem('talentai_auth_refresh_token');
      localStorage.removeItem('talentai_auth_user');
      localStorage.removeItem('talentai_remember_user');
    }
  },

  async getCurrentUser(): Promise<UserSessionData | null> {
    const token = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_token') : null;
    if (token) {
      try {
        const res = await fetch(`${API_URL}/api/v1/auth/me`, {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });

        if (res.ok) {
          const body = await res.json();
          const userSession: UserSessionData = {
            id: body.user.id,
            email: body.user.email,
            role: body.user.role,
            name: body.user.full_name,
            accountState: body.user.is_verified ? 'Active' : 'EmailNotVerified',
            twoFactorEnabled: false,
            lastLogin: new Date().toISOString(),
            lastDevice: 'Chrome (Windows)',
            trustedDevices: [],
          };

          if (typeof window !== 'undefined') {
            localStorage.setItem('talentai_auth_user', JSON.stringify(userSession));
          }

          return userSession;
        }

        if (res.status === 401) {
          const fresh = await this.refreshTokens();
          if (fresh) return fresh.user;
          if (typeof window !== 'undefined') {
            localStorage.removeItem('talentai_auth_token');
            localStorage.removeItem('talentai_auth_refresh_token');
            localStorage.removeItem('talentai_auth_user');
          }
        }
      } catch (err) {
        console.warn('Backend GET /api/v1/auth/me error:', err);
      }
    }

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

    return null;
  },

  async refreshTokens(): Promise<{ user: UserSessionData; token: string } | null> {
    const refreshToken = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_refresh_token') : null;
    if (!refreshToken) return null;

    const res = await fetch(`${API_URL}/api/v1/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (!res.ok) return null;

    const body = await res.json();
    let userSession: UserSessionData | null = null;
    const storedUser = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_user') : null;
    if (storedUser) {
      try {
        userSession = JSON.parse(storedUser);
      } catch {}
    }

    if (body.user) {
      userSession = {
        id: body.user.id,
        email: body.user.email,
        role: body.user.role,
        name: body.user.full_name,
        accountState: body.user.is_verified ? 'Active' : 'EmailNotVerified',
        twoFactorEnabled: false,
        lastLogin: new Date().toISOString(),
        lastDevice: 'Chrome (Windows)',
        trustedDevices: [],
      };
    }

    const token = body.tokens?.access_token || body.access_token;
    const nextRefreshToken = body.tokens?.refresh_token || body.refresh_token;

    if (typeof window !== 'undefined') {
      if (userSession) {
        localStorage.setItem('talentai_auth_user', JSON.stringify(userSession));
      }
      if (token) {
        localStorage.setItem('talentai_auth_token', token);
      }
      if (nextRefreshToken) {
        localStorage.setItem('talentai_auth_refresh_token', nextRefreshToken);
      }
    }

    return userSession ? { user: userSession, token } : null;
  },
};
