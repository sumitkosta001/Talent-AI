import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { SystemHealthMetrics } from '@/types/systemHealth';
import { MOCK_SYSTEM_HEALTH } from '@/mock/systemHealth';

export class AdminSystemService {
  static async getHealthMetrics(): Promise<SystemHealthMetrics> {
    if (DEV_MODE) {
      await mockDelay(300);
      return MOCK_SYSTEM_HEALTH;
    }

    const res = await fetch('/api/admin/system/health');
    if (!res.ok) throw new Error('Failed to retrieve server health report');
    return res.json();
  }
}
