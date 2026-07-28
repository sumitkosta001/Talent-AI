import { SystemHealthMetrics } from '../types/systemHealth';

export const MOCK_SYSTEM_HEALTH: SystemHealthMetrics = {
  apiStatus: 'Healthy',
  dbStatus: 'Healthy',
  cpuUsagePct: 14.5,
  memoryUsagePct: 48.2,
  storageUsagePct: 68.4,
  uptimeSeconds: 1209600, // 14 days
  backgroundJobsCount: 4,
  emailQueueCount: 0,
  notificationQueueCount: 0,
  environment: 'Production (Next.js Turbopack)',
  version: 'v2.1.0-release',
  errorLogs: [
    { timestamp: '2026-07-26 14:02:10', level: 'WARNING', message: 'API request latency spike on /api/jobs endpoint.' },
    { timestamp: '2026-07-26 10:15:45', level: 'WARNING', message: 'Storage container reached 68% threshold capacity.' },
  ],
};
