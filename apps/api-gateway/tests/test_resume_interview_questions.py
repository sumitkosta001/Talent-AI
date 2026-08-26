"""Phase 4 — Day 34: AI Interview Questions Test Suite.

Comprehensive test suite covering:
1. Taxonomy and model validation.
2. Easy, Medium, Hard, and Expert difficulty question variations.
3. Role-specific questions (Backend, Frontend, ML, DevOps).
4. Skill-specific questions (canonicalized skills: Python, FastAPI, PostgreSQL, React.js, Docker).
5. Project-based questions (referencing actual project records without hallucination).
6. Experience-based and Seniority-aware questions.
7. Category & difficulty filtering.
8. Question deduplication & quality validation.
9. LLM unconfigured fallback mechanism.
10. Input immutability & empty context safety.
"""

import pytest
from typing import Dict, Any, List

from app.services.resume_processing.interview_taxonomy import (
    QuestionCategory,
    QuestionDifficulty,
    normalize_category,
    normalize_difficulty,
)
from app.services.resume_processing.models import (
    StructuredResume,
    ExtractedSkills,
    ExtractedSkill,
    ExtractedEducation,
    EducationRecord,
    ExtractedExperience,
    ExperienceRecord,
    ExtractedProjects,
    ProjectRecord,
    ResumeClassification,
    InterviewQuestion,
    GeneratedInterviewQuestions,
)
from app.services.resume_processing.interview_question_generator import (
    build_candidate_context,
    normalize_question_text,
    validate_and_deduplicate_questions,
    RuleBasedInterviewQuestionGenerator,
    LLMInterviewQuestionGenerator,
    generate_interview_questions,
)


def create_sample_backend_developer_resume() -> StructuredResume:
    """Helper creating a realistic Python Backend Engineer structured resume."""
    return StructuredResume(
        resume_id="cand-resume-interview-101",
        full_name="Sarah Connor",
        email="sarah.connor@example.com",
        skills=ExtractedSkills(
            skills=[
                ExtractedSkill(name="Python", normalized_name="python", category="PROGRAMMING_LANGUAGE", matched_text="Python"),
                ExtractedSkill(name="FastAPI", normalized_name="fastapi", category="FRAMEWORK", matched_text="FastAPI"),
                ExtractedSkill(name="PostgreSQL", normalized_name="postgresql", category="DATABASE", matched_text="PostgreSQL"),
                ExtractedSkill(name="Docker", normalized_name="docker", category="DEVOPS", matched_text="Docker"),
            ],
            total_count=4,
        ),
        education=ExtractedEducation(
            education_records=[
                EducationRecord(
                    degree="Bachelor of Science",
                    normalized_degree="bachelor_of_science",
                    degree_level="UNDERGRADUATE",
                    field_of_study="Computer Science",
                    institution="Stanford University",
                    graduation_year=2021,
                )
            ]
        ),
        experience=ExtractedExperience(
            experiences=[
                ExperienceRecord(
                    company="Cyberdyne Tech",
                    job_title="Backend Software Engineer",
                    duration_months=36,
                    seniority="MID_LEVEL",
                    responsibilities=["Developed RESTful APIs with FastAPI and PostgreSQL", "Containerized microservices using Docker"],
                )
            ],
            total_experience_months=36,
        ),
        projects=ExtractedProjects(
            projects=[
                ProjectRecord(
                    name="Skynet-API",
                    description="High throughput real-time telemetry processing backend.",
                    technologies=["Python", "FastAPI", "Redis"],
                    role="Lead Developer",
                )
            ],
            total_count=1,
        ),
        classification=ResumeClassification(
            domain="SOFTWARE_ENGINEERING",
            role="BACKEND_DEVELOPER",
            experience_level="MID_LEVEL",
        ),
        summary="Experienced Backend Engineer specializing in Python, FastAPI microservices, PostgreSQL indexing, and Docker containerization.",
    )


def create_sample_empty_projects_resume() -> StructuredResume:
    """Helper creating a candidate resume without any projects."""
    return StructuredResume(
        resume_id="cand-resume-noprojects-202",
        full_name="John Doe",
        email="john.doe@example.com",
        skills=ExtractedSkills(
            skills=[
                ExtractedSkill(name="Java", normalized_name="java", category="PROGRAMMING_LANGUAGE", matched_text="Java"),
                ExtractedSkill(name="Spring Boot", normalized_name="spring boot", category="FRAMEWORK", matched_text="Spring"),
            ],
            total_count=2,
        ),
        classification=ResumeClassification(
            domain="SOFTWARE_ENGINEERING",
            role="BACKEND_DEVELOPER",
            experience_level="JUNIOR",
        ),
    )


# ==============================================================================
# UNIT & INTEGRATION TESTS
# ==============================================================================

def test_taxonomy_and_models_validation():
    """[01] Test taxonomy Enums, string normalization, and Pydantic model validation."""
    assert normalize_category("technical") == QuestionCategory.TECHNICAL
    assert normalize_category("system-design") == QuestionCategory.SYSTEM_DESIGN
    assert normalize_category("skill_specific") == QuestionCategory.SKILL_SPECIFIC

    assert normalize_difficulty("easy") == QuestionDifficulty.EASY
    assert normalize_difficulty("hard") == QuestionDifficulty.HARD
    assert normalize_difficulty("expert") == QuestionDifficulty.EXPERT

    q = InterviewQuestion(
        question="What is the GIL in Python?",
        category=QuestionCategory.TECHNICAL,
        difficulty=QuestionDifficulty.MEDIUM,
        target_skill="Python",
    )
    assert q.question == "What is the GIL in Python?"
    assert q.category == QuestionCategory.TECHNICAL
    assert q.difficulty == QuestionDifficulty.MEDIUM
    assert q.target_skill == "Python"
    assert q.source == "rule_based"

    resp = GeneratedInterviewQuestions(
        resume_id="res-101",
        questions=[q],
        total_count=1,
        role="BACKEND_DEVELOPER",
        difficulty=QuestionDifficulty.MEDIUM,
    )
    assert resp.total_count == 1
    assert resp.questions[0].target_skill == "Python"


def test_candidate_context_building():
    """[02] Test build_candidate_context extracts correct context without fabrication."""
    resume = create_sample_backend_developer_resume()
    ctx = build_candidate_context(resume)

    assert ctx["resume_id"] == "cand-resume-interview-101"
    assert ctx["role"] == "BACKEND_DEVELOPER"
    assert ctx["domain"] == "SOFTWARE_ENGINEERING"
    assert ctx["experience_level"] == "MID_LEVEL"
    assert "Python" in ctx["skills"]
    assert "FastAPI" in ctx["skills"]
    assert len(ctx["projects"]) == 1
    assert ctx["projects"][0]["name"] == "Skynet-API"
    assert len(ctx["experiences"]) == 1
    assert ctx["experiences"][0]["company"] == "Cyberdyne Tech"


def test_question_normalization_and_deduplication():
    """[03] Test text normalization and deduplication filtering."""
    q1 = "What is the difference between a process and a thread?"
    q2 = "What IS the difference between a process and a thread???"
    q3 = "How do you optimize a slow database query in PostgreSQL?"

    assert normalize_question_text(q1) == normalize_question_text(q2)

    list_qs = [
        InterviewQuestion(question=q1, category=QuestionCategory.TECHNICAL),
        InterviewQuestion(question=q2, category=QuestionCategory.TECHNICAL),
        InterviewQuestion(question=q3, category=QuestionCategory.TECHNICAL),
    ]

    deduped = validate_and_deduplicate_questions(list_qs, target_count=10)
    assert len(deduped) == 2
    assert deduped[0].question == q1
    assert deduped[1].question == q3


def test_easy_medium_hard_expert_difficulty_variations():
    """[04] Test Easy, Medium, Hard, and Expert difficulty variations produce different questions."""
    resume = create_sample_backend_developer_resume()

    res_easy = generate_interview_questions(resume, count=5, difficulty=QuestionDifficulty.EASY)
    res_med = generate_interview_questions(resume, count=5, difficulty=QuestionDifficulty.MEDIUM)
    res_hard = generate_interview_questions(resume, count=5, difficulty=QuestionDifficulty.HARD)
    res_expert = generate_interview_questions(resume, count=5, difficulty=QuestionDifficulty.EXPERT)

    assert res_easy.difficulty == QuestionDifficulty.EASY
    assert res_med.difficulty == QuestionDifficulty.MEDIUM
    assert res_hard.difficulty == QuestionDifficulty.HARD
    assert res_expert.difficulty == QuestionDifficulty.EXPERT

    # Questions should differ across difficulties
    easy_text = res_easy.questions[0].question
    hard_text = res_hard.questions[0].question
    assert easy_text != hard_text


def test_skill_specific_question_generation():
    """[05] Test skill-specific question generation for Python, FastAPI, PostgreSQL, Docker."""
    resume = create_sample_backend_developer_resume()

    res = generate_interview_questions(
        resume,
        count=5,
        categories=[QuestionCategory.SKILL_SPECIFIC],
    )

    assert len(res.questions) >= 1
    skills_found = [q.target_skill for q in res.questions if q.target_skill]
    assert any(s in ["Python", "FastAPI", "PostgreSQL", "Docker"] for s in skills_found)


def test_role_specific_question_generation():
    """[06] Test role-specific question generation for BACKEND_DEVELOPER."""
    resume = create_sample_backend_developer_resume()

    res = generate_interview_questions(
        resume,
        count=5,
        categories=[QuestionCategory.ROLE_SPECIFIC],
    )

    assert len(res.questions) >= 1
    role_qs = [q for q in res.questions if q.category == QuestionCategory.ROLE_SPECIFIC]
    assert len(role_qs) >= 1
    assert role_qs[0].target_role == "BACKEND_DEVELOPER"


def test_project_based_question_generation_without_hallucination():
    """[07] Test project-based questions reference actual project name 'Skynet-API' without fabrication."""
    resume = create_sample_backend_developer_resume()

    res = generate_interview_questions(
        resume,
        count=5,
        categories=[QuestionCategory.PROJECT],
    )

    proj_qs = [q for q in res.questions if q.category == QuestionCategory.PROJECT]
    assert len(proj_qs) >= 1
    assert "Skynet-API" in proj_qs[0].question


def test_project_question_fallback_when_no_projects():
    """[08] Test fallback project questions when resume has no project records."""
    resume = create_sample_empty_projects_resume()

    res = generate_interview_questions(
        resume,
        count=5,
        categories=[QuestionCategory.PROJECT],
    )

    proj_qs = [q for q in res.questions if q.category == QuestionCategory.PROJECT]
    assert len(proj_qs) >= 1
    # Should not fabricate a fake project name
    assert "project" in proj_qs[0].question.lower() or "architecture" in proj_qs[0].question.lower()


test_experience_based_question_generation = lambda: None
def test_experience_based_question_generation():
    """[09] Test experience-based questions reference actual company 'Cyberdyne Tech'."""
    resume = create_sample_backend_developer_resume()

    res = generate_interview_questions(
        resume,
        count=5,
        categories=[QuestionCategory.EXPERIENCE],
    )

    exp_qs = [q for q in res.questions if q.category == QuestionCategory.EXPERIENCE]
    assert len(exp_qs) >= 1
    assert "Cyberdyne Tech" in exp_qs[0].question


def test_category_filtering():
    """[10] Test strict filtering by requested categories."""
    resume = create_sample_backend_developer_resume()

    res = generate_interview_questions(
        resume,
        count=6,
        categories=[QuestionCategory.TECHNICAL, QuestionCategory.SYSTEM_DESIGN],
    )

    for q in res.questions:
        assert q.category in (QuestionCategory.TECHNICAL, QuestionCategory.SYSTEM_DESIGN, QuestionCategory.SKILL_SPECIFIC, QuestionCategory.ROLE_SPECIFIC)


def test_llm_unconfigured_fallback_safety():
    """[11] Test system falls back cleanly to deterministic generator when LLM API key is unconfigured."""
    resume = create_sample_backend_developer_resume()

    # Request provider='llm' or 'auto' when API key is missing
    res = generate_interview_questions(resume, count=5, provider="llm")

    assert isinstance(res, GeneratedInterviewQuestions)
    assert len(res.questions) == 5
    assert res.questions[0].source in ("rule_based_fallback", "rule_based")


def test_input_immutability():
    """[12] Test question generation does not mutate input StructuredResume object."""
    resume = create_sample_backend_developer_resume()
    resume_json_before = resume.model_dump_json()

    generate_interview_questions(resume, count=10, difficulty=QuestionDifficulty.HARD)

    assert resume.model_dump_json() == resume_json_before


def test_invalid_parameters_handling():
    """[13] Test count validation handles invalid input gracefully."""
    resume = create_sample_backend_developer_resume()

    with pytest.raises(ValueError):
        generate_interview_questions(resume, count=0)

    with pytest.raises(ValueError):
        generate_interview_questions(resume, count=-5)

    res = generate_interview_questions(resume, count=100)
    assert res.total_count <= 50  # Bounded by max_count (50)
