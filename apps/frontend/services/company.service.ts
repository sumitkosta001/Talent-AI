import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { Company, CompanyDetail } from '@/types/company';
import { MOCK_COMPANIES } from '@/mock/companies';
import { MOCK_COMPANY } from '@/mock/company';

export class CompanyService {
  static async getCompanies(): Promise<Company[]> {
    if (DEV_MODE) {
      await mockDelay(300);
      return MOCK_COMPANIES;
    }

    const res = await fetch('/api/companies');
    if (!res.ok) throw new Error('Failed to fetch companies');
    return res.json();
  }

  static async getCompanyById(id: string): Promise<Company | null> {
    if (DEV_MODE) {
      await mockDelay(200);
      const match = MOCK_COMPANIES.find(c => c.id === id);
      return match || null;
    }

    const res = await fetch(`/api/companies/${id}`);
    if (!res.ok) throw new Error('Failed to fetch company profile');
    return res.json();
  }
}

export class RecruiterCompanyService {
  static getLocalCompany(): CompanyDetail {
    if (typeof window === 'undefined') return MOCK_COMPANY;
    const stored = localStorage.getItem('talentai_recruiter_company');
    if (!stored) {
      localStorage.setItem('talentai_recruiter_company', JSON.stringify(MOCK_COMPANY));
      return MOCK_COMPANY;
    }
    return JSON.parse(stored);
  }

  static saveLocalCompany(company: CompanyDetail) {
    if (typeof window === 'undefined') return;
    localStorage.setItem('talentai_recruiter_company', JSON.stringify(company));
  }

  static async getCompany(): Promise<CompanyDetail> {
    if (DEV_MODE) {
      await mockDelay(200);
      return this.getLocalCompany();
    }

    const res = await fetch('/api/recruiter/company');
    if (!res.ok) throw new Error('Failed to retrieve company profile');
    return res.json();
  }

  static async updateCompany(company: CompanyDetail): Promise<CompanyDetail> {
    if (DEV_MODE) {
      await mockDelay(300);
      this.saveLocalCompany(company);
      return company;
    }

    const res = await fetch('/api/recruiter/company', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(company),
    });
    if (!res.ok) throw new Error('Failed to save company profile changes');
    return res.json();
  }
}
