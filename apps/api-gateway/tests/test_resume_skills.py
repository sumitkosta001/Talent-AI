"""Comprehensive Test Suite for Phase 4 Day 24: Resume Skills Extraction using spaCy & Skill Dictionary.

Tests:
1. spaCy model loading & singleton caching (en_core_web_sm)
2. Basic and category skill extraction (Languages, Frontend, Backend, DB, Cloud, DevOps, ML, AI, Testing, Security, Tools)
3. Multi-word skill extraction (Machine Learning, Amazon Web Services, GitHub Actions, Tailwind CSS, Large Language Models)
4. Technical punctuation preservation (C++, C#, .NET, Node.js, React.js, Next.js, CI/CD, scikit-learn)
5. False-positive guards (Java vs JavaScript, Go in prose, R, IT, C, AI)
6. Skill alias normalization (react/reactjs -> React.js, postgres -> PostgreSQL, sklearn -> scikit-learn, gcp -> Google Cloud)
7. Deduplication and mention count aggregation
8. Section context confidence scoring (SKILLS vs EXPERIENCE vs PROJECTS vs generic text)
9. Category grouping and deterministic output ordering
10. Non-mutation of input ProcessedResumeText and error handling for None/empty inputs
11. Full synthetic resume test (John Doe software engineer)
12. Pytest compatibility
"""

import asyncio
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Ensure api-gateway root is in sys.path for direct script execution
_root_dir = str(Path(__file__).resolve().parent.parent)
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

import pytest

from app.services.resume_processing.models import (
    ExtractedDocument,
    DocumentPage,
    ProcessedSection,
    ProcessedResumeText,
    ExtractedSkill,
    ExtractedSkills,
)
from app.services.resume_processing.spacy_service import get_spacy_nlp, reset_spacy_cache
from app.services.resume_processing.text_cleaner import clean_text
from app.services.resume_processing.section_detector import detect_sections
from app.services.resume_processing.tokenizer import tokenize_resume_text
from app.services.resume_processing.text_processor import process_extracted_document
from app.services.resume_processing.skill_dictionary import SKILL_DICTIONARY, SKILL_CATEGORIES, ALIAS_MAP
from app.services.resume_processing.skill_normalizer import normalize_and_deduplicate_skills
from app.services.resume_processing.skill_extractor import extract_skills
from app.exceptions.resume import ResumeParsingError

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def create_processed_resume_fixture(
    text: str,
    sections_data: Optional[List[Dict[str, Any]]] = None,
) -> ProcessedResumeText:
    """Helper to create a ProcessedResumeText object for testing skill extraction."""
    cleaned = clean_text(text)
    tokens, norm_tokens = tokenize_resume_text(cleaned)

    if sections_data:
        sections = [
            ProcessedSection(
                name=s["name"],
                title=s.get("title") if s.get("title") is not None else s["name"],
                content=s["content"],
                confidence=s.get("confidence", 1.0),
                start_line=1,
                end_line=len(s["content"].split("\n")),
            )
            for s in sections_data
        ]
    else:
        sections = detect_sections(cleaned)

    dummy_doc = ExtractedDocument(
        text=text,
        document_type="pdf",
        extraction_method="pymupdf",
        page_count=1,
        pages=[DocumentPage(page_number=1, text=text)],
        character_count=len(text),
        word_count=len(tokens),
    )

    return ProcessedResumeText(
        cleaned_text=cleaned,
        normalized_text=cleaned,
        lowercase_text=cleaned.lower(),
        sections=sections,
        tokens=tokens,
        normalized_tokens=norm_tokens,
        metadata={"test_fixture": True},
        original_document=dummy_doc,
    )


async def run_resume_skills_tests():
    print("\n============================================================", flush=True)
    print("RUNNING RESUME SKILLS EXTRACTION TESTS (DAY 24)", flush=True)
    print("============================================================", flush=True)

    passed = 0
    failed = 0
    total = 0

    def check(condition: bool, test_name: str, detail: str = ""):
        nonlocal passed, failed, total
        total += 1
        if condition:
            passed += 1
            print(f"  PASS [{total:02d}] {test_name}", flush=True)
        else:
            failed += 1
            print(f"  FAIL [{total:02d}] {test_name} - {detail}", flush=True)

    # -------------------------------------------------------------------
    # SECTION 1: spaCy Model Loading & Singleton Behavior
    # -------------------------------------------------------------------
    print("\n--- Section 1: spaCy Model Loading & Singleton Behavior ---", flush=True)

    reset_spacy_cache()
    nlp1 = get_spacy_nlp()
    check(nlp1 is not None, "spaCy model loaded successfully")
    check(hasattr(nlp1, "pipe_names") and "tok2vec" in nlp1.pipe_names, "Loaded model is en_core_web_sm pipeline")

    nlp2 = get_spacy_nlp()
    check(nlp1 is nlp2, "spaCy singleton returns cached Language instance on subsequent calls")

    # -------------------------------------------------------------------
    # SECTION 2: Technical Skill Extraction & Categories
    # -------------------------------------------------------------------
    print("\n--- Section 2: Technical Skill Extraction & Categories ---", flush=True)

    sample_text = (
        "TECHNICAL SKILLS\n"
        "Languages: Python, Java, C++, C#, JavaScript, TypeScript, Rust, Go, SQL\n"
        "Frontend: HTML, CSS, React.js, Next.js, Vue.js, Tailwind CSS\n"
        "Backend: Node.js, FastAPI, Django, Express.js, .NET\n"
        "Databases: PostgreSQL, MongoDB, Redis, MySQL\n"
        "Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD, Terraform, Linux\n"
        "Data Science & AI: NumPy, Pandas, PyTorch, TensorFlow, scikit-learn, Machine Learning, OpenAI, Gemini\n"
        "Testing & Tools: Pytest, Jest, Postman, Git, GitHub\n"
    )

    proc_text = create_processed_resume_fixture(sample_text)
    extracted = extract_skills(proc_text)
    skill_names = [s.name for s in extracted.skills]

    # Category checks
    check("Python" in skill_names, "PROGRAMMING_LANGUAGE: Python extracted")
    check("C++" in skill_names, "PROGRAMMING_LANGUAGE: C++ extracted")
    check("C#" in skill_names, "PROGRAMMING_LANGUAGE: C# extracted")
    check("TypeScript" in skill_names, "PROGRAMMING_LANGUAGE: TypeScript extracted")
    check("React.js" in skill_names, "FRONTEND: React.js extracted")
    check("Next.js" in skill_names, "FRONTEND: Next.js extracted")
    check("Node.js" in skill_names, "BACKEND: Node.js extracted")
    check("FastAPI" in skill_names, "BACKEND: FastAPI extracted")
    check(".NET" in skill_names, "BACKEND: .NET extracted")
    check("PostgreSQL" in skill_names, "DATABASE: PostgreSQL extracted")
    check("MongoDB" in skill_names, "DATABASE: MongoDB extracted")
    check("AWS" in skill_names, "CLOUD: AWS extracted")
    check("Docker" in skill_names, "DEVOPS: Docker extracted")
    check("Kubernetes" in skill_names, "DEVOPS: Kubernetes extracted")
    check("CI/CD" in skill_names, "DEVOPS: CI/CD extracted")
    check("scikit-learn" in skill_names, "MACHINE_LEARNING: scikit-learn extracted")
    check("PyTorch" in skill_names, "MACHINE_LEARNING: PyTorch extracted")
    check("Machine Learning" in skill_names, "MACHINE_LEARNING: Multi-word 'Machine Learning' extracted")
    check("OpenAI" in skill_names, "AI: OpenAI extracted")
    check("Pytest" in skill_names, "TESTING: Pytest extracted")
    check("Git" in skill_names, "VERSION_CONTROL: Git extracted")

    # -------------------------------------------------------------------
    # SECTION 3: Multi-Word & Technical Punctuation Skills
    # -------------------------------------------------------------------
    print("\n--- Section 3: Multi-Word & Technical Punctuation Skills ---", flush=True)

    mw_text = (
        "SKILLS\n"
        "Experience in Amazon Web Services, Google Cloud Platform, GitHub Actions, "
        "Large Language Models, Deep Learning, Natural Language Processing, and REST API."
    )
    proc_mw = create_processed_resume_fixture(mw_text)
    ext_mw = extract_skills(proc_mw)
    mw_names = [s.name for s in ext_mw.skills]

    check("AWS" in mw_names or "Google Cloud" in mw_names, "Multi-word cloud provider extracted")
    check("GitHub Actions" in mw_names, "Multi-word 'GitHub Actions' extracted")
    check("Large Language Models" in mw_names, "Multi-word 'Large Language Models' extracted")
    check("Deep Learning" in mw_names, "Multi-word 'Deep Learning' extracted")
    check("Natural Language Processing" in mw_names, "Multi-word 'Natural Language Processing' extracted")
    check("REST API" in mw_names, "Multi-word 'REST API' extracted")

    # -------------------------------------------------------------------
    # SECTION 4: False Positive Protection
    # -------------------------------------------------------------------
    print("\n--- Section 4: False Positive Protection ---", flush=True)

    # 4a. JavaScript does NOT extract Java unless Java is separately present
    js_only_text = "SUMMARY\nExpert JavaScript developer building web applications using React.js and Node.js."
    proc_js = create_processed_resume_fixture(js_only_text)
    ext_js = extract_skills(proc_js)
    js_names = [s.name for s in ext_js.skills]

    check("JavaScript" in js_names, "JavaScript extracted from JavaScript developer text")
    check("Java" not in js_names, "FALSE POSITIVE GUARD: 'Java' NOT extracted from 'JavaScript'")

    # Both Java and JavaScript present
    java_and_js_text = "SKILLS\nProficient in Java and JavaScript."
    proc_both = create_processed_resume_fixture(java_and_js_text)
    ext_both = extract_skills(proc_both)
    both_names = [s.name for s in ext_both.skills]
    check("Java" in both_names and "JavaScript" in both_names, "Both Java and JavaScript extracted when separately present")

    # 4b. "Go" in prose (e.g., "Go to the office") -> NOT extracted
    go_prose_text = "SUMMARY\nI like to go to the office every morning and work hard."
    proc_go_prose = create_processed_resume_fixture(go_prose_text)
    ext_go_prose = extract_skills(proc_go_prose)
    check("Go" not in [s.name for s in ext_go_prose.skills], "FALSE POSITIVE GUARD: 'Go' in prose ('go to office') NOT extracted")

    # "Go" in SKILLS section -> extracted
    go_skills_text = "TECHNICAL SKILLS\nGo, Python, Docker"
    proc_go_skills = create_processed_resume_fixture(go_skills_text)
    ext_go_skills = extract_skills(proc_go_skills)
    check("Go" in [s.name for s in ext_go_skills.skills], "'Go' extracted when listed in TECHNICAL SKILLS section")

    # 4c. "IT" in prose -> NOT extracted
    it_text = "SUMMARY\nWorked in the IT department for 3 years."
    proc_it = create_processed_resume_fixture(it_text)
    ext_it = extract_skills(proc_it)
    check("IT" not in [s.name for s in ext_it.skills], "FALSE POSITIVE GUARD: 'IT' in 'IT department' NOT extracted as skill")

    # 4d. React Native vs React.js overlap resolution
    rn_text = "SUMMARY\nExperienced React Native developer."
    proc_rn = create_processed_resume_fixture(rn_text)
    ext_rn = extract_skills(proc_rn)
    rn_names = [s.name for s in ext_rn.skills]
    check("React Native" in rn_names, "React Native extracted from 'React Native developer'")
    check("React.js" not in rn_names, "FALSE POSITIVE GUARD: 'React.js' NOT extracted from 'React Native'")

    # Both React Native and React.js present
    rn_and_react = "SKILLS\nReact Native and React.js"
    proc_both_react = create_processed_resume_fixture(rn_and_react)
    ext_both_react = extract_skills(proc_both_react)
    both_react_names = [s.name for s in ext_both_react.skills]
    check("React Native" in both_react_names and "React.js" in both_react_names, "Both React Native and React.js extracted when separately present")

    # 4e. Contextual AI vs arbitrary prose 'I'
    ai_text = "SUMMARY\nAI engineer building generative AI applications using artificial intelligence."
    proc_ai = create_processed_resume_fixture(ai_text)
    ext_ai = extract_skills(proc_ai)
    ai_names = [s.name for s in ext_ai.skills]
    check("Artificial Intelligence" in ai_names or "Generative AI" in ai_names, "Artificial Intelligence extracted from AI engineer")

    prose_no_ai = "SUMMARY\nThe candidate and I discussed the project details."
    proc_no_ai = create_processed_resume_fixture(prose_no_ai)
    ext_no_ai = extract_skills(proc_no_ai)
    check("Artificial Intelligence" not in [s.name for s in ext_no_ai.skills], "FALSE POSITIVE GUARD: Arbitrary 'I' in prose does NOT extract AI")

    # -------------------------------------------------------------------
    # SECTION 5: Alias Normalization, Hybrid Sources & Deduplication
    # -------------------------------------------------------------------
    print("\n--- Section 5: Alias Normalization, Hybrid Sources & Deduplication ---", flush=True)

    alias_text = (
        "SKILLS\n"
        "reactjs, react.js, REACT, node, nodejs, postgres, psql, sklearn, gcp, aws\n\n"
        "EXPERIENCE\n"
        "Built web apps with react and node.js. Used postgresql on aws."
    )
    proc_alias = create_processed_resume_fixture(alias_text)
    ext_alias = extract_skills(proc_alias)
    alias_names = [s.name for s in ext_alias.skills]

    check("React.js" in alias_names, "Aliases ('reactjs', 'react.js', 'react') normalized to canonical 'React.js'")
    check("Node.js" in alias_names, "Aliases ('node', 'nodejs', 'node.js') normalized to canonical 'Node.js'")
    check("PostgreSQL" in alias_names, "Aliases ('postgres', 'psql', 'postgresql') normalized to canonical 'PostgreSQL'")
    check("scikit-learn" in alias_names, "Aliases ('sklearn', 'scikit-learn') normalized to canonical 'scikit-learn'")
    check("Google Cloud" in alias_names, "Alias 'gcp' normalized to canonical 'Google Cloud'")

    # Check hybrid source detection for React.js
    react_skill = [s for s in ext_alias.skills if s.name == "React.js"][0]
    check(react_skill.source in ("hybrid", "phrase_match", "regex"), f"Skill source correctly populated (got {react_skill.source})")
    check(react_skill.mentions_count > 1, f"Skill mentions count aggregated correctly (got {react_skill.mentions_count})")
    check(len(set([s.name for s in ext_alias.skills])) == len(ext_alias.skills), "Deduplicated skills list contains no duplicates")


    # -------------------------------------------------------------------
    # SECTION 6: Section Context Confidence Scoring & Category Grouping
    # -------------------------------------------------------------------
    print("\n--- Section 6: Section Context Confidence Scoring & Category Grouping ---", flush=True)

    multi_section_text = (
        "SKILLS\n"
        "Python, FastAPI\n\n"
        "EXPERIENCE\n"
        "Docker, PostgreSQL\n\n"
        "PROJECTS\n"
        "React.js\n"
    )
    proc_ms = create_processed_resume_fixture(multi_section_text)
    ext_ms = extract_skills(proc_ms)

    python_skill = [s for s in ext_ms.skills if s.name == "Python"][0]
    docker_skill = [s for s in ext_ms.skills if s.name == "Docker"][0]
    check(python_skill.confidence == 0.99, f"Skill in SKILLS section gets highest confidence 0.99 (got {python_skill.confidence})")
    check(docker_skill.confidence == 0.93, f"Skill in EXPERIENCE section gets experience confidence 0.93 (got {docker_skill.confidence})")
    check(len(ext_ms.categories) > 0, "Categories dictionary populated with category breakdowns")
    check("Python" in ext_ms.categories.get("PROGRAMMING_LANGUAGE", []), "Categories map contains 'Python' under PROGRAMMING_LANGUAGE")

    # -------------------------------------------------------------------
    # SECTION 7: Full Synthetic Resume Test (John Doe)
    # -------------------------------------------------------------------
    print("\n--- Section 7: Full Synthetic Resume Test (John Doe) ---", flush=True)

    john_doe_resume = (
        "JOHN DOE\n"
        "Software Engineer\n"
        "john.doe@example.com | +91 9876543210\n\n"
        "PROFESSIONAL SUMMARY\n"
        "Backend developer experienced in Python and FastAPI.\n\n"
        "TECHNICAL SKILLS\n"
        "Python, JavaScript, TypeScript, React.js, Next.js, Node.js, FastAPI, "
        "PostgreSQL, Docker, AWS, Git, GitHub, CI/CD, PyTorch, scikit-learn\n\n"
        "EXPERIENCE\n"
        "Software Engineer | ABC Technologies\n"
        "Built backend services using Python, FastAPI, and PostgreSQL.\n"
        "Deployed applications using Docker and AWS.\n\n"
        "PROJECTS\n"
        "TalentAI\n"
        "Built a recruitment platform using Next.js, Node.js, PostgreSQL, and Machine Learning.\n\n"
        "EDUCATION\n"
        "B.Tech in Electrical Engineering | NIT Rourkela\n"
    )

    proc_john = create_processed_resume_fixture(john_doe_resume)
    ext_john = extract_skills(proc_john)
    john_skill_names = [s.name for s in ext_john.skills]

    expected_john_skills = [
        "Python", "JavaScript", "TypeScript", "React.js", "Next.js", "Node.js",
        "FastAPI", "PostgreSQL", "Docker", "AWS", "Git", "GitHub", "CI/CD",
        "PyTorch", "scikit-learn", "Machine Learning"
    ]

    for expected in expected_john_skills:
        check(expected in john_skill_names, f"John Doe resume extracted '{expected}'")

    check(len(set(john_skill_names)) == len(john_skill_names), "John Doe extracted skills list contains 0 duplicates")
    check(ext_john.total_count == len(john_skill_names), "total_count metadata matches skills count")

    # -------------------------------------------------------------------
    # SECTION 8: Error Handling & Input Validation
    # -------------------------------------------------------------------
    print("\n--- Section 8: Error Handling & Input Validation ---", flush=True)

    # None input
    try:
        extract_skills(None)
        check(False, "None ProcessedResumeText raises ResumeParsingError")
    except ResumeParsingError as e:
        check("Cannot extract skills" in str(e) or "None" in str(e), "None input raises controlled ResumeParsingError")

    # Empty text input
    try:
        empty_proc = create_processed_resume_fixture("")
        empty_proc.normalized_text = ""
        extract_skills(empty_proc)
        check(False, "Empty text ProcessedResumeText raises ResumeParsingError")
    except ResumeParsingError as e:
        check("no text" in str(e).lower(), "Empty text raises controlled ResumeParsingError")

    # Non-mutation check
    original_john_text = proc_john.normalized_text
    _ = extract_skills(proc_john)
    check(proc_john.normalized_text == original_john_text, "ProcessedResumeText is NOT mutated by skill extraction")

    # -------------------------------------------------------------------
    # SECTION 9: Day 24 Final Normalizer Hardening Regression Tests
    # -------------------------------------------------------------------
    print("\n--- Section 9: Day 24 Final Normalizer Hardening Regression Tests ---", flush=True)

    # 1. Canonical fallback preservation
    # scikit-learn -> scikit-learn (NOT Scikit-Learn)
    proc_sklearn = create_processed_resume_fixture("Experienced with scikit-learn and Machine Learning algorithms.")
    res_sklearn = extract_skills(proc_sklearn)
    sk_names = [s.name for s in res_sklearn.skills]
    check("scikit-learn" in sk_names, "scikit-learn canonical name preserved (not Scikit-Learn)")

    # CI/CD -> CI/CD (NOT Ci/Cd)
    proc_cicd = create_processed_resume_fixture("Built CI/CD pipelines using GitHub Actions.")
    res_cicd = extract_skills(proc_cicd)
    cicd_names = [s.name for s in res_cicd.skills]
    check("CI/CD" in cicd_names, "CI/CD canonical name preserved (not Ci/Cd)")

    # Node.js -> Node.js (NOT Node.Js)
    proc_nodejs = create_processed_resume_fixture("Backend development using Node.js and Express.")
    res_nodejs = extract_skills(proc_nodejs)
    nodejs_names = [s.name for s in res_nodejs.skills]
    check("Node.js" in nodejs_names, "Node.js canonical name preserved (not Node.Js)")

    # Unrecognized matches skipped, no invented skills
    unresolved_matches = [
        {"matched_text": "NonExistentRandomSkill123", "canonical_name": "NonExistentRandomSkill123", "category": "OTHER", "source": "phrase_match", "confidence": 0.9}
    ]
    norm_unresolved = normalize_and_deduplicate_skills(unresolved_matches)
    check(norm_unresolved.total_count == 0, "Unresolved matches not in SKILL_DICTIONARY are skipped (no fallback creation)")

    # 2. Duplicate occurrences mention counting
    proc_dup_py = create_processed_resume_fixture("Python developer. Wrote Python scripts. Python expert.")
    res_dup_py = extract_skills(proc_dup_py)
    py_skill = next((s for s in res_dup_py.skills if s.name == "Python"), None)
    check(py_skill is not None, "Python extracted from text with 3 occurrences")
    if py_skill:
        check(py_skill.mentions_count == 3, f"Python mentions_count is 3 (got {py_skill.mentions_count})")

    # 3. PhraseMatcher + regex source merging (React.js -> source = hybrid, mentions_count = 1 for single span)
    proc_react = create_processed_resume_fixture("Developed frontend with React.js")
    res_react = extract_skills(proc_react)
    react_skill = next((s for s in res_react.skills if s.name == "React.js"), None)
    check(react_skill is not None, "React.js extracted via hybrid phrase_match + regex")
    if react_skill:
        check(react_skill.source == "hybrid", f"React.js source is 'hybrid' (got '{react_skill.source}')")
        check(react_skill.mentions_count == 1, f"React.js single span mentions_count is 1 (got {react_skill.mentions_count})")

    # 4. Section aggregation across SKILLS, PROJECTS, EXPERIENCE
    proc_sections = create_processed_resume_fixture(
        text="Skills: Python. Projects: Python microservice. Experience: Lead Python developer.",
        sections_data=[
            {"name": "SKILLS", "content": "Skills: Python.", "confidence": 0.99},
            {"name": "PROJECTS", "content": "Projects: Python microservice.", "confidence": 0.95},
            {"name": "EXPERIENCE", "content": "Experience: Lead Python developer.", "confidence": 0.93},
        ]
    )
    res_sec_py = extract_skills(proc_sections)
    sec_py_skill = next((s for s in res_sec_py.skills if s.name == "Python"), None)
    check(sec_py_skill is not None, "Python extracted across multiple sections")
    if sec_py_skill:
        expected_sec = ["EXPERIENCE", "PROJECTS", "SKILLS"]
        check(sorted(sec_py_skill.sections) == expected_sec, f"Python sections aggregated deterministically to {expected_sec} (got {sec_py_skill.sections})")
        check(sec_py_skill.mentions_count == 3, f"Python mentions_count across 3 sections is 3 (got {sec_py_skill.mentions_count})")

    # 5. Category verification from SKILL_DICTIONARY
    cat_test_text = "Proficient in Python, React.js, PostgreSQL, and Docker."
    res_cat = extract_skills(create_processed_resume_fixture(cat_test_text))
    cat_map = {s.name: s.category for s in res_cat.skills}
    check(cat_map.get("Python") == "PROGRAMMING_LANGUAGE", f"Python category is PROGRAMMING_LANGUAGE (got {cat_map.get('Python')})")
    check(cat_map.get("React.js") == "FRONTEND", f"React.js category is FRONTEND (got {cat_map.get('React.js')})")
    check(cat_map.get("PostgreSQL") == "DATABASE", f"PostgreSQL category is DATABASE (got {cat_map.get('PostgreSQL')})")
    check(cat_map.get("Docker") == "DEVOPS", f"Docker category is DEVOPS (got {cat_map.get('Docker')})")

    # 6. Normalized names validation (canonical_name.lower())
    norm_test_text = "Skills include Python, React.js, C++, C#, .NET, and CI/CD."
    res_norm = extract_skills(create_processed_resume_fixture(norm_test_text))
    norm_map = {s.name: s.normalized_name for s in res_norm.skills}
    check(norm_map.get("Python") == "python", "Python normalized_name is 'python'")
    check(norm_map.get("React.js") == "react.js", "React.js normalized_name is 'react.js'")
    check(norm_map.get("C++") == "c++", "C++ normalized_name is 'c++'")
    check(norm_map.get("C#") == "c#", "C# normalized_name is 'c#'")
    check(norm_map.get(".NET") == ".net", ".NET normalized_name is '.net'")
    check(norm_map.get("CI/CD") == "ci/cd", "CI/CD normalized_name is 'ci/cd'")

    # -------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------
    print(f"\n============================================================", flush=True)
    print(f"RESUME SKILLS EXTRACTION TESTS: {passed} passed, {failed} failed, {total} total", flush=True)
    print(f"============================================================", flush=True)

    if failed > 0:
        sys.exit(1)


@pytest.mark.asyncio
async def test_resume_skills():
    await run_resume_skills_tests()


if __name__ == "__main__":
    asyncio.run(run_resume_skills_tests())
