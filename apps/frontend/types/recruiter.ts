export interface RecruiterDashboardStats {
  totalJobs: number;
  activeJobs: number;
  closedJobs: number;
  totalApplications: number;
  todayApplications: number;
  interviewsScheduled: number;
  offersSent: number;
  offersAccepted: number;
  hiringRate: number;
  averageAtsScore: number;
}

export interface HiringFunnelStep {
  stage: string;
  count: number;
}

export interface RecentActivity {
  id: string;
  type: 'application' | 'interview' | 'offer' | 'job';
  description: string;
  timestamp: string;
}
