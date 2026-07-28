import {
  SectionAnalysis,
  FormattingScore,
  GrammarScore,
  SkillAnalysis,
  EducationAnalysis,
  ExperienceAnalysis,
  ProjectAnalysis
} from '../types/ats';

export const MOCK_SECTION_ANALYSIS: SectionAnalysis[] = [
  { sectionName: 'Header', status: 'excellent', score: 98, suggestion: 'Contact details, LinkedIn, and GitHub links are well presented.' },
  { sectionName: 'Summary', status: 'poor', score: 45, suggestion: 'Summary is too generic. Needs to highlight key tech stack and years of experience.' },
  { sectionName: 'Experience', status: 'good', score: 84, suggestion: 'Add more quantified accomplishments to your professional experience bullet points.' },
  { sectionName: 'Education', status: 'excellent', score: 95, suggestion: 'Degree and NIT Rourkela graduation details are clearly outlined.' },
  { sectionName: 'Projects', status: 'excellent', score: 92, suggestion: 'Excellent tech stack details and functional descriptions.' },
  { sectionName: 'Skills', status: 'excellent', score: 96, suggestion: 'Strong balance of technical skills, frameworks, and programming languages.' },
  { sectionName: 'Certifications', status: 'average', score: 70, suggestion: 'Consider adding cloud certificates (AWS Cloud Practitioner or Developer Associate).' },
  { sectionName: 'Achievements', status: 'good', score: 85, suggestion: 'Hackathon wins are listed, but could emphasize role in teams.' }
];

export const MOCK_FORMATTING_ANALYSIS: FormattingScore = {
  margins: 'Correct (1 inch standard)',
  font: 'ATS-Friendly (Inter, Arial)',
  spacing: 'Consistent (1.15 line spacing)',
  headings: 'Standard (Clear hierarchy)',
  bulletPoints: 'Correct (Uses standard bullet list items)',
  alignment: 'Left aligned (Best for parsing)',
  tables: 'None found (Excellent for ATS)',
  columns: 'Single column layout (ATS preferred)',
  icons: 'Few (Will not interfere with text extraction)',
  graphics: 'None (Excellent compatibility)',
  atsCompatibility: 'Highly compatible layout'
};

export const MOCK_GRAMMAR_ANALYSIS: GrammarScore = {
  score: 91,
  spellingErrors: 0,
  sentenceStructure: 'Excellent readability, active voice dominant.',
  readability: 'Professional (Grade 10 level)',
  actionVerbs: 18,
  repeatedWords: ['development', 'frontend', 'built'],
  passiveVoicePercentage: 8,
  suggestions: [
    'Replace repetitive use of "built" with dynamic verbs like "engineered", "orchestrated", or "deployed".',
    'Keep sentence length under 20 words for maximum impact.'
  ]
};

export const MOCK_SKILL_ANALYSIS: SkillAnalysis = {
  technical: ['React', 'TypeScript', 'Node.js', 'REST APIs', 'PostgreSQL', 'AWS', 'Docker', 'Git', 'Agile', 'CI/CD'],
  frameworks: ['React', 'Next.js', 'Express'],
  libraries: ['Redux Toolkit', 'Tailwind CSS', 'Framer Motion'],
  languages: ['JavaScript', 'TypeScript', 'SQL', 'HTML/CSS'],
  soft: ['Communication', 'Teamwork', 'Problem Solving', 'Agile Leadership'],
  tools: ['Git', 'Docker', 'PostgreSQL', 'VS Code', 'Jira'],
  missing: ['Kubernetes', 'Terraform', 'Redis', 'GraphQL Federation'],
  recommended: ['Kubernetes', 'GraphQL', 'AWS Lambda', 'Terraform'],
  trending: ['Next.js App Router', 'Tailwind CSS v4', 'React Server Components']
};

export const MOCK_EDUCATION_ANALYSIS: EducationAnalysis = {
  degree: 'Bachelor of Technology (B.Tech)',
  university: 'National Institute of Technology, Rourkela',
  cgpa: '8.7 / 10.0',
  relevantCoursework: ['Data Structures and Algorithms', 'Database Management Systems', 'Software Engineering', 'Web Development'],
  suggestions: [
    'List GPA scale explicitly (e.g., 8.7/10.0 or GPA of 3.68/4.0).'
  ]
};

export const MOCK_EXPERIENCE_ANALYSIS: ExperienceAnalysis = {
  years: 5,
  leadership: 'Led a team of 3 junior developers during migration tasks.',
  achievementsCount: 6,
  quantifiedResultsCount: 4,
  actionVerbsCount: 18,
  suggestions: [
    'Quantify results more precisely, e.g. "reduced bundle size by 40%" instead of "significantly improved performance".'
  ]
};

export const MOCK_PROJECT_ANALYSIS: ProjectAnalysis = {
  quality: 'Excellent',
  techStack: ['React', 'Next.js', 'Tailwind CSS', 'TypeScript'],
  complexity: 'high',
  hasGithub: true,
  hasLiveDemo: true,
  hasDocumentation: true,
  innovationScore: 88,
  suggestions: [
    'Add deployment links to all listed personal or open-source projects.'
  ]
};
