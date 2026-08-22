"""Phase 4 Day 29 — Resume Classification Engine.

Implements candidate domain classification, role prediction, experience-level prediction,
heuristic confidence scoring, and explainable evidence generation from StructuredResume data.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any
import logging
import time

from app.exceptions.resume import ResumeParsingError
from .models import StructuredResume, ResumeClassification
from .classification_taxonomy import (
    DOMAIN_TAXONOMY,
    ROLE_TAXONOMY,
    EXPERIENCE_LEVEL_TAXONOMY,
    TITLE_ALIAS_MAP,
    DOMAIN_SKILL_MAP,
    SKILL_WEIGHT,
    PROJECT_WEIGHT,
    EXPERIENCE_WEIGHT,
    EDUCATION_WEIGHT,
    TITLE_WEIGHT,
)

logger = logging.getLogger("talentai.resume_processing.resume_classifier")


class BaseResumeClassifier(ABC):
    """Abstract interface for resume classifiers (enables future ML model integration)."""

    @abstractmethod
    def classify(self, structured_resume: StructuredResume) -> ResumeClassification:
        """Classify candidate domain, role, and experience level from a StructuredResume."""
        pass


class HybridResumeClassifier(BaseResumeClassifier):
    """Production deterministic, evidence-driven hybrid classifier.

    Combines skill categories, project classifications, job titles, experience duration,
    and education signals with configurable weights and heuristic confidence bounds.
    """

    def classify_domain(
        self, structured_resume: StructuredResume
    ) -> Tuple[str, float, Dict[str, float], List[str]]:
        """Classify candidate domain based on weighted evidence."""
        scores: Dict[str, float] = {d: 0.0 for d in DOMAIN_TAXONOMY if d != "UNKNOWN"}
        evidence: List[str] = []

        # 1. Skill Evidence (Weight: 0.35)
        if structured_resume.skills and structured_resume.skills.skills:
            skill_names = {s.normalized_name for s in structured_resume.skills.skills if s.normalized_name}
            for domain, domain_skills in DOMAIN_SKILL_MAP.items():
                matches = skill_names.intersection(domain_skills)
                if matches:
                    added_score = (len(matches) / max(len(domain_skills), 1)) * SKILL_WEIGHT * 2.5
                    scores[domain] = scores.get(domain, 0.0) + added_score
                    for m in matches:
                        evidence.append(f"Matched skill '{m}' for domain {domain}")

        # 2. Project Evidence (Weight: 0.30)
        if structured_resume.projects and structured_resume.projects.projects:
            for proj in structured_resume.projects.projects:
                proj_class = proj.classification
                if proj_class in DOMAIN_TAXONOMY and proj_class != "UNKNOWN":
                    scores[proj_class] = scores.get(proj_class, 0.0) + PROJECT_WEIGHT
                    evidence.append(f"Project '{proj.name}' classified as {proj_class}")

        # 3. Experience & Job Title Evidence (Weight: 0.20 + 0.05)
        if structured_resume.experience and structured_resume.experience.experiences:
            for exp in structured_resume.experience.experiences:
                title_clean = exp.job_title.lower() if exp.job_title else ""
                for alias, role in TITLE_ALIAS_MAP.items():
                    if alias in title_clean:
                        if role in {"SOFTWARE_ENGINEER", "FULL_STACK_DEVELOPER", "BACKEND_DEVELOPER", "FRONTEND_DEVELOPER"}:
                            scores["SOFTWARE_ENGINEERING"] = scores.get("SOFTWARE_ENGINEERING", 0.0) + (EXPERIENCE_WEIGHT + TITLE_WEIGHT)
                            evidence.append(f"Job title '{exp.job_title}' maps to SOFTWARE_ENGINEERING")
                        elif role in {"MACHINE_LEARNING_ENGINEER", "AI_ENGINEER"}:
                            scores["MACHINE_LEARNING"] = scores.get("MACHINE_LEARNING", 0.0) + (EXPERIENCE_WEIGHT + TITLE_WEIGHT)
                            evidence.append(f"Job title '{exp.job_title}' maps to MACHINE_LEARNING")
                        elif role in {"DATA_SCIENTIST", "DATA_ANALYST"}:
                            scores["DATA_SCIENCE"] = scores.get("DATA_SCIENCE", 0.0) + (EXPERIENCE_WEIGHT + TITLE_WEIGHT)
                            evidence.append(f"Job title '{exp.job_title}' maps to DATA_SCIENCE")
                        elif role in {"DEVOPS_ENGINEER", "CLOUD_ENGINEER"}:
                            scores["CLOUD_DEVOPS"] = scores.get("CLOUD_DEVOPS", 0.0) + (EXPERIENCE_WEIGHT + TITLE_WEIGHT)
                            evidence.append(f"Job title '{exp.job_title}' maps to CLOUD_DEVOPS")
                        elif role in {"EMBEDDED_ENGINEER", "FIRMWARE_ENGINEER"}:
                            scores["EMBEDDED_SYSTEMS"] = scores.get("EMBEDDED_SYSTEMS", 0.0) + (EXPERIENCE_WEIGHT + TITLE_WEIGHT)
                            evidence.append(f"Job title '{exp.job_title}' maps to EMBEDDED_SYSTEMS")

        # 4. Education Evidence (Weight: 0.10) - Non-dominant
        if structured_resume.education and structured_resume.education.education_records:
            for edu in structured_resume.education.education_records:
                field_clean = (edu.field_of_study or edu.degree or "").lower()
                if "electrical" in field_clean:
                    scores["ELECTRICAL_ENGINEERING"] = scores.get("ELECTRICAL_ENGINEERING", 0.0) + EDUCATION_WEIGHT
                    evidence.append(f"Education degree/field '{edu.degree}' signals ELECTRICAL_ENGINEERING")
                elif "computer" in field_clean or "software" in field_clean or "information technology" in field_clean:
                    scores["SOFTWARE_ENGINEERING"] = scores.get("SOFTWARE_ENGINEERING", 0.0) + EDUCATION_WEIGHT
                    evidence.append(f"Education degree/field '{edu.degree}' signals SOFTWARE_ENGINEERING")

        # Determine top domain
        best_domain = "UNKNOWN"
        best_score = 0.0
        for dom, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            if score > best_score:
                best_score = score
                best_domain = dom

        if best_score < 0.05:
            return "UNKNOWN", 0.0, scores, ["Insufficient domain evidence found."]

        # Calculate heuristic confidence (0.0 to 1.0)
        confidence = min(0.98, max(0.40, round(best_score / (best_score + 0.3), 2)))
        return best_domain, confidence, scores, evidence

    def predict_role(
        self, structured_resume: StructuredResume, domain: str
    ) -> Tuple[str, float, Dict[str, float], List[str]]:
        """Predict specific candidate role based on title history and skills."""
        scores: Dict[str, float] = {r: 0.0 for r in ROLE_TAXONOMY if r != "UNKNOWN"}
        evidence: List[str] = []

        # 1. Job Title Aliases First
        if structured_resume.experience and structured_resume.experience.experiences:
            for exp in structured_resume.experience.experiences:
                t_clean = exp.job_title.lower() if exp.job_title else ""
                for alias, role in TITLE_ALIAS_MAP.items():
                    if alias in t_clean:
                        scores[role] = scores.get(role, 0.0) + 0.50
                        evidence.append(f"Direct title alias match '{exp.job_title}' -> {role}")

        # 2. Skill Combinations for Role Refinement
        if structured_resume.skills and structured_resume.skills.skills:
            skill_set = {s.normalized_name for s in structured_resume.skills.skills if s.normalized_name}

            has_frontend = bool(skill_set.intersection({"react.js", "react", "next.js", "angular", "vue.js", "javascript", "typescript", "html", "css"}))
            has_backend = bool(skill_set.intersection({"fastapi", "django", "flask", "node.js", "express.js", "spring boot", "postgresql", "mysql", "mongodb"}))
            has_ml = bool(skill_set.intersection({"tensorflow", "pytorch", "scikit-learn", "keras", "opencv", "machine learning"}))
            has_devops = bool(skill_set.intersection({"docker", "kubernetes", "aws", "terraform", "jenkins", "ci/cd"}))
            has_embedded = bool(skill_set.intersection({"embedded c", "arduino", "stm32", "rtos", "microcontrollers", "c"}))

            if has_frontend and has_backend:
                scores["FULL_STACK_DEVELOPER"] = scores.get("FULL_STACK_DEVELOPER", 0.0) + 0.40
                evidence.append("Frontend + Backend skills combination signals FULL_STACK_DEVELOPER")
            elif has_backend:
                scores["BACKEND_DEVELOPER"] = scores.get("BACKEND_DEVELOPER", 0.0) + 0.30
                evidence.append("Backend skills signal BACKEND_DEVELOPER")
            elif has_frontend:
                scores["FRONTEND_DEVELOPER"] = scores.get("FRONTEND_DEVELOPER", 0.0) + 0.30
                evidence.append("Frontend skills signal FRONTEND_DEVELOPER")

            if has_ml:
                scores["MACHINE_LEARNING_ENGINEER"] = scores.get("MACHINE_LEARNING_ENGINEER", 0.0) + 0.40
                evidence.append("ML frameworks signal MACHINE_LEARNING_ENGINEER")

            if has_devops:
                scores["DEVOPS_ENGINEER"] = scores.get("DEVOPS_ENGINEER", 0.0) + 0.35
                evidence.append("DevOps/Cloud skills signal DEVOPS_ENGINEER")

            if has_embedded:
                scores["EMBEDDED_ENGINEER"] = scores.get("EMBEDDED_ENGINEER", 0.0) + 0.40
                evidence.append("Embedded systems skills signal EMBEDDED_ENGINEER")

        # Fallback role based on domain if no role matched
        best_role = "UNKNOWN"
        best_score = 0.0
        for r, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            if score > best_score:
                best_score = score
                best_role = r

        if best_score < 0.10:
            if domain == "SOFTWARE_ENGINEERING":
                return "SOFTWARE_ENGINEER", 0.50, scores, ["Defaulted to SOFTWARE_ENGINEER based on domain."]
            elif domain == "MACHINE_LEARNING":
                return "MACHINE_LEARNING_ENGINEER", 0.50, scores, ["Defaulted to MACHINE_LEARNING_ENGINEER based on domain."]
            elif domain == "EMBEDDED_SYSTEMS":
                return "EMBEDDED_ENGINEER", 0.50, scores, ["Defaulted to EMBEDDED_ENGINEER based on domain."]
            return "UNKNOWN", 0.0, scores, ["Insufficient role evidence."]

        confidence = min(0.98, max(0.40, round(best_score / (best_score + 0.2), 2)))
        return best_role, confidence, scores, evidence

    def predict_experience_level(
        self, structured_resume: StructuredResume
    ) -> Tuple[str, float, List[str]]:
        """Predict candidate experience level using Day 26 seniority and duration records."""
        evidence: List[str] = []

        if not structured_resume.experience or not structured_resume.experience.experiences:
            return "ENTRY_LEVEL", 0.60, ["No professional experience records found -> ENTRY_LEVEL"]

        experiences = structured_resume.experience.experiences

        # 1. Check for Internship Status in any experience record
        if any("intern" in (e.job_title or "").lower() for e in experiences) and len(experiences) <= 2:
            return "INTERN", 0.90, [f"Job title '{experiences[0].job_title}' indicates INTERN status."]

        # 2. Prioritize explicitly detected Seniority in the latest/current job title
        latest = experiences[0]
        if latest.seniority and latest.seniority in EXPERIENCE_LEVEL_TAXONOMY and latest.seniority != "UNKNOWN":
            return latest.seniority, 0.95, [f"Day 26 explicit seniority detected in latest role: {latest.seniority}"]

        # 3. Calculate total experience duration in months
        total_months = structured_resume.experience.total_experience_months
        if total_months is None or total_months == 0:
            total_months = 0
            for e in experiences:
                if e.duration_months:
                    total_months += e.duration_months

        evidence.append(f"Total calculated experience duration: {total_months} months across {len(experiences)} roles")

        if total_months <= 12:
            return "ENTRY_LEVEL", 0.85, evidence
        elif total_months <= 36:
            return "MID_LEVEL", 0.85, evidence
        elif total_months <= 84:
            return "SENIOR", 0.90, evidence
        else:
            return "LEAD", 0.90, evidence

    def classify(self, structured_resume: StructuredResume) -> ResumeClassification:
        """Execute full candidate classification workflow."""
        if structured_resume is None:
            raise ResumeParsingError("Cannot classify a None StructuredResume.")

        start_time = time.perf_counter()

        domain, dom_conf, dom_scores, dom_ev = self.classify_domain(structured_resume)
        role, role_conf, role_scores, role_ev = self.predict_role(structured_resume, domain)
        exp_level, exp_conf, exp_ev = self.predict_experience_level(structured_resume)

        all_evidence = {
            "domain_evidence": dom_ev,
            "role_evidence": role_ev,
            "experience_level_evidence": exp_ev,
        }

        classification = ResumeClassification(
            domain=domain,
            domain_confidence=dom_conf,
            role=role,
            role_confidence=role_conf,
            experience_level=exp_level,
            experience_level_confidence=exp_conf,
            domain_scores=dom_scores,
            role_scores=role_scores,
            evidence=all_evidence,
            classifier_version="day29-v1",
            classification_method="hybrid_rule_based",
            metadata={
                "duration_seconds": round(time.perf_counter() - start_time, 4),
            },
        )

        return classification


def classify_resume(structured_resume: Optional[StructuredResume]) -> ResumeClassification:
    """Public helper function to classify a StructuredResume payload.

    Args:
        structured_resume: Valid StructuredResume object from Day 28.

    Returns:
        ResumeClassification object.

    Raises:
        ResumeParsingError: If structured_resume is None.
    """
    if structured_resume is None:
        raise ResumeParsingError("Cannot classify a None StructuredResume payload.")

    classifier = HybridResumeClassifier()
    return classifier.classify(structured_resume)
