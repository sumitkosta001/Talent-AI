import { CareerInsightCard } from '../types/careerInsight';

export const MOCK_CAREER_INSIGHTS: CareerInsightCard[] = [
  {
    id: 'ins-1',
    type: 'resume',
    title: 'Improve Resume Layout',
    priority: 'high',
    reason: 'Your resume lacks container orchestration technology. Add Kubernetes to match 78% of senior frontend roles.',
    actionText: 'Optimize Resume',
    actionUrl: '/candidate/resume/analysis',
  },
  {
    id: 'ins-2',
    type: 'profile',
    title: 'Complete Profile Details',
    priority: 'medium',
    reason: 'Add absolute links to your public GitHub profile and LinkedIn. This will boost profile views by up to 35%.',
    actionText: 'Edit Profile',
    actionUrl: '/candidate/profile',
  },
  {
    id: 'ins-3',
    type: 'skill',
    title: 'Learn React Server Actions',
    priority: 'high',
    reason: 'React 19 Server Actions queries are featured in 5 current Vercel and Google openings.',
    actionText: 'Start Learning',
    actionUrl: '/candidate/ai/learning',
  },
  {
    id: 'ins-4',
    type: 'ats',
    title: 'Improve ATS Score',
    priority: 'high',
    reason: 'Ensure professional summary mentions active user counts to bypass automated screening filters.',
    actionText: 'Run ATS Scan',
    actionUrl: '/candidate/resume/ats',
  },
  {
    id: 'ins-5',
    type: 'interview',
    title: 'Prepare Vercel Architecture',
    priority: 'high',
    reason: 'Upcoming technical screening scheduled in 3 days. Focus on system design and SSR caching strategies.',
    actionText: 'Practice Mock',
    actionUrl: '/candidate/ai/mock-interview',
  },
];
