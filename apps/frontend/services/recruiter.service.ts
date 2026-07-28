import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { RecruiterDashboardStats, HiringFunnelStep, RecentActivity } from '@/types/recruiter';
import { MOCK_RECRUITER_STATS, MOCK_HIRING_FUNNEL, MOCK_RECENT_ACTIVITIES } from '@/mock/recruiterDashboard';

export class RecruiterDashboardService {
  static async getStats(): Promise<RecruiterDashboardStats> {
    if (DEV_MODE) {
      await mockDelay(200);
      return MOCK_RECRUITER_STATS;
    }

    const res = await fetch('/api/recruiter/dashboard/stats');
    if (!res.ok) throw new Error('Failed to retrieve dashboard stats');
    return res.json();
  }

  static async getFunnel(): Promise<HiringFunnelStep[]> {
    if (DEV_MODE) {
      await mockDelay(200);
      return MOCK_HIRING_FUNNEL;
    }

    const res = await fetch('/api/recruiter/dashboard/funnel');
    if (!res.ok) throw new Error('Failed to retrieve hiring funnel');
    return res.json();
  }

  static async getActivities(): Promise<RecentActivity[]> {
    if (DEV_MODE) {
      await mockDelay(200);
      return MOCK_RECENT_ACTIVITIES;
    }

    const res = await fetch('/api/recruiter/dashboard/activities');
    if (!res.ok) throw new Error('Failed to retrieve recent activities');
    return res.json();
  }
}
