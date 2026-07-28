import { ProductivityGoal } from '../types/dashboard';

export const MOCK_PRODUCTIVITY_GOALS: ProductivityGoal[] = [
  {
    id: 'goal-1',
    title: 'Daily Practice Goal',
    current: 3,
    target: 5,
    unit: 'tasks',
    color: '#3B82F6', // Blue
  },
  {
    id: 'goal-2',
    title: 'Weekly Application Goal',
    current: 5,
    target: 8,
    unit: 'apps',
    color: '#10B981', // Emerald
  },
  {
    id: 'goal-3',
    title: 'Interview Preparation',
    current: 4,
    target: 4,
    unit: 'hrs',
    color: '#8B5CF6', // Violet
  },
  {
    id: 'goal-4',
    title: 'Learning Progression',
    current: 12,
    target: 15,
    unit: 'modules',
    color: '#F59E0B', // Amber
  },
];
