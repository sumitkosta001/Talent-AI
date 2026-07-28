import { CompanyDetail } from '../types/company';

export const MOCK_COMPANY: CompanyDetail = {
  name: 'TalentAI Technologies',
  logo: 'T',
  logoColor: 'bg-blue-600',
  bannerUrl: '/banner.jpg',
  about: 'TalentAI is a next generation hiring optimization engine powered by advanced language modeling and resume parsed ranking matrices.',
  industry: 'Software & Technology / AI SaaS',
  website: 'https://talentai.co',
  location: 'San Francisco, CA (Remote First)',
  employees: '150 - 250 Employees',
  founded: '2024',
  culture: [
    'Open source integration focus.',
    'Sustained high standards engineering loops.',
    'Remote first asynchronous flexibility.',
  ],
  benefits: [
    'Competitive stock option packages.',
    'Full health, dental, and vision insurance premiums covered.',
    'Flexible workspace stipend budgets.',
  ],
  hiringTeam: [
    { name: 'Sarah Mitchell', role: 'Principal Recruiter Coordinator' },
    { name: 'Marcus Aurelius', role: 'Staff Engineering Lead' },
  ],
  socials: {
    linkedin: 'https://linkedin.com/company/talentai',
    twitter: 'https://twitter.com/talentai_hq',
    github: 'https://github.com/talentai-hq',
  },
};
