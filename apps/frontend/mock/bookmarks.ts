import { BookmarkItem } from '../types/bookmark';

export const MOCK_BOOKMARKS: BookmarkItem[] = [
  {
    id: 'book-1',
    type: 'job',
    title: 'Senior Software Engineer',
    subtitle: 'Google · Mountain View, CA',
    url: '/jobs/google-sde-3',
    savedDate: 'Jul 25, 2026',
  },
  {
    id: 'book-2',
    type: 'company',
    title: 'Stripe',
    subtitle: 'Fintech & Payments Infrastructure',
    url: '/companies/stripe',
    savedDate: 'Jul 24, 2026',
  },
  {
    id: 'book-3',
    type: 'article',
    title: 'How to Ace Vercel System Design Interviews',
    subtitle: 'Vercel Blog · 12 min read',
    url: '/candidate/ai/learning',
    savedDate: 'Jul 22, 2026',
  },
  {
    id: 'book-4',
    type: 'learning',
    title: 'Next.js 16 Server Components In-Depth',
    subtitle: 'TalentAI Coaching · 4-part course',
    url: '/candidate/ai/learning',
    savedDate: 'Jul 20, 2026',
  },
];
