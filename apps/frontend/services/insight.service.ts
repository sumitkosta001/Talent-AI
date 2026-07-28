import { MOCK_CAREER_INSIGHTS } from '@/mock/careerInsights';
import { mockDelay } from '@/lib/mockDelay';

export class InsightService {
  static async getInsights() {
    await mockDelay(100);
    return MOCK_CAREER_INSIGHTS;
  }
}
