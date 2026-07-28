import { CalendarEvent } from '../types/calendar';

export const MOCK_CALENDAR_EVENTS: CalendarEvent[] = [
  {
    id: 'cal-1',
    title: 'Google Technical Screening',
    type: 'interview',
    date: '2026-07-28',
    time: '10:00 AM',
    company: 'Google',
    location: 'Google Meet',
    description: 'Algorithms and Data Structures review.',
  },
  {
    id: 'cal-2',
    title: 'Vercel Lead Architect Call',
    type: 'interview',
    date: '2026-07-30',
    time: '2:30 PM',
    company: 'Vercel',
    location: 'Zoom',
    description: 'Framework architecture, SSR performance, and systems scaling.',
  },
  {
    id: 'cal-3',
    title: 'Stripe Assessment Deadline',
    type: 'deadline',
    date: '2026-07-29',
    time: '11:59 PM',
    company: 'Stripe',
    description: 'Complete the take-home client integrations project.',
  },
  {
    id: 'cal-4',
    title: 'Figma Coding Challenge',
    type: 'assessment',
    date: '2026-08-02',
    time: '4:00 PM',
    company: 'Figma',
    description: 'Codesandbox live canvas UI challenge.',
  },
];
