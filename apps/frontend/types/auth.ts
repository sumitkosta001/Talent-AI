export type AccountState = 'Active' | 'EmailNotVerified' | 'Locked' | 'Suspended' | 'Disabled' | 'PendingApproval' | 'ExpiredSession';

export interface UserSessionData {
  id: string;
  email: string;
  role: 'candidate' | 'recruiter' | 'admin';
  name: string;
  accountState: AccountState;
  twoFactorEnabled: boolean;
  lastLogin: string;
  lastDevice: string;
  trustedDevices: string[];
}
