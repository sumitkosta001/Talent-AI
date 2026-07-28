import { SearchResultItem } from '@/types/search';

export const MOCK_SEARCH_ITEMS: SearchResultItem[] = [
  // Jobs
  {
    id: 'search-job-1',
    title: 'Senior Software Engineer (Next.js)',
    subtitle: 'Vercel • Full-time • Remote',
    category: 'jobs',
    route: '/candidate/jobs/google-sde-3',
  },
  {
    id: 'search-job-2',
    title: 'Staff Frontend Engineer (Tailwind)',
    subtitle: 'Stripe • Full-time • San Francisco',
    category: 'jobs',
    route: '/candidate/jobs',
  },
  // Companies
  {
    id: 'search-comp-1',
    title: 'Google',
    subtitle: 'Silicon Valley • Technology & Software',
    category: 'companies',
    route: '/companies/google',
  },
  {
    id: 'search-comp-2',
    title: 'Vercel',
    subtitle: 'Remote-first • Hosting & Frameworks',
    category: 'companies',
    route: '/companies/vercel',
  },
  // Candidates
  {
    id: 'search-cand-1',
    title: 'Alex Johnson',
    subtitle: 'Senior Full Stack Developer • SF, CA',
    category: 'candidates',
    route: '/recruiter/applicants/1',
  },
  // Recruiters
  {
    id: 'search-rec-1',
    title: 'Sarah Mitchell',
    subtitle: 'Tech Recruitment Manager • Vercel',
    category: 'recruiters',
    route: '/admin/recruiters',
  },
  // Applications
  {
    id: 'search-app-1',
    title: 'Google SSE Application',
    subtitle: 'Status: Interview Scheduled • Last updated 2 days ago',
    category: 'applications',
    route: '/candidate/applications',
  },
  // Interviews
  {
    id: 'search-int-1',
    title: 'Technical Screening Round',
    subtitle: 'Google • 2026-07-28 10:00 AM • Google Meet',
    category: 'interviews',
    route: '/candidate',
  },
  // Skills
  {
    id: 'search-skill-1',
    title: 'Next.js 16 (App Router)',
    subtitle: 'Skill match: 95% • Advanced proficiency',
    category: 'skills',
    route: '/candidate/profile',
  },
  {
    id: 'search-skill-2',
    title: 'Tailwind CSS v4',
    subtitle: 'Skill match: 90% • Custom utility styling',
    category: 'skills',
    route: '/candidate/profile',
  },
  // Projects
  {
    id: 'search-proj-1',
    title: 'TalentAI Recruitment SaaS',
    subtitle: 'Project matched with SSE job requirements',
    category: 'projects',
    route: '/candidate/profile',
  },
  // Resumes
  {
    id: 'search-res-1',
    title: 'Alex_Johnson_Resume_2026.pdf',
    subtitle: 'Primary Resume • Analyzed Score: 82/100',
    category: 'resumes',
    route: '/candidate/resume',
  },
  // Tools
  {
    id: 'search-tool-1',
    title: 'AI Resume Builder',
    subtitle: 'Generate tailored resumes based on target descriptions',
    category: 'tools',
    route: '/candidate/ai/resume-builder',
  },
  {
    id: 'search-tool-2',
    title: 'AI Cover Letter Generator',
    subtitle: 'Write compelling, personalized outreach letters',
    category: 'tools',
    route: '/candidate/ai/cover-letter',
  },
  {
    id: 'search-tool-3',
    title: 'AI Interview Coach Simulator',
    subtitle: 'Practice technical, system design and behavioral rounds',
    category: 'tools',
    route: '/candidate/ai/mock-interview',
  },
  {
    id: 'search-tool-4',
    title: 'AI Interactive Career Roadmap',
    subtitle: 'Custom skill trees based on target positions',
    category: 'tools',
    route: '/candidate/ai/roadmap',
  },
  // Bookmarks
  {
    id: 'search-book-1',
    title: 'Saved Job: Google Technical Lead',
    subtitle: 'Silicon Valley • Saved on 2026-07-25',
    category: 'bookmarks',
    route: '/candidate/profile',
  },
  // Notifications
  {
    id: 'search-notif-1',
    title: 'New Interview Invitation',
    subtitle: 'Google Technical recruiter sent an invitation',
    category: 'notifications',
    route: '/candidate/notifications',
  },
  // Settings
  {
    id: 'search-set-1',
    title: 'Candidate Profile Settings',
    subtitle: 'Update email preferences, theme, and accessibility settings',
    category: 'settings',
    route: '/candidate/settings',
  },
];
