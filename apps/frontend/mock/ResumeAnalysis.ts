import { ResumeAnalysis } from '../types/resume';

export const MOCK_RESUME_ANALYSIS: ResumeAnalysis = {
  overallScore: 92,
  formattingScore: 91,
  keywordCoverageScore: 94,
  educationScore: 96,
  experienceScore: 88,
  projectScore: 85,
  skillScore: 95,
  strengths: [
    'Strong technical skills section with highly relevant, in-demand frontend technologies.',
    'Excellent use of action verbs and quantifiable achievements in work descriptions (e.g., "Reduced load time by 40%").',
    'Consistent page layout, typography hierarchy, and standard margins ideal for ATS parsing.',
  ],
  weaknesses: [
    'Lacks cloud container orchestration technologies like Kubernetes.',
    'Professional summary section is slightly brief and could summarize core achievements better.',
    'Social contact linkages like LinkedIn and GitHub are missing from the contact details header.',
  ],
  suggestions: [
    { priority: 'high', text: 'Add "Kubernetes" — this appears in 78% of senior engineering job requirements.' },
    { priority: 'high', text: 'Include a detailed professional summary paragraph at the top of your resume.' },
    { priority: 'medium', text: 'Add absolute links to your public GitHub profile and LinkedIn.' },
    { priority: 'medium', text: 'Quantify impact in the Startup Labs role using active user numbers or load performance metrics.' },
    { priority: 'low', text: 'Include secondary certifications like cloud computing credentials to highlight deployment knowledge.' },
  ],
  matchedKeywords: ['React', 'TypeScript', 'Node.js', 'REST APIs', 'PostgreSQL', 'AWS', 'Docker', 'Git', 'Agile', 'CI/CD'],
  missingKeywords: ['Kubernetes', 'Terraform', 'Redis', 'GraphQL Federation'],
};
