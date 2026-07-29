import { PlatformKPIs } from '../types/admin';

export const MOCK_ADMIN_KPI: PlatformKPIs = {
  totalUsers: 1766,
  candidatesCount: 1482,
  recruitersCount: 284,
  companiesCount: 110,
  activeJobsCount: 42,
  applicationsCount: 8403,
  interviewsCount: 184,
  offersCount: 32,
  dau: 420,
  mau: 1850,
  storageUsagePct: 68.4,
  apiRequestsToday: 14820,
};

export const MOCK_ADMIN_ACTIVITIES = [
  { id: 'act-1', description: 'User account Jordan Lee was promoted to Admin by Sarah Mitchell.', timestamp: '5 min ago' },
  { id: 'act-2', description: 'Hiring company stripe-integrations status set to Active.', timestamp: '1 hour ago' },
  { id: 'act-3', description: 'System database maintenance successfully completed.', timestamp: '4 hours ago' },
  { id: 'act-4', description: 'New registration candidate Maya Patel submitted a resume file.', timestamp: 'Yesterday' },
];
