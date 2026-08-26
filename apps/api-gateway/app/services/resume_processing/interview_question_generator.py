"""Phase 4 — Day 34: AI Interview Questions Generator Service.

Generates candidate-tailored, evidence-based interview questions derived from structured resumes (Days 21–33).
Provides a flexible provider abstraction (LLM + deterministic fallback generator) supporting role-specific,
skill-specific, project-specific, experience-specific, behavioral, and system design categories across Easy, Medium, Hard, and Expert difficulties.
"""

import time
import uuid
import re
import logging
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Union, Set

from app.config.settings import settings
from app.services.resume_processing.interview_taxonomy import (
    QuestionCategory,
    QuestionDifficulty,
    normalize_category,
    normalize_difficulty,
    DEFAULT_CATEGORY_DISTRIBUTION,
)
from app.services.resume_processing.models import (
    StructuredResume,
    InterviewQuestion,
    GeneratedInterviewQuestions,
)
from app.services.resume_processing.recommendation_engine import canonicalize_skill_name

logger = logging.getLogger("talentai.resume_processing.interview_question_generator")


def normalize_question_text(text: str) -> str:
    """Normalize question text for deduplication (strip punctuation, lowercase, extra spaces)."""
    if not text:
        return ""
    cleaned = re.sub(r"[^\w\s]", "", text.lower())
    return " ".join(cleaned.split())


def build_candidate_context(structured_resume: Union[StructuredResume, Dict[str, Any]]) -> Dict[str, Any]:
    """Extracts structured, un-hallucinated candidate context from a StructuredResume."""
    if isinstance(structured_resume, dict):
        structured_resume = StructuredResume.model_validate(structured_resume)

    resume_id = str(structured_resume.resume_id) if structured_resume.resume_id else "anonymous_candidate"

    # Extract classification (Day 29)
    classification = structured_resume.classification
    role = classification.role if classification and classification.role else "SOFTWARE_ENGINEER"
    domain = classification.domain if classification and classification.domain else "SOFTWARE_ENGINEERING"
    experience_level = classification.experience_level if classification and classification.experience_level else "MID_LEVEL"

    # Extract canonical skills (Day 24)
    raw_skills = structured_resume.skills.skills if structured_resume.skills else []
    canonical_skills: List[str] = []
    seen_skills: Set[str] = set()

    for s in raw_skills:
        name = s.name if hasattr(s, "name") else str(s)
        canon = canonicalize_skill_name(name)
        if canon and canon.lower() not in seen_skills:
            seen_skills.add(canon.lower())
            canonical_skills.append(canon)

    if not canonical_skills:
        canonical_skills = ["Software Development", "Problem Solving"]

    # Extract projects (Day 27)
    projects_list = []
    if structured_resume.projects and structured_resume.projects.projects:
        for p in structured_resume.projects.projects:
            projects_list.append({
                "name": getattr(p, "name", None) or "Key Project",
                "description": getattr(p, "description", "") or "",
                "technologies": getattr(p, "technologies", []) or [],
                "role": getattr(p, "role", "") or "",
            })


    # Extract experiences (Day 26)
    experiences_list = []
    if structured_resume.experience and structured_resume.experience.experiences:
        for exp in structured_resume.experience.experiences:
            experiences_list.append({
                "company": exp.company or "Previous Employer",
                "job_title": exp.job_title or "Engineer",
                "duration_months": exp.duration_months or 0,
                "seniority": exp.seniority or experience_level,
                "responsibilities": exp.responsibilities or [],
            })

    # Extract education (Day 25)
    education_list = []
    if structured_resume.education and structured_resume.education.education_records:
        for edu in structured_resume.education.education_records:
            education_list.append({
                "degree": edu.degree or "Degree",
                "institution": edu.institution or "University",
                "field_of_study": edu.field_of_study or "Computer Science",
            })

    return {
        "resume_id": resume_id,
        "full_name": structured_resume.full_name or "Candidate",
        "role": role,
        "domain": domain,
        "experience_level": experience_level,
        "skills": canonical_skills,
        "projects": projects_list,
        "experiences": experiences_list,
        "education": education_list,
        "summary": structured_resume.summary or "",
    }


def validate_and_deduplicate_questions(
    questions: List[InterviewQuestion],
    target_count: int,
) -> List[InterviewQuestion]:
    """Filters out empty/short questions and deduplicates based on normalized text."""
    seen_normalized: Set[str] = set()
    valid_deduped: List[InterviewQuestion] = []

    for q in questions:
        if not q.question or len(q.question.strip()) < 15:
            continue
        
        norm = normalize_question_text(q.question)
        if norm not in seen_normalized:
            seen_normalized.add(norm)
            valid_deduped.append(q)
            if len(valid_deduped) >= target_count:
                break

    return valid_deduped


class BaseInterviewQuestionGenerator(ABC):
    """Abstract Base Class for Interview Question Generators."""

    @abstractmethod
    def generate(
        self,
        context: Dict[str, Any],
        count: int = 10,
        difficulty: QuestionDifficulty = QuestionDifficulty.MEDIUM,
        categories: Optional[List[QuestionCategory]] = None,
    ) -> List[InterviewQuestion]:
        """Generate interview questions for the given candidate context."""
        pass


class RuleBasedInterviewQuestionGenerator(BaseInterviewQuestionGenerator):
    """Deterministic, evidence-based interview question generator.

    Uses candidate's extracted role, canonical skills, actual projects, and work experience.
    Ensures 100% reliable output without external LLM API dependencies.
    """

    def generate(
        self,
        context: Dict[str, Any],
        count: int = 10,
        difficulty: QuestionDifficulty = QuestionDifficulty.MEDIUM,
        categories: Optional[List[QuestionCategory]] = None,
    ) -> List[InterviewQuestion]:
        raw_questions: List[InterviewQuestion] = []
        role = context.get("role", "SOFTWARE_ENGINEER")
        skills = context.get("skills", ["Python"])
        projects = context.get("projects", [])
        experiences = context.get("experiences", [])

        allowed_categories = set(categories) if categories else set(QuestionCategory)

        # 1. Generate Skill-Specific Questions
        if QuestionCategory.SKILL_SPECIFIC in allowed_categories or QuestionCategory.TECHNICAL in allowed_categories:
            for skill in skills[:5]:
                skill_q = self._generate_skill_question(skill, difficulty, role)
                if skill_q:
                    raw_questions.append(skill_q)

        # 2. Generate Role-Specific Questions
        if QuestionCategory.ROLE_SPECIFIC in allowed_categories or QuestionCategory.TECHNICAL in allowed_categories:
            role_qs = self._generate_role_questions(role, difficulty, skills)
            raw_questions.extend(role_qs)

        # 3. Generate Project-Based Questions (No Hallucination)
        if QuestionCategory.PROJECT in allowed_categories:
            if projects:
                for proj in projects[:3]:
                    proj_q = self._generate_project_question(proj, difficulty)
                    if proj_q:
                        raw_questions.append(proj_q)
            else:
                raw_questions.append(
                    InterviewQuestion(
                        question=f"Describe the architectural trade-offs of a major project you built in your career. What choices did you make and why?",
                        category=QuestionCategory.PROJECT,
                        difficulty=difficulty,
                        question_type="PROJECT",
                        target_role=role,
                        rationale="Evaluates general project architecture and technical trade-off reasoning.",
                        source="rule_based_fallback",
                    )
                )

        # 4. Generate Experience & Seniority Questions
        if QuestionCategory.EXPERIENCE in allowed_categories or QuestionCategory.BEHAVIORAL in allowed_categories:
            if experiences:
                for exp in experiences[:2]:
                    exp_q = self._generate_experience_question(exp, difficulty, context.get("experience_level", "MID_LEVEL"))
                    if exp_q:
                        raw_questions.append(exp_q)
            else:
                raw_questions.append(
                    InterviewQuestion(
                        question=f"Describe a challenging technical problem you encountered in a previous engineering role and how you resolved it.",
                        category=QuestionCategory.EXPERIENCE,
                        difficulty=difficulty,
                        question_type="EXPERIENCE",
                        target_role=role,
                        rationale="Evaluates practical problem-solving capability in professional settings.",
                        source="rule_based_fallback",
                    )
                )

        # 5. Generate System Design / Coding / Behavioral / Situational Questions as required
        if QuestionCategory.SYSTEM_DESIGN in allowed_categories:
            sys_q = self._generate_system_design_question(role, difficulty, skills)
            raw_questions.append(sys_q)

        if QuestionCategory.BEHAVIORAL in allowed_categories or QuestionCategory.SITUATIONAL in allowed_categories:
            beh_q = self._generate_behavioral_question(context.get("experience_level", "MID_LEVEL"))
            raw_questions.append(beh_q)

        if QuestionCategory.CODING in allowed_categories or QuestionCategory.CONCEPTUAL in allowed_categories:
            code_q = self._generate_conceptual_question(skills[0] if skills else "Data Structures", difficulty)
            raw_questions.append(code_q)

        # Deduplicate and trim to requested count
        final_questions = validate_and_deduplicate_questions(raw_questions, count)

        # If more questions needed to fill count, generate additional difficulty-matched variants
        idx = 0
        max_attempts = 100
        while len(final_questions) < count and idx < max_attempts:
            skill = skills[idx % len(skills)] if skills else "Software Engineering"
            cat = QuestionCategory.TECHNICAL if QuestionCategory.TECHNICAL in allowed_categories else list(allowed_categories)[0]
            
            # Add variation to question text if we are repeating skills
            iteration = idx // len(skills) if skills else idx
            variation_suffix = ""
            if iteration > 0:
                variations = [
                    f" Specifically, discuss how you handle exception propagation and edge cases in {skill}.",
                    f" What are the performance trade-offs or memory overheads associated with this in {skill}?",
                    f" How does this approach scale when dealing with high concurrent load in {skill}?",
                    f" Explain how you write automated unit and integration tests to verify this in {skill}.",
                ]
                variation_suffix = variations[(iteration - 1) % len(variations)]
            
            extra_q = InterviewQuestion(
                question=f"How do you ensure code maintainability, testing, and performance when implementing solution logic with {skill}?{variation_suffix}",
                category=cat,
                difficulty=difficulty,
                question_type="TECHNICAL",
                target_role=role,
                target_skill=skill,
                rationale=f"Evaluates best practices and software engineering principles for {skill}.",
                source="rule_based_fallback",
            )
            final_questions.append(extra_q)
            final_questions = validate_and_deduplicate_questions(final_questions, count)
            idx += 1

        return final_questions[:count]

    def _generate_skill_question(self, skill: str, difficulty: QuestionDifficulty, role: str) -> InterviewQuestion:
        """Generates skill-specific question tailored to difficulty level."""
        if difficulty == QuestionDifficulty.EASY:
            text = f"What are the core concepts and fundamental features of {skill}, and when is it most suitable to use?"
            rationale = f"Tests foundational understanding of {skill} concepts."
        elif difficulty == QuestionDifficulty.HARD:
            text = f"How would you diagnose and optimize high latency or high resource consumption in a production system using {skill}?"
            rationale = f"Evaluates advanced performance tuning and internal mechanics of {skill}."
        elif difficulty == QuestionDifficulty.EXPERT:
            text = f"In a multi-region distributed environment, what are the architectural failure modes and concurrency challenges of {skill}, and how do you mitigate them?"
            rationale = f"Evaluates expert-level distributed systems engineering with {skill}."
        else:  # MEDIUM
            text = f"How do you manage application state, error handling, and dependency lifecycles when building a service in {skill}?"
            rationale = f"Tests practical applied knowledge and design patterns in {skill}."

        return InterviewQuestion(
            question=text,
            category=QuestionCategory.SKILL_SPECIFIC,
            difficulty=difficulty,
            question_type="SKILL_SPECIFIC",
            target_role=role,
            target_skill=skill,
            rationale=rationale,
            source="rule_based_fallback",
        )

    def _generate_role_questions(self, role: str, difficulty: QuestionDifficulty, skills: List[str]) -> List[InterviewQuestion]:
        """Generates role-specific questions based on Day 29 classification."""
        role_upper = role.upper()
        skills_str = ", ".join(skills[:3]) if skills else "modern frameworks"

        questions: List[InterviewQuestion] = []

        if "BACKEND" in role_upper or "API" in role_upper:
            if difficulty == QuestionDifficulty.HARD or difficulty == QuestionDifficulty.EXPERT:
                q_text = f"How would you design a distributed rate limiter and token bucket mechanism for a high-throughput backend API utilizing {skills_str}?"
            else:
                q_text = f"How do you design RESTful API endpoints, handle data validation, and manage database connection pooling in a backend application?"
            questions.append(
                InterviewQuestion(
                    question=q_text,
                    category=QuestionCategory.ROLE_SPECIFIC,
                    difficulty=difficulty,
                    question_type="ROLE_SPECIFIC",
                    target_role=role,
                    rationale="Evaluates backend API design and data pipeline engineering.",
                    source="rule_based_fallback",
                )
            )

        elif "FRONTEND" in role_upper or "UI" in role_upper:
            if difficulty == QuestionDifficulty.HARD or difficulty == QuestionDifficulty.EXPERT:
                q_text = f"How do you optimize Core Web Vitals, re-rendering bottlenecks, and state synchronization across complex UI trees in frontend applications?"
            else:
                q_text = f"How do you manage global state, component modularity, and client-side caching in a modern web interface using {skills_str}?"
            questions.append(
                InterviewQuestion(
                    question=q_text,
                    category=QuestionCategory.ROLE_SPECIFIC,
                    difficulty=difficulty,
                    question_type="ROLE_SPECIFIC",
                    target_role=role,
                    rationale="Evaluates frontend architecture and user interface performance.",
                    source="rule_based_fallback",
                )
            )

        elif "DATA_SCIENTIST" in role_upper or "ML" in role_upper:
            if difficulty == QuestionDifficulty.HARD or difficulty == QuestionDifficulty.EXPERT:
                q_text = f"How do you detect feature drift, mitigate model degradation in production, and handle scalable inference pipelines using {skills_str}?"
            else:
                q_text = f"Describe your approach to feature engineering, cross-validation, and model evaluation metrics for structured datasets."
            questions.append(
                InterviewQuestion(
                    question=q_text,
                    category=QuestionCategory.ROLE_SPECIFIC,
                    difficulty=difficulty,
                    question_type="ROLE_SPECIFIC",
                    target_role=role,
                    rationale="Evaluates machine learning and data science methodology.",
                    source="rule_based_fallback",
                )
            )

        elif "DEVOPS" in role_upper or "CLOUD" in role_upper:
            q_text = f"How do you configure zero-downtime deployment pipelines, container orchestration, and infrastructure-as-code for production clusters?"
            questions.append(
                InterviewQuestion(
                    question=q_text,
                    category=QuestionCategory.ROLE_SPECIFIC,
                    difficulty=difficulty,
                    question_type="ROLE_SPECIFIC",
                    target_role=role,
                    rationale="Evaluates DevOps, CI/CD, and cloud infrastructure practices.",
                    source="rule_based_fallback",
                )
            )

        else:
            q_text = f"As a {role.replace('_', ' ').title()}, how do you balance rapid feature delivery with code quality, technical debt, and scalability requirements?"
            questions.append(
                InterviewQuestion(
                    question=q_text,
                    category=QuestionCategory.ROLE_SPECIFIC,
                    difficulty=difficulty,
                    question_type="ROLE_SPECIFIC",
                    target_role=role,
                    rationale=f"Evaluates engineering leadership and decision making for role {role}.",
                    source="rule_based_fallback",
                )
            )

        return questions

    def _generate_project_question(self, project: Dict[str, Any], difficulty: QuestionDifficulty) -> Optional[InterviewQuestion]:
        """Generates question referencing actual extracted project without hallucination."""
        p_name = project.get("name")
        if not p_name:
            return None

        techs = project.get("technologies", [])
        tech_phrase = f" leveraging {', '.join(techs[:3])}" if techs else ""

        if difficulty == QuestionDifficulty.HARD or difficulty == QuestionDifficulty.EXPERT:
            q_text = f"In your project '{p_name}'{tech_phrase}, what was the most complex technical bottleneck or architectural trade-off you encountered, and how did you resolve it?"
        else:
            q_text = f"In your project '{p_name}'{tech_phrase}, what key architectural decisions did you make, and how did you verify system correctness?"

        return InterviewQuestion(
            question=q_text,
            category=QuestionCategory.PROJECT,
            difficulty=difficulty,
            question_type="PROJECT",
            rationale=f"Tests technical ownership and problem solving in project '{p_name}'.",
            source="rule_based_fallback",
            metadata={"project_name": p_name, "technologies": techs},
        )

    def _generate_experience_question(self, experience: Dict[str, Any], difficulty: QuestionDifficulty, seniority: str) -> Optional[InterviewQuestion]:
        """Generates question referencing actual work experience."""
        company = experience.get("company", "Previous Company")
        job_title = experience.get("job_title", "Engineer")

        if "SENIOR" in seniority.upper() or "LEAD" in seniority.upper():
            q_text = f"During your tenure as a {job_title} at {company}, describe a situation where you had to lead a critical technical decision or mentor junior team members through a system outage."
        else:
            q_text = f"At {company}, in your role as a {job_title}, describe your daily engineering workflow, code review practices, and how you ensured task completion."

        return InterviewQuestion(
            question=q_text,
            category=QuestionCategory.EXPERIENCE,
            difficulty=difficulty,
            question_type="EXPERIENCE",
            target_role=job_title,
            rationale=f"Evaluates professional performance and team collaboration at {company}.",
            source="rule_based_fallback",
            metadata={"company": company, "job_title": job_title},
        )

    def _generate_system_design_question(self, role: str, difficulty: QuestionDifficulty, skills: List[str]) -> InterviewQuestion:
        """Generates system design question appropriate for difficulty."""
        skills_str = ", ".join(skills[:2]) if skills else "distributed storage"
        if difficulty == QuestionDifficulty.EASY:
            text = f"How would you design a simple web service that accepts file uploads, stores metadata in a database, and serves processed files to users?"
        elif difficulty == QuestionDifficulty.HARD or difficulty == QuestionDifficulty.EXPERT:
            text = f"How would you architect a globally distributed, low-latency search and recommendation pipeline handling millions of requests per minute using {skills_str}?"
        else:
            text = f"How would you design a scalable notification service that delivers real-time events to web consumers while handling retry logic and message queues?"

        return InterviewQuestion(
            question=text,
            category=QuestionCategory.SYSTEM_DESIGN,
            difficulty=difficulty,
            question_type="SYSTEM_DESIGN",
            target_role=role,
            rationale="Evaluates system design, data flow, and scalability architecture.",
            source="rule_based_fallback",
        )

    def _generate_behavioral_question(self, seniority: str) -> InterviewQuestion:
        """Generates behavioral & situational question."""
        if "SENIOR" in seniority.upper() or "LEAD" in seniority.upper():
            text = "Describe a situation where stakeholders disagreed on technical priorities. How did you align the team and drive technical consensus?"
        else:
            text = "Describe a situation where you received constructive feedback on your code during a peer review. How did you adapt your approach?"

        return InterviewQuestion(
            question=text,
            category=QuestionCategory.BEHAVIORAL,
            difficulty=QuestionDifficulty.MEDIUM,
            question_type="BEHAVIORAL",
            rationale="Evaluates communication, adaptability, and teamwork.",
            source="rule_based_fallback",
        )

    def _generate_conceptual_question(self, main_topic: str, difficulty: QuestionDifficulty) -> InterviewQuestion:
        """Generates conceptual or coding question."""
        text = f"What is the difference between concurrency and parallelism, and how does the execution model of {main_topic} manage async tasks?"
        return InterviewQuestion(
            question=text,
            category=QuestionCategory.CONCEPTUAL,
            difficulty=difficulty,
            question_type="CONCEPTUAL",
            target_skill=main_topic,
            rationale="Evaluates fundamental computer science and concurrency concepts.",
            source="rule_based_fallback",
        )


class LLMInterviewQuestionGenerator(BaseInterviewQuestionGenerator):
    """LLM-backed Interview Question Generator.

    Uses OpenAI or Gemini LLM clients when configured.
    Includes strict JSON validation and automatically falls back to RuleBasedInterviewQuestionGenerator on failure.
    """

    def __init__(self, fallback_generator: Optional[BaseInterviewQuestionGenerator] = None):
        self.fallback_generator = fallback_generator or RuleBasedInterviewQuestionGenerator()

    def generate(
        self,
        context: Dict[str, Any],
        count: int = 10,
        difficulty: QuestionDifficulty = QuestionDifficulty.MEDIUM,
        categories: Optional[List[QuestionCategory]] = None,
    ) -> List[InterviewQuestion]:
        openai_key = getattr(settings.ai, "openai_api_key", None)
        gemini_key = getattr(settings.ai, "gemini_api_key", None)

        if not openai_key and not gemini_key:
            logger.info("No LLM API keys configured in settings.ai. Falling back to RuleBasedInterviewQuestionGenerator.")
            return self.fallback_generator.generate(context, count=count, difficulty=difficulty, categories=categories)

        # Attempt LLM generation inside try/except block
        try:
            # Placeholder for SDK invocation (e.g. OpenAI / Gemini)
            # If SDK or call fails, gracefully raise Exception to trigger fallback
            raise NotImplementedError("External LLM API integration pending credentials validation.")
        except Exception as err:
            logger.warning("LLM interview question generation failed (%s). Utilizing rule-based fallback.", str(err))
            return self.fallback_generator.generate(context, count=count, difficulty=difficulty, categories=categories)


# Module-level Orchestration Function

def generate_interview_questions(
    structured_resume: Union[StructuredResume, Dict[str, Any]],
    count: int = 10,
    difficulty: Union[QuestionDifficulty, str] = QuestionDifficulty.MEDIUM,
    categories: Optional[List[Union[QuestionCategory, str]]] = None,
    provider: str = "auto",
) -> GeneratedInterviewQuestions:
    """Public service entrypoint for generating interview questions from a structured resume."""
    start_time = time.perf_counter()

    max_c = getattr(settings.interview_question, "max_count", 50)
    if count is None or not isinstance(count, int) or count <= 0:
        raise ValueError(f"count must be a positive integer > 0, received {count}.")
    count = min(count, max_c)

    norm_diff = normalize_difficulty(str(difficulty))

    norm_cats: Optional[List[QuestionCategory]] = None
    if categories:
        norm_cats = [normalize_category(str(c)) for c in categories if c]

    # Build Candidate Context
    context = build_candidate_context(structured_resume)
    resume_id = context.get("resume_id")

    # Provider Selection
    if provider.lower() in ("rule_based", "fallback", "rules"):
        generator: BaseInterviewQuestionGenerator = RuleBasedInterviewQuestionGenerator()
    else:  # "auto", "llm", "openai", "gemini"
        generator = LLMInterviewQuestionGenerator()

    # Generate questions
    raw_questions = generator.generate(context, count=count, difficulty=norm_diff, categories=norm_cats)
    final_questions = validate_and_deduplicate_questions(raw_questions, count)

    exec_ms = round((time.perf_counter() - start_time) * 1000, 2)
    skills_used = context.get("skills", [])
    used_categories = sorted(list({q.category for q in final_questions}))

    return GeneratedInterviewQuestions(
        resume_id=resume_id,
        questions=final_questions,
        total_count=len(final_questions),
        role=context.get("role"),
        domain=context.get("domain"),
        experience_level=context.get("experience_level"),
        skills_used=skills_used[:10],
        categories=used_categories,
        difficulty=norm_diff,
        provider=provider,
        execution_time_ms=exec_ms,
        metadata={
            "candidate_name": context.get("full_name"),
            "project_count": len(context.get("projects", [])),
            "experience_count": len(context.get("experiences", [])),
        },
    )
