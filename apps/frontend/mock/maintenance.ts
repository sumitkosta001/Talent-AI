export interface MaintenanceStatus {
  isUnderMaintenance: boolean;
  estimatedEndTime: string;
  systemMessage: string;
  progressPercentage: number;
}

export const MOCK_MAINTENANCE_STATUS: MaintenanceStatus = {
  isUnderMaintenance: true,
  estimatedEndTime: '2026-07-27 04:00 AM UTC',
  systemMessage: 'We are currently upgrading our AI Career Core LLM indices to a faster, low-latency framework. Services will return shortly.',
  progressPercentage: 75,
};
