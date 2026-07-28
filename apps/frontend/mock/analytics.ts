import { Analytics } from '../types/application';

export const MOCK_ANALYTICS: Analytics = {
  applicationsPerMonth: [
    { month: 'Feb', count: 8 },
    { month: 'Mar', count: 12 },
    { month: 'Apr', count: 15 },
    { month: 'May', count: 22 },
    { month: 'Jun', count: 18 },
    { month: 'Jul', count: 28 },
  ],
  statusDistribution: [
    { status: 'Applied', count: 8 },
    { status: 'Technical Interview', count: 4 },
    { status: 'Offer Received', count: 2 },
    { status: 'Rejected', count: 6 },
    { status: 'Withdrawn', count: 3 },
  ],
  averageAtsScore: 84.5,
  successRate: 35.8, // percentage of shortlists
  responseRate: 78.4, // percentage of views
  interviewRatio: 45.2, // percentage of interviews from total applications
};
export const MOCK_ATS_TREND = [
  { month: 'Feb', score: 72 },
  { month: 'Mar', score: 75 },
  { month: 'Apr', score: 81 },
  { month: 'May', score: 84 },
  { month: 'Jun', score: 83 },
  { month: 'Jul', score: 91 },
];
