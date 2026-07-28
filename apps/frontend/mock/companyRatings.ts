import { CompanyRating } from '../types/companyRating';

export const MOCK_COMPANY_RATINGS: Record<string, CompanyRating> = {
  stripe: {
    overall: 4.8,
    workLifeBalance: 4.2,
    salaryBenefits: 4.9,
    careerGrowth: 4.7,
    management: 4.5,
    culture: 4.8,
    jobSecurity: 4.6,
  },
  vercel: {
    overall: 4.9,
    workLifeBalance: 4.4,
    salaryBenefits: 4.8,
    careerGrowth: 4.9,
    management: 4.7,
    culture: 4.9,
    jobSecurity: 4.5,
  },
  google: {
    overall: 4.7,
    workLifeBalance: 4.6,
    salaryBenefits: 4.8,
    careerGrowth: 4.5,
    management: 4.3,
    culture: 4.6,
    jobSecurity: 4.8,
  },
};
