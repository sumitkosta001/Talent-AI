export interface RecruiterStats {
  jobsPosted: number;
  activeApps: number;
  shortlisted: number;
  interviewsScheduled: number;
  companyName: string;
}

export const MOCK_RECRUITER_STATS: RecruiterStats = {
  jobsPosted: 14,
  activeApps: 128,
  shortlisted: 18,
  interviewsScheduled: 5,
  companyName: 'Vercel',
};
