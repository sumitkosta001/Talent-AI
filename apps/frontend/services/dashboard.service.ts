import { MOCK_DASHBOARD_OVERVIEW } from '@/mock/dashboardStats';
import { MOCK_UPCOMING_INTERVIEWS } from '@/mock/interviews';
import { MOCK_APPLICATION_DEADLINES } from '@/mock/deadlines';
import { MOCK_PRODUCTIVITY_GOALS } from '@/mock/productivity';
import { mockDelay } from '@/lib/mockDelay';
import { CandidateProfileService } from './profile.service';

export class DashboardService {
  static async getOverview() {
    const token = typeof window !== 'undefined' ? localStorage.getItem('talentai_auth_token') : null;
    if (token) {
      try {
        const profile = await CandidateProfileService.getProfile();
        return {
          ...MOCK_DASHBOARD_OVERVIEW,
          candidateName: profile.name,
          profileCompletion: profile.completionPercentage,
          location: profile.location || undefined,
        };
      } catch {
        // Fall back to local mock if API fails
      }
    }
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
