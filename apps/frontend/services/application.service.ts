import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { Application, Analytics } from '@/types/application';
import { MOCK_APPLICATIONS } from '@/mock/applications';
import { MOCK_ANALYTICS } from '@/mock/analytics';

export class ApplicationService {
  static getLocalApplications(): Application[] {
    if (typeof window === 'undefined') return MOCK_APPLICATIONS;
    const stored = localStorage.getItem('talentai_applications');
    if (!stored) {
      localStorage.setItem('talentai_applications', JSON.stringify(MOCK_APPLICATIONS));
      return MOCK_APPLICATIONS;
    }
    return JSON.parse(stored);
  }

  static saveLocalApplications(apps: Application[]) {
    if (typeof window === 'undefined') return;
    localStorage.setItem('talentai_applications', JSON.stringify(apps));
  }

  static async getApplications(): Promise<Application[]> {
    if (DEV_MODE) {
      await mockDelay(300);
      return this.getLocalApplications();
    }

    const res = await fetch('/api/applications');
    if (!res.ok) throw new Error('Failed to fetch applications');
    return res.json();
  }

  static async getApplicationById(id: string): Promise<Application | null> {
    if (DEV_MODE) {
      await mockDelay(200);
      const apps = this.getLocalApplications();
      const match = apps.find(a => a.id === id);
      return match || null;
    }

    const res = await fetch(`/api/applications/${id}`);
    if (!res.ok) throw new Error('Failed to fetch application detail');
    return res.json();
  }

  static async withdrawApplication(id: string, reason: string): Promise<Application> {
    if (DEV_MODE) {
      await mockDelay(400);
      const apps = this.getLocalApplications();
      const matchIndex = apps.findIndex(a => a.id === id);
      if (matchIndex === -1) throw new Error('Application not found');
      
      const app = apps[matchIndex];
      app.status = 'Withdrawn';
      app.lastUpdated = new Date().toISOString().split('T')[0];
      app.timeline = [
        ...app.timeline,
        {
          status: 'Withdrawn',
          date: app.lastUpdated,
          time: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
          description: `Application withdrawn by candidate. Reason: ${reason}`,
          completed: true,
        }
      ];

      apps[matchIndex] = app;
      this.saveLocalApplications(apps);
      return app;
    }

    const res = await fetch(`/api/applications/${id}/withdraw`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason }),
    });
    if (!res.ok) throw new Error('Failed to withdraw application');
    return res.json();
  }

  static async archiveApplication(id: string): Promise<Application> {
    if (DEV_MODE) {
      await mockDelay(300);
      const apps = this.getLocalApplications();
      const matchIndex = apps.findIndex(a => a.id === id);
      if (matchIndex === -1) throw new Error('Application not found');

      const app = apps[matchIndex];
      app.archived = true;
      app.status = 'Archived';
      app.lastUpdated = new Date().toISOString().split('T')[0];

      apps[matchIndex] = app;
      this.saveLocalApplications(apps);
      return app;
    }

    const res = await fetch(`/api/applications/${id}/archive`, { method: 'PATCH' });
    if (!res.ok) throw new Error('Failed to archive application');
    return res.json();
  }

  static async restoreApplication(id: string): Promise<Application> {
    if (DEV_MODE) {
      await mockDelay(300);
      const apps = this.getLocalApplications();
      const matchIndex = apps.findIndex(a => a.id === id);
      if (matchIndex === -1) throw new Error('Application not found');

      const app = apps[matchIndex];
      app.archived = false;
      // Revert status to Under Review or Applied
      app.status = 'Under Review';
      app.lastUpdated = new Date().toISOString().split('T')[0];

      apps[matchIndex] = app;
      this.saveLocalApplications(apps);
      return app;
    }

    const res = await fetch(`/api/applications/${id}/restore`, { method: 'PATCH' });
    if (!res.ok) throw new Error('Failed to restore application');
    return res.json();
  }

  static async getAnalytics(): Promise<Analytics> {
    if (DEV_MODE) {
      await mockDelay(300);
      return MOCK_ANALYTICS;
    }

    const res = await fetch('/api/applications/analytics');
    if (!res.ok) throw new Error('Failed to fetch analytics');
    return res.json();
  }

  static async applyForJob(
    jobId: string,
    jobTitle: string,
    company: string,
    logo: string,
    logoColor: string,
    salary: string,
    location: string
  ): Promise<Application> {
    if (DEV_MODE) {
      await mockDelay(400);
      const apps = this.getLocalApplications();
      
      const newApp: Application = {
        id: `app-${jobId}-${Date.now()}`,
        jobId,
        jobTitle,
        company,
        logo,
        logoColor,
        location,
        employmentType: 'Full-time',
        salary,
        appliedDate: new Date().toISOString().split('T')[0],
        lastUpdated: new Date().toISOString().split('T')[0],
        status: 'Applied',
        atsScore: 85,
        matchPercentage: 88,
        recruiter: {
          name: 'TalentAI Coordinator',
          email: 'support@talentai.com',
        },
        timeline: [
          { status: 'Applied', date: new Date().toISOString().split('T')[0], time: '12:00 PM', description: 'Application submitted successfully.', completed: true }
        ]
      };
      
      this.saveLocalApplications([newApp, ...apps]);
      return newApp;
    }

    const res = await fetch('/api/applications', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ jobId }),
    });
    if (!res.ok) throw new Error('Failed to submit application');
    return res.json();
  }
}
