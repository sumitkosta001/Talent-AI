import { CandidateExperience } from '../types/experience';

export const MOCK_EXPERIENCE: CandidateExperience[] = [
  {
    id: 'exp-1',
    companyName: 'Stripe',
    companyLogo: 'S',
    jobTitle: 'Senior Frontend Engineer',
    employmentType: 'Full-time',
    location: 'San Francisco, CA',
    startDate: '2024-03',
    endDate: '',
    isCurrentJob: true,
    description: 'Led development on Stripe Payment Links merchant portals. Optimized core developer onboarding flows, reducing latency by 24%. Collaborated closely with design team coordinators.',
    achievements: ['Reduced page render times by 320ms.', 'Mentored 4 junior frontend developers.'],
    technologiesUsed: ['React', 'TypeScript', 'Tailwind CSS', 'GraphQL'],
  },
  {
    id: 'exp-2',
    companyName: 'Vercel',
    companyLogo: 'V',
    jobTitle: 'Software Engineer II',
    employmentType: 'Full-time',
    location: 'Remote',
    startDate: '2022-01',
    endDate: '2024-02',
    isCurrentJob: false,
    description: 'Developed next-dev framework performance tooling dashboards. Integrated Server Actions and Turbopack core diagnostics panels.',
    achievements: ['Designed framework diagnostic pages.', 'Collaborated on Next.js 13 release layouts.'],
    technologiesUsed: ['Next.js', 'React', 'TypeScript', 'Node.js'],
  },
];
