export interface ATSScore {
  overall: number;
  formatting: number;
  grammar: number;
  keywordMatch: number;
  projects: number;
  skills: number;
  experience: number;
  education: number;
}

export interface Keyword {
  name: string;
  matched: boolean;
  frequency: number;
  category: 'technical' | 'soft' | 'tool' | 'framework';
  importance: 'high' | 'medium' | 'low';
}

export interface SectionAnalysis {
  sectionName: string;
  status: 'excellent' | 'good' | 'average' | 'poor';
  score: number;
  suggestion: string;
}

export interface Suggestion {
  id: string;
  priority: 'high' | 'medium' | 'low';
  text: string;
  category: 'formatting' | 'keyword' | 'grammar' | 'content';
}

export interface Timeline {
  step: number;
  title: string;
  description: string;
  status: 'completed' | 'in-progress' | 'pending';
}

export interface ChartData {
  subject: string;
  score: number;
}

export interface FormattingScore {
  margins: string;
  font: string;
  spacing: string;
  headings: string;
  bulletPoints: string;
  alignment: string;
  tables: string;
  columns: string;
  icons: string;
  graphics: string;
  atsCompatibility: string;
}

export interface GrammarScore {
  score: number;
  spellingErrors: number;
  sentenceStructure: string;
  readability: string;
  actionVerbs: number;
  repeatedWords: string[];
  passiveVoicePercentage: number;
  suggestions: string[];
}

export interface SkillAnalysis {
  technical: string[];
  frameworks: string[];
  libraries: string[];
  languages: string[];
  soft: string[];
  tools: string[];
  missing: string[];
  recommended: string[];
  trending: string[];
}

export interface EducationAnalysis {
  degree: string;
  university: string;
  cgpa: string;
  relevantCoursework: string[];
  suggestions: string[];
}

export interface ExperienceAnalysis {
  years: number;
  leadership: string;
  achievementsCount: number;
  quantifiedResultsCount: number;
  actionVerbsCount: number;
  suggestions: string[];
}

export interface ProjectAnalysis {
  quality: string;
  techStack: string[];
  complexity: 'high' | 'medium' | 'low';
  hasGithub: boolean;
  hasLiveDemo: boolean;
  hasDocumentation: boolean;
  innovationScore: number;
  suggestions: string[];
}

export interface ATSResult {
  score: ATSScore;
  keywords: Keyword[];
  sections: SectionAnalysis[];
  suggestions: Suggestion[];
  timeline: Timeline[];
  formatting: FormattingScore;
  grammar: GrammarScore;
  skills: SkillAnalysis;
  education: EducationAnalysis;
  experience: ExperienceAnalysis;
  projects: ProjectAnalysis;
}
