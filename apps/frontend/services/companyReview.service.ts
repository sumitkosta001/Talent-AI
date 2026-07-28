import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { CompanyReview } from '@/types/companyReview';
import { MOCK_COMPANY_REVIEWS } from '@/mock/companyReviews';

export class CompanyReviewService {
  static async getReviewsByCompanyId(companyId: string): Promise<CompanyReview[]> {
    if (DEV_MODE) {
      await mockDelay(300);
      return MOCK_COMPANY_REVIEWS[companyId] || [];
    }

    const res = await fetch(`/api/companies/${companyId}/reviews`);
    if (!res.ok) throw new Error('Failed to retrieve company reviews');
    return res.json();
  }
}
