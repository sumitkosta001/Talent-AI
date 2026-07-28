import { UserSessionData } from '@/types/auth';

export const MOCK_USER_SESSION: UserSessionData = {
  id: 'user-123',
  email: 'alex@example.com',
  role: 'candidate',
  name: 'Alex Johnson',
  accountState: 'Active',
  twoFactorEnabled: true,
  lastLogin: '2026-07-26 18:30',
  lastDevice: 'Chrome on MacOS (San Francisco, CA)',
  trustedDevices: ['macbook-pro-123', 'iphone-15-456'],
};

export const MOCK_RECRUITER_SESSION: UserSessionData = {
  id: 'user-456',
  email: 'sarah.mitchell@vercel.com',
  role: 'recruiter',
  name: 'Sarah Mitchell',
  accountState: 'Active',
  twoFactorEnabled: false,
  lastLogin: '2026-07-26 19:15',
  lastDevice: 'Safari on iPhone (San Jose, CA)',
  trustedDevices: ['imac-789'],
};
