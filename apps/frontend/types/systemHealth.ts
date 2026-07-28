export interface SystemHealthMetrics {
  apiStatus: 'Healthy' | 'Degraded' | 'Offline';
  dbStatus: 'Healthy' | 'Degraded' | 'Offline';
  cpuUsagePct: number;
  memoryUsagePct: number;
  storageUsagePct: number;
  uptimeSeconds: number;
  backgroundJobsCount: number;
  emailQueueCount: number;
  notificationQueueCount: number;
  environment: string;
  version: string;
  errorLogs: {
    timestamp: string;
    level: 'ERROR' | 'WARNING';
    message: string;
  }[];
}
