import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { PlatformKPIs } from '@/types/admin';
import { MOCK_ADMIN_KPI, MOCK_ADMIN_ACTIVITIES } from '@/mock/adminDashboard';

export class AdminDashboardService {
  static async getKPIs(): Promise<PlatformKPIs> {
    if (DEV_MODE) {
      await mockDelay(200);
      return MOCK_ADMIN_KPI;
    }

    const res = await fetch('/api/admin/kpis');
    if (!res.ok) throw new Error('Failed to retrieve Platform KPIs');
    return res.json();
  }

  static async getRecentActivities(): Promise<{ id: string; description: string; timestamp: string }[]> {
    if (DEV_MODE) {
      await mockDelay(200);
      return MOCK_ADMIN_ACTIVITIES;
    }

    const res = await fetch('/api/admin/activities');
    if (!res.ok) throw new Error('Failed to retrieve admin dashboard activities log');
    return res.json();
  }
}
