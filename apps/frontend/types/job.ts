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
  salaryMax?: number;
  skills: string[];
  sortBy: 'newest' | 'oldest' | 'highest-salary' | 'lowest-salary' | 'best-match';
  page?: number;
  size?: number;
}

export interface JobSearchParams {
  q?: string;
  location?: string;
  skills?: string;
  experience_months?: number;
  salary_min?: number;
  salary_max?: number;
  work_mode?: 'REMOTE' | 'HYBRID' | 'ONSITE';
  page?: number;
  size?: number;
  sort_by?: string;
  sort_order?: string;
}

export interface JobApiItem {
  id: string;
  company_id: string;
  company_name?: string;
  title: string;
  description: string;
  department?: string;
  location?: string;
  work_mode?: 'REMOTE' | 'HYBRID' | 'ONSITE';
  employment_type?: string;
  required_experience_months?: number;
  required_skills?: string[];
  preferred_skills?: string[];
  salary_min?: number;
  salary_max?: number;
  currency?: string;
  status: 'DRAFT' | 'PUBLISHED' | 'CLOSED';
  published_at?: string;
  created_at?: string;
  updated_at?: string;
}

export interface JobPaginatedResponse {
  items: JobApiItem[];
  total: number;
  page: number;
  size: number;
  total_pages: number;
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
