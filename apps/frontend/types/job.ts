export interface Salary {
  min: number;
  max: number;
  currency: string;
  period: 'yearly' | 'monthly' | 'hourly';
}

export interface Benefit {
  icon: string;
  label: string;
  desc: string;
}

export interface Job {
  id: string;
  companyId: string;
  company: string;
  role: string;
  title: string; // Keep both role and title for backward compatibility
  salary: string; // Formatted salary, e.g. "$160K–$200K"
  salaryDetail?: Salary;
  match: number; // AI match percentage
  location: string;
  logo: string;
  logoColor: string;
  experience: string;
  skills: string[];
  bookmarked: boolean;
  applied: boolean;
  description: string;
  responsibilities?: string[];
  requirements?: string[];
  benefits?: Benefit[];
  date: string; // Date posted description
  type: 'Full-time' | 'Part-time' | 'Contract' | 'Internship';
  remoteStatus: 'Remote' | 'Hybrid' | 'On-site';
  deadline?: string;
  applicantsCount?: number;
  isFeatured?: boolean;
  isPopular?: boolean;
  category?: string;
}

export interface JobFilter {
  search: string;
  location: string;
  experience: string;
  jobType: string;
  remoteStatus: string;
  salaryMin: number;
  skills: string[];
  sortBy: 'newest' | 'oldest' | 'highest-salary' | 'best-match';
}

export type JobStatus = 'Draft' | 'Published' | 'Closed';

export interface RecruiterJob {
  id: string;
  role: string; // matches jobTitle/role
  department: string;
  employmentType: 'Full-time' | 'Part-time' | 'Contract' | 'Internship';
  workMode: 'Remote' | 'Hybrid' | 'On-site';
  experience: string;
  salary: string;
  location: string;
  openings: number;
  deadline: string;
  skills: string[];
  responsibilities: string[];
  requirements: string[];
  preferredSkills?: string[];
  benefits?: string[];
  company: string;
  logo: string;
  logoColor: string;
  hiringManager: string;
  description: string;
  status: JobStatus;
  date: string;
  views: number;
  applicationsCount: number;
  shortlistedCount: number;
  rejectedCount: number;
  interviewScheduledCount: number;
  offersSentCount: number;
}
