import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { Applicant, ApplicantStatus } from '@/types/applicant';
import { MOCK_APPLICANTS } from '@/mock/applicants';

export class RecruiterApplicantService {
  static getLocalApplicants(): Applicant[] {
    if (typeof window === 'undefined') return MOCK_APPLICANTS;
    const stored = localStorage.getItem('talentai_recruiter_applicants');
    if (!stored) {
      localStorage.setItem('talentai_recruiter_applicants', JSON.stringify(MOCK_APPLICANTS));
      return MOCK_APPLICANTS;
    }
    return JSON.parse(stored);
  }

  static saveLocalApplicants(applicants: Applicant[]) {
    if (typeof window === 'undefined') return;
    localStorage.setItem('talentai_recruiter_applicants', JSON.stringify(applicants));
  }

  static async getApplicants(): Promise<Applicant[]> {
    if (DEV_MODE) {
      await mockDelay(300);
      return this.getLocalApplicants();
    }

    const res = await fetch('/api/recruiter/applicants');
    if (!res.ok) throw new Error('Failed to retrieve applicants');
    return res.json();
  }

  static async getApplicantById(id: string): Promise<Applicant | null> {
    if (DEV_MODE) {
      await mockDelay(200);
      const items = this.getLocalApplicants();
      return items.find(a => a.id === id) || null;
    }

    const res = await fetch(`/api/recruiter/applicants/${id}`);
    if (!res.ok) throw new Error('Failed to retrieve applicant detail');
    return res.json();
  }

  static async updateStatus(id: string, status: ApplicantStatus): Promise<Applicant> {
    if (DEV_MODE) {
      await mockDelay(300);
      const items = this.getLocalApplicants();
      const idx = items.findIndex(a => a.id === id);
      if (idx === -1) throw new Error('Applicant not found');

      const app = items[idx];
      app.status = status;
      app.timeline = [
        ...app.timeline,
        {
          stage: status,
          date: new Date().toISOString().split('T')[0],
          notes: `Status updated to ${status} by recruiter coordinator.`,
        }
      ];

      items[idx] = app;
      this.saveLocalApplicants(items);
      return app;
    }

    const res = await fetch(`/api/recruiter/applicants/${id}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    });
    if (!res.ok) throw new Error('Failed to update status');
    return res.json();
  }

  static async addNotes(id: string, notes: string): Promise<Applicant> {
    if (DEV_MODE) {
      await mockDelay(200);
      const items = this.getLocalApplicants();
      const idx = items.findIndex(a => a.id === id);
      if (idx === -1) throw new Error('Applicant not found');

      items[idx].notes = notes;
      this.saveLocalApplicants(items);
      return items[idx];
    }

    const res = await fetch(`/api/recruiter/applicants/${id}/notes`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ notes }),
    });
    if (!res.ok) throw new Error('Failed to save recruiter notes');
    return res.json();
  }
}
