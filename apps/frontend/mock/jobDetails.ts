import { Job } from '../types/job';
import { MOCK_JOBS } from './jobs';

export const MOCK_JOB_DETAILS_MAP = new Map<string, Job>(
  MOCK_JOBS.map(job => [job.id, job])
);

export function getMockJobDetails(id: string): Job | undefined {
  return MOCK_JOB_DETAILS_MAP.get(id);
}
