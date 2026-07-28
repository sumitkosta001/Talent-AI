import { ChartData } from '../types/ats';

export const MOCK_RADAR_DATA: ChartData[] = [
  { subject: 'Keywords', score: 94 },
  { subject: 'Experience', score: 88 },
  { subject: 'Education', score: 96 },
  { subject: 'Projects', score: 85 },
  { subject: 'Formatting', score: 91 },
  { subject: 'Grammar', score: 90 }
];

export const MOCK_ATS_BREAKDOWN_TIME = [
  { date: 'Jun 10', score: 68 },
  { date: 'Jun 22', score: 75 },
  { date: 'Jul 01', score: 81 },
  { date: 'Jul 10', score: 87 },
  { date: 'Jul 23', score: 92 }
];

export const MOCK_SKILL_DISTRIBUTION = [
  { name: 'Core Languages', match: 98 },
  { name: 'Frameworks', match: 92 },
  { name: 'Databases', match: 85 },
  { name: 'DevOps/Containers', match: 40 },
  { name: 'Cloud/Infra', match: 65 }
];
