/**
 * Phase 4 ML API TypeScript Types & Schemas
 * TalentAI Recruitment Platform - Days 28-34 ML Pipeline Integration
 */

// ==============================================================================
// DAY 28 STRUCTURED RESUME & DAY 29 CLASSIFICATION TYPES
// ==============================================================================

export interface ExtractedSkill {
  name: string;
  normalized_name: string;
  category: string;
  source: string;
  confidence: number;
  matched_text: string;
  sections: string[];
  mentions_count: number;
}

export interface ExtractedSkills {
  skills: ExtractedSkill[];
  total_count: number;
  categories: Record<string, string[]>;
  metadata?: Record<string, unknown>;
}

export interface EducationRecord {
  degree?: string | null;
  normalized_degree?: string | null;
  degree_level?: string | null;
  field_of_study?: string | null;
  institution?: string | null;
  normalized_institution?: string | null;
  start_year?: number | null;
  end_year?: number | null;
  graduation_year?: number | null;
  graduation_status?: string | null;
  cgpa?: number | null;
  percentage?: number | null;
  score_type?: string | null;
  source_text?: string;
  section?: string;
  source?: string;
  confidence?: number;
}

export interface ExtractedEducation {
  education_records: EducationRecord[];
  total_count: number;
  metadata?: Record<string, unknown>;
}

export interface ExperienceRecord {
  company?: string | null;
  normalized_company?: string | null;
  job_title?: string | null;
  normalized_job_title?: string | null;
  employment_type?: string | null;
  start_date?: string | null;
  end_date?: string | null;
  start_year?: number | null;
  start_month?: number | null;
  end_year?: number | null;
  end_month?: number | null;
  duration_months?: number | null;
  duration_text?: string | null;
  is_current?: boolean | null;
  responsibilities: string[];
  seniority?: string | null;
  location?: string | null;
  source_text?: string;
  section?: string;
  source?: string;
  confidence?: number;
}

export interface ExtractedExperience {
  experiences: ExperienceRecord[];
  total_count: number;
  total_experience_months?: number | null;
  metadata?: Record<string, unknown>;
}

export interface ProjectRecord {
  name?: string | null;
  normalized_name?: string | null;
  technologies: string[];
  normalized_technologies: string[];
  description: string;
  project_type?: string | null;
  classification?: string | null;
  start_year?: number | null;
  end_year?: number | null;
  project_url?: string | null;
  github_url?: string | null;
  source_text?: string;
  section?: string;
  source?: string;
  confidence?: number;
}

export interface ExtractedProjects {
  projects: ProjectRecord[];
  total_count: number;
  classifications: Record<string, string[]>;
  metadata?: Record<string, unknown>;
}

export interface ResumeClassification {
  domain: string;
  domain_confidence: number;
  role: string;
  role_confidence: number;
  experience_level: string;
  experience_level_confidence: number;
  domain_scores: Record<string, number>;
  role_scores: Record<string, number>;
  evidence: Record<string, string[]>;
  classifier_version: string;
  classification_method: string;
  metadata?: Record<string, unknown>;
}

export interface StructuredResume {
  schema_version: string;
  pipeline_version: string;
  resume_id?: string | null;
  candidate_profile_id?: string | null;
  full_name?: string | null;
  email?: string | null;
  phone?: string | null;
  location?: string | null;
  linkedin?: string | null;
  github?: string | null;
  portfolio?: string | null;
  summary?: string | null;
  skills: ExtractedSkills;
  education: ExtractedEducation;
  experience: ExtractedExperience;
  projects: ExtractedProjects;
  classification?: ResumeClassification | null;
  certifications?: unknown[];
  languages?: unknown[];
  achievements?: unknown[];
  metadata?: Record<string, unknown>;
}

// ==============================================================================
// DAY 30 ATS SCORING TYPES
// ==============================================================================

export interface JobRequirements {
  job_id?: string | null;
  title?: string | null;
  description?: string | null;
  required_keywords?: string[];
  preferred_keywords?: string[];
  required_skills?: string[];
  preferred_skills?: string[];
  required_education?: string[];
  preferred_education?: string[];
  required_experience_months?: number | null;
  preferred_experience_months?: number | null;
  required_roles?: string[];
  preferred_roles?: string[];
  required_domains?: string[];
  preferred_domains?: string[];
  required_experience_level?: string | null;
  metadata?: Record<string, unknown>;
}

export interface ATSScoreResponse {
  score: number;
  keyword_score: number;
  skill_score: number;
  education_score: number;
  experience_score: number;
  matched_keywords: string[];
  missing_required_keywords: string[];
  missing_preferred_keywords: string[];
  matched_required_skills: string[];
  missing_required_skills: string[];
  matched_preferred_skills: string[];
  missing_preferred_skills: string[];
  matched_education: string[];
  missing_education: string[];
  experience_match: Record<string, unknown>;
  score_breakdown: Record<string, Record<string, unknown>>;
  explanation: string;
  recommendations: string[];
  scorer_version: string;
  scoring_method: string;
  metadata?: Record<string, unknown>;
}

// ==============================================================================
// DAY 31 SIMILARITY MATCHING TYPES
// ==============================================================================

export interface SimilarityMatchResponse {
  resume_id?: string | null;
  job_id?: string | null;
  raw_cosine_similarity: number;
  similarity_score: number;
  model_name: string;
  embedding_dimension: number;
  resume_text_length: number;
  job_text_length: number;
  similarity_tier: string;
  metadata?: Record<string, unknown>;
}

// ==============================================================================
// DAY 32 FAISS SEARCH TYPES
// ==============================================================================

export interface FAISSSearchItem {
  entity_id: string;
  raw_similarity: number;
  similarity_score: number;
  similarity_tier: string;
  metadata?: Record<string, unknown>;
}

export interface FAISSSearchResult {
  query_type: string;
  total_results: number;
  top_k: number;
  results: FAISSSearchItem[];
  execution_time_ms: number;
  metadata?: Record<string, unknown>;
}

// ==============================================================================
// DAY 33 JOB RECOMMENDATION TYPES
// ==============================================================================

export interface CandidateJobRecommendationRequest {
  jobs?: JobRequirements[] | null;
}

export interface RecommendationExplanation {
  summary: string;
  strengths: string[];
  gaps: string[];
  matched_skills: string[];
  missing_skills: string[];
  matched_keywords: string[];
  missing_keywords: string[];
  role_domain_compatibility?: string | null;
  metadata?: Record<string, unknown>;
}

export interface JobRecommendation {
  job_id: string;
  title?: string | null;
  company?: string | null;
  recommendation_score: number;
  semantic_similarity_score: number;
  ats_score: number;
  skill_match_score: number;
  education_match_score: number;
  experience_match_score: number;
  matched_skills: string[];
  missing_skills: string[];
  matched_keywords: string[];
  missing_keywords: string[];
  ranking_position: number;
  explanation: RecommendationExplanation;
  confidence: number;
  metadata?: Record<string, unknown>;
}

export interface JobRecommendationResponse {
  resume_id?: string | null;
  recommendations: JobRecommendation[];
  total_results: number;
  top_k: number;
  ranking_method: string;
  scoring_version: string;
  execution_time_ms: number;
  metadata?: Record<string, unknown>;
}

// ==============================================================================
// DAY 34 INTERVIEW QUESTION TYPES
// ==============================================================================

export type QuestionCategory =
  | 'TECHNICAL'
  | 'BEHAVIORAL'
  | 'SITUATIONAL'
  | 'ROLE_SPECIFIC'
  | 'SYSTEM_DESIGN'
  | 'PROBLEM_SOLVING'
  | 'CODING'
  | 'PROJECT_BASED'
  | 'EXPERIENCE_BASED'
  | 'GENERAL';

export type QuestionDifficulty = 'EASY' | 'MEDIUM' | 'HARD' | 'EXPERT';

export interface InterviewQuestion {
  id: string;
  question: string;
  category: QuestionCategory;
  difficulty: QuestionDifficulty;
  question_type: string;
  target_role?: string | null;
  target_skill?: string | null;
  rationale?: string | null;
  source: string;
  confidence: number;
  metadata?: Record<string, unknown>;
}

export interface GeneratedInterviewQuestions {
  resume_id?: string | null;
  questions: InterviewQuestion[];
  total_count: number;
  role?: string | null;
  domain?: string | null;
  experience_level?: string | null;
  skills_used: string[];
  categories: QuestionCategory[];
  difficulty: QuestionDifficulty;
  provider: string;
  execution_time_ms: number;
  metadata?: Record<string, unknown>;
}

export interface InterviewQuestionRequest {
  count?: number;
  difficulty?: QuestionDifficulty;
  categories?: QuestionCategory[];
  provider?: string;
}
