import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { Job } from '@/types/job';
import { MOCK_COMPANY_JOBS } from '@/mock/companyJobs';

export class CompanyJobService {
  static async getJobsByCompanyId(companyId: string): Promise<Job[]> {
    if (DEV_MODE) {
      await mockDelay(300);
      return MOCK_COMPANY_JOBS[companyId] || [];
    }

    const res = await fetch(`/api/companies/${companyId}/jobs`);
    if (!res.ok) throw new Error('Failed to retrieve company open jobs');
    return res.json();
  }
}
