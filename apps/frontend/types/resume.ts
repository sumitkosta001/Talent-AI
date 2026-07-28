export interface CandidateResume {
  id: string;
  name: string;
  uploadDate: string;
  version: string;
  atsScore?: number;
  downloadUrl: string;
  lastUpdated: string;
  profileCompletion: number;
  resumeStatus: string;
  summary: string;
}

export interface ResumeAnalysis {
  overallScore: number;
  formattingScore: number;
  keywordCoverageScore: number;
  educationScore: number;
  experienceScore: number;
  projectScore: number;
  skillScore: number;
  strengths: string[];
  weaknesses: string[];
  suggestions: { priority: 'high' | 'medium' | 'low'; text: string }[];
  matchedKeywords: string[];
  missingKeywords: string[];
}

export interface ResumeHistory {
  id: string;
  name: string;
  size: string;
  date: string;
  status: 'Parsed' | 'Processing' | 'Failed' | 'Analyzed';
  score?: number;
}

export interface Skill {
  name: string;
  type: 'technical' | 'framework' | 'tool' | 'soft';
}

export interface Project {
  id?: string;
  name: string;
  description: string;
  techStack: string[];
  github?: string;
  liveLink?: string;
  duration?: string;
}

export interface Experience {
  id?: string;
  company: string;
  role: string;
  duration: string;
  description: string;
  technologies?: string[];
}

export interface Education {
  id?: string;
  university: string;
  degree: string;
  gpa: string;
  year: string;
  location: string;
}

export interface Certificate {
  id?: string;
  certificate: string;
  issuer: string;
  issueDate: string;
  credentialId?: string;
}

export interface Resume {
  candidateName: string;
  email: string;
  phone: string;
  location: string;
  website?: string;
  github?: string;
  linkedin?: string;
  summary: string;
  experience: Experience[];
  projects: Project[];
  education: Education[];
  certificates: Certificate[];
  skills: Skill[];
  languages: string[];
  achievements: string[];
}
