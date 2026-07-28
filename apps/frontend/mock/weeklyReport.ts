import { WeeklyReportData } from '../types/weeklyReport';

export const MOCK_WEEKLY_REPORT: WeeklyReportData = {
  weekStartDate: 'Jul 20, 2026',
  weekEndDate: 'Jul 26, 2026',
  productivityScore: 88,
  productivityScoreChange: 4,
  metrics: [
    {
      label: 'Applications Submitted',
      currentValue: 5,
      previousValue: 3,
      changePercentage: 66.7,
      improved: true,
    },
    {
      label: 'Interviews Completed',
      currentValue: 2,
      previousValue: 1,
      changePercentage: 100,
      improved: true,
    },
    {
      label: 'Offers Received',
      currentValue: 1,
      previousValue: 0,
      changePercentage: 100,
      improved: true,
    },
    {
      label: 'New Skills Learned',
      currentValue: 3,
      previousValue: 2,
      changePercentage: 50,
      improved: true,
    },
    {
      label: 'Certificates Added',
      currentValue: 1,
      previousValue: 0,
      changePercentage: 100,
      improved: true,
    },
    {
      label: 'Hours Practiced',
      currentValue: 18,
      previousValue: 12,
      changePercentage: 50,
      unit: 'hrs',
      improved: true,
    },
    {
      label: 'Resume Refinements',
      currentValue: 4,
      previousValue: 2,
      changePercentage: 100,
      improved: true,
    },
    {
      label: 'AI Coach Requests',
      currentValue: 24,
      previousValue: 15,
      changePercentage: 60,
      improved: true,
    },
  ],
};
