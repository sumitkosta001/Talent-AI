export type ResumeStatus = 'uploaded' | 'processing' | 'processed' | 'failed';

export interface BackendResume {
  id: string;
  candidate_profile_id: string;
  original_filename: string;
  mime_type: string;
  file_extension: string;
  file_size_bytes: number;
  status: ResumeStatus;
  version: number;
  is_current: boolean;
  storage_provider?: string | null;
  bucket_name?: string | null;
  object_key?: string | null;
  uploaded_at: string;
  processing_started_at?: string | null;
  processing_completed_at?: string | null;
  failure_reason?: string | null;
  created_at: string;
}

export interface PaginatedResumeResponse {
  items: BackendResume[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  has_next: boolean;
  has_previous: boolean;
}

export interface ResumeProcessingResponse {
  success: boolean;
  message: string;
  resume: BackendResume;
}

export interface ResumeRestoreResponse {
  success: boolean;
  message: string;
  resume: BackendResume;
}

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
