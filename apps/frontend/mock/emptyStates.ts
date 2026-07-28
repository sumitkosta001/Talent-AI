export interface EmptyStateConfig {
  title: string;
  description: string;
  primaryActionText?: string;
  primaryActionUrl?: string;
  secondaryActionText?: string;
  secondaryActionUrl?: string;
  iconType: 'briefcase' | 'file-text' | 'bell' | 'bookmark' | 'search' | 'building' | 'users' | 'database' | 'history' | 'alert';
}

export const MOCK_EMPTY_STATES: Record<string, EmptyStateConfig> = {
  jobs: {
    title: 'No Job Openings Found',
    description: 'We couldn’t find any job postings matching your current profile filters. Try adjusting your preferences.',
    primaryActionText: 'Reset Filters',
    secondaryActionText: 'Edit Profile Skills',
    secondaryActionUrl: '/candidate/profile',
    iconType: 'briefcase',
  },
  applications: {
    title: 'No Active Applications',
    description: 'You haven’t submitted any applications yet. Explore openings and apply with your AI-optimized resume!',
    primaryActionText: 'Browse Open Jobs',
    primaryActionUrl: '/candidate/jobs',
    secondaryActionText: 'Upload Resume',
    secondaryActionUrl: '/candidate/resume/upload',
    iconType: 'file-text',
  },
  notifications: {
    title: 'All Caught Up!',
    description: 'No new system alerts or recruiter invitations at the moment. We will notify you when things change.',
    primaryActionText: 'Adjust Alerts Settings',
    primaryActionUrl: '/candidate/settings',
    iconType: 'bell',
  },
  bookmarks: {
    title: 'No Saved Bookmarks',
    description: 'Save interesting jobs, articles, or career roadmaps to view them later in this bookmark panel.',
    primaryActionText: 'Browse Jobs',
    primaryActionUrl: '/candidate/jobs',
    iconType: 'bookmark',
  },
  search: {
    title: 'No Matching Results',
    description: 'We couldn’t find any matches matching your query. Check spelling or try different keywords.',
    primaryActionText: 'Clear Search Input',
    iconType: 'search',
  },
  companies: {
    title: 'No Companies Discovered',
    description: 'There are no followed companies in your inventory. Follow companies to track their active openings.',
    primaryActionText: 'Explore Companies',
    primaryActionUrl: '/companies',
    iconType: 'building',
  },
  recruiter: {
    title: 'No Applicants Yet',
    description: 'No candidate profiles have submitted application requests for this opening yet.',
    primaryActionText: 'Share Job Link',
    iconType: 'users',
  },
  admin: {
    title: 'No Platform Reports',
    description: 'System health logs and metrics collections are currently empty. Check system tasks schedules.',
    primaryActionText: 'Trigger Diagnostic Run',
    iconType: 'database',
  },
  ai: {
    title: 'No AI Career History',
    description: 'Practice interactive mock interviews or generate resume variations to see your AI history list here.',
    primaryActionText: 'Practice Mock Interview',
    primaryActionUrl: '/candidate/ai/mock-interview',
    secondaryActionText: 'Generate Resume',
    secondaryActionUrl: '/candidate/ai/resume-builder',
    iconType: 'history',
  },
};
