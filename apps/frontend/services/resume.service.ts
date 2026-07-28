import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { CandidateResume } from '@/types/resume';
import { MOCK_RESUME } from '@/mock/resume';

export class CandidateResumeService {
  static getLocalResume(): CandidateResume {
    if (typeof window === 'undefined') return MOCK_RESUME;
    const stored = localStorage.getItem('talentai_candidate_resume');
    if (!stored) {
      localStorage.setItem('talentai_candidate_resume', JSON.stringify(MOCK_RESUME));
      return MOCK_RESUME;
    }
    return JSON.parse(stored);
  }

  static saveLocalResume(res: CandidateResume) {
    if (typeof window === 'undefined') return;
    localStorage.setItem('talentai_candidate_resume', JSON.stringify(res));
  }

  static async getResume(): Promise<CandidateResume> {
    if (DEV_MODE) {
      await mockDelay(200);
      return this.getLocalResume();
    }

    const res = await fetch('/api/profile/resume');
    if (!res.ok) throw new Error('Failed to retrieve resume details');
    return res.json();
  }
}
