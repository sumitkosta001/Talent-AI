"""Hybrid Resume Skill Extractor for Day 24.

Combines spaCy NLP (PhraseMatcher), Section Context Scoring, and Strict False-Positive Guards
to extract, normalize, categorize, and deduplicate skills from ProcessedResumeText.

Preserves technical terms (C++, C#, .NET, Node.js, React.js, CI/CD), multi-word skills
(Machine Learning, Amazon Web Services, GitHub Actions), and original ProcessedResumeText.
"""

import time
import re
import logging
from typing import List, Dict, Any, Set
from spacy.matcher import PhraseMatcher

from app.config.settings import settings
from app.exceptions.resume import ResumeParsingError
from .models import ProcessedResumeText, ExtractedSkills
from .spacy_service import get_spacy_nlp, get_loaded_model_name
from .skill_dictionary import (
    SKILL_DICTIONARY,
    ALIAS_MAP,
    SHORT_AMBIGUOUS_ALIASES,
)
from .skill_normalizer import normalize_and_deduplicate_skills

logger = logging.getLogger("talentai.resume_processing.skill_extractor")

# Section confidence multipliers
SECTION_CONFIDENCE_WEIGHTS = {
    "SKILLS": 0.99,
    "TECHNICAL_SKILLS": 0.99,
    "PROJECTS": 0.95,
    "PROJECT_EXPERIENCE": 0.95,
    "EXPERIENCE": 0.93,
    "WORK_EXPERIENCE": 0.93,
    "PROFESSIONAL_EXPERIENCE": 0.93,
    "CERTIFICATIONS": 0.90,
    "SUMMARY": 0.85,
    "EDUCATION": 0.80,
    "UNKNOWN": 0.75,
}

# Special technical punctuation skills regex pattern for terms spaCy might tokenize separately
SPECIAL_TECH_PATTERNS = [
    (re.compile(r'(?<!\w)C\+\+(?!\w)', re.IGNORECASE), "C++", "PROGRAMMING_LANGUAGE"),
    (re.compile(r'(?<!\w)C#(?!\w)', re.IGNORECASE), "C#", "PROGRAMMING_LANGUAGE"),
    (re.compile(r'(?<!\w)\.NET(?!\w)', re.IGNORECASE), ".NET", "BACKEND"),
    (re.compile(r'(?<!\w)Node\.js(?!\w)', re.IGNORECASE), "Node.js", "BACKEND"),
    (re.compile(r'(?<!\w)React\.js(?!\w)', re.IGNORECASE), "React.js", "FRONTEND"),
    (re.compile(r'(?<!\w)Next\.js(?!\w)', re.IGNORECASE), "Next.js", "FRONTEND"),
    (re.compile(r'(?<!\w)Vue\.js(?!\w)', re.IGNORECASE), "Vue.js", "FRONTEND"),
    (re.compile(r'(?<!\w)Express\.js(?!\w)', re.IGNORECASE), "Express.js", "BACKEND"),
    (re.compile(r'(?<!\w)CI/CD(?!\w)', re.IGNORECASE), "CI/CD", "DEVOPS"),
    (re.compile(r'(?<!\w)scikit-learn(?!\w)', re.IGNORECASE), "scikit-learn", "MACHINE_LEARNING"),
]


def extract_skills(processed_text: ProcessedResumeText | None) -> ExtractedSkills:
    """Extract, categorize, and normalize technical skills from a ProcessedResumeText object.

    Does NOT mutate input ProcessedResumeText or ExtractedDocument.

    Args:
        processed_text: ProcessedResumeText instance from Day 23 text processing (or None).

    Returns:
        ExtractedSkills container with deduplicated, categorized skills.

    Raises:
        ResumeParsingError: If processed_text is None or has no text.
    """
    if processed_text is None:
        logger.error("Skill extraction rejected: ProcessedResumeText is None.")
        raise ResumeParsingError("Cannot extract skills from a None ProcessedResumeText.")

    if not processed_text.normalized_text:
        logger.warning("Skill extraction rejected: ProcessedResumeText contains empty text.")
        raise ResumeParsingError("The processed resume document contains no text.")

    start_time = time.time()

    # Step 1: Load singleton spaCy NLP pipeline
    nlp = get_spacy_nlp()

    # Step 2: Initialize PhraseMatcher with skill dictionary aliases
    matcher = _build_phrase_matcher(nlp)

    raw_candidates: List[Dict[str, Any]] = []

    # Step 3: Section-aware extraction
    sections_to_process = processed_text.sections if processed_text.sections else []

    if not sections_to_process:
        from .models import ProcessedSection
        sections_to_process = [
            ProcessedSection(
                name="UNKNOWN",
                title="Full Content",
                content=processed_text.normalized_text,
                confidence=1.0,
            )
        ]

    for section in sections_to_process:
        sec_name = section.name
        sec_content = section.content
        if not sec_content:
            continue

        sec_confidence = SECTION_CONFIDENCE_WEIGHTS.get(sec_name, 0.75)
        doc = nlp(sec_content)

        # 3a. Run PhraseMatcher on spaCy doc
        spacy_matches = matcher(doc)
        for match_id, start, end in spacy_matches:
            matched_span = doc[start:end]
            matched_text = matched_span.text.strip()
            raw_lower = matched_text.lower()

            if raw_lower in ALIAS_MAP:
                canonical_name, category = ALIAS_MAP[raw_lower]

                # Ambiguous short-token guard
                if raw_lower in SHORT_AMBIGUOUS_ALIASES:
                    if not _is_valid_short_ambiguous_match(matched_span, sec_name, sec_content):
                        continue

                raw_candidates.append({
                    "start_char": matched_span.start_char,
                    "end_char": matched_span.end_char,
                    "matched_text": matched_text,
                    "canonical_name": canonical_name,
                    "category": category,
                    "section_name": sec_name,
                    "source": "phrase_match",
                    "confidence": sec_confidence,
                })

        # 3b. Run special technical symbol regex pattern matches
        for pattern, canonical_name, category in SPECIAL_TECH_PATTERNS:
            for match in pattern.finditer(sec_content):
                matched_str = match.group(0).strip()
                raw_candidates.append({
                    "start_char": match.start(),
                    "end_char": match.end(),
                    "matched_text": matched_str,
                    "canonical_name": canonical_name,
                    "category": category,
                    "section_name": sec_name,
                    "source": "regex",
                    "confidence": sec_confidence,
                })

    # Step 4: Systematic longest-match span overlap resolution
    resolved_matches = _resolve_span_overlaps(raw_candidates)

    # Step 5: Normalize and deduplicate skills
    extracted_result = normalize_and_deduplicate_skills(resolved_matches)

    elapsed = round(time.time() - start_time, 4)
    extracted_result.metadata.update({
        "spacy_model": get_loaded_model_name(),
        "extraction_duration_seconds": elapsed,
    })

    logger.info(
        "Skill extraction completed: total_skills=%d, categories=%d, duration=%.4fs",
        extracted_result.total_count, len(extracted_result.categories), elapsed,
    )

    return extracted_result


def _build_phrase_matcher(nlp) -> PhraseMatcher:
    """Build and cache spaCy PhraseMatcher with skill dictionary terms."""
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

    for canonical_name, info in SKILL_DICTIONARY.items():
        patterns = [canonical_name] + info.get("aliases", [])
        docs = [nlp.make_doc(p) for p in patterns if p and p.strip()]
        if docs:
            matcher.add(canonical_name, docs)

    return matcher


def _resolve_span_overlaps(candidate_matches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Deterministic span overlap resolution algorithm.

    Rules:
    1. Sort candidate matches by span length descending (longer match beats shorter match),
       then confidence score descending, then canonical name ascending.
    2. Eliminate weaker overlapping matches covered by a longer/more-specific match.
    3. Merge sources (e.g. phrase_match + regex -> hybrid) when exact span & canonical match.
    4. Retain non-overlapping distinct spans (e.g. Java and JavaScript in separate spans).
    """
    if not candidate_matches:
        return []

    # Sort candidates
    sorted_candidates = sorted(
        candidate_matches,
        key=lambda m: (
            -(m["end_char"] - m["start_char"]),
            -m["confidence"],
            m["canonical_name"].lower(),
        ),
    )

    accepted: List[Dict[str, Any]] = []

    for cand in sorted_candidates:
        c_start = cand["start_char"]
        c_end = cand["end_char"]
        c_canonical = cand["canonical_name"]
        c_source = cand["source"]
        c_section = cand.get("section_name", "UNKNOWN")

        is_overlapping = False
        for acc in accepted:
            a_start = acc["start_char"]
            a_end = acc["end_char"]
            a_section = acc.get("section_name", "UNKNOWN")

            # Check if candidates are in the same section before span comparison
            if c_section != a_section:
                continue

            # Exact span overlap check
            if c_start == a_start and c_end == a_end:
                is_overlapping = True
                if c_canonical == acc["canonical_name"]:
                    if acc["source"] != c_source:
                        acc["source"] = "hybrid"
                break

            # Partial/Sub-span overlap check (c_start < a_end and c_end > a_start)
            if c_start < a_end and c_end > a_start:
                is_overlapping = True
                break

        if not is_overlapping:
            accepted.append(cand)

    return accepted


def _is_valid_short_ambiguous_match(span, section_name: str, section_content: str) -> bool:
    """Apply strict context guards for ambiguous short tokens (e.g. Go, R, C, IT, AI)."""
    token_text = span.text.strip() if hasattr(span, "text") else str(span).strip()
    token_lower = token_text.lower()
    is_skills_sec = section_name in ("SKILLS", "TECHNICAL_SKILLS")

    try:
        sent_text = span.sent.text.lower() if hasattr(span, "sent") else section_content.lower()
    except Exception:
        sent_text = section_content.lower()

    if token_lower == "go":
        if is_skills_sec and (token_text in ("Go", "GO") or token_text.istitle()):
            return True
        if any(term in sent_text for term in ("golang", "go language", "go programming", "go developer", "go backend", "go microservices")):
            return True
        return False

    if token_lower == "r":
        if is_skills_sec and token_text == "R":
            return True
        if any(term in sent_text for term in ("r language", "r programming", "statistics", "data analysis", "r package", "r/python")):
            return True
        return False

    if token_lower == "c":
        if is_skills_sec and token_text == "C":
            return True
        if any(term in sent_text for term in ("c language", "c programming", "c/c++", "c & c++", "embedded c")):
            return True
        return False

    if token_lower == "ai":
        if token_text in ("AI", "GenAI"):
            return True
        if any(term in sent_text for term in ("artificial intelligence", "ai engineer", "ai/ml", "ai systems", "generative ai", "ai & machine learning")):
            return True
        return False

    if is_skills_sec:
        return True

    if token_text == token_text.upper() and len(token_text) <= 3:
        return True

    return True

