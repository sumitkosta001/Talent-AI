import { Job } from '../types/job';

export const MOCK_JOBS: Job[] = [
  {
    id: 'google-sde-3',
    companyId: 'google',
    company: 'Google',
    role: 'Senior Software Engineer (L5)',
    title: 'Senior Software Engineer (L5)',
    salary: '$180K–$240K',
    match: 95,
    location: 'Bangalore, India',
    logo: 'G',
    logoColor: 'bg-blue-600',
    experience: '5+ years',
    skills: ['React', 'TypeScript', 'System Design', 'Algorithms', 'Go'],
    bookmarked: false,
    applied: false,
    description: 'Lead frontend engineering pipelines for high-scale developer platform dashboards. Collaborate on rendering speeds, compiler toolchains, and visual component systems.',
    responsibilities: [
      'Architect and build modular user interfaces for Google Cloud tools.',
      'Optimize web client execution rates, aiming for sub-100ms render frames.',
      'Mentor intermediate engineers and establish system performance review gates.'
    ],
    requirements: [
      '5+ years programming scalable Single Page Applications using React or Angular.',
      'Solid command of TypeScript typing architectures and compilation details.',
      'Experience optimizing render performance, bundle weights, and client-side memory usage.'
    ],
    benefits: [
      { icon: '🏥', label: 'Premium Health', desc: 'Fully covered medical, dental, and eye insurances.' },
      { icon: '🍽️', label: 'Catered Food', desc: 'Free breakfast, lunch, and dinner inside office blocks.' },
      { icon: '🏖️', label: 'Generous PTO', desc: '25 days vacation plus global calendar leaves.' }
    ],
    date: '2 days ago',
    type: 'Full-time',
    remoteStatus: 'Hybrid',
    deadline: 'Aug 12, 2025',
    applicantsCount: 142,
    isFeatured: true,
    category: 'Frontend Engineering'
  },
  {
    id: 'microsoft-fe-2',
    companyId: 'microsoft',
    company: 'Microsoft',
    role: 'Frontend Engineer II',
    title: 'Frontend Engineer II',
    salary: '$140K–$190K',
    match: 92,
    location: 'Hyderabad, India',
    logo: 'M',
    logoColor: 'bg-red-500',
    experience: '3+ years',
    skills: ['React', 'TypeScript', 'CSS', 'Redux Toolkit', 'REST APIs'],
    bookmarked: true,
    applied: false,
    description: 'Join the Teams Web Client core team. Refactor chat threads, implement real-time communication protocols, and enhance responsive layout speeds across multiple monitors.',
    responsibilities: [
      'Implement real-time rendering layers for Teams chat panels using WebSockets.',
      'Refactor layouts to adhere strictly to visual contrast and screen reader accessibility guidelines.',
      'Conduct rigorous peer code reviews to maintain strict engineering quality standards.'
    ],
    requirements: [
      '3+ years web developer experience focusing on Javascript and CSS structures.',
      'Strong capabilities using state managers like Redux Toolkit or Recoil.',
      'Proven history implementing pixel-perfect templates matching Figma UI drawings.'
    ],
    benefits: [
      { icon: '📚', label: 'Learning Fund', desc: '$3,000 yearly training budget for books and conferences.' },
      { icon: '🏠', label: 'Hybrid Work', desc: 'Up to 3 days remote work authorization per week.' },
      { icon: '📈', label: 'ESPP Plans', desc: 'Generous discount rates on company stock purchasing program.' }
    ],
    date: '3 days ago',
    type: 'Full-time',
    remoteStatus: 'Hybrid',
    deadline: 'Aug 24, 2025',
    applicantsCount: 98,
    isFeatured: false,
    category: 'Frontend Engineering'
  },
  {
    id: 'vercel-nextjs-sde',
    companyId: 'vercel',
    company: 'Vercel',
    role: 'Staff Next.js Platform Engineer',
    title: 'Staff Next.js Platform Engineer',
    salary: '$190K–$250K',
    match: 97,
    location: 'Remote First',
    logo: 'V',
    logoColor: 'bg-black',
    experience: '8+ years',
    skills: ['Next.js', 'React', 'TypeScript', 'Turbopack', 'Rust', 'Performance Optimization'],
    bookmarked: false,
    applied: false,
    description: 'Shape the future of Vercel’s deployment workflows. Collaborate closely on React Server Components implementation, Next.js build performance optimization, and serverless hosting runtimes.',
    responsibilities: [
      'Set engineering paths for Next.js build compilation speeds.',
      'Collaborate on Node.js and Rust compilers to minimize page bundle packages.',
      'Actively participate inside open-source frameworks community discussions.'
    ],
    requirements: [
      '8+ years developing web application architectures.',
      'Strong involvement within open source framework communities.',
      'Detailed knowledge of Node.js runtimes, Edge computation, and serverless functions.'
    ],
    benefits: [
      { icon: '🏠', label: 'Fully Remote', desc: 'Work from wherever you have robust internet access.' },
      { icon: '📈', label: 'Equity Grants', desc: 'Pre-IPO stock options with significant upside targets.' },
      { icon: '💻', label: 'Workspace Setup', desc: 'Free Macbook Pro, dual displays, and home ergonomic equipment.' }
    ],
    date: '1 day ago',
    type: 'Full-time',
    remoteStatus: 'Remote',
    deadline: 'Sep 02, 2025',
    applicantsCount: 64,
    isFeatured: true,
    category: 'Full Stack Engineering'
  },
  {
    id: 'stripe-integrations',
    companyId: 'stripe',
    company: 'Stripe',
    role: 'Full Stack Engineer (Payments)',
    title: 'Full Stack Engineer (Payments)',
    salary: '$160K–$210K',
    match: 87,
    location: 'San Francisco, CA',
    logo: 'S',
    logoColor: 'bg-violet-600',
    experience: '4+ years',
    skills: ['React', 'TypeScript', 'Ruby on Rails', 'PostgreSQL', 'REST APIs'],
    bookmarked: false,
    applied: true,
    description: 'Build robust, developer-friendly payment APIs. Integrate global banking infrastructures, secure transaction payloads, and compose highly performant dashboards for Stripe Merchants.',
    responsibilities: [
      'Design RESTful web endpoints matching Stripe payment specifications.',
      'Implement transaction processing pipelines with strict consistency guarantees.',
      'Ensure merchants metrics dashboard loads millions of records with minimal lag.'
    ],
    requirements: [
      '4+ years full stack engineering background.',
      'Experience working inside database transactions, isolation levels, and scale constraints.',
      'Strong alignment to clean code architectures, testing patterns, and API designs.'
    ],
    benefits: [
      { icon: '🧘', label: 'Wellness Stipend', desc: '$150 monthly mental wellness or gym membership voucher.' },
      { icon: '🏥', label: 'Premium Insurance', desc: '100% covered health, vision, and mental support services.' },
      { icon: '🍽️', label: 'Food Perks', desc: 'Free gourmet meals served daily in executive cafeterias.' }
    ],
    date: '5 days ago',
    type: 'Full-time',
    remoteStatus: 'On-site',
    deadline: 'Aug 18, 2025',
    applicantsCount: 112,
    isFeatured: false,
    category: 'Full Stack Engineering'
  },
  {
    id: 'linear-product-designer',
    companyId: 'linear',
    company: 'Linear',
    role: 'Senior Product Designer',
    title: 'Senior Product Designer',
    salary: '$130K–$180K',
    match: 84,
    location: 'Remote First',
    logo: 'L',
    logoColor: 'bg-[#5E6AD2]',
    experience: '5+ years',
    skills: ['Figma', 'Product Design', 'UI/UX', 'Design Systems', 'CSS'],
    bookmarked: false,
    applied: false,
    description: 'Help craft the future of project management software. Design highly responsive interactive workflows, custom styling variables, and maintain pixel-perfect design systems used globally.',
    responsibilities: [
      'Translate complex product specs into intuitive, simple mockups.',
      'Collaborate with developers to ensure final code is visually identical to design proposals.',
      'Conduct frequent customer feedback sessions to refine feature flows.'
    ],
    requirements: [
      '5+ years designing SaaS desktop or web applications.',
      'Stunning design portfolio showcasing details-driven user layouts and typography.',
      'Basic command of HTML/CSS is highly welcome to write code prototypes.'
    ],
    benefits: [
      { icon: '🏠', label: 'Work Anywhere', desc: 'Flexible hours and fully remote team environment.' },
      { icon: '✈️', label: 'Company Retreats', desc: 'Semi-annual team meetups in beautiful global locations.' },
      { icon: '🧘', label: 'Health Benefits', desc: 'Generous medical insurance coverage for entire family.' }
    ],
    date: '4 days ago',
    type: 'Full-time',
    remoteStatus: 'Remote',
    deadline: 'Sep 10, 2025',
    applicantsCount: 45,
    isFeatured: true,
    category: 'Product Design'
  }
];
