import { Suggestion } from '../types/ats';

export const MOCK_SUGGESTIONS: Suggestion[] = [
  { id: 's1', priority: 'high', text: 'Add more quantified achievements to professional experience. Mention user numbers, speed improvements, or revenue impacts (e.g. "optimized load time by 40%, boosting retention").', category: 'content' },
  { id: 's2', priority: 'high', text: 'Include "Kubernetes" and "Terraform" keywords in your technical skills and project descriptors. These appear in 78% of modern senior engineering job profiles.', category: 'keyword' },
  { id: 's3', priority: 'medium', text: 'Optimize the Professional Summary. Change from general statements to active statements highlighting years of experience and your core technical stack (e.g. "Senior Frontend Architect with 5+ years specialized in React/TypeScript").', category: 'content' },
  { id: 's4', priority: 'medium', text: 'Reduce paragraph length in your work experience bullet lists. Break long sentences into action-oriented statements.', category: 'formatting' },
  { id: 's5', priority: 'low', text: 'Include links to active GitHub, LinkedIn profiles, and personal portfolio sites clearly under the header contact details.', category: 'formatting' },
  { id: 's6', priority: 'low', text: 'Consider listing professional developer certifications such as AWS Certified Developer or HashiCorp Terraform Associate.', category: 'content' }
];
export const MOCK_STRENGTHS = [
  { title: 'Strong Technical Foundation', description: 'Excellent match for React, TypeScript, and Node.js environments.' },
  { title: 'High-Impact Projects', description: 'Strong demonstration of full-stack system implementation and tech details.' },
  { title: 'Formatting Cleanliness', description: 'Zero tables, columns, or graphics clashing with parser software.' },
];
export const MOCK_WEAKNESSES = [
  { title: 'Generic Summary', description: 'Professional summary lacks strong hook and key metrics.' },
  { title: 'Missing Cloud Native Tools', description: 'Lacks mentions of container orchestration (Kubernetes) and IaC (Terraform).' },
  { title: 'Low Action Verb Density', description: 'Repetitive use of words like "built" and "developed" instead of active metrics.' },
];
