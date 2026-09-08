import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { RecruiterDashboardStats, HiringFunnelStep, RecentActivity } from '@/types/recruiter';
import { MOCK_RECRUITER_STATS, MOCK_HIRING_FUNNEL, MOCK_RECENT_ACTIVITIES } from '@/mock/recruiterDashboard';
import { RecruiterJobsService } from './jobs.service';

export class RecruiterDashboardService {
  static async getStats(): Promise<RecruiterDashboardStats> {
    try {
      const jobs = await RecruiterJobsService.getJobs();
      const totalJobs = jobs.length;
      const activeJobs = jobs.filter(j => j.status === 'Published').length;
      const closedJobs = jobs.filter(j => j.status === 'Closed').length;

      return {
        totalJobs,
        activeJobs,
        closedJobs,
        totalApplications: 0,
        todayApplications: 0,
        interviewsScheduled: 0,
        offersSent: 0,
        offersAccepted: 0,
        hiringRate: 0,
        averageAtsScore: 0,
      };
    } catch (e) {
      console.warn('Failed to derive recruiter stats from backend, falling back:', e);
    }

    if (DEV_MODE) {
      await mockDelay(200);
      return MOCK_RECRUITER_STATS;
    }

    return {
      totalJobs: 0,
      activeJobs: 0,
      closedJobs: 0,
      totalApplications: 0,
      todayApplications: 0,
      interviewsScheduled: 0,
      offersSent: 0,
      offersAccepted: 0,
      hiringRate: 0,
      averageAtsScore: 0,
    };
  }

  static async getFunnel(): Promise<HiringFunnelStep[]> {
    try {
      // Funnel metrics will be populated when application tracking is enabled
      return [
        { stage: 'Applied', count: 0 },
        { stage: 'Under Review', count: 0 },
        { stage: 'Shortlisted', count: 0 },
        { stage: 'Interview', count: 0 },
        { stage: 'Hired', count: 0 },
      ];
    } catch (e) {
      console.warn('Failed to fetch hiring funnel:', e);
    }

    if (DEV_MODE) {
      await mockDelay(200);
      return MOCK_HIRING_FUNNEL;
    }

    return [];
  }

  static async getActivities(): Promise<RecentActivity[]> {
    try {
      const jobs = await RecruiterJobsService.getJobs();
      const recentJobs = jobs.slice(0, 5);
      return recentJobs.map(job => ({
        id: job.id,
        type: 'job',
        description: `Job "${job.role}" is currently ${job.status}`,
        timestamp: job.date || 'Recently',
      }));
    } catch (e) {
      console.warn('Failed to fetch recent activities:', e);
    }

    if (DEV_MODE) {
      await mockDelay(200);
      return MOCK_RECENT_ACTIVITIES;
    }

    return [];
  }
}
