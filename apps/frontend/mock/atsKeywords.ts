import { Keyword } from '../types/ats';

export const MOCK_KEYWORDS: Keyword[] = [
  { name: 'React', matched: true, frequency: 8, category: 'framework', importance: 'high' },
  { name: 'TypeScript', matched: true, frequency: 6, category: 'technical', importance: 'high' },
  { name: 'Node.js', matched: true, frequency: 4, category: 'technical', importance: 'high' },
  { name: 'REST APIs', matched: true, frequency: 3, category: 'technical', importance: 'medium' },
  { name: 'PostgreSQL', matched: true, frequency: 3, category: 'technical', importance: 'medium' },
  { name: 'AWS', matched: true, frequency: 2, category: 'tool', importance: 'high' },
  { name: 'Docker', matched: true, frequency: 2, category: 'tool', importance: 'medium' },
  { name: 'Git', matched: true, frequency: 4, category: 'tool', importance: 'low' },
  { name: 'Agile', matched: true, frequency: 3, category: 'soft', importance: 'medium' },
  { name: 'CI/CD', matched: true, frequency: 1, category: 'technical', importance: 'high' },
  { name: 'Kubernetes', matched: false, frequency: 0, category: 'tool', importance: 'high' },
  { name: 'Terraform', matched: false, frequency: 0, category: 'tool', importance: 'high' },
  { name: 'Redis', matched: false, frequency: 0, category: 'tool', importance: 'medium' },
  { name: 'GraphQL Federation', matched: false, frequency: 0, category: 'framework', importance: 'medium' },
];
export const MOCK_MATCHED_KEYWORDS = MOCK_KEYWORDS.filter(k => k.matched);
export const MOCK_MISSING_KEYWORDS = MOCK_KEYWORDS.filter(k => !k.matched);
export const MOCK_IMPORTANT_KEYWORDS = MOCK_KEYWORDS.filter(k => k.importance === 'high');
export const MOCK_WEAK_KEYWORDS = MOCK_KEYWORDS.filter(k => k.frequency <= 1 && k.matched);
export const MOCK_SUGGESTED_KEYWORDS = [
  { name: 'Next.js', category: 'framework', relevance: '95%' },
  { name: 'Tailwind CSS', category: 'framework', relevance: '90%' },
  { name: 'Framer Motion', category: 'framework', relevance: '85%' },
  { name: 'System Design', category: 'technical', relevance: '80%' },
];
