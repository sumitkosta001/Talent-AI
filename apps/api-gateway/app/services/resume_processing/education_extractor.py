"""Phase 4 Day 25 — Education Extraction Engine.

Rule-based, section-aware, deterministic education extractor for resume processing.
Consumes ProcessedResumeText without mutating input objects.
"""

from typing import List, Dict, Any, Optional, Set, Tuple
import re
import time
import logging

from app.exceptions.resume import ResumeParsingError
from .models import ProcessedResumeText, EducationRecord, ExtractedEducation
from .degree_dictionary import (
    DEGREE_DICTIONARY,
    DEGREE_ALIAS_MAP,
    INSTITUTION_KEYWORDS,
)
from .education_normalizer import (
    normalize_degree,
    normalize_institution,
    parse_year_and_status,
    parse_score,
    deduplicate_education_records,
)
from .spacy_service import get_spacy_nlp

logger = logging.getLogger("talentai.resume_processing.education_extractor")

# Job / Experience false positive guards
EXPERIENCE_INDICATORS = re.compile(
    r'\b(?:Software\s+Engineer|Developer|Senior\s+Developer|Architect|Manager|Lead|Intern|Consultant|Analyst|Designer|Tester)\b'
    r'|\b(?:\d+\+?\s*years?\s+(?:of\s+)?experience|experience\s+in|worked\s+at)\b',
    re.IGNORECASE,
)

# Project / Coverage false positive guards
PROJECT_INDICATORS = re.compile(
    r'\b(?:test\s+coverage|code\s+coverage|remotely|worked\s+\d+%\s+remotely|project\s+completed)\b',
    re.IGNORECASE,
)


def _is_experience_or_project_line(line: str) -> bool:
    """Check if line is clearly from an experience or project context."""
    if EXPERIENCE_INDICATORS.search(line):
        return True
    if PROJECT_INDICATORS.search(line):
        return True
    return False


def _extract_field_of_study(line: str, raw_degree_match: str) -> Optional[str]:
    """Extract field of study / major following a degree match in a line."""
    if not line or not raw_degree_match:
        return None

    # Look for connectors after degree match (e.g. B.Tech in Electrical Engineering)
    pattern = re.compile(
        re.escape(raw_degree_match) + r'\s*(?:in|,|-|\||\s+major\s+in|\s+specialization\s+in)?\s*([A-Za-z\s&]{3,40})',
        re.IGNORECASE,
    )
    match = pattern.search(line)
    if match:
        field_candidate = match.group(1).strip(" ,.-|:\t\n")
        # Filter out numbers, years, institutions, or unwanted noise
        if (
            field_candidate
            and not re.search(r'\d', field_candidate)
            and not any(kw.lower() in field_candidate.lower() for kw in INSTITUTION_KEYWORDS)
            and len(field_candidate) >= 3
            and field_candidate.lower() not in ("in", "and", "or", "of", "the", "for", "with")
        ):
            # Clean capitalization
            return field_candidate.title()

    return None


def _find_institution_in_block(lines: List[str]) -> Tuple[Optional[str], Optional[str]]:
    """Scan block lines for institutional names using structural indicators or spaCy ORG entities."""
    for line in lines:
        if _is_experience_or_project_line(line):
            continue

        # Check for institution keywords
        for kw in INSTITUTION_KEYWORDS:
            if re.search(r'\b' + re.escape(kw) + r'\b', line, re.IGNORECASE):
                # Clean up full line segment
                inst_cand = line.strip(" ,.-|:\t\n")
                if inst_cand and len(inst_cand) >= 4:
                    return normalize_institution(inst_cand)

    # Optional spaCy NER fallback within education block
    nlp = get_spacy_nlp()
    if nlp is not None:
        block_text = " ".join(lines)
        doc = nlp(block_text)
        for ent in doc.ents:
            if ent.label_ == "ORG":
                text_cand = ent.text.strip()
                # Ensure it's not a known corporate entity
                if not re.search(r'\b(?:Google|Microsoft|Amazon|Meta|Apple|Netflix|TCS|Infosys|Wipro|Cognizant)\b', text_cand, re.IGNORECASE):
                    return normalize_institution(text_cand)

    return None, None


def extract_education(processed_text: Optional[ProcessedResumeText]) -> ExtractedEducation:
    """Extract, normalize, group, and deduplicate education entries from ProcessedResumeText.

    Args:
        processed_text: ProcessedResumeText object from Day 23.

    Returns:
        ExtractedEducation container with extracted EducationRecord items and metadata.

    Raises:
        ResumeParsingError: If processed_text is None or has no text.
    """
    if processed_text is None:
        raise ResumeParsingError("Cannot extract education from a None ProcessedResumeText.")

    if not processed_text.normalized_text or not processed_text.normalized_text.strip():
        raise ResumeParsingError("The processed resume document contains no text.")

    start_time = time.perf_counter()
    records: List[EducationRecord] = []

    # 1. Identify Education Sections vs Fallback Full Text Lines
    edu_sections = [s for s in processed_text.sections if s.name == "EDUCATION"]

    lines_to_process: List[Tuple[str, str, float]] = []  # (line_text, section_name, base_confidence)

    if edu_sections:
        for sec in edu_sections:
            sec_lines = [l.strip() for l in sec.content.splitlines() if l.strip()]
            for l in sec_lines:
                lines_to_process.append((l, sec.name, 0.95))
    else:
        # Fallback: scan all lines with lower base confidence
        all_lines = [l.strip() for l in processed_text.normalized_text.splitlines() if l.strip()]
        for l in all_lines:
            lines_to_process.append((l, "EDUCATION_FALLBACK", 0.80))

    # 2. Group lines into cohesive Education Candidate Blocks
    # Split blocks on blank lines or new degree matches
    blocks: List[List[Tuple[str, str, float]]] = []
    current_block: List[Tuple[str, str, float]] = []

    for line_text, sec_name, base_conf in lines_to_process:
        # Check if line starts a new degree
        has_new_degree = False
        for canonical_name, info in DEGREE_DICTIONARY.items():
            pattern: re.Pattern = info["pattern"]
            if pattern.search(line_text):
                has_new_degree = True
                break

        if has_new_degree and current_block:
            blocks.append(current_block)
            current_block = []

        current_block.append((line_text, sec_name, base_conf))

    if current_block:
        blocks.append(current_block)

    # 3. Process each Candidate Block
    for block in blocks:
        block_text = " ".join([item[0] for item in block])
        block_lines = [item[0] for item in block]
        sec_name = block[0][1]
        base_confidence = block[0][2]

        # Guard against experience / project false positive blocks
        if any(_is_experience_or_project_line(l) for l in block_lines):
            continue

        # Look for degree in block
        matched_degree_canonical: Optional[str] = None
        matched_degree_normalized: Optional[str] = None
        matched_degree_level: Optional[str] = None
        matched_raw_str: Optional[str] = None

        for canonical_name, info in DEGREE_DICTIONARY.items():
            pattern: re.Pattern = info["pattern"]
            for l in block_lines:
                m = pattern.search(l)
                if m:
                    matched_raw_str = m.group(0)
                    matched_degree_canonical, matched_degree_normalized, matched_degree_level = normalize_degree(matched_raw_str)
                    break
            if matched_degree_canonical:
                break

        # Check school education patterns if no university degree matched
        if not matched_degree_canonical:
            for l in block_lines:
                if re.search(r'\b(?:Class\s+(?:XII|12)|12th|Higher\s+Secondary|Senior\s+Secondary)\b', l, re.IGNORECASE):
                    matched_degree_canonical = "Senior Secondary"
                    matched_degree_normalized = "senior_secondary"
                    matched_degree_level = "SECONDARY"
                    matched_raw_str = "Class XII"
                    break
                elif re.search(r'\b(?:Class\s+(?:X|10)|10th|Secondary\s+School)\b', l, re.IGNORECASE):
                    matched_degree_canonical = "Secondary"
                    matched_degree_normalized = "secondary"
                    matched_degree_level = "SECONDARY"
                    matched_raw_str = "Class X"
                    break

        if not matched_degree_canonical:
            # Skip block if no degree or school education matched
            continue

        # Extract Field of Study
        field_of_study: Optional[str] = None
        for l in block_lines:
            fos = _extract_field_of_study(l, matched_raw_str or "")
            if fos:
                field_of_study = fos
                break

        # Extract Institution
        institution, normalized_inst = _find_institution_in_block(block_lines)

        # Extract Years
        start_yr, end_yr, grad_yr, grad_status = parse_year_and_status(block_text)

        # Extract Score (CGPA or Percentage)
        cgpa_val, pct_val, score_tp = parse_score(block_text)

        # Compute heuristic confidence score
        confidence = base_confidence
        if matched_degree_canonical and institution and grad_yr and (cgpa_val or pct_val):
            confidence = min(0.98, base_confidence + 0.03)
        elif matched_degree_canonical and institution:
            confidence = base_confidence
        elif matched_degree_canonical:
            confidence = max(0.70, base_confidence - 0.15)

        record = EducationRecord(
            degree=matched_degree_canonical,
            normalized_degree=matched_degree_normalized,
            degree_level=matched_degree_level,
            field_of_study=field_of_study,
            institution=institution,
            normalized_institution=normalized_inst,
            start_year=start_yr,
            end_year=end_yr,
            graduation_year=grad_yr,
            graduation_status=grad_status,
            cgpa=cgpa_val,
            percentage=pct_val,
            score_type=score_tp,
            source_text=block_text[:300],
            section=sec_name,
            source="pattern" if sec_name == "EDUCATION" else "fallback",
            confidence=round(confidence, 2),
        )
        records.append(record)

    # 4. Deduplicate Records
    deduped_records = deduplicate_education_records(records)
    elapsed_sec = round(time.perf_counter() - start_time, 4)

    logger.info(
        "Extracted %d education records (%d deduplicated) in %.4fs",
        len(records),
        len(deduped_records),
        elapsed_sec,
    )

    return ExtractedEducation(
        education_records=deduped_records,
        total_count=len(deduped_records),
        metadata={
            "duration_seconds": elapsed_sec,
            "raw_candidate_blocks": len(blocks),
            "accepted_records_count": len(deduped_records),
        },
    )
