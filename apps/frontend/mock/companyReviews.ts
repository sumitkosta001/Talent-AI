import { CompanyReview } from '../types/companyReview';

export const MOCK_COMPANY_REVIEWS: Record<string, CompanyReview[]> = {
  stripe: [
    {
      id: 'rev-stripe-1',
      authorName: 'Senior Frontend Architect',
      isCurrentEmployee: true,
      department: 'Engineering',
      rating: 5,
      title: 'Inspiring engineering culture with great perks',
      description: 'The talent level at Stripe is incredibly high. You work with brilliant colleagues on highly visible financial APIs. High autonomy and strong ownership of products.',
      pros: 'Top compensation, high-end laptops, remote-friendly culture, excellent peer reviews.',
      cons: 'Pace is fast, which can lead to stress if you do not set clear personal boundaries.',
      recommendation: 'Highly recommended',
      reviewDate: '2026-06-15',
    },
    {
      id: 'rev-stripe-2',
      authorName: 'Product Designer',
      isCurrentEmployee: false,
      department: 'Design',
      rating: 4,
      title: 'Brilliant design team but high launch threshold',
      description: 'Stripe values design and user interface polish more than almost any other company. The documentation layouts are beautiful.',
      pros: 'Exceptional attention to product detail, helpful benefits, competitive base salaries.',
      cons: 'Projects can stall in review loops because the launch standards are extremely high.',
      recommendation: 'Recommended',
      reviewDate: '2026-04-10',
    },
  ],
  vercel: [
    {
      id: 'rev-vercel-1',
      authorName: 'Backend Developer',
      isCurrentEmployee: true,
      department: 'Infrastructure',
      rating: 5,
      title: 'Fast-paced frontend innovation workspace',
      description: 'Vercel is shipping next-generation web technologies daily. Great culture of speed, execution, and simplicity.',
      pros: 'Awesome team, fully remote culture, flexible budgets, work with top framework maintainers.',
      cons: 'Rapid scaling requires constant adaptation to team structure reorganizations.',
      recommendation: 'Highly recommended',
      reviewDate: '2026-07-01',
    },
  ],
};
