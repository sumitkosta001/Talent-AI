import { CompanyBenefit } from '../types/companyBenefit';

export const MOCK_COMPANY_BENEFITS: Record<string, CompanyBenefit[]> = {
  stripe: [
    { id: 'ben-1', icon: 'heart', label: 'Premium Health Insurance', description: '100% covered health, vision, and dental plans.' },
    { id: 'ben-2', icon: 'calendar', label: 'Unlimited Paid Leave', description: 'Encouraged minimum of 4 weeks off annually.' },
    { id: 'ben-3', icon: 'clock', label: 'Flexible Working Hours', description: 'Core hours focus; align with your timezone team.' },
    { id: 'ben-4', icon: 'laptop', label: 'Remote Office Allowance', description: '$1,000 yearly stipend to customize home offices.' },
    { id: 'ben-5', icon: 'graduation-cap', label: 'Learning Budget', description: '$2,000 yearly budget for courses and books.' },
  ],
  vercel: [
    { id: 'ben-v1', icon: 'heart', label: 'Comprehensive Healthcare', description: 'Global healthcare coverage support.' },
    { id: 'ben-v2', icon: 'calendar', label: 'Flexible Time Off', description: 'Take time off whenever you need it.' },
    { id: 'ben-v3', icon: 'home', label: '100% Remote Workspace', description: 'Work from anywhere globally.' },
  ],
};
