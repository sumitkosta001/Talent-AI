import { RecruiterDashboardStats, HiringFunnelStep, RecentActivity } from '../types/recruiter';

export const MOCK_RECRUITER_STATS: RecruiterDashboardStats = {
  totalJobs: 12,
  activeJobs: 8,
  closedJobs: 4,
  totalApplications: 284,
  todayApplications: 8,
  interviewsScheduled: 18,
  offersSent: 5,
  offersAccepted: 3,
  hiringRate: 72.5,
  averageAtsScore: 83.4,
};

export const MOCK_HIRING_FUNNEL: HiringFunnelStep[] = [
  { stage: 'Applied', count: 284 },
  { stage: 'Under Review', count: 142 },
  { stage: 'Shortlisted', count: 68 },
  { stage: 'Interviewing', count: 32 },
  { stage: 'Offer Issued', count: 8 },
  { stage: 'Hired', count: 3 },
];

export const MOCK_RECENT_ACTIVITIES: RecentActivity[] = [
  { id: 'act-1', type: 'application', description: 'Jordan Lee applied for Staff Next.js Platform Engineer.', timestamp: '10 min ago' },
  { id: 'act-2', type: 'interview', description: 'Technical loop with Alex Johnson scheduled by Marcus Aurelius.', timestamp: '1 hour ago' },
  { id: 'act-3', type: 'offer', description: 'Offer accepted by Jordan Lee for Staff Next.js role.', timestamp: 'Yesterday' },
  { id: 'act-4', type: 'job', description: 'Full Stack Engineer (Payments) job status set to Published.', timestamp: '2 days ago' },
];
