import { ApplicationDeadline } from '../types/dashboard';

export const MOCK_APPLICATION_DEADLINES: ApplicationDeadline[] = [
  {
    id: 'dead-1',
    companyName: 'Stripe',
    logoColor: '#635BFF',
    role: 'Staff Engineer - Core API',
    deadlineDate: 'Jul 29, 2026',
    daysRemaining: 2,
    priority: 'High',
    progress: 90,
  },
  {
    id: 'dead-2',
    companyName: 'Figma',
    logoColor: '#F24E1E',
    role: 'Senior Product Engineer',
    deadlineDate: 'Aug 02, 2026',
    daysRemaining: 6,
    priority: 'High',
    progress: 75,
  },
  {
    id: 'dead-3',
    companyName: 'Netflix',
    logoColor: '#E50914',
    role: 'UI Engineer (L5) - Growth',
    deadlineDate: 'Aug 10, 2026',
    daysRemaining: 14,
    priority: 'Medium',
    progress: 40,
  },
  {
    id: 'dead-4',
    companyName: 'Slack',
    logoColor: '#4A154B',
    role: 'Senior Frontend Developer',
    deadlineDate: 'Aug 20, 2026',
    daysRemaining: 24,
    priority: 'Low',
    progress: 15,
  },
];
