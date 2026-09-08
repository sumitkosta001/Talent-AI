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
      employees: '50-200',
      founded: '2022',
      culture: ['Innovation', 'Inclusivity', 'Autonomy'],
      benefits: ['Health Insurance', 'Remote Work', 'Learning Budget'],
      hiringTeam: [],
      socials: {},
    };
  }

  static async getCompany(): Promise<CompanyDetail> {
    try {
      const res = await fetch('/api/v1/companies/me');
      if (res.ok) {
        const data = await res.json();
        return this.mapApiItemToCompanyDetail(data);
      }
    } catch (e) {
      console.warn('Backend GET /api/v1/companies/me unavailable:', e);
    }

    if (DEV_MODE) {
      await mockDelay(200);
      return this.getLocalCompany();
    }

    return this.getLocalCompany();
  }

  static async updateCompany(company: CompanyDetail): Promise<CompanyDetail> {
    try {
      const payload = {
        name: company.name,
        description: company.about,
        website: company.website,
        logo_url: company.logo,
        location: company.location,
        industry: company.industry,
      };

      const res = await fetch('/api/v1/companies/me', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        const data = await res.json();
        return this.mapApiItemToCompanyDetail(data);
      }
    } catch (e) {
      console.warn('Backend PATCH /api/v1/companies/me error:', e);
    }

    if (DEV_MODE) {
      await mockDelay(300);
      this.saveLocalCompany(company);
      return company;
    }

    this.saveLocalCompany(company);
    return company;
  }
}
