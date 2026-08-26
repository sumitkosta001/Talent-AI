"""Phase 4 — Day 33: Recommendation Engine Service.

Combines Day 32 FAISS vector semantic retrieval with Day 30 explicit ATS requirement matching
to provide transparent, evidence-based recommendations, deterministic ranking, and match explanations
for both Job Recommendations (candidates searching jobs) and Candidate Recommendations (recruiters searching candidates).
"""

import time
import logging
from typing import Optional, List, Dict, Any, Tuple, Union, Set, Sequence

from pydantic import BaseModel

from app.config.settings import settings
from app.exceptions.resume import ResumeParsingError
from app.services.resume_processing.models import (
    StructuredResume,
    JobRequirements,
    ATSScore,
    RecommendationExplanation,
    JobRecommendation,
    CandidateRecommendation,
    JobRecommendationResponse,
    CandidateRecommendationResponse,
    FAISSSearchResult,
)
from app.services.resume_processing.ats_scorer import (
    score_resume_against_job,
    HybridATSScorer,
    _is_empty_job_requirements,
)
from app.services.resume_processing.faiss_index_service import (
    search_jobs_for_resume,
    search_resumes_for_job,
    get_job_faiss_index,
    get_resume_faiss_index,
)
from app.services.resume_processing.similarity_matcher import calculate_resume_job_similarity
from app.services.resume_processing.embedding_service import (
    build_resume_embedding_text,
    build_job_embedding_text,
)

from app.services.resume_processing.skill_dictionary import ALIAS_MAP

logger = logging.getLogger("talentai.resume_processing.recommendation_engine")


def canonicalize_skill_name(term: str) -> str:
    """Helper to resolve skill term to canonical display name using Day 24 ALIAS_MAP."""
    if not term or not term.strip():
        return ""
    lowered = term.strip().lower()
    if lowered in ALIAS_MAP:
        entry = ALIAS_MAP[lowered]
        return entry[0] if isinstance(entry, (tuple, list)) else str(entry)
    return term.strip()


def calculate_recommendation_score(
    semantic_score: float,
    ats_score: float,
    semantic_weight: Optional[float] = None,
    ats_weight: Optional[float] = None,
) -> float:
    """Computes a normalized, clamped weighted recommendation score (0.0 - 100.0).

    Formula:
        recommendation_score = semantic_score * sem_w + ats_score * ats_w
    """
    sem_w = semantic_weight if semantic_weight is not None else getattr(settings.recommendation, "semantic_weight", 0.50)
    ats_w = ats_weight if ats_weight is not None else getattr(settings.recommendation, "ats_weight", 0.50)

    total_weight = sem_w + ats_w
    if total_weight <= 0:
        sem_w, ats_w = 0.50, 0.50
        total_weight = 1.0

    norm_sem_w = sem_w / total_weight
    norm_ats_w = ats_w / total_weight

    raw_score = (float(semantic_score) * norm_sem_w) + (float(ats_score) * norm_ats_w)
    clamped = max(0.0, min(100.0, raw_score))
    return round(clamped, 2)


def build_match_explanation(
    structured_resume: StructuredResume,
    job_requirements: JobRequirements,
    ats_score: ATSScore,
    semantic_score: float,
) -> RecommendationExplanation:
    """Generates a structured, evidence-based match explanation without LLM fabrication."""

    # 1. Canonical skill matching breakdown
    raw_matched_skills = getattr(ats_score, "matched_required_skills", []) + getattr(ats_score, "matched_preferred_skills", [])
    raw_missing_skills = getattr(ats_score, "missing_required_skills", []) + getattr(ats_score, "missing_preferred_skills", [])

    matched_skills = sorted(list({canonicalize_skill_name(s) for s in raw_matched_skills if s}))
    missing_skills = sorted(list({canonicalize_skill_name(s) for s in raw_missing_skills if s}))

    matched_keywords = getattr(ats_score, "matched_keywords", [])
    missing_keywords = getattr(ats_score, "missing_required_keywords", []) + getattr(ats_score, "missing_preferred_keywords", [])

    # 2. Extract strengths from evidence
    strengths: List[str] = []
    if semantic_score >= 60.0:
        strengths.append(f"Strong semantic context match ({round(semantic_score, 1)}/100)")
    elif semantic_score >= 40.0:
        strengths.append(f"Moderate semantic relevance ({round(semantic_score, 1)}/100)")

    if matched_skills:
        strengths.append(f"Matched key required skills: {', '.join(matched_skills[:5])}")

    if ats_score.education_score >= 80.0:
        strengths.append("Education requirements are well-satisfied")

    exp_details = getattr(ats_score, "experience_match", {})
    cand_exp_m = exp_details.get("candidate_experience_months", 0)
    req_exp_m = exp_details.get("required_experience_months")
    if req_exp_m and cand_exp_m >= req_exp_m:
        strengths.append(f"Experience duration requirement met ({cand_exp_m} months vs {req_exp_m} required)")

    # 3. Extract role/domain compatibility evidence (Day 29)
    role_domain_comp: Optional[str] = None
    if structured_resume.classification and job_requirements:
        cand_domain = structured_resume.classification.domain
        cand_role = structured_resume.classification.role
        job_domains = getattr(job_requirements, "required_domains", []) + getattr(job_requirements, "preferred_domains", [])
        job_roles = getattr(job_requirements, "required_roles", []) + getattr(job_requirements, "preferred_roles", [])

        domain_match = cand_domain in job_domains if (cand_domain and job_domains) else False
        role_match = cand_role in job_roles if (cand_role and job_roles) else False

        if domain_match or role_match:
            parts = []
            if domain_match:
                parts.append(f"Domain alignment ({cand_domain})")
            if role_match:
                parts.append(f"Role alignment ({cand_role})")
            role_domain_comp = " and ".join(parts)
            strengths.append(f"Compatible candidate classification: {role_domain_comp}")

    # 4. Extract gaps from evidence
    gaps: List[str] = []
    if missing_skills:
        gaps.append(f"Missing required skills: {', '.join(missing_skills[:5])}")
    if missing_keywords:
        gaps.append(f"Missing keywords: {', '.join(missing_keywords[:5])}")
    if req_exp_m and cand_exp_m < req_exp_m:
        gaps.append(f"Experience gap ({cand_exp_m} months vs {req_exp_m} required)")
    if ats_score.education_score < 50.0 and getattr(ats_score, "missing_education", []):
        gaps.append(f"Education gaps: {', '.join(ats_score.missing_education)}")

    # 5. Build summary sentence based on recommendation score
    rec_score = calculate_recommendation_score(semantic_score, ats_score.score)
    job_title = job_requirements.title or "Target Role"

    if rec_score >= 75.0:
        skills_phrase = f" with strong skills in {', '.join(matched_skills[:3])}" if matched_skills else ""
        summary = f"Strong recommendation for {job_title}{skills_phrase}. High alignment across semantic context and explicit requirements."
    elif rec_score >= 50.0:
        gaps_phrase = f" but missing {', '.join(missing_skills[:2])}" if missing_skills else ""
        summary = f"Moderate recommendation for {job_title}. Candidate meets core qualifications{gaps_phrase}."
    else:
        summary = f"Low suitability for {job_title}. Significant gaps in key skills or required experience."

    return RecommendationExplanation(
        summary=summary,
        strengths=strengths,
        gaps=gaps,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        matched_keywords=matched_keywords,
        missing_keywords=missing_keywords,
        role_domain_compatibility=role_domain_comp,
        metadata={
            "ats_score": ats_score.score,
            "semantic_score": round(semantic_score, 2),
        },
    )


class RecommendationEngine:
    """Production Hybrid Recommendation Engine combining FAISS Vector Retrieval & Day 30 ATS Scoring."""

    def __init__(
        self,
        semantic_weight: Optional[float] = None,
        ats_weight: Optional[float] = None,
    ):
        self.semantic_weight = semantic_weight if semantic_weight is not None else getattr(settings.recommendation, "semantic_weight", 0.50)
        self.ats_weight = ats_weight if ats_weight is not None else getattr(settings.recommendation, "ats_weight", 0.50)

    def recommend_jobs_for_resume(
        self,
        structured_resume: Union[StructuredResume, Dict[str, Any]],
        candidate_jobs: Optional[Sequence[Union[JobRequirements, Dict[str, Any]]]] = None,
        top_k: int = 10,
    ) -> JobRecommendationResponse:
        """Recommends top-k best suited jobs for a candidate resume."""
        start_time = time.perf_counter()

        max_k = getattr(settings.recommendation, "max_top_k", 50)
        if top_k is None or not isinstance(top_k, int) or top_k <= 0:
            raise ValueError(f"top_k must be a positive integer > 0, received {top_k}.")
        top_k = min(top_k, max_k)

        if structured_resume is None:
            raise ResumeParsingError("structured_resume cannot be None.")

        if isinstance(structured_resume, dict):
            structured_resume = StructuredResume.model_validate(structured_resume)

        resume_id = str(structured_resume.resume_id) if structured_resume.resume_id else "anonymous_candidate"

        # Step 1: Retrieval Pool Assembly
        pool_factor = getattr(settings.recommendation, "pool_factor", 3)
        retrieval_k = min(top_k * pool_factor, 100)

        faiss_search_results: Dict[str, float] = {}  # job_id -> semantic_similarity_score
        faiss_job_meta: Dict[str, Dict[str, Any]] = {}

        try:
            faiss_res: FAISSSearchResult = search_jobs_for_resume(structured_resume, top_k=retrieval_k)
            for item in faiss_res.results:
                faiss_search_results[item.entity_id] = item.similarity_score
                faiss_job_meta[item.entity_id] = item.metadata
        except Exception as e:
            logger.warning("FAISS vector retrieval produced empty or exception result: %s", str(e))

        # Build combined job requirements pool
        job_pool_dict: Dict[str, JobRequirements] = {}

        # Add explicit candidate_jobs if supplied
        if candidate_jobs:
            for c_job in candidate_jobs:
                if isinstance(c_job, dict):
                    c_job = JobRequirements.model_validate(c_job)
                if c_job and c_job.job_id:
                    job_pool_dict[str(c_job.job_id)] = c_job

        # Add jobs found in FAISS search metadata if not present
        for j_id, meta in faiss_job_meta.items():
            if j_id not in job_pool_dict:
                title = meta.get("title", "Job Title")
                req_sk = meta.get("required_skills", [])
                req_dom = meta.get("required_domains", [])
                job_pool_dict[j_id] = JobRequirements(
                    job_id=j_id,
                    title=title,
                    required_skills=req_sk,
                    required_domains=req_dom,
                )

        if not job_pool_dict:
            return JobRecommendationResponse(
                resume_id=resume_id,
                recommendations=[],
                total_results=0,
                top_k=top_k,
                execution_time_ms=round((time.perf_counter() - start_time) * 1000, 2),
                metadata={"status": "empty_job_pool"},
            )

        # Step 2: Scoring & Reranking
        recommendations: List[JobRecommendation] = []

        for j_id, job_req in job_pool_dict.items():
            # Get ATS score
            try:
                ats_result: ATSScore = score_resume_against_job(structured_resume, job_req)
            except Exception as ats_err:
                logger.debug("ATS scoring skipped for job '%s': %s", j_id, str(ats_err))
                ats_result = ATSScore(score=50.0, explanation="Default baseline ATS score.")

            # Get Semantic score (from FAISS or fallback Day 31 direct semantic similarity)
            if j_id in faiss_search_results:
                sem_score = faiss_search_results[j_id]
            else:
                try:
                    sim_match = calculate_resume_job_similarity(structured_resume, job_req)
                    sem_score = sim_match.similarity_score
                except Exception:
                    sem_score = 50.0


            # Compute combined recommendation score
            rec_score = calculate_recommendation_score(
                sem_score, ats_result.score, self.semantic_weight, self.ats_weight
            )

            # Generate match explanation
            explanation = build_match_explanation(structured_resume, job_req, ats_result, sem_score)
            confidence = round(min(1.0, max(0.1, (rec_score / 100.0) * 0.9 + 0.1)), 2)

            rec_item = JobRecommendation(
                job_id=j_id,
                title=job_req.title or f"Job {j_id}",
                company=job_req.metadata.get("company"),
                recommendation_score=rec_score,
                semantic_similarity_score=round(sem_score, 2),
                ats_score=round(ats_result.score, 2),
                skill_match_score=round(ats_result.skill_score, 2),
                education_match_score=round(ats_result.education_score, 2),
                experience_match_score=round(ats_result.experience_score, 2),
                matched_skills=explanation.matched_skills,
                missing_skills=explanation.missing_skills,
                matched_keywords=explanation.matched_keywords,
                missing_keywords=explanation.missing_keywords,
                explanation=explanation,
                confidence=confidence,
                metadata={"job_title": job_req.title},
            )
            recommendations.append(rec_item)

        # Step 3: Deterministic Sorting & Tie-Breaking
        # Primary: recommendation_score DESC, Tie-breaker 1: ats_score DESC, Tie-breaker 2: semantic_similarity_score DESC, Tie-breaker 3: job_id ASC
        recommendations.sort(
            key=lambda x: (
                x.recommendation_score,
                x.ats_score,
                x.semantic_similarity_score,
                -ord(x.job_id[0]) if x.job_id else 0,
            ),
            reverse=True,
        )

        # Step 4: Deduplicate and assign ranking positions
        seen_job_ids: Set[str] = set()
        deduped_recs: List[JobRecommendation] = []
        rank_pos = 1

        for r in recommendations:
            if r.job_id not in seen_job_ids:
                seen_job_ids.add(r.job_id)
                r.ranking_position = rank_pos
                rank_pos += 1
                deduped_recs.append(r)

        final_recs = deduped_recs[:top_k]
        exec_ms = round((time.perf_counter() - start_time) * 1000, 2)

        return JobRecommendationResponse(
            resume_id=resume_id,
            recommendations=final_recs,
            total_results=len(final_recs),
            top_k=top_k,
            execution_time_ms=exec_ms,
            metadata={
                "candidate_pool_size": len(job_pool_dict),
                "semantic_weight": self.semantic_weight,
                "ats_weight": self.ats_weight,
            },
        )

    def recommend_candidates_for_job(
        self,
        job_requirements: Union[JobRequirements, Dict[str, Any]],
        candidate_resumes: Optional[Sequence[Union[StructuredResume, Dict[str, Any]]]] = None,
        top_k: int = 10,
        self_resume_id: Optional[str] = None,
    ) -> CandidateRecommendationResponse:
        """Recommends top-k best suited candidate resumes for job requirements."""
        start_time = time.perf_counter()

        max_k = getattr(settings.recommendation, "max_top_k", 50)
        if top_k is None or not isinstance(top_k, int) or top_k <= 0:
            raise ValueError(f"top_k must be a positive integer > 0, received {top_k}.")
        top_k = min(top_k, max_k)

        if job_requirements is None:
            raise ValueError("job_requirements cannot be None.")

        if isinstance(job_requirements, dict):
            job_requirements = JobRequirements.model_validate(job_requirements)

        job_id = str(job_requirements.job_id) if job_requirements.job_id else "anonymous_job"

        # Step 1: Retrieval Pool Assembly
        pool_factor = getattr(settings.recommendation, "pool_factor", 3)
        retrieval_k = min(top_k * pool_factor, 100)

        faiss_search_results: Dict[str, float] = {}  # resume_id -> semantic_similarity_score
        faiss_cand_meta: Dict[str, Dict[str, Any]] = {}

        try:
            faiss_res: FAISSSearchResult = search_resumes_for_job(job_requirements, top_k=retrieval_k)
            for item in faiss_res.results:
                faiss_search_results[item.entity_id] = item.similarity_score
                faiss_cand_meta[item.entity_id] = item.metadata
        except Exception as e:
            logger.warning("FAISS vector retrieval produced empty or exception result: %s", str(e))

        # Build combined candidate resume pool
        resume_pool_dict: Dict[str, StructuredResume] = {}

        # Add explicit candidate_resumes if supplied
        if candidate_resumes:
            for c_res in candidate_resumes:
                if isinstance(c_res, dict):
                    c_res = StructuredResume.model_validate(c_res)
                if c_res and c_res.resume_id:
                    resume_pool_dict[str(c_res.resume_id)] = c_res

        # Add resumes found in FAISS search metadata if not present
        for r_id, meta in faiss_cand_meta.items():
            if r_id not in resume_pool_dict:
                full_name = meta.get("full_name")
                email = meta.get("email")
                resume_pool_dict[r_id] = StructuredResume(
                    resume_id=r_id,
                    full_name=full_name,
                    email=email,
                )

        # Step 2: Self-Match Prevention & Filtering
        if self_resume_id and str(self_resume_id) in resume_pool_dict:
            resume_pool_dict.pop(str(self_resume_id), None)

        if not resume_pool_dict:
            return CandidateRecommendationResponse(
                job_id=job_id,
                recommendations=[],
                total_results=0,
                top_k=top_k,
                execution_time_ms=round((time.perf_counter() - start_time) * 1000, 2),
                metadata={"status": "empty_candidate_pool"},
            )

        # Step 3: Scoring & Reranking
        recommendations: List[CandidateRecommendation] = []

        for r_id, s_resume in resume_pool_dict.items():
            # Get ATS score
            try:
                ats_result: ATSScore = score_resume_against_job(s_resume, job_requirements)
            except Exception as ats_err:
                logger.debug("ATS scoring skipped for candidate resume '%s': %s", r_id, str(ats_err))
                ats_result = ATSScore(score=50.0, explanation="Default baseline ATS score.")

            # Get Semantic score (from FAISS or fallback Day 31 direct semantic similarity)
            if r_id in faiss_search_results:
                sem_score = faiss_search_results[r_id]
            else:
                try:
                    sim_match = calculate_resume_job_similarity(s_resume, job_requirements)
                    sem_score = sim_match.similarity_score
                except Exception:
                    sem_score = 50.0


            # Compute combined recommendation score
            rec_score = calculate_recommendation_score(
                sem_score, ats_result.score, self.semantic_weight, self.ats_weight
            )

            # Generate match explanation
            explanation = build_match_explanation(s_resume, job_requirements, ats_result, sem_score)
            confidence = round(min(1.0, max(0.1, (rec_score / 100.0) * 0.9 + 0.1)), 2)

            rec_item = CandidateRecommendation(
                candidate_id=str(s_resume.candidate_profile_id) if s_resume.candidate_profile_id else None,
                resume_id=r_id,
                full_name=s_resume.full_name or f"Candidate {r_id[:8]}",
                recommendation_score=rec_score,
                semantic_similarity_score=round(sem_score, 2),
                ats_score=round(ats_result.score, 2),
                skill_match_score=round(ats_result.skill_score, 2),
                education_match_score=round(ats_result.education_score, 2),
                experience_match_score=round(ats_result.experience_score, 2),
                matched_skills=explanation.matched_skills,
                missing_skills=explanation.missing_skills,
                matched_keywords=explanation.matched_keywords,
                missing_keywords=explanation.missing_keywords,
                explanation=explanation,
                confidence=confidence,
                metadata={"full_name": s_resume.full_name},
            )
            recommendations.append(rec_item)

        # Step 4: Deterministic Sorting & Tie-Breaking
        recommendations.sort(
            key=lambda x: (
                x.recommendation_score,
                x.ats_score,
                x.semantic_similarity_score,
                -ord(x.resume_id[0]) if x.resume_id else 0,
            ),
            reverse=True,
        )

        # Step 5: Deduplicate and assign ranking positions
        seen_resume_ids: Set[str] = set()
        deduped_recs: List[CandidateRecommendation] = []
        rank_pos = 1

        for r in recommendations:
            if r.resume_id not in seen_resume_ids:
                seen_resume_ids.add(r.resume_id)
                r.ranking_position = rank_pos
                rank_pos += 1
                deduped_recs.append(r)

        final_recs = deduped_recs[:top_k]
        exec_ms = round((time.perf_counter() - start_time) * 1000, 2)

        return CandidateRecommendationResponse(
            job_id=job_id,
            recommendations=final_recs,
            total_results=len(final_recs),
            top_k=top_k,
            execution_time_ms=exec_ms,
            metadata={
                "candidate_pool_size": len(resume_pool_dict),
                "semantic_weight": self.semantic_weight,
                "ats_weight": self.ats_weight,
            },
        )


# High-level module helper functions

def recommend_jobs_for_resume(
    structured_resume: Union[StructuredResume, Dict[str, Any]],
    candidate_jobs: Optional[Sequence[Union[JobRequirements, Dict[str, Any]]]] = None,
    top_k: int = 10,
    semantic_weight: Optional[float] = None,
    ats_weight: Optional[float] = None,
) -> JobRecommendationResponse:
    """Public helper function to generate job recommendations for a structured resume."""
    engine = RecommendationEngine(semantic_weight=semantic_weight, ats_weight=ats_weight)
    return engine.recommend_jobs_for_resume(structured_resume, candidate_jobs=candidate_jobs, top_k=top_k)


def recommend_candidates_for_job(
    job_requirements: Union[JobRequirements, Dict[str, Any]],
    candidate_resumes: Optional[Sequence[Union[StructuredResume, Dict[str, Any]]]] = None,
    top_k: int = 10,
    self_resume_id: Optional[str] = None,
    semantic_weight: Optional[float] = None,
    ats_weight: Optional[float] = None,
) -> CandidateRecommendationResponse:
    """Public helper function to generate candidate recommendations for job requirements."""
    engine = RecommendationEngine(semantic_weight=semantic_weight, ats_weight=ats_weight)
    return engine.recommend_candidates_for_job(
        job_requirements,
        candidate_resumes=candidate_resumes,
        top_k=top_k,
        self_resume_id=self_resume_id,
    )
