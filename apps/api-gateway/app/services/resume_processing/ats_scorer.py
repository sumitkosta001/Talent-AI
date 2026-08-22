"""Phase 4 Day 30 — ATS Scoring Engine.

Implements an explainable, job-specific ATS scoring engine evaluating
StructuredResume (Day 28) and ResumeClassification (Day 29) against JobRequirements.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Set, Tuple, Any
import re
import math
import logging
import time

from app.exceptions.resume import ResumeParsingError
from .models import StructuredResume, JobRequirements, ATSScore, ExtractedSkill
from .skill_dictionary import ALIAS_MAP, SKILL_DICTIONARY
from .education_normalizer import normalize_degree
from .ats_taxonomy import (
    ATS_KEYWORD_WEIGHT,
    ATS_SKILL_WEIGHT,
    ATS_EDUCATION_WEIGHT,
    ATS_EXPERIENCE_WEIGHT,
    REQUIRED_SKILL_WEIGHT,
    PREFERRED_SKILL_WEIGHT,
    REQUIRED_KEYWORD_WEIGHT,
    PREFERRED_KEYWORD_WEIGHT,
    REQUIRED_EDUCATION_WEIGHT,
    PREFERRED_EDUCATION_WEIGHT,
    EXP_DURATION_WEIGHT,
    EXP_ROLE_WEIGHT,
    EXP_DOMAIN_WEIGHT,
    EXP_SENIORITY_WEIGHT,
    SCORER_VERSION,
    SCORING_METHOD,
    DEGREE_LEVEL_RANKS,
    ROLE_COMPATIBILITY_MAP,
)

logger = logging.getLogger("talentai.resume_processing.ats_scorer")


def _is_empty_job_requirements(job: JobRequirements) -> bool:
    """Check if a JobRequirements object has no actionable scoring criteria."""
    if not job:
        return True
    has_keywords = bool(job.required_keywords or job.preferred_keywords)
    has_skills = bool(job.required_skills or job.preferred_skills)
    has_edu = bool(job.required_education or job.preferred_education)
    has_exp = bool(
        job.required_experience_months is not None
        or job.preferred_experience_months is not None
        or job.required_roles
        or job.preferred_roles
        or job.required_domains
        or job.preferred_domains
        or job.required_experience_level
    )
    return not (has_keywords or has_skills or has_edu or has_exp)


class BaseATSScorer(ABC):
    """Abstract base class for ATS scoring engines."""

    @abstractmethod
    def score(
        self, structured_resume: StructuredResume, job_requirements: JobRequirements
    ) -> ATSScore:
        """Calculate job-specific ATS score for a StructuredResume."""
        pass


class HybridATSScorer(BaseATSScorer):
    """Production deterministic, weighted hybrid ATS scoring engine."""

    def _normalize_skill_term(self, term: str) -> str:
        """Normalize a skill term to canonical form using Day 24 ALIAS_MAP."""
        if not term or not term.strip():
            return ""
        lowered = term.strip().lower()
        if lowered in ALIAS_MAP:
            entry = ALIAS_MAP[lowered]
            return entry[0] if isinstance(entry, (tuple, list)) else str(entry)
        return term.strip()

    def _build_resume_text_corpus(self, resume: StructuredResume) -> str:
        """Consolidate full resume text fields into a normalized corpus for keyword searching."""
        corpus_parts: List[str] = []

        if resume.summary:
            corpus_parts.append(resume.summary)

        if resume.skills and resume.skills.skills:
            for s in resume.skills.skills:
                corpus_parts.append(s.name)
                if s.matched_text:
                    corpus_parts.append(s.matched_text)

        if resume.experience and resume.experience.experiences:
            for exp in resume.experience.experiences:
                if exp.job_title:
                    corpus_parts.append(exp.job_title)
                if exp.company:
                    corpus_parts.append(exp.company)
                if exp.responsibilities:
                    corpus_parts.extend(exp.responsibilities)

        if resume.projects and resume.projects.projects:
            for proj in resume.projects.projects:
                if proj.name:
                    corpus_parts.append(proj.name)
                if proj.description:
                    corpus_parts.append(proj.description)
                if proj.technologies:
                    corpus_parts.extend(proj.technologies)

        if resume.education and resume.education.education_records:
            for edu in resume.education.education_records:
                if edu.degree:
                    corpus_parts.append(edu.degree)
                if edu.field_of_study:
                    corpus_parts.append(edu.field_of_study)
                if edu.institution:
                    corpus_parts.append(edu.institution)

        return " ".join(corpus_parts)

    def _match_keyword_in_corpus(self, keyword: str, corpus: str) -> bool:
        """Check if keyword exists in corpus using exact token boundaries."""
        if not keyword or not keyword.strip():
            return False

        clean_kw = keyword.strip()
        
        # Special character handling (C++, C#, .NET, Node.js, React.js)
        if any(c in clean_kw for c in ["+", "#", ".", "-", "/"]):
            escaped = re.escape(clean_kw)
            pattern = rf"(?:\b|(?<=\s)){escaped}(?:\b|(?=\s))"
            return bool(re.search(pattern, corpus, re.IGNORECASE))
        else:
            pattern = rf"\b{re.escape(clean_kw)}\b"
            return bool(re.search(pattern, corpus, re.IGNORECASE))

    def match_keywords(
        self, resume: StructuredResume, job: JobRequirements
    ) -> Tuple[float, List[str], List[str], List[str]]:
        """Evaluate keyword matching against resume corpus."""
        req_kw = [k.strip() for k in job.required_keywords if k and k.strip()]
        pref_kw = [k.strip() for k in job.preferred_keywords if k and k.strip()]

        if not req_kw and not pref_kw:
            return 100.0, [], [], []

        corpus = self._build_resume_text_corpus(resume)

        matched_req: List[str] = []
        missing_req: List[str] = []
        for kw in req_kw:
            if self._match_keyword_in_corpus(kw, corpus):
                matched_req.append(kw)
            else:
                missing_req.append(kw)

        matched_pref: List[str] = []
        missing_pref: List[str] = []
        for kw in pref_kw:
            if self._match_keyword_in_corpus(kw, corpus):
                matched_pref.append(kw)
            else:
                missing_pref.append(kw)

        req_score = (len(matched_req) / len(req_kw) * 100.0) if req_kw else 100.0
        pref_score = (len(matched_pref) / len(pref_kw) * 100.0) if pref_kw else 100.0

        if req_kw and pref_kw:
            score = (req_score * REQUIRED_KEYWORD_WEIGHT) + (pref_score * PREFERRED_KEYWORD_WEIGHT)
        elif req_kw:
            score = req_score
        else:
            score = pref_score

        all_matched = sorted(list(set(matched_req + matched_pref)))
        return round(score, 2), all_matched, missing_req, missing_pref

    def match_skills(
        self, resume: StructuredResume, job: JobRequirements
    ) -> Tuple[float, List[str], List[str], List[str], List[str]]:
        """Evaluate skill matching using Day 24 canonical skill normalization."""
        req_skills_raw = [s.strip() for s in job.required_skills if s and s.strip()]
        pref_skills_raw = [s.strip() for s in job.preferred_skills if s and s.strip()]

        if not req_skills_raw and not pref_skills_raw:
            return 100.0, [], [], [], []

        candidate_skills_canonical: Set[str] = set()
        if resume.skills and resume.skills.skills:
            for s in resume.skills.skills:
                canon = self._normalize_skill_term(s.normalized_name or s.name)
                if canon:
                    candidate_skills_canonical.add(canon.lower())

        # Also check project technologies
        if resume.projects and resume.projects.projects:
            for p in resume.projects.projects:
                for tech in (p.technologies or []):
                    canon = self._normalize_skill_term(tech)
                    if canon:
                        candidate_skills_canonical.add(canon.lower())

        matched_req: List[str] = []
        missing_req: List[str] = []
        for s_raw in req_skills_raw:
            canon = self._normalize_skill_term(s_raw).lower()
            if canon in candidate_skills_canonical:
                matched_req.append(s_raw)
            else:
                missing_req.append(s_raw)

        matched_pref: List[str] = []
        missing_pref: List[str] = []
        for s_raw in pref_skills_raw:
            canon = self._normalize_skill_term(s_raw).lower()
            if canon in candidate_skills_canonical:
                matched_pref.append(s_raw)
            else:
                missing_pref.append(s_raw)

        req_score = (len(matched_req) / len(req_skills_raw) * 100.0) if req_skills_raw else 100.0
        pref_score = (len(matched_pref) / len(pref_skills_raw) * 100.0) if pref_skills_raw else 100.0

        if req_skills_raw and pref_skills_raw:
            score = (req_score * REQUIRED_SKILL_WEIGHT) + (pref_score * PREFERRED_SKILL_WEIGHT)
        elif req_skills_raw:
            score = req_score
        else:
            score = pref_score

        return round(score, 2), matched_req, missing_req, matched_pref, missing_pref

    def match_education(
        self, resume: StructuredResume, job: JobRequirements
    ) -> Tuple[float, List[str], List[str]]:
        """Evaluate education requirements using Day 25 degree normalization."""
        req_edu = [e.strip() for e in job.required_education if e and e.strip()]
        pref_edu = [e.strip() for e in job.preferred_education if e and e.strip()]

        if not req_edu and not pref_edu:
            return 100.0, [], []

        matched_edu: List[str] = []
        missing_edu: List[str] = []

        candidate_records = resume.education.education_records if resume.education else []

        for req in req_edu + pref_edu:
            req_canon_degree, req_norm_degree, req_level = normalize_degree(req)
            req_clean = req.lower()

            req_rank = DEGREE_LEVEL_RANKS.get(req_level, 0)
            if req_rank == 0:
                if "doctor" in req_clean or "phd" in req_clean:
                    req_rank = 4
                elif "master" in req_clean or "m.tech" in req_clean or "m.s." in req_clean or "postgraduate" in req_clean:
                    req_rank = 3
                elif "bachelor" in req_clean or "b.tech" in req_clean or "b.s." in req_clean or "undergraduate" in req_clean:
                    req_rank = 2

            is_matched = False
            for cand in candidate_records:
                cand_degree_raw = cand.degree or ""
                cand_field_raw = cand.field_of_study or ""

                cand_canon_degree, cand_norm_degree, cand_level = normalize_degree(cand_degree_raw)
                cand_rank = DEGREE_LEVEL_RANKS.get(cand_level, 0)

                # Direct match or rank satisfaction
                if (req_norm_degree and cand_norm_degree and req_norm_degree == cand_norm_degree) or \
                   (cand_rank >= req_rank and req_rank > 0):
                    # Check field mismatch (e.g. computer requested but candidate only has electrical)
                    if "computer" in req_clean and "electrical" in (cand_field_raw + cand_degree_raw).lower() and "computer" not in (cand_field_raw + cand_degree_raw).lower():
                        continue
                    is_matched = True
                    break
                elif req_clean in (cand_degree_raw + " " + cand_field_raw).lower():
                    is_matched = True
                    break

            if is_matched:
                matched_edu.append(req)
            else:
                missing_edu.append(req)

        matched_req_count = sum(1 for e in req_edu if e in matched_edu)
        req_score = (matched_req_count / len(req_edu) * 100.0) if req_edu else 100.0

        matched_pref_count = sum(1 for e in pref_edu if e in matched_edu)
        pref_score = (matched_pref_count / len(pref_edu) * 100.0) if pref_edu else 100.0

        if req_edu and pref_edu:
            score = (req_score * REQUIRED_EDUCATION_WEIGHT) + (pref_score * PREFERRED_EDUCATION_WEIGHT)
        elif req_edu:
            score = req_score
        else:
            score = pref_score

        return round(score, 2), sorted(list(set(matched_edu))), sorted(list(set(missing_edu)))

    def match_experience(
        self, resume: StructuredResume, job: JobRequirements
    ) -> Tuple[float, Dict[str, Any]]:
        """Evaluate experience duration, role, domain, and seniority matching."""
        details: Dict[str, Any] = {}

        has_req_months = job.required_experience_months is not None
        has_roles = bool(job.required_roles or job.preferred_roles)
        has_domains = bool(job.required_domains or job.preferred_domains)
        has_seniority = bool(job.required_experience_level)

        if not (has_req_months or has_roles or has_domains or has_seniority):
            return 100.0, {"status": "No experience requirements specified"}

        # 1. Duration Score
        duration_score = 100.0
        candidate_months = 0
        if resume.experience and resume.experience.total_experience_months is not None:
            candidate_months = resume.experience.total_experience_months
        elif resume.experience and resume.experience.experiences:
            for exp in resume.experience.experiences:
                candidate_months += (exp.duration_months or 0)

        details["candidate_experience_months"] = candidate_months
        if has_req_months and job.required_experience_months > 0:
            ratio = candidate_months / job.required_experience_months
            duration_score = min(ratio, 1.0) * 100.0
            details["required_experience_months"] = job.required_experience_months
            details["duration_match_score"] = round(duration_score, 2)

        # 2. Role Score
        role_score = 100.0
        candidate_role = resume.classification.role if resume.classification else "UNKNOWN"
        details["candidate_role"] = candidate_role
        if has_roles:
            target_roles = [r.upper() for r in (job.required_roles + job.preferred_roles)]
            details["target_roles"] = target_roles

            if candidate_role in target_roles:
                role_score = 100.0
            else:
                best_compat = 0.0
                compat_table = ROLE_COMPATIBILITY_MAP.get(candidate_role, {})
                for tr in target_roles:
                    compat = compat_table.get(tr, 0.0)
                    if compat > best_compat:
                        best_compat = compat
                role_score = best_compat * 100.0
            details["role_match_score"] = round(role_score, 2)

        # 3. Domain Score
        domain_score = 100.0
        candidate_domain = resume.classification.domain if resume.classification else "UNKNOWN"
        details["candidate_domain"] = candidate_domain
        if has_domains:
            target_domains = [d.upper() for d in (job.required_domains + job.preferred_domains)]
            details["target_domains"] = target_domains
            if candidate_domain in target_domains:
                domain_score = 100.0
            else:
                domain_score = 40.0 if candidate_domain != "UNKNOWN" else 0.0
            details["domain_match_score"] = round(domain_score, 2)

        # 4. Seniority Score
        seniority_score = 100.0
        candidate_level = resume.classification.experience_level if resume.classification else "UNKNOWN"
        details["candidate_experience_level"] = candidate_level
        if has_seniority:
            target_level = job.required_experience_level.upper()
            details["required_experience_level"] = target_level
            if candidate_level == target_level:
                seniority_score = 100.0
            elif candidate_level == "SENIOR" and target_level in {"MID_LEVEL", "JUNIOR", "ENTRY_LEVEL"}:
                seniority_score = 90.0
            elif candidate_level == "MID_LEVEL" and target_level == "ENTRY_LEVEL":
                seniority_score = 85.0
            elif candidate_level in {"INTERN", "ENTRY_LEVEL"} and target_level in {"SENIOR", "LEAD", "MANAGER"}:
                seniority_score = 20.0
            else:
                seniority_score = 50.0
            details["seniority_match_score"] = round(seniority_score, 2)

        # Weighted Experience Score
        exp_score = (
            (duration_score * EXP_DURATION_WEIGHT)
            + (role_score * EXP_ROLE_WEIGHT)
            + (domain_score * EXP_DOMAIN_WEIGHT)
            + (seniority_score * EXP_SENIORITY_WEIGHT)
        )
        return round(exp_score, 2), details

    def score(
        self, structured_resume: StructuredResume, job_requirements: JobRequirements
    ) -> ATSScore:
        """Calculate complete job-specific ATS score for StructuredResume."""
        if structured_resume is None:
            raise ResumeParsingError("Cannot calculate ATS score for a None StructuredResume.")
        if _is_empty_job_requirements(job_requirements):
            raise ValueError("JobRequirements object cannot be empty. Please specify scoring criteria.")

        start_time = time.perf_counter()

        kw_score, matched_kw, miss_req_kw, miss_pref_kw = self.match_keywords(structured_resume, job_requirements)
        sk_score, matched_req_sk, miss_req_sk, matched_pref_sk, miss_pref_sk = self.match_skills(structured_resume, job_requirements)
        edu_score, matched_edu, miss_edu = self.match_education(structured_resume, job_requirements)
        exp_score, exp_details = self.match_experience(structured_resume, job_requirements)

        # Component presence mask for dynamic weight redistribution if a component has 0 requirements
        has_kw = bool(job_requirements.required_keywords or job_requirements.preferred_keywords)
        has_sk = bool(job_requirements.required_skills or job_requirements.preferred_skills)
        has_edu = bool(job_requirements.required_education or job_requirements.preferred_education)
        has_exp = bool(
            job_requirements.required_experience_months is not None
            or job_requirements.preferred_experience_months is not None
            or job_requirements.required_roles
            or job_requirements.preferred_roles
            or job_requirements.required_domains
            or job_requirements.preferred_domains
            or job_requirements.required_experience_level
        )

        w_kw = ATS_KEYWORD_WEIGHT if has_kw else 0.0
        w_sk = ATS_SKILL_WEIGHT if has_sk else 0.0
        w_edu = ATS_EDUCATION_WEIGHT if has_edu else 0.0
        w_exp = ATS_EXPERIENCE_WEIGHT if has_exp else 0.0

        total_weight = w_kw + w_sk + w_edu + w_exp
        if total_weight <= 0.0:
            total_weight = 1.0

        norm_w_kw = w_kw / total_weight
        norm_w_sk = w_sk / total_weight
        norm_w_edu = w_edu / total_weight
        norm_w_exp = w_exp / total_weight

        raw_final_score = (
            (kw_score * norm_w_kw)
            + (sk_score * norm_w_sk)
            + (edu_score * norm_w_edu)
            + (exp_score * norm_w_exp)
        )

        final_score = min(100.0, max(0.0, round(raw_final_score, 2)))

        score_breakdown = {
            "keyword": {
                "score": round(kw_score, 2),
                "weight": round(norm_w_kw, 4),
                "contribution": round(kw_score * norm_w_kw, 2),
            },
            "skill": {
                "score": round(sk_score, 2),
                "weight": round(norm_w_sk, 4),
                "contribution": round(sk_score * norm_w_sk, 2),
            },
            "education": {
                "score": round(edu_score, 2),
                "weight": round(norm_w_edu, 4),
                "contribution": round(edu_score * norm_w_edu, 2),
            },
            "experience": {
                "score": round(exp_score, 2),
                "weight": round(norm_w_exp, 4),
                "contribution": round(exp_score * norm_w_exp, 2),
            },
        }

        # Deterministic Explanation Construction
        exp_parts: List[str] = [f"ATS Match Score: {final_score}/100."]
        if miss_req_sk:
            exp_parts.append(f"Missing required skills: {', '.join(miss_req_sk)}.")
        else:
            exp_parts.append("All required skills are satisfied.")

        if miss_req_kw:
            exp_parts.append(f"Missing required keywords: {', '.join(miss_req_kw)}.")

        if miss_edu:
            exp_parts.append(f"Education requirements not fully satisfied ({', '.join(miss_edu)} missing).")
        else:
            exp_parts.append("Education requirements are satisfied.")

        cand_m = exp_details.get("candidate_experience_months", 0)
        req_m = exp_details.get("required_experience_months")
        if req_m:
            exp_parts.append(f"Candidate has {cand_m} months experience vs {req_m} required months.")

        explanation_str = " ".join(exp_parts)

        # Deterministic Recommendations ("if applicable")
        recs: List[str] = []
        for sk in miss_req_sk:
            recs.append(f"Add {sk} experience to the Skills section if applicable.")
        for kw in miss_req_kw:
            recs.append(f"Include keyword '{kw}' in resume summary or experience if applicable.")
        for edu in miss_edu:
            recs.append(f"Highlight {edu} degree or relevant coursework if applicable.")

        ats_res = ATSScore(
            score=final_score,
            keyword_score=round(kw_score, 2),
            skill_score=round(sk_score, 2),
            education_score=round(edu_score, 2),
            experience_score=round(exp_score, 2),
            matched_keywords=matched_kw,
            missing_required_keywords=miss_req_kw,
            missing_preferred_keywords=miss_pref_kw,
            matched_required_skills=matched_req_sk,
            missing_required_skills=miss_req_sk,
            matched_preferred_skills=matched_pref_sk,
            missing_preferred_skills=miss_pref_sk,
            matched_education=matched_edu,
            missing_education=miss_edu,
            experience_match=exp_details,
            score_breakdown=score_breakdown,
            explanation=explanation_str,
            recommendations=recs,
            scorer_version=SCORER_VERSION,
            scoring_method=SCORING_METHOD,
            metadata={
                "duration_seconds": round(time.perf_counter() - start_time, 4),
                "job_id": job_requirements.job_id,
            },
        )

        return ats_res


def score_resume_against_job(
    structured_resume: Optional[StructuredResume], job_requirements: Optional[JobRequirements]
) -> ATSScore:
    """Public helper function to calculate job-specific ATS score for a StructuredResume.

    Args:
        structured_resume: StructuredResume payload from Day 28.
        job_requirements: JobRequirements payload for evaluation.

    Returns:
        ATSScore result.

    Raises:
        ResumeParsingError: If structured_resume is None.
        ValueError: If job_requirements is None or empty.
    """
    if structured_resume is None:
        raise ResumeParsingError("Cannot score a None StructuredResume.")
    if job_requirements is None or _is_empty_job_requirements(job_requirements):
        raise ValueError("JobRequirements object cannot be None or empty.")

    scorer = HybridATSScorer()
    return scorer.score(structured_resume, job_requirements)
