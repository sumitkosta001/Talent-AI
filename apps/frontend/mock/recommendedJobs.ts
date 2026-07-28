import { Job } from '../types/job';
import { MOCK_JOBS } from './jobs';

export const MOCK_RECOMMENDED_JOBS: Job[] = MOCK_JOBS.filter(j => j.match >= 90);
