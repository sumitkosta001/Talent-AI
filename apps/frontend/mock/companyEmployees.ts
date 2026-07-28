import { CompanyEmployee } from '../types/companyEmployee';

export const MOCK_COMPANY_EMPLOYEES: Record<string, CompanyEmployee[]> = {
  stripe: [
    { id: 'emp-1', name: 'Sarah Mitchell', role: 'Head of Talent Acquisition', initials: 'SM', color: 'bg-violet-600' },
    { id: 'emp-2', name: 'James Park', role: 'Staff Technical Recruiter', initials: 'JP', color: 'bg-blue-600' },
    { id: 'emp-3', name: 'Priya Sharma', role: 'Talent Partner Coordinator', initials: 'PS', color: 'bg-emerald-600' },
  ],
  vercel: [
    { id: 'emp-v1', name: 'Guillermo Rauch', role: 'Founder & CEO', initials: 'GR', color: 'bg-black' },
    { id: 'emp-v2', name: 'Lee Robinson', role: 'VP of Developer Experience', initials: 'LR', color: 'bg-slate-700' },
  ],
};
