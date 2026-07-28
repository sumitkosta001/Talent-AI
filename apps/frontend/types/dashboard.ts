export interface DashboardStats {
  applications: number;
  interviews: number;
  offers: number;
  bookmarks: number;
  savedJobs: number;
  companiesFollowed: number;
  resumeViews: number;
  profileViews: number;
  careerScore: number;
  atsScore: number;
}

export interface DashboardOverview {
  stats: DashboardStats;
  candidateName: string;
  profileCompletion: number;
  atsScore: number;
  careerScore: number;
  resumeScore: number;
}

export interface UpcomingInterview {
  id: string;
  companyName: string;
  logoColor: string;
  role: string;
  type: 'Technical' | 'HR' | 'System Design' | 'Behavioral';
  mode: 'Online' | 'Offline';
  date: string;
  time: string;
  meetingLink?: string;
  countdownDays: number;
  status: 'Scheduled' | 'Confirmed' | 'Rescheduled';
}

export interface ApplicationDeadline {
  id: string;
  companyName: string;
  logoColor: string;
  role: string;
  deadlineDate: string;
  daysRemaining: number;
  priority: 'High' | 'Medium' | 'Low';
  progress: number;
}

export interface RecentSearchItem {
  id: string;
  query: string;
  category: 'jobs' | 'companies' | 'skills' | 'locations';
  timestamp: string;
}

export interface ProductivityGoal {
  id: string;
  title: string;
  current: number;
  target: number;
  unit?: string;
  color: string;
}
