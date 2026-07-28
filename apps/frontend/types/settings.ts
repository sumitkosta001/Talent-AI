import { CandidateProfile } from './profile';

export interface SocialLinks {
  linkedin: string;
  github: string;
  portfolio: string;
  leetcode?: string;
  codeforces?: string;
  hackerrank?: string;
  stackoverflow?: string;
  twitter?: string;
  medium?: string;
  personalWebsite?: string;
}

export interface ResumeVisibility {
  status: 'Public' | 'Private' | 'Recruiters Only';
  hideContactInfo: boolean;
  allowDownload: boolean;
  allowSearch: boolean;
  allowContact: boolean;
}

export interface PrivacySettings {
  profileVisibility: 'All' | 'Recruiters' | 'Connections' | 'None';
  emailVisibility: 'All' | 'Recruiters' | 'None';
  phoneVisibility: 'All' | 'Recruiters' | 'None';
  searchEngineIndexing: boolean;
  allowInvitations: boolean;
  allowAiRecommendations: boolean;
  allowAnalytics: boolean;
}

export interface NotificationSettings {
  jobRecommendations: boolean;
  atsUpdates: boolean;
  recruiterMessages: boolean;
  interviewReminders: boolean;
  offerNotifications: boolean;
  resumeReminder: boolean;
  email: boolean;
  push: boolean;
  sms: boolean;
  weeklyDigest: boolean;
  monthlyReport: boolean;
}

export interface PasswordChange {
  currentPassword: string;
  newPassword: string;
  confirmPassword: string;
}

export interface CandidateSettings {
  profile: CandidateProfile;
  socials: SocialLinks;
  resume: ResumeVisibility;
  privacy: PrivacySettings;
  notifications: NotificationSettings;
  theme: 'Light' | 'Dark' | 'System';
  language: string;
}

export interface NotificationStats {
  unread: number;
}
