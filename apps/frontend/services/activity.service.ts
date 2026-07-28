import { MOCK_RECENT_ACTIVITY } from '@/mock/recentActivity';
import { mockDelay } from '@/lib/mockDelay';

export class ActivityService {
  static async getActivities() {
    await mockDelay(100);
    return MOCK_RECENT_ACTIVITY;
  }
}
