import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { Job, JobFilter, JobPaginatedResponse, JobSearchParams, JobStatus, RecruiterJob } from '@/types/job';
import { MOCK_JOBS } from '@/mock/jobs';
import { MOCK_RECRUITER_JOBS } from '@/mock/recruiterJobs';

export class JobsService {
  static async searchJobs(params: JobSearchParams): Promise<JobPaginatedResponse> {
    const query = new URLSearchParams();
    if (params.q) query.append('q', params.q);
    if (params.location) query.append('location', params.location);
    if (params.skills) query.append('skills', params.skills);
    if (params.experience_months !== undefined && params.experience_months !== null) {
      query.append('experience_months', params.experience_months.toString());
    }
    if (params.salary_min !== undefined && params.salary_min !== null) {
      query.append('salary_min', params.salary_min.toString());
    }
    if (params.salary_max !== undefined && params.salary_max !== null) {
      query.append('salary_max', params.salary_max.toString());
    }
    if (params.work_mode) query.append('work_mode', params.work_mode);
    if (params.page) query.append('page', params.page.toString());
    if (params.size) query.append('size', params.size.toString());
    if (params.sort_by) query.append('sort_by', params.sort_by);
    if (params.sort_order) query.append('sort_order', params.sort_order);

    const res = await fetch(`/api/v1/jobs?${query.toString()}`);
    if (!res.ok) {
      throw new Error(`Failed to search jobs: ${res.statusText}`);
    }
    return res.json();
  }

  static mapApiItemToJob(item: any): Job {
    const minSalary = item.salary_min ? (item.salary_min >= 100000 ? `${(item.salary_min / 100000).toFixed(1).replace(/\.0$/, '')}L` : item.salary_min) : null;
    const maxSalary = item.salary_max ? (item.salary_max >= 100000 ? `${(item.salary_max / 100000).toFixed(1).replace(/\.0$/, '')}L` : item.salary_max) : null;
    const currencySym = item.currency === 'INR' || !item.currency ? '₹' : item.currency + ' ';
    
    let salaryStr = 'Salary not specified';
    if (minSalary && maxSalary) {
      salaryStr = `${currencySym}${minSalary} – ${currencySym}${maxSalary}`;
    } else if (minSalary) {
      salaryStr = `From ${currencySym}${minSalary}`;
    } else if (maxSalary) {
      salaryStr = `Up to ${currencySym}${maxSalary}`;
    }

    const months = item.required_experience_months || 0;
    let expStr = 'No experience required';
    if (months > 0) {
      const years = Math.floor(months / 12);
      const remMonths = months % 12;
      if (years > 0 && remMonths > 0) {
        expStr = `${years} yrs ${remMonths} mos`;
      } else if (years > 0) {
        expStr = `${years}+ year${years > 1 ? 's' : ''}`;
      } else {
        expStr = `${remMonths} months`;
      }
    }

    const workModeStr = item.work_mode === 'REMOTE' ? 'Remote' : item.work_mode === 'HYBRID' ? 'Hybrid' : 'On-site';

    return {
      id: item.id,
      companyId: item.company_id || 'company',
      company: item.company_name || 'Company',
      role: item.title,
      title: item.title,
      salary: salaryStr,
      salaryDetail: item.salary_min ? {
        min: item.salary_min,
        max: item.salary_max || item.salary_min,
        currency: item.currency || 'INR',
        period: 'yearly'
      } : undefined,
      match: 90,
      location: item.location || 'Remote',
      logo: (item.company_name || item.title || 'J').charAt(0).toUpperCase(),
      logoColor: 'bg-blue-600',
      experience: expStr,
      skills: item.required_skills && item.required_skills.length > 0 ? item.required_skills : [],
      bookmarked: false,
      applied: false,
      description: item.description || '',
      responsibilities: item.required_keywords || [],
      requirements: item.preferred_skills || [],
      benefits: item.education_requirements || [],
      date: item.published_at ? new Date(item.published_at).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' }) : 'Recently posted',
      type: (item.employment_type as any) || 'Full-time',
      remoteStatus: workModeStr as any,
      category: item.department || 'Engineering',
    };
  }

  static async getJobs(filters?: Partial<JobFilter>): Promise<Job[]> {
    try {
      let expMonths: number | undefined;
      if (filters?.experience) {
        const parsed = parseInt(filters.experience);
        if (!isNaN(parsed)) {
          expMonths = parsed * 12;
        }
      }

      let sort_by = 'published_at';
      let sort_order = 'desc';
      if (filters?.sortBy === 'oldest') {
        sort_by = 'published_at';
        sort_order = 'asc';
      } else if (filters?.sortBy === 'highest-salary') {
        sort_by = 'salary_max';
        sort_order = 'desc';
      } else if (filters?.sortBy === 'lowest-salary') {
        sort_by = 'salary_min';
        sort_order = 'asc';
      }

      let work_mode: 'REMOTE' | 'HYBRID' | 'ONSITE' | undefined;
      if (filters?.remoteStatus && filters.remoteStatus !== 'Any') {
        const u = filters.remoteStatus.toUpperCase();
        if (u === 'REMOTE' || u === 'HYBRID' || u === 'ONSITE') {
          work_mode = u as any;
        }
      }

      const backendRes = await this.searchJobs({
        q: filters?.search || undefined,
        location: filters?.location || undefined,
        skills: filters?.skills && filters.skills.length > 0 ? filters.skills.join(',') : undefined,
        experience_months: expMonths,
        salary_min: filters?.salaryMin && filters.salaryMin > 0 ? filters.salaryMin : undefined,
        salary_max: filters?.salaryMax && filters.salaryMax > 0 ? filters.salaryMax : undefined,
        work_mode,
        page: filters?.page || 1,
        size: filters?.size || 10,
        sort_by,
        sort_order,
      });

      return backendRes.items.map(this.mapApiItemToJob);
    } catch (e) {
      console.warn('Backend GET /api/v1/jobs search API unavailable or DEV mode fallback:', e);
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
      return MOCK_JOBS;
    }
  }

  static async getJobById(id: string): Promise<Job | null> {
    if (DEV_MODE) {
      await mockDelay(300);
      const match = MOCK_JOBS.find(j => j.id === id);
      return match || null;
    }

    const res = await fetch(`/api/v1/jobs/${id}`);
    if (!res.ok) throw new Error('Failed to fetch job detail');
    const data = await res.json();
    return this.mapApiItemToJob(data);
  }
}

export class RecruiterJobsService {
  static mapApiItemToRecruiterJob(item: any): RecruiterJob {
    const minSalary = item.salary_min ? (item.salary_min >= 100000 ? `${(item.salary_min / 100000).toFixed(1).replace(/\.0$/, '')}L` : item.salary_min) : null;
    const maxSalary = item.salary_max ? (item.salary_max >= 100000 ? `${(item.salary_max / 100000).toFixed(1).replace(/\.0$/, '')}L` : item.salary_max) : null;
    const currencySym = item.currency === 'INR' || !item.currency ? '₹' : item.currency + ' ';
    const salaryStr = minSalary && maxSalary ? `${currencySym}${minSalary} – ${currencySym}${maxSalary}` : minSalary ? `${currencySym}${minSalary}+` : 'Salary not specified';

    const months = item.required_experience_months || 0;
    const expYears = Math.floor(months / 12);
    const expStr = expYears > 0 ? `${expYears}+ years` : 'Entry level';

    const statusMap: Record<string, JobStatus> = {
      DRAFT: 'Draft',
      PUBLISHED: 'Published',
      CLOSED: 'Closed',
    };

    const workModeStr = item.work_mode === 'REMOTE' ? 'Remote' : item.work_mode === 'HYBRID' ? 'Hybrid' : 'On-site';

    return {
      id: item.id,
      role: item.title,
      department: item.department || 'Engineering',
      employmentType: (item.employment_type as any) || 'Full-time',
      workMode: workModeStr as any,
      experience: expStr,
      salary: salaryStr,
      location: item.location || 'Remote',
      openings: 1,
      deadline: item.published_at ? new Date(item.published_at).toISOString().split('T')[0] : 'Open',
      skills: item.required_skills || [],
      responsibilities: item.required_keywords || [],
      requirements: item.preferred_skills || [],
      preferredSkills: item.preferred_skills || [],
      benefits: item.education_requirements || [],
      company: item.company_name || 'Company',
      logo: (item.company_name || item.title || 'C').charAt(0).toUpperCase(),
      logoColor: 'bg-blue-600',
      hiringManager: 'Hiring Lead',
      description: item.description || '',
      status: statusMap[item.status] || 'Draft',
      date: item.created_at ? new Date(item.created_at).toISOString().split('T')[0] : new Date().toISOString().split('T')[0],
      views: 0,
      applicationsCount: 0,
      shortlistedCount: 0,
      rejectedCount: 0,
      interviewScheduledCount: 0,
      offersSentCount: 0,
    };
  }

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
    try {
      const res = await fetch('/api/v1/jobs/company/me');
      if (res.ok) {
        const data = await res.json();
        if (data.items && Array.isArray(data.items)) {
          return data.items.map(this.mapApiItemToRecruiterJob);
        }
      }
    } catch (e) {
      console.warn('Backend GET /api/v1/jobs/company/me unavailable, using fallback:', e);
    }

    if (DEV_MODE) {
      await mockDelay(300);
      return this.getLocalJobs();
    }
    return MOCK_RECRUITER_JOBS;
  }

  static async getJobById(id: string): Promise<RecruiterJob | null> {
    try {
      const res = await fetch(`/api/v1/jobs/${id}`);
      if (res.ok) {
        const data = await res.json();
        return this.mapApiItemToRecruiterJob(data);
      }
    } catch (e) {
      console.warn(`Backend GET /api/v1/jobs/${id} unavailable, using fallback:`, e);
    }

    if (DEV_MODE) {
      await mockDelay(200);
      const jobs = this.getLocalJobs();
      return jobs.find(j => j.id === id) || null;
    }

    return null;
  }

  static async createJob(job: Partial<RecruiterJob> & { salary_min?: number; salary_max?: number; required_experience_months?: number }): Promise<RecruiterJob> {
    try {
      const workModeEnum = job.workMode?.toUpperCase() === 'REMOTE' ? 'REMOTE' : job.workMode?.toUpperCase() === 'HYBRID' ? 'HYBRID' : 'ONSITE';

      const payload = {
        title: job.role || 'New Job Posting',
        description: job.description || 'Job description',
        department: job.department || 'Engineering',
        work_mode: workModeEnum,
        location: job.location || 'Remote',
        salary_min: job.salary_min || 0,
        salary_max: job.salary_max || 0,
        currency: 'INR',
        required_skills: job.skills || [],
        preferred_skills: job.preferredSkills || job.requirements || [],
        required_experience_months: job.required_experience_months || 0,
        education_requirements: job.benefits || [],
        required_keywords: job.responsibilities || [],
      };

      const res = await fetch('/api/v1/jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        const createdItem = await res.json();
        if (job.status === 'Published') {
          try {
            const pubRes = await fetch(`/api/v1/jobs/${createdItem.id}/publish`, { method: 'POST' });
            if (pubRes.ok) {
              const publishedItem = await pubRes.json();
              return this.mapApiItemToRecruiterJob(publishedItem);
            }
          } catch (pubErr) {
            console.error('Publish transition error:', pubErr);
          }
        }
        return this.mapApiItemToRecruiterJob(createdItem);
      }
    } catch (e) {
      console.warn('Backend POST /api/v1/jobs error, falling back:', e);
    }

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
        salary: job.salary || '₹8L – ₹14L',
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

    throw new Error('Failed to create job');
  }

  static async updateJob(id: string, updates: Partial<RecruiterJob> & { salary_min?: number; salary_max?: number; required_experience_months?: number }): Promise<RecruiterJob> {
    try {
      const workModeEnum = updates.workMode ? (updates.workMode.toUpperCase() === 'REMOTE' ? 'REMOTE' : updates.workMode.toUpperCase() === 'HYBRID' ? 'HYBRID' : 'ONSITE') : undefined;

      const payload: any = {};
      if (updates.role) payload.title = updates.role;
      if (updates.description) payload.description = updates.description;
      if (updates.department) payload.department = updates.department;
      if (workModeEnum) payload.work_mode = workModeEnum;
      if (updates.location) payload.location = updates.location;
      if (updates.salary_min !== undefined) payload.salary_min = updates.salary_min;
      if (updates.salary_max !== undefined) payload.salary_max = updates.salary_max;
      if (updates.skills) payload.required_skills = updates.skills;
      if (updates.preferredSkills || updates.requirements) payload.preferred_skills = updates.preferredSkills || updates.requirements;
      if (updates.required_experience_months !== undefined) payload.required_experience_months = updates.required_experience_months;
      if (updates.benefits) payload.education_requirements = updates.benefits;
      if (updates.responsibilities) payload.required_keywords = updates.responsibilities;

      const res = await fetch(`/api/v1/jobs/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        const updatedItem = await res.json();
        return this.mapApiItemToRecruiterJob(updatedItem);
      }
    } catch (e) {
      console.warn(`Backend PATCH /api/v1/jobs/${id} error, falling back:`, e);
    }

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

    throw new Error('Failed to update job');
  }

  static async publishJob(id: string): Promise<RecruiterJob> {
    try {
      const res = await fetch(`/api/v1/jobs/${id}/publish`, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        return this.mapApiItemToRecruiterJob(data);
      }
      const errData = await res.json().catch(() => null);
      throw new Error(errData?.detail || 'Failed to publish job');
    } catch (e: any) {
      if (DEV_MODE) {
        return this.updateJob(id, { status: 'Published' });
      }
      throw e;
    }
  }

  static async unpublishJob(id: string): Promise<RecruiterJob> {
    try {
      const res = await fetch(`/api/v1/jobs/${id}/unpublish`, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        return this.mapApiItemToRecruiterJob(data);
      }
      const errData = await res.json().catch(() => null);
      throw new Error(errData?.detail || 'Failed to unpublish job');
    } catch (e: any) {
      if (DEV_MODE) {
        return this.updateJob(id, { status: 'Draft' });
      }
      throw e;
    }
  }

  static async closeJob(id: string): Promise<RecruiterJob> {
    try {
      const res = await fetch(`/api/v1/jobs/${id}/close`, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        return this.mapApiItemToRecruiterJob(data);
      }
      const errData = await res.json().catch(() => null);
      throw new Error(errData?.detail || 'Failed to close job');
    } catch (e: any) {
      if (DEV_MODE) {
        return this.updateJob(id, { status: 'Closed' });
      }
      throw e;
    }
  }

  static async deleteJob(id: string): Promise<boolean> {
    try {
      const res = await fetch(`/api/v1/jobs/${id}`, { method: 'DELETE' });
      if (res.ok || res.status === 204) {
        return true;
      }
    } catch (e) {
      console.warn(`Backend DELETE /api/v1/jobs/${id} error, falling back:`, e);
    }

    if (DEV_MODE) {
      await mockDelay(200);
      const jobs = this.getLocalJobs();
      const filtered = jobs.filter(j => j.id !== id);
      this.saveLocalJobs(filtered);
      return true;
    }

    return true;
  }
}
