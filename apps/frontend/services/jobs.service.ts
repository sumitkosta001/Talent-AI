import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { Job, JobFilter, RecruiterJob } from '@/types/job';
import { MOCK_JOBS } from '@/mock/jobs';
import { MOCK_RECRUITER_JOBS } from '@/mock/recruiterJobs';

export class JobsService {
  static async getJobs(filters?: Partial<JobFilter>): Promise<Job[]> {
    if (DEV_MODE) {
      await mockDelay(400);
      let list = [...MOCK_JOBS];

      if (filters) {
        if (filters.search) {
          const s = filters.search.toLowerCase();
          list = list.filter(
            j =>
              j.role.toLowerCase().includes(s) ||
              j.company.toLowerCase().includes(s) ||
              j.skills.some(skill => skill.toLowerCase().includes(s))
          );
        }
        if (filters.location) {
          list = list.filter(j => j.location.toLowerCase().includes(filters.location!.toLowerCase()));
        }
        if (filters.experience) {
          list = list.filter(j => j.experience.toLowerCase().includes(filters.experience!.toLowerCase()));
        }
        if (filters.jobType && filters.jobType !== 'Any') {
          list = list.filter(j => j.type === filters.jobType);
        }
        if (filters.remoteStatus && filters.remoteStatus !== 'Any') {
          list = list.filter(j => j.remoteStatus === filters.remoteStatus);
        }
        if (filters.sortBy) {
          if (filters.sortBy === 'best-match') {
            list.sort((a, b) => b.match - a.match);
          } else if (filters.sortBy === 'newest') {
            list.reverse();
          }
        }
      }
      return list;
    }

    const res = await fetch('/api/jobs');
    if (!res.ok) throw new Error('Failed to fetch jobs');
    return res.json();
  }

  static async getJobById(id: string): Promise<Job | null> {
    if (DEV_MODE) {
      await mockDelay(300);
      const match = MOCK_JOBS.find(j => j.id === id);
      return match || null;
    }

    const res = await fetch(`/api/jobs/${id}`);
    if (!res.ok) throw new Error('Failed to fetch job detail');
    return res.json();
  }
}

export class RecruiterJobsService {
  static getLocalJobs(): RecruiterJob[] {
    if (typeof window === 'undefined') return MOCK_RECRUITER_JOBS;
    const stored = localStorage.getItem('talentai_recruiter_jobs');
    if (!stored) {
      localStorage.setItem('talentai_recruiter_jobs', JSON.stringify(MOCK_RECRUITER_JOBS));
      return MOCK_RECRUITER_JOBS;
    }
    return JSON.parse(stored);
  }

  static saveLocalJobs(jobs: RecruiterJob[]) {
    if (typeof window === 'undefined') return;
    localStorage.setItem('talentai_recruiter_jobs', JSON.stringify(jobs));
  }

  static async getJobs(): Promise<RecruiterJob[]> {
    if (DEV_MODE) {
      await mockDelay(300);
      return this.getLocalJobs();
    }

    const res = await fetch('/api/recruiter/jobs');
    if (!res.ok) throw new Error('Failed to fetch jobs');
    return res.json();
  }

  static async getJobById(id: string): Promise<RecruiterJob | null> {
    if (DEV_MODE) {
      await mockDelay(200);
      const jobs = this.getLocalJobs();
      return jobs.find(j => j.id === id) || null;
    }

    const res = await fetch(`/api/recruiter/jobs/${id}`);
    if (!res.ok) throw new Error('Failed to fetch job details');
    return res.json();
  }

  static async createJob(job: Partial<RecruiterJob>): Promise<RecruiterJob> {
    if (DEV_MODE) {
      await mockDelay(400);
      const jobs = this.getLocalJobs();
      const newJob: RecruiterJob = {
        id: `job-${Date.now()}`,
        role: job.role || 'New Job Title',
        department: job.department || 'Engineering',
        employmentType: job.employmentType || 'Full-time',
        workMode: job.workMode || 'Remote',
        experience: job.experience || '3+ years',
        salary: job.salary || '$120K - $150K',
        location: job.location || 'Remote',
        openings: job.openings || 1,
        deadline: job.deadline || new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        skills: job.skills || [],
        responsibilities: job.responsibilities || [],
        requirements: job.requirements || [],
        company: 'TalentAI Technologies',
        logo: 'T',
        logoColor: 'bg-blue-600',
        hiringManager: job.hiringManager || 'Hiring Lead',
        description: job.description || '',
        status: job.status || 'Published',
        date: new Date().toISOString().split('T')[0],
        views: 0,
        applicationsCount: 0,
        shortlistedCount: 0,
        rejectedCount: 0,
        interviewScheduledCount: 0,
        offersSentCount: 0,
      };

      jobs.unshift(newJob);
      this.saveLocalJobs(jobs);
      return newJob;
    }

    const res = await fetch('/api/recruiter/jobs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(job),
    });
    if (!res.ok) throw new Error('Failed to create new job');
    return res.json();
  }

  static async updateJob(id: string, updates: Partial<RecruiterJob>): Promise<RecruiterJob> {
    if (DEV_MODE) {
      await mockDelay(300);
      const jobs = this.getLocalJobs();
      const idx = jobs.findIndex(j => j.id === id);
      if (idx === -1) throw new Error('Job not found');
      
      const updated = { ...jobs[idx], ...updates };
      jobs[idx] = updated;
      this.saveLocalJobs(jobs);
      return updated;
    }

    const res = await fetch(`/api/recruiter/jobs/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates),
    });
    if (!res.ok) throw new Error('Failed to update job details');
    return res.json();
  }

  static async deleteJob(id: string): Promise<boolean> {
    if (DEV_MODE) {
      await mockDelay(200);
      const jobs = this.getLocalJobs();
      const filtered = jobs.filter(j => j.id !== id);
      this.saveLocalJobs(filtered);
      return true;
    }

    const res = await fetch(`/api/recruiter/jobs/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to delete job post');
    return true;
  }
}
