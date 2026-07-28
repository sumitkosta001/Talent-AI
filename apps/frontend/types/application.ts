export type ApplicationStatus =
  | 'Applied'
  | 'Application Viewed'
  | 'Under Review'
  | 'Resume Shortlisted'
  | 'Assessment Pending'
  | 'Technical Interview'
  | 'HR Interview'
  | 'Final Interview'
  | 'Offer Received'
  | 'Offer Accepted'
  | 'Rejected'
  | 'Withdrawn'
  | 'Archived';

export interface Recruiter {
  name: string;
  email: string;
  phone?: string;
  avatar?: string;
}

export interface ApplicationTimeline {
  status: ApplicationStatus;
  date: string;
  time?: string;
  description: string;
  completed: boolean;
}

export interface Interview {
  id: string;
  date: string;
  time: string;
  type: 'Technical' | 'HR' | 'Managerial' | 'Online' | 'Offline';
  interviewer: string;
  link?: string;
  prepNotes?: string;
  status: 'Scheduled' | 'Completed' | 'Cancelled';
}

export interface Offer {
  salary: string;
  joiningDate: string;
  location: string;
  employmentType: string;
  deadline: string;
  letterUrl?: string;
  status: 'Pending' | 'Accepted' | 'Declined';
}

export interface Application {
  id: string;
  jobId: string;
  jobTitle: string;
  company: string;
  logo: string;
  logoColor: string;
  location: string;
  employmentType: string;
  salary: string;
  appliedDate: string;
  lastUpdated: string;
  status: ApplicationStatus;
  atsScore: number;
  matchPercentage: number;
  recruiter: Recruiter;
  notes?: string;
  timeline: ApplicationTimeline[];
  interview?: Interview;
  offer?: Offer;
  rejectionReason?: string;
  rejectionFeedback?: string;
  rejectionImprovement?: string[];
  archived?: boolean;
}

export interface ApplicationFilter {
  search: string;
  status: string;
  location: string;
  company: string;
  appliedDate: string;
  workplace: 'All' | 'Remote' | 'Hybrid' | 'On-site';
  salaryMin: number;
  interviewStage: string;
}

export interface Analytics {
  applicationsPerMonth: { month: string; count: number }[];
  statusDistribution: { status: string; count: number }[];
  averageAtsScore: number;
  successRate: number;
  responseRate: number;
  interviewRatio: number;
}
