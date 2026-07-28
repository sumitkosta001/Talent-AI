import { MOCK_DASHBOARD_OVERVIEW } from '@/mock/dashboardStats';
import { MOCK_UPCOMING_INTERVIEWS } from '@/mock/interviews';
import { MOCK_APPLICATION_DEADLINES } from '@/mock/deadlines';
import { MOCK_PRODUCTIVITY_GOALS } from '@/mock/productivity';
import { mockDelay } from '@/lib/mockDelay';

export class DashboardService {
  static async getOverview() {
    await mockDelay(150);
    return MOCK_DASHBOARD_OVERVIEW;
  }

  static async getUpcomingInterviews() {
    await mockDelay(150);
    return MOCK_UPCOMING_INTERVIEWS;
  }

  static async getApplicationDeadlines() {
    await mockDelay(150);
    return MOCK_APPLICATION_DEADLINES;
  }

  static async getProductivityGoals() {
    await mockDelay(150);
    return MOCK_PRODUCTIVITY_GOALS;
  }
}
