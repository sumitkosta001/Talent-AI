/**
 * Phase 4 ML Service
 * TalentAI Recruitment Platform - Days 28-34 ML Pipeline Integration
 */

import { apiClient } from '@/lib/apiClient';
import {
  StructuredResume,
  ResumeClassification,
  JobRequirements,
  ATSScoreResponse,
  SimilarityMatchResponse,
  CandidateJobRecommendationRequest,
  JobRecommendationResponse,
  InterviewQuestionRequest,
  GeneratedInterviewQuestions,
  FAISSSearchResult,
} from '@/types/ml';

export class MLService {
  /**
   * Day 28: Retrieve canonical Day 28 structured JSON representation
   * GET /api/v1/candidates/me/resumes/{resume_id}/structured
   */
  static async getStructuredResume(resumeId: string): Promise<StructuredResume> {
    const res = await apiClient.get(`/api/v1/candidates/me/resumes/${resumeId}/structured`);
    if (!res.ok) {
      // Fallback check on resume metadata if direct structured endpoint is not available
      if (res.status === 404) {
        const metaRes = await apiClient.get(`/api/v1/candidates/me/resumes/${resumeId}`);
        if (metaRes.ok) {
          const metaData = await metaRes.json();
          if (metaData.structured_data) {
            return metaData.structured_data as StructuredResume;
          }
        }
      }
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to fetch structured resume');
    }
    return res.json();
  }

  /**
   * Day 29: Retrieve domain, role, and experience level classification
   * GET /api/v1/candidates/me/resumes/{resume_id}/classification
   */
  static async getClassification(resumeId: string): Promise<ResumeClassification> {
    const res = await apiClient.get(`/api/v1/candidates/me/resumes/${resumeId}/classification`);
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to fetch resume classification');
    }
    return res.json();
  }

  /**
   * Day 30: Calculate job-specific ATS score and explainable breakdown
   * POST /api/v1/candidates/me/resumes/{resume_id}/ats-score
   */
  static async calculateATSScore(
    resumeId: string,
    jobRequirements: JobRequirements
  ): Promise<ATSScoreResponse> {
    const res = await apiClient.post(
      `/api/v1/candidates/me/resumes/${resumeId}/ats-score`,
      jobRequirements
    );
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to calculate ATS score');
    }
    return res.json();
  }

  /**
   * Day 31: Calculate semantic embedding similarity score
   * POST /api/v1/candidates/me/resumes/{resume_id}/similarity-score
   */
  static async calculateSimilarityScore(
    resumeId: string,
    jobRequirements: JobRequirements
  ): Promise<SimilarityMatchResponse> {
    const res = await apiClient.post(
      `/api/v1/candidates/me/resumes/${resumeId}/similarity-score`,
      jobRequirements
    );
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to calculate similarity score');
    }
    return res.json();
  }

  /**
   * Day 32: FAISS vector similarity search for jobs matching candidate resume
   * POST /api/v1/candidates/me/resumes/{resume_id}/search-jobs?top_k=10
   */
  static async searchJobsFAISS(resumeId: string, topK: number = 10): Promise<FAISSSearchResult> {
    const res = await apiClient.post(
      `/api/v1/candidates/me/resumes/${resumeId}/search-jobs?top_k=${topK}`
    );
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'FAISS job search failed');
    }
    return res.json();
  }

  /**
   * Day 33: Get ranked, evidence-explained job recommendations for candidate resume
   * POST /api/v1/candidates/me/resumes/{resume_id}/recommendations/jobs?top_k=10
   */
  static async getJobRecommendations(
    resumeId: string,
    request?: CandidateJobRecommendationRequest,
    topK: number = 10
  ): Promise<JobRecommendationResponse> {
    const res = await apiClient.post(
      `/api/v1/candidates/me/resumes/${resumeId}/recommendations/jobs?top_k=${topK}`,
      request || {}
    );
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to fetch job recommendations');
    }
    return res.json();
  }

  /**
   * Day 34: Generate interview questions for candidate resume
   * POST /api/v1/candidates/me/resumes/{resume_id}/interview-questions
   */
  static async generateInterviewQuestions(
    resumeId: string,
    request?: InterviewQuestionRequest
  ): Promise<GeneratedInterviewQuestions> {
    const queryParams = new URLSearchParams();
    if (request?.count) queryParams.append('count', request.count.toString());
    if (request?.difficulty) queryParams.append('difficulty', request.difficulty);
    if (request?.categories && request.categories.length > 0) {
      request.categories.forEach((cat) => queryParams.append('categories', cat));
    }
    if (request?.provider) queryParams.append('provider', request.provider);

    const queryString = queryParams.toString();
    const endpoint = `/api/v1/candidates/me/resumes/${resumeId}/interview-questions${
      queryString ? `?${queryString}` : ''
    }`;

    const res = await apiClient.post(endpoint, {});
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData?.error?.message || errData?.detail || 'Failed to generate interview questions');
    }
    return res.json();
  }
}
