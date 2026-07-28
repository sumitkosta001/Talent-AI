export interface JobDescriptionMatch {
  title: string;
  company: string;
  matchRate: number;
  compatibilityLevel: 'Ready to Apply' | 'Recommended' | 'Needs Improvement';
  requiredSkills: string[];
  keyHighlights: string[];
}

export const MOCK_JOB_DESCRIPTION: JobDescriptionMatch = {
  title: 'Senior Frontend Engineer',
  company: 'Stripe',
  matchRate: 87,
  compatibilityLevel: 'Ready to Apply',
  requiredSkills: ['React', 'TypeScript', 'Node.js', 'System Design', 'Kubernetes', 'AWS', 'GraphQL'],
  keyHighlights: [
    '5+ years engineering responsive and performant user interfaces.',
    'Collaborated in single-page applications optimization and build flows.',
    'Experience working with container management pipelines.'
  ]
};
