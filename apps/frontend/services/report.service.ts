import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { PlatformReport } from '@/types/report';
import { MOCK_REPORTS } from '@/mock/reports';
import { MOCK_WEEKLY_REPORT } from '@/mock/weeklyReport';

export class AdminReportService {
  static async getReports(): Promise<PlatformReport[]> {
    if (DEV_MODE) {
      await mockDelay(200);
      return MOCK_REPORTS;
    }

    const res = await fetch('/api/admin/reports');
    if (!res.ok) throw new Error('Failed to retrieve platform reports list');
    return res.json();
  }
}

export class ReportService {
  static async getWeeklyReport() {
    await mockDelay(100);
    return MOCK_WEEKLY_REPORT;
  }
}
