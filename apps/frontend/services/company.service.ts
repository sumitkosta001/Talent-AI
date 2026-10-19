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

  static mapApiItemToCompany(item: Record<string, unknown>): Company {
    const name = (item.name as string) || 'Company Profile';
    return {
      id: (item.id as string) || '',
      name: (item.name as string) || '',
      description: (item.description as string) || null,
      about: (item.description as string) || '',
      website: (item.website as string) || '',
      logo_url: (item.logo_url as string) || null,
      logo: (item.logo_url as string) || (name ? name.charAt(0).toUpperCase() : 'C'),
      logoColor: 'bg-blue-600',
      location: (item.location as string) || '',
      headquarters: (item.location as string) || '',
      industry: (item.industry as string) || '',
      employees: (item.employees as string) || '',
      techStack: Array.isArray(item.techStack) ? (item.techStack as string[]) : [],
    };
  }

  static async getCompanyById(id: string): Promise<Company | null> {
    if (DEV_MODE) {
      await mockDelay(200);
      const match = MOCK_COMPANIES.find(c => c.id === id);
      return match || null;
    }

    const res = await apiClient.get(`/api/v1/companies/${id}`);
    if (!res.ok) {
      if (res.status === 404) return null;
      throw new Error('Failed to fetch company profile');
    }
    const data = await res.json();
    return this.mapApiItemToCompany(data);
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

  static mapApiItemToCompanyDetail(item: Record<string, unknown>): CompanyDetail {
    const name = (item.name as string) || 'Company Profile';
    return {
      name: (item.name as string) || '',
      logo: (item.logo_url as string) || (name ? name.charAt(0).toUpperCase() : 'C'),
      logoColor: 'bg-blue-600',
      bannerUrl: (item.banner_url as string) || undefined,
      about: (item.description as string) || '',
      industry: (item.industry as string) || 'Technology',
      website: (item.website as string) || '',
      location: (item.location as string) || 'Remote',
      employees: (item.employees as string) || '50-200',
      founded: (item.founded as string) || '2024',
      culture: Array.isArray(item.culture) ? (item.culture as string[]) : ['Innovation', 'Inclusivity', 'Autonomy'],
      benefits: Array.isArray(item.benefits) ? (item.benefits as string[]) : ['Health Insurance', 'Remote Work', 'Learning Budget'],
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
    } catch (e: unknown) {
      console.warn('Backend company update error:', e);
      throw e;
    }
  }
}
