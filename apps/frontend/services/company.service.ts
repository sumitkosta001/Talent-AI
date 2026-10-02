import { DEV_MODE } from '@/lib/config';
import { mockDelay } from '@/lib/mockDelay';
import { Company, CompanyDetail } from '@/types/company';
import { MOCK_COMPANIES } from '@/mock/companies';
import { MOCK_COMPANY } from '@/mock/company';
import { apiClient } from '@/lib/apiClient';

export class CompanyService {
  static async getCompanies(): Promise<Company[]> {
    if (DEV_MODE) {
      await mockDelay(300);
      return MOCK_COMPANIES;
    }

    const res = await apiClient.get('/api/v1/companies');
    if (!res.ok) throw new Error('Failed to fetch companies');
    return res.json();
  }

  static async getCompanyById(id: string): Promise<Company | null> {
    if (DEV_MODE) {
      await mockDelay(200);
      const match = MOCK_COMPANIES.find(c => c.id === id);
      return match || null;
    }

    const res = await apiClient.get(`/api/v1/companies/${id}`);
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
    try {
      return JSON.parse(stored);
    } catch {
      return MOCK_COMPANY;
    }
  }

  static saveLocalCompany(company: CompanyDetail) {
    if (typeof window === 'undefined') return;
    localStorage.setItem('talentai_recruiter_company', JSON.stringify(company));
  }

  static mapApiItemToCompanyDetail(item: any): CompanyDetail {
    const name = item.name || 'Company Profile';
    return {
      name: item.name || '',
      logo: item.logo_url || (name ? name.charAt(0).toUpperCase() : 'C'),
      logoColor: 'bg-blue-600',
      bannerUrl: item.banner_url || undefined,
      about: item.description || '',
      industry: item.industry || 'Technology',
      website: item.website || '',
      location: item.location || 'Remote',
      employees: item.employees || '50-200',
      founded: item.founded || '2024',
      culture: item.culture || ['Innovation', 'Inclusivity', 'Autonomy'],
      benefits: item.benefits || ['Health Insurance', 'Remote Work', 'Learning Budget'],
      hiringTeam: [],
      socials: {},
    };
  }

  static async getCompany(): Promise<CompanyDetail> {
    try {
      const res = await apiClient.get('/api/v1/companies/me');
      if (res.ok) {
        const data = await res.json();
        const mapped = this.mapApiItemToCompanyDetail(data);
        this.saveLocalCompany(mapped);
        return mapped;
      }
    } catch (e) {
      console.warn('Backend GET /api/v1/companies/me error:', e);
    }

    return this.getLocalCompany();
  }

  static async updateCompany(company: CompanyDetail): Promise<CompanyDetail> {
    const payload = {
      name: company.name.trim(),
      description: company.about?.trim() || undefined,
      website: company.website?.trim() || undefined,
      logo_url: company.logo?.trim() || undefined,
      location: company.location?.trim() || undefined,
      industry: company.industry?.trim() || undefined,
    };

    try {
      // First attempt to update existing company
      const patchRes = await apiClient.patch('/api/v1/companies/me', payload);
      if (patchRes.ok) {
        const data = await patchRes.json();
        const mapped = this.mapApiItemToCompanyDetail(data);
        this.saveLocalCompany(mapped);
        return mapped;
      }

      // If 404, user account is not associated with a company yet -> create it
      if (patchRes.status === 404) {
        const createRes = await apiClient.post('/api/v1/companies', payload);
        if (createRes.ok) {
          const data = await createRes.json();
          const mapped = this.mapApiItemToCompanyDetail(data);
          this.saveLocalCompany(mapped);
          return mapped;
        } else {
          const errData = await createRes.json().catch(() => null);
          const msg = errData?.error?.message || errData?.detail || 'Failed to create company';
          throw new Error(msg);
        }
      } else {
        const errData = await patchRes.json().catch(() => null);
        const msg = errData?.error?.message || errData?.detail || 'Failed to update company';
        throw new Error(msg);
      }
    } catch (e: any) {
      console.warn('Backend company update error:', e);
      throw e;
    }
  }
}
